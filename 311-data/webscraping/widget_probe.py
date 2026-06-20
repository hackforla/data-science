# widget_probe.py — heuristic HTML scan (no BuiltWith needed)
import os, re, time, requests, pandas as pd

CSV = "NCSurvey.csv" if os.path.exists("NCSurvey.csv") else "NCsurvey.csv"
OUT_DIR = "out"
THROTTLE_S = 0.3
TIMEOUT_S = 20

# --- patterns to detect common widgets (case-insensitive) ---
CAL_PATTERNS  = [r'fullcalendar', r'calendar\.js', r'/calendar\b', r'\bevents?\b', r'eventbrite\.com', r'time\.ly']
CHAT_PATTERNS = [r'tawk\.to', r'crisp\.chat', r'intercom', r'livechatinc', r'zendesk', r'tidio', r'drift\.sh', r'smartsupp']
SEARCH_PATS   = [r'role=["\']search', r'type=["\']search', r'wp-block-search', r'site-search', r'gcse_search']
TRANS_PATS    = [r'google_translate_element', r'gtranslate', r'translate\.goog', r'weglot', r'lang(uage)?-switch']

UA = {"User-Agent": "Mozilla/5.0 (widget-probe/0.1)"}

def normalize_url(u: str):
    if not isinstance(u, str): return None
    u = u.strip()
    if not u or u.lower() in ("nan", "#error!"): return None
    if not u.startswith(("http://", "https://")):
        u = "http://" + u
    return u

def any_match(html: str, patterns):
    txt = html.lower()
    return any(re.search(p, txt) for p in patterns)

def read_wide_csv_pairs(csv_path: str):
    """Return parallel lists: [(nc_name, url), ...] reading the 'wide' matrix."""
    df = pd.read_csv(csv_path, header=None)
    lab = df.iloc[:,0].astype(str).str.strip().str.lower()

    def find(label):
        idx = lab[lab.str.contains(label, na=False, regex=False)].index
        return int(idx[0]) if len(idx) else None

    i_name = find("name of neighborhood council")
    i_nc   = find("nc url (if avail)")
    i_emp  = find("empowerla.org nc page url")

    if i_name is None:
        raise SystemExit("Could not find the 'Name of Neighborhood Council (NC)' row.")
    if i_nc is None and i_emp is None:
        raise SystemExit("Could not find URL rows ('NC URL (if avail)' or 'EmpowerLA.org NC page URL').")

    names = df.iloc[i_name, 1:].astype(str).tolist()
    urls_nc  = df.iloc[i_nc,  1:].astype(str).tolist() if i_nc  is not None else []
    urls_emp = df.iloc[i_emp, 1:].astype(str).tolist() if i_emp is not None else []

    out = []
    n = max(len(names), len(urls_nc), len(urls_emp))
    for i in range(n):
        name = (names[i].strip() if i < len(names) else "")
        raw  = (urls_nc[i].strip() if i < len(urls_nc) else "") or (urls_emp[i].strip() if i < len(urls_emp) else "")
        url  = normalize_url(raw)
        if url:
            out.append((name, url))
    # de-dup by URL, keep first name seen
    seen, dedup = set(), []
    for name, url in out:
        if url not in seen:
            dedup.append((name, url)); seen.add(url)
    return dedup

def main():
    if not os.path.exists(CSV):
        raise SystemExit("Missing NCsurvey.csv/NCSurvey.csv in this folder.")
    pairs = read_wide_csv_pairs(CSV)
    os.makedirs(OUT_DIR, exist_ok=True)

    rows = []
    total = len(pairs)
    for i, (name, url) in enumerate(pairs, 1):
        print(f"[{i}/{total}] {url}")
        rec = {"nc_name": name, "url": url, "has_calendar": False, "has_chatbot": False,
               "has_search": False, "has_translation": False}
        try:
            r = requests.get(url, headers=UA, timeout=TIMEOUT_S)
            r.raise_for_status()
            html = r.text
            rec["has_calendar"]    = any_match(html, CAL_PATTERNS)
            rec["has_chatbot"]     = any_match(html, CHAT_PATTERNS)
            rec["has_search"]      = any_match(html, SEARCH_PATS)
            rec["has_translation"] = any_match(html, TRANS_PATS)
        except Exception as e:
            rec["error"] = str(e)
        rows.append(rec)
        time.sleep(THROTTLE_S)

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "widgets_report.csv"), index=False)

    # quick summary counts
    summary = pd.DataFrame({
        "metric": ["has_calendar","has_chatbot","has_search","has_translation"],
        "count":  [int(df["has_calendar"].sum()),
                   int(df["has_chatbot"].sum()),
                   int(df["has_search"].sum()),
                   int(df["has_translation"].sum())]
    })
    summary.to_csv(os.path.join(OUT_DIR, "widgets_summary.csv"), index=False)

    print("Wrote out/widgets_report.csv and out/widgets_summary.csv")

if __name__ == "__main__":
    main()
