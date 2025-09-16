import os
import time
import json
import pandas as pd
import requests
from urllib.parse import urlsplit

# --- Keys / endpoints ---
RAPID_KEY = os.getenv("RAPIDAPI_KEY", "")        # if using RapidAPI
# e.g. builtwith-free-api.p.rapidapi.com
RAPID_HOST = os.getenv("RAPIDAPI_HOST", "")
BW_KEY = os.getenv("BUILTWITH_API_KEY", "")   # if calling BuiltWith directly

# RapidAPI free tier is 1 req/sec; direct BuiltWith can be faster depending on plan


def BASE_RAPID(host): return f"https://{host}/free1/api.json"


BASE_BW = "https://api.builtwith.com/free1/api.json"   # free1 endpoint


def normalize_domain(u: str):
    if not isinstance(u, str):
        return None
    u = u.strip()
    if not u:
        return None
    if not u.startswith(("http://", "https://")):
        u = "http://" + u
    netloc = urlsplit(u).netloc.lower().split(":")[0]
    # strip leading www.
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc or None


def read_urls_any_shape(csv_path: str):
    """
    Supports BOTH:
      1) Tall table: a column named like 'url' / 'website'
      2) Wide matrix: a row labeled 'NC URL (if avail)' or 'EmpowerLA.org NC page URL'
         (the label might be in column 0, 1, 2, ...). We scan the first few columns.
    Returns a list of URL strings.
    """
    # Try tall first
    try:
        df_tall = pd.read_csv(csv_path)
        url_cols = [c for c in df_tall.columns if any(
            k in str(c).lower() for k in ("url", "site", "website"))]
        if url_cols:
            vals = df_tall[url_cols[0]].dropna().astype(str).tolist()
            return [v.strip() for v in vals if v.strip()]
    except Exception:
        pass

    # Wide fallback
    df = pd.read_csv(csv_path, header=None)
    # helper: find row index and column index of the label cell

    def find_row_anycol(patterns, max_search_cols=6):
        for col in range(min(max_search_cols, df.shape[1])):
            series = df.iloc[:, col].astype(str).str.strip()
            low = series.str.lower()
            for pat in patterns:
                # literal contains (regex=False) so parentheses don't break it
                idx = low[low.str.contains(pat, na=False, regex=False)].index
                if len(idx):
                    return int(idx[0]), col
        return None, None

    idx_nc, col_nc = find_row_anycol([
        "nc url (if avail)", "nc url", "website url"
    ])
    idx_emp, col_emp = find_row_anycol([
        "empowerla.org nc page url", "empowerla"
    ])

    # read horizontally to the right of the found label cell
    vals_nc = df.iloc[idx_nc,  col_nc +
                      1:].astype(str).tolist() if idx_nc is not None else []
    vals_emp = df.iloc[idx_emp, col_emp +
                       1:].astype(str).tolist() if idx_emp is not None else []

    # prefer NC URL; fall back to EmpowerLA URL slot-by-slot
    n = max(len(vals_nc), len(vals_emp))
    urls = []
    for i in range(n):
        a = (vals_nc[i].strip() if i < len(vals_nc) else "")
        b = (vals_emp[i].strip() if i < len(vals_emp) else "")
        v = a or b
        if not v:
            continue
        v_low = v.lower()
        if v_low in ("nan", "#error!", "none"):
            continue
        urls.append(v)

    # De-dup (preserve order)
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            out.append(u)
            seen.add(u)
    return out


def builtwith_lookup(domain: str, retries=3, backoff=2.0, timeout=25):
    """
    Calls via RapidAPI if RAPID_KEY+RAPID_HOST set; otherwise direct BuiltWith (needs BW_KEY).
    """
    if RAPID_KEY and RAPID_HOST:
        url = BASE_RAPID(RAPID_HOST)
        headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": RAPID_HOST}
        params = {"LOOKUP": domain}
    else:
        if not BW_KEY:
            raise SystemExit(
                "No API credentials. Set RAPIDAPI_KEY+RAPIDAPI_HOST or BUILTWITH_API_KEY.")
        url = BASE_BW
        headers = {}
        params = {"KEY": BW_KEY, "LOOKUP": domain}

    err = None
    for _ in range(retries):
        try:
            r = requests.get(url, headers=headers,
                             params=params, timeout=timeout)
            if r.status_code == 429:                       # rate-limited
                time.sleep(backoff)
                backoff *= 2
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:
            err = e
            time.sleep(backoff)
            backoff *= 2
    raise err


def extract_rows(domain: str, data: dict):
    rows = []
    for res in (data or {}).get("Results", []):
        result = res.get("Result", {})
        for p in result.get("Paths", []):
            for t in p.get("Technologies", []):
                rows.append({
                    "site_domain": domain,
                    "technology": t.get("Name"),
                    "category":   t.get("Tag") or t.get("Category"),
                    "confidence": t.get("Confidence"),
                    "first_detected": t.get("FirstDetected"),
                    "last_detected":  t.get("LastDetected"),
                })
    return rows


def main():
    csv = "NCSurvey.csv" if os.path.exists("NCSurvey.csv") else "NCsurvey.csv"
    if not os.path.exists(csv):
        raise SystemExit(
            "Missing NCSurvey.csv (or NCsurvey.csv) in this folder.")

    urls = read_urls_any_shape(csv)
    if not urls:
        raise SystemExit(
            "No URLs found. Check the CSV content/rows for 'NC URL (if avail)' or 'EmpowerLA.org NC page URL'.")

    # Convert to domains
    domains = []
    for u in urls:
        d = normalize_domain(u)
        if d:
            domains.append(d)
    # De-dup
    domains = list(dict.fromkeys(domains))
    print(f"Found {len(domains)} domains. Sample: {domains[:5]}")

    # Polite delay (RapidAPI free: 1 req/sec)
    delay = 1.0 if RAPID_KEY else 0.5

    raw, all_rows = {}, []
    for i, d in enumerate(domains, 1):
        print(f"[{i}/{len(domains)}] {d}")
        data = builtwith_lookup(d)
        raw[d] = data
        all_rows.extend(extract_rows(d, data))
        time.sleep(delay)

    os.makedirs("out", exist_ok=True)
    with open("out/data.json", "w") as f:
        json.dump(raw, f)

    long = pd.DataFrame(all_rows).dropna(subset=["technology"])
    long.to_csv("out/tech_long.csv", index=False)

    pivot = (long.assign(value=1)
             .pivot_table(index="technology",
                          columns="site_domain",
                          values="value",
                          aggfunc="sum",
                          fill_value=0)
             .sort_index())
    pivot.to_csv("out/tech_table.csv")
    print("Wrote out/data.json, out/tech_long.csv, out/tech_table.csv")


if __name__ == "__main__":
    main()
