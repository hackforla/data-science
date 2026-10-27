# pipelines/refresh_step_1.py
import time
import json
import requests
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone

# =========================
# CONFIG
# =========================
WIKI = "https://en.wikipedia.org/w/api.php"
WD   = "https://www.wikidata.org/w/api.php"

HEADERS = {
    "User-Agent": "WikiGapsRefresh/1.0 (https://github.com/ashhik96; contact: ashhik96@gmail.com)"
}

DATA_DIR     = Path("data")
EVENTS_DIR   = DATA_DIR / "events"
ENTITIES_DIR = DATA_DIR / "entities"
LOGS_DIR     = DATA_DIR / "logs"
CKPT_PATH    = DATA_DIR / "checkpoints.json"

for p in (EVENTS_DIR, ENTITIES_DIR, LOGS_DIR):
    p.mkdir(parents=True, exist_ok=True)

# Biography-ish category keywords (case-insensitive)
BIO_CATEGORY_KEYWORDS = [
    "living people",
    "births", "deaths",
    "people from",
    "footballers", "cricketers", "basketball players", "ice hockey players",
    "actors", "actresses", "singers", "musicians", "rappers",
    "politicians", "writers", "poets", "painters", "sculptors",
    "journalists", "philanthropists", "bishops", "saints"
]

BATCH = 50
POLITE_DELAY = 0.1

# OVERLAP: Each run looks back 2 weeks from the last checkpoint to catch late updates
# Example: If last run was Oct 30, next run fetches from Oct 16 (Oct 30 - 14 days)
OVERLAP_DAYS = 14  # 2 weeks overlap for safety

# =========================
# HELPERS
# =========================
def load_ckpt():
    """Load checkpoint file, initialize if doesn't exist."""
    if not CKPT_PATH.exists():
        # Initialize with project start date (adjust as needed for your project)
        print("⚠️  No checkpoint found. Initializing...")
        default = {"last_run_ts": "2025-01-01T00:00:00Z"}
        save_ckpt(default)
        return default
    
    with open(CKPT_PATH, "r") as f:
        return json.load(f)

def save_ckpt(d):
    with open(CKPT_PATH, "w") as f:
        json.dump(d, f, indent=2)

def batched(items, n=BATCH):
    buf = []
    for x in items:
        buf.append(x)
        if len(buf) == n:
            yield buf; buf=[]
    if buf:
        yield buf

def get_json(url, params, retries=3):
    for i in range(retries):
        r = requests.get(url, params=params, headers=HEADERS, timeout=60)
        if r.status_code in (429, 503):
            time.sleep(1.5 * (i + 1)); continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError(f"Failed after {retries} retries: {params}")

def upsert_csv(path: Path, df_new: pd.DataFrame, key_cols: list):
    if path.exists():
        base = pd.read_csv(path)
        merged = pd.concat([base, df_new], ignore_index=True)
        merged = merged.drop_duplicates(subset=key_cols, keep="last")
    else:
        merged = df_new.copy()
    merged.to_csv(path, index=False)

def is_bio_like(cat: str) -> bool:
    s = (cat or "").lower()
    return any(k in s for k in BIO_CATEGORY_KEYWORDS)

# =========================
# 1) Discover new pages (recentchanges)
# =========================
def discover_new_pages(since_iso: str) -> pd.DataFrame:
    pages = []
    cont = {}
    while True:
        params = dict(
            action="query", format="json", formatversion="2",
            list="recentchanges", rcnamespace="0", rctype="new",
            rcdir="newer", rcprop="title|ids|timestamp",
            rclimit="max", rcstart=since_iso, **cont
        )
        data = get_json(WIKI, params)
        pages.extend(data["query"]["recentchanges"])
        cont = data.get("continue", {})
        if not cont:
            break
    return pd.DataFrame(pages)

# =========================
# 2) Fetch categories & filter biography-like
# =========================
def fetch_categories(pageids):
    rows = []
    for batch in batched(pageids):
        params = dict(
            action="query", format="json", formatversion="2",
            prop="categories", pageids="|".join(map(str, batch)),
            cllimit="max", clshow="!hidden"
        )
        data = get_json(WIKI, params)
        for page in data.get("query", {}).get("pages", []):
            pid = page.get("pageid")
            for cat in page.get("categories", []) or []:
                title = cat.get("title", "")
                if pid and title:
                    rows.append({"pageid": int(pid), "category": title})
        time.sleep(POLITE_DELAY)
    return pd.DataFrame(rows)

# =========================
# 3) QIDs via pageprops
# =========================
def fetch_qids(pageids):
    rows = []
    for batch in batched(pageids):
        params = dict(
            action="query", format="json", formatversion="2",
            prop="pageprops", pageids="|".join(map(str, batch)),
            ppprop="wikibase_item"
        )
        data = get_json(WIKI, params)
        for p in data.get("query", {}).get("pages", []):
            pid = p.get("pageid")
            qid = (p.get("pageprops") or {}).get("wikibase_item")
            if pid and qid:
                rows.append({"pageid": int(pid), "qid": qid})
        time.sleep(POLITE_DELAY)
    return pd.DataFrame(rows)

# =========================
# 4) Wikidata entities (P21/P27/P106)
# =========================
def fetch_wd_entities(qids):
    recs = []
    for batch in batched(qids):
        params = dict(
            action="wbgetentities", format="json",
            ids="|".join(batch), props="claims|labels"
        )
        data = get_json(WD, params)
        ents = data.get("entities", {})
        for q, e in ents.items():
            claims = e.get("claims", {})
            def ids(prop):
                out = []
                for c in claims.get(prop, []):
                    val = c.get("mainsnak", {}).get("datavalue", {}).get("value", {})
                    if isinstance(val, dict) and "id" in val:
                        out.append(val["id"])
                return out
            recs.append({
                "qid": q,
                "P21": ids("P21"),
                "P27": ids("P27"),
                "P106": ids("P106"),
                "label_en": (e.get("labels", {}).get("en") or {}).get("value")
            })
        time.sleep(POLITE_DELAY * 2)
    return pd.DataFrame(recs)

# =========================
# 5) First revision timestamp (creation)
# =========================
def fetch_first_revisions(pageids):
    """Oldest revision per page = article creation time on Wikipedia."""
    rows = []
    for batch in batched(pageids):
        params = dict(
            action="query", format="json", formatversion="2",
            prop="revisions", pageids="|".join(map(str, batch)),
            rvprop="timestamp|ids", rvdir="newer", rvlimit=1
        )
        data = get_json(WIKI, params)
        for page in data.get("query", {}).get("pages", []):
            pid = page.get("pageid")
            if "revisions" in page:
                rev = page["revisions"][0]
                rows.append({
                    "pageid": int(pid),
                    "first_rev_id": rev.get("revid"),
                    "first_rev_ts": rev.get("timestamp")
                })
        time.sleep(POLITE_DELAY)
    return pd.DataFrame(rows)

# =========================
# MAIN
# =========================
def main():
    ckpt = load_ckpt()
    checkpoint_ts = ckpt["last_run_ts"]

    # Calculate month start and grace window
    now_dt = datetime.now(timezone.utc)
    month_start = datetime(now_dt.year, now_dt.month, 1, tzinfo=timezone.utc)
    grace_start = (month_start - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Apply 2-week overlap: go back 14 days from checkpoint
    checkpoint_dt = datetime.fromisoformat(checkpoint_ts.replace('Z', '+00:00'))
    overlap_start = (checkpoint_dt - timedelta(days=OVERLAP_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Choose the later of overlap_start or grace_start
    since = max(overlap_start, grace_start)
    
    print(f"📸 Fetching biographies since: {since}")
    print(f"   (checkpoint={checkpoint_ts}, with {OVERLAP_DAYS}-day overlap → {overlap_start})")
    print(f"   (grace window={grace_start})")

    # 1) Discover
    df_new = discover_new_pages(since)

    print(f"🧭 New mainspace pages: {len(df_new):,}")
    if df_new.empty:
        print("Nothing new. Exiting.")
        return

    # debug dump
    df_new.to_csv(EVENTS_DIR / f"recent_changes_{since[:10]}.csv", index=False)

    # 2) Categories -> biography filter
    pageids = df_new["pageid"].dropna().astype(int).unique().tolist()
    df_cats = fetch_categories(pageids)
    print(f"🏷️ Category rows: {len(df_cats):,}")

    df_cats["is_bio_like"] = df_cats["category"].apply(is_bio_like)
    bio_ids = set(df_cats.loc[df_cats["is_bio_like"], "pageid"].unique().tolist())
    df_bio = df_new[df_new["pageid"].isin(bio_ids)].copy()
    print(f"✅ Biography-like pages: {len(df_bio):,} (of {len(df_new):,})")

    # save filters
    df_cats.to_csv(EVENTS_DIR / f"categories_{since[:10]}.csv", index=False)
    df_bio[["pageid", "title", "timestamp"]].to_csv(
        EVENTS_DIR / f"biography_candidates_{since[:10]}.csv", index=False
    )

    if df_bio.empty:
        print("No biography-like pages; updating checkpoint and exiting.")
        # Save checkpoint with overlap so next run includes buffer
        now = datetime.now(timezone.utc) - timedelta(days=OVERLAP_DAYS)
        ckpt["last_run_ts"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        save_ckpt(ckpt)
        return

    # 3) QIDs for bio pages
    pageids_bio = df_bio["pageid"].astype(int).unique().tolist()
    df_qids = fetch_qids(pageids_bio)
    print(f"🔗 QIDs found: {len(df_qids):,}")

    # 4) Wikidata attributes
    qids = df_qids["qid"].dropna().unique().tolist()
    df_wd = fetch_wd_entities(qids) if qids else pd.DataFrame(columns=["qid","P21","P27","P106","label_en"])
    print(f"📦 WD entities: {len(df_wd):,}")

    # 5) First revisions (creation)
    df_revs = fetch_first_revisions(pageids_bio)
    print(f"🕐 First-rev rows: {len(df_revs):,}")

    # =========================
    # SAVE / UPSERT ARTIFACTS
    # =========================
    # events: creations (guard for empty)
    if not df_revs.empty and "pageid" in df_revs.columns and "first_rev_ts" in df_revs.columns:
        creations = df_revs[["pageid", "first_rev_ts"]].dropna()
        if not creations.empty:
            upsert_csv(EVENTS_DIR / "creations.csv", creations, key_cols=["pageid"])
            print(f"💾 Saved: {EVENTS_DIR / 'creations.csv'}  (upserted)")
        else:
            print("⚠️ No creation timestamps to save this run.")
    else:
        print("⚠️ No revision data returned – skipping creations.csv update.")

    # entities: pageid + qid + attributes
    df_entities = df_qids.merge(df_wd, on="qid", how="left")
    if not df_entities.empty:
        upsert_csv(ENTITIES_DIR / "entities.csv", df_entities, key_cols=["pageid"])
        print(f"💾 Saved: {ENTITIES_DIR / 'entities.csv'} (upserted)")
    else:
        print("⚠️ No entities to save this run.")

    # Move checkpoint forward with overlap buffer
    # This ensures next run will include the last OVERLAP_DAYS of this run
    now = datetime.now(timezone.utc) - timedelta(days=OVERLAP_DAYS)
    ckpt["last_run_ts"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    save_ckpt(ckpt)
    print(f"⭐️ Updated checkpoint to: {ckpt['last_run_ts']} (with {OVERLAP_DAYS}-day overlap)")
    print(f"   Next run will fetch from {(checkpoint_dt - timedelta(days=OVERLAP_DAYS)).strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
