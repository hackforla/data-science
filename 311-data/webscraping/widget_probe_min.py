# widget_probe_min.py — HTML heuristic for widgets (no "Name..." row needed)
import os, re, time, requests, pandas as pd
from urllib.parse import urlsplit

CSV = "NCSurvey.csv" if os.path.exists("NCSurvey.csv") else "NCsurvey.csv"
OUT_DIR = "out"
THROTTLE_S = 0.3
TIMEOUT_S = 20
UA = {"User-Agent": "Mozilla/5.0 (widget-probe/0.3)"}

# Patterns for common widgets (case-insensitive)
CAL  = [r'fullcalendar', r'calendar\.js', r'/calendar\b', r'\bevents?\b', r'eventbrite\.com', r'time\.ly']
CHAT = [r'tawk\.to', r'crisp\.chat', r'intercom', r'livechatinc', r'zendesk', r'tidio', r'drift\.sh', r'smartsupp']
SRCH = [r'role=["\']search', r'type=["\']search', r'wp-block-search', r'site-search', r'gcse_search']
TRAN = [r'google_translate_element', r'gtranslate', r'translate\.goog', r'weglot', r'lang(uage)?-switch']

URL_LABELS = ["nc url (if avail)", "nc url", "website url",
              "empowerla.org nc page url", "empowerla"]

def normalize_url(u: str):
    if not isinstance(u, str): return None
    u = u.strip().strip(",")
    if not u or u.lower() in ("nan", "#error!"): return None
    if not u.startswith(("http://", "https://")):
        u = "http://" + u
    return u

def any_match(html: str, patterns):
    txt = html.lower()
    return any(re.search(p, txt) for p in patterns)

def find_row_anycol(df, labels, max_search_cols=12):
    for col in range(min(max_search_cols, df.shape[1])):
        series = df.iloc[:, col].astype(str).str.strip().str.lower()
        for lab in labels:
            idx = series[series.str.contains(lab, na=False, regex=False)].index
            if len(idx):
                return int(idx[0]), col
    return None, None

def read_urls(csv_path: str):
    df = pd.read_csv(csv_path, header=None)
    i_url, c_url = find_row_anycol(df, URL_LABELS)
    if i_url is None:
        raise SystemExit("Could not find any URL row. Look for 'NC URL (if avail)' or 'EmpowerLA.org NC page URL'.")

    vals = df.iloc[i_url, c_url+1:].astype(str).tolist()
    urls = [normalize_url(v) for v in vals if isinstance(v, str)]
    urls = [u for u in urls if u]  # drop blanks
    # de-dup, keep order
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            out.append(u); seen.add(u)
    return out

def main():
    if not os.path.exists(CSV):
        raise SystemExit("Missing NCsurvey.csv/NCSurvey.csv in this folder.")
    urls = read_urls(CSV)
    os.makedirs(OUT_DIR, exist_ok=True)

    rows = []
    total = len(urls)
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{total}] {url}")
        rec = {
            "site_domain": urlsplit(url).netloc.replace("www.", ""),
            "url": url,
            "has_calendar": False, "has_chatbot": False,
            "has_search": False, "has_translation": False
        }
        try:
            r = requests.get(url, headers=UA, timeout=TIMEOUT_S)
            r.raise_for_status()
            html = r.text
            rec["has_calendar"]    = any_match(html, CAL)
            rec["has_chatbot"]     = any_match(html, CHAT)
            rec["has_search"]      = any_match(html, SRCH)
            rec["has_translation"] = any_match(html, TRAN)
        except Exception as e:
            rec["error"] = str(e)
        rows.append(rec)
        time.sleep(THROTTLE_S)

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "widgets_report.csv"), index=False)

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
