# builtwith_free_probe.py — BuiltWith FREE API group/category probe
import os, time, requests, pandas as pd
from urllib.parse import urlsplit

API_KEY = os.getenv("BUILTWITH_API_KEY", "").strip()
BASE = "https://api.builtwith.com/free1/api.json"
TIMEOUT = 25
THROTTLE = float(os.getenv("THROTTLE_SECONDS", "1.2"))  # free API says 1 req/sec
UA = {"User-Agent": "hfla-bw-free-probe/0.1"}

# Categories we’ll treat as widgets
WIDGET_CATS = {
    "calendar":    {"Schedule Management"},
    "chatbot":     {"Live Chat"},
    "search":      {"Site Search"},
    "translation": {"Translation"},
}

def normalize_url(u: str):
    if not isinstance(u, str): return None
    u = u.strip().strip(",")
    if not u or u.lower() in ("nan", "#error!"): return None
    if not u.startswith(("http://", "https://")):
        u = "http://" + u
    return u

def read_urls(csv="NCsurvey.csv"):
    # Wide sheet: find a row that looks like URLs
    import pandas as pd, re
    alt = "NCSurvey.csv" if os.path.exists("NCSurvey.csv") else csv
    df = pd.read_csv(alt, header=None)
    labels = ["nc url (if avail)", "nc url", "website url", "empowerla.org nc page url", "empowerla"]
    # scan first ~12 columns for any of those labels
    for c in range(min(12, df.shape[1])):
        col = df.iloc[:, c].astype(str).str.strip().str.lower()
        for lab in labels:
            hits = col[col.str.contains(lab, na=False, regex=False)]
            if not hits.empty:
                i = hits.index[0]
                vals = df.iloc[i, c+1:].astype(str).tolist()
                out = [normalize_url(v) for v in vals]
                out = [u for u in out if u]
                # dedupe, preserve order
                seen, dedup = set(), []
                for u in out:
                    if u not in seen:
                        dedup.append(u); seen.add(u)
                return dedup
    raise SystemExit("Could not find a URL row in NCsurvey.csv/NCSurvey.csv")

def bw_free_lookup(domain: str):
    if not API_KEY:
        raise SystemExit("BUILTWITH_API_KEY is not set. Export it first.")
    params = {"KEY": API_KEY, "LOOKUP": domain}
    r = requests.get(BASE, params=params, headers=UA, timeout=TIMEOUT)
    if r.status_code == 429:
        time.sleep(2.0)
        r = requests.get(BASE, params=params, headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

def main():
    os.makedirs("out", exist_ok=True)
    urls = read_urls()
    domains = [urlsplit(u).netloc.replace("www.","") for u in urls]

    rows = []
    print(f"Found {len(domains)} domains. Sample: {domains[:5]}")
    for i, d in enumerate(domains, 1):
        print(f"[{i}/{len(domains)}] {d}")
        try:
            j = bw_free_lookup(d)
            for g in j.get("groups", []):
                gname = g.get("name", "")
                for c in g.get("categories", []):
                    rows.append({
                        "domain": d,
                        "group": gname,
                        "category": c.get("name",""),
                        "live": int(c.get("live", 0) or 0),
                        "dead": int(c.get("dead", 0) or 0),
                    })
        except Exception as e:
            rows.append({"domain": d, "group": "_error", "category": str(e), "live": 0, "dead": 0})
        time.sleep(THROTTLE)

    df = pd.DataFrame(rows)
    df.to_csv("out/bw_groups_categories.csv", index=False)

      # Build a safe DataFrame even if rows is empty or malformed
    expected_cols = ["domain", "group", "category", "live", "dead"]
    df = pd.DataFrame.from_records(rows)
    if df.empty:
        df = pd.DataFrame(columns=expected_cols)
    else:
        # Ensure all expected columns exist (fill missing with defaults)
        for col in expected_cols:
            if col not in df.columns:
                df[col] = pd.Series(dtype="object")
        # Coerce numeric columns
        for col in ["live", "dead"]:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
        # Keep only expected columns in a stable order
        df = df[expected_cols]

    os.makedirs("out", exist_ok=True)
    df.to_csv("out/bw_groups_categories.csv", index=False)

    # Derive widget booleans from categories in the "widgets" group
    def _flag(dom, catset):
        if df.empty:
            return False
        sub = df[
            (df["domain"] == dom)
            & (df["group"].str.lower() == "widgets")
            & (df["category"].isin(catset))
        ]
        return bool((sub["live"] > 0).any())

    # Use the known domain list even if df has no rows
    uniq = sorted(set(domains))
    flags = []
    for d in uniq:
        flags.append({
            "domain": d,
            "has_calendar":    _flag(d, WIDGET_CATS["calendar"]),
            "has_chatbot":     _flag(d, WIDGET_CATS["chatbot"]),
            "has_search":      _flag(d, WIDGET_CATS["search"]),
            "has_translation": _flag(d, WIDGET_CATS["translation"]),
        })

    wf = pd.DataFrame(flags)
    wf.to_csv("out/bw_widgets_flags.csv", index=False)

    summary = pd.DataFrame({
        "metric": ["has_calendar","has_chatbot","has_search","has_translation"],
        "count": [
            int(wf["has_calendar"].sum()),
            int(wf["has_chatbot"].sum()),
            int(wf["has_search"].sum()),
            int(wf["has_translation"].sum()),
        ],
    })
    summary.to_csv("out/bw_widgets_summary.csv", index=False)
    print("Wrote out/bw_groups_categories.csv, out/bw_widgets_flags.csv, out/bw_widgets_summary.csv")

if __name__ == "__main__":
    main()
