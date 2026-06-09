"""
Bootstrap new bios (from refresh_step_1 outputs) into the SAME files
your notebooks already read:

1) data/processed/tmp_normalized/normalized_chunk_YYYYMMDD.csv
   - columns compatible with your existing normalized chunks:
     ['qid','gender','country','occupation']  (strings)

2) data/raw/seed_enwiki_YYYYMMDD.csv
   - columns: ['qid','first_edit_ts']  (ISO8601)

Notes:
- We map P21/P27/P106 IDs -> English labels via Wikidata (batched)
  and cache those in data/cache/id_labels.csv to avoid refetching.
- We keep rows with a qid; rows without qid are skipped.
- Pages without a first revision timestamp are skipped in the seed file
  (they'll be picked up in a later refresh when timestamps appear).
"""

from pathlib import Path
import pandas as pd
import requests
import time
from datetime import datetime, timezone

# ---------- Paths ----------
ROOT = Path.cwd()
if ROOT.name == "notebooks":
    ROOT = ROOT.parent

DATA          = ROOT / "data"
RAW_DIR       = DATA / "raw"
PROC_DIR      = DATA / "processed"
TMP_NORM_DIR  = PROC_DIR / "tmp_normalized"
CACHE_DIR     = DATA / "cache"
ENTITIES_CSV  = DATA / "entities" / "entities.csv"
CREATIONS_CSV = DATA / "events"   / "creations.csv"

RAW_DIR.mkdir(parents=True, exist_ok=True)
TMP_NORM_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# ---------- Config ----------
WD_API = "https://www.wikidata.org/w/api.php"
HEADERS = {"User-Agent": "WikiGapsBootstrap/1.0 (ashhik96@gmail.com)"}
BATCH = 50
SLEEP = 0.1

# ---------- Helpers ----------
def batched(seq, n=BATCH):
    buf = []
    for x in seq:
        buf.append(x)
        if len(buf) == n:
            yield buf
            buf = []
    if buf:
        yield buf

def wd_labels_for_qids(qids):
    """Return {qid: label_en} for the provided qids (batched)."""
    out = {}
    for batch in batched(qids, 50):
        params = {
            "action": "wbgetentities",
            "format": "json",
            "ids": "|".join(batch),
            "props": "labels",
        }
        r = requests.get(WD_API, params=params, headers=HEADERS, timeout=45)
        r.raise_for_status()
        ents = r.json().get("entities", {})
        for q, e in ents.items():
            lbl = (e.get("labels", {}).get("en") or {}).get("value")
            if lbl:
                out[q] = lbl
        time.sleep(SLEEP)
    return out

def get_or_build_id_label_cache(unique_ids):
    """
    Maintain a local cache 'data/cache/id_labels.csv' with columns [id,label_en].
    Only query Wikidata for IDs we don't have yet.
    """
    cache_path = CACHE_DIR / "id_labels.csv"
    if cache_path.exists():
        cache = pd.read_csv(cache_path, dtype=str)
    else:
        cache = pd.DataFrame(columns=["id","label_en"], dtype=str)

    have = set(cache["id"].astype(str)) if not cache.empty else set()
    needed = [x for x in unique_ids if x and str(x) not in have]

    if needed:
        lab_map = wd_labels_for_qids(needed)
        if lab_map:
            add = pd.DataFrame({"id": list(lab_map.keys()), "label_en": list(lab_map.values())})
            cache = pd.concat([cache, add], ignore_index=True).drop_duplicates("id", keep="last")
            cache.to_csv(cache_path, index=False)

    return cache  # up-to-date cache

# ---------- Load incremental outputs (from refresh_step_1) ----------
if not ENTITIES_CSV.exists():
    raise SystemExit("❌ data/entities/entities.csv not found. Run refresh_step_1.py first.")

print(f"📂 Loading incremental data...")
ent = pd.read_csv(ENTITIES_CSV, dtype=str)  # pageid,qid,P21,P27,P106,label_en
print(f"   Found {len(ent):,} entities")

if not CREATIONS_CSV.exists():
    # We can still produce normalized chunks (no timestamps), but seed file will be empty.
    print("⚠️  No creations.csv found - seed file will be empty")
    cre = pd.DataFrame(columns=["pageid","first_rev_ts"], dtype=str)
else:
    cre = pd.read_csv(CREATIONS_CSV, dtype=str)  # pageid, first_rev_ts
    print(f"   Found {len(cre):,} creation timestamps")

# join pageid->qid so we can produce seed file keyed by qid
ent_min = ent[["pageid","qid"]].dropna().drop_duplicates()
seed = cre.merge(ent_min, on="pageid", how="inner")[["qid","first_rev_ts"]].dropna().drop_duplicates()

# ---------- Expand / normalize P21,P27,P106 (ID lists) ----------
# Ensure list-like strings -> python lists (safe eval)
def to_list_safe(x):
    if pd.isna(x) or x == "":
        return []
    # Expect things like "['Q6581097']" or "['Q30','Q145']"
    x = str(x).strip()
    if x.startswith("[") and x.endswith("]"):
        try:
            return [s.strip().strip("'").strip('"') for s in x[1:-1].split(",") if s.strip()]
        except Exception:
            return []
    # otherwise single ID
    return [x]

print("🔄 Parsing property lists...")
ent["P21_list"]  = ent["P21"].apply(to_list_safe)   if "P21" in ent.columns else [[]]*len(ent)
ent["P27_list"]  = ent["P27"].apply(to_list_safe)   if "P27" in ent.columns else [[]]*len(ent)
ent["P106_list"] = ent["P106"].apply(to_list_safe)  if "P106" in ent.columns else [[]]*len(ent)

# Collect all unique IDs to label
all_ids = set()
for col in ["P21_list","P27_list","P106_list"]:
    for lst in ent[col]:
        all_ids.update(lst)
all_ids = {i for i in all_ids if i}

print(f"🏷️  Fetching labels for {len(all_ids):,} unique property values...")
# Pull labels (cached)
cache = get_or_build_id_label_cache(sorted(all_ids))
id2label = dict(zip(cache["id"].astype(str), cache["label_en"].astype(str)))

def first_label(lst):
    """Choose the first non-empty label if there are multiple IDs."""
    for q in lst:
        lab = id2label.get(str(q))
        if lab:
            return lab
    return "unknown"

# Map to strings your notebooks expect
print("🔀 Normalizing to notebook format...")
ent["gender"]     = ent["P21_list"].apply(first_label).str.lower()
ent["country"]    = ent["P27_list"].apply(first_label)
ent["occupation"] = ent["P106_list"].apply(first_label)

# Keep qid and these 3 columns for the normalized chunk
norm = ent[["qid","gender","country","occupation"]].dropna(subset=["qid"]).copy()
norm["qid"] = norm["qid"].astype(str)

# Basic cleanup to align with your notebooks
# (gender lowercased; unknown values remain 'unknown')
norm["gender"] = norm["gender"].str.strip().str.lower().fillna("unknown")
norm["country"] = norm["country"].fillna("unknown")
norm["occupation"] = norm["occupation"].fillna("unknown")

# ---------- Write the two artifacts your notebooks use ----------
stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# 1) normalized chunk - MATCHES notebook 02 pattern: "normalized_chunk_*.csv"
chunk_path = TMP_NORM_DIR / f"normalized_chunk_{stamp}.csv"
norm.to_csv(chunk_path, index=False)
print(f"💾 Wrote normalized chunk: {chunk_path}")
print(f"   Columns: {list(norm.columns)}")
print(f"   Rows: {len(norm):,}")

# 2) seed file (qid, first_edit_ts)
#    Note: 03/04 call the column 'first_edit_ts', so we rename here.
seed_out = seed.rename(columns={"first_rev_ts": "first_edit_ts"})[["qid","first_edit_ts"]].copy()
if not seed_out.empty:
    # Ensure proper ISO format
    seed_out["first_edit_ts"] = pd.to_datetime(seed_out["first_edit_ts"], errors="coerce", utc=True)\
                                    .dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    seed_out.dropna(subset=["first_edit_ts"], inplace=True)

seed_path = RAW_DIR / f"seed_enwiki_{stamp}.csv"
seed_out.to_csv(seed_path, index=False)
print(f"💾 Wrote seed file: {seed_path}")
print(f"   Columns: {list(seed_out.columns)}")
print(f"   Rows: {len(seed_out):,}")

print("\n" + "="*60)
print("✅ Bootstrap complete!")
print("="*60)
print("\nNext steps:")
print("1. Re-run notebook 03 (aggregate_and_qc.ipynb)")
print("2. Re-run notebook 06 (statistical_analysis.ipynb)")
print("3. Re-run notebook 07 (intersectional_analysis.ipynb)")
print("4. Re-run notebook 04 (visualization.ipynb)")
print("5. Re-run notebook 05 (dashboard.ipynb)")
print("\nYour dashboard will now include the refreshed data!")
