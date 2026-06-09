# Wikipedia Language Equity Analysis

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Status](https://img.shields.io/badge/status-complete-green.svg)

**Quantifying the "Information Gap": How long does critical information take to reach different language communities?**

---

## Project Overview

When a pandemic or disaster strikes, English Wikipedia is updated within hours. But what about the other 7 billion people who don't speak English?

This project analyzes **56 time-sensitive topics** (Public Health, Climate Disasters, Human Rights) across **40 Wikipedia language editions** to quantify systematic information inequality.

### Key Findings

* **23% Coverage Gap**: Low-resource languages cover 23% fewer critical topics (54.1% vs 77.3%)
* **3.2x Update Lag**: Information in low-resource languages is 3.2x more outdated (499 vs 156 days)
* **97.5% Missing Rate**: Essential health topics (Ebola, Monkeypox) missing in 39/40 languages
* **Real Impact**: COVID-19 info in Hausa (80M speakers) appeared **4.7 years late**

**Bottom Line**: Billions of people systematically receive outdated or missing life-saving information.

---

## How It Works

### Data Pipeline

1. **Data Collection** (approximately 2 hours)
   - Queries Wikipedia MediaWiki API for 56 topics × 40 languages = 2,240 data points
   - Fetches creation timestamps and latest edit timestamps
   - Implements caching to reduce API load on subsequent runs

2. **Metric Calculation**
   - **Coverage**: Does the page exist? (Yes/No)
   - **Time-to-Translation**: Days between English creation and target language creation
   - **Update Lag**: Days between English latest edit and target language latest edit

3. **Visualization**
   - 6 interactive charts: heatmaps, coverage charts, distribution plots
   - Reveals patterns of information inequality

### Tech Stack
* **Python 3.12**
* **Pandas** - Data transformation and analysis
* **Requests** - API client with retry logic and caching
* **Plotly** - Interactive HTML visualizations
* **PyArrow** - Efficient Parquet storage format

---

## Getting Started

### Prerequisites

Python 3.8+ installed on your system.

### Installation

```bash
# Install required libraries
pip install requests pandas plotly openpyxl pyarrow
```

### Usage

**Step 1: Run the analysis**
```bash
python wikipedia_analyzer_corrected.py
```
This collects data from Wikipedia (takes approximately 2 hours, uses cache on subsequent runs).

**Step 2: Generate visualizations**
```bash
python visualize_results.py data/language_equity_analysis_v2.csv
```
Creates 6 interactive HTML charts in `visualizations/` folder.

**Step 3: Explore the data**
Open the generated files:
- `data/language_equity_analysis_v2.xlsx` - Excel spreadsheet
- `visualizations/summary_dashboard.html` - Interactive dashboard

---

## Data Scale

- **56 time-sensitive topics** across 7 categories (Public Health, Climate, Human Rights, etc.)
- **40 languages**: 30 major languages + 10 low-resource languages
- **2,240 data points** analyzed
- **626 missing pages** (27.9% coverage gap)

---

## Example Outputs

### Summary Dashboard
Interactive 4-panel dashboard showing:
- Average update lag by language
- Coverage rates (percentage of topics available)
- Distribution of lags (box plots)
- Correlation between translation delay and maintenance

### Update Lag Heatmap
Color-coded matrix (languages × topics):
- Green = Current information
- Yellow = Moderate lag (months)
- Red = Severely outdated (years)

### Coverage Chart
Shows which languages are missing which critical topics.

---

## Key Insights

### Major vs Low-Resource Languages

| Metric | Major Languages | Low-Resource Languages |
|--------|-----------------|------------------------|
| Coverage | 77.3% | 54.1% (-23.2%) |
| Avg Update Lag | 156 days | 499 days (+3.2x) |

### Case Study: COVID-19

| Language | Speakers | Page Created | Info Outdated By |
|----------|----------|--------------|------------------|
| English | Baseline | Jan 5, 2020 | Current |
| German | 90M | Jan 25, 2020 (+20d) | Current |
| Bengali | 265M | Jan 24, 2020 (+19d) | 1 year |
| Hausa | 80M | Oct 2, 2024 (+1731d) | **4.7 years late** |

---

## Repository Structure

```
wikipedia-language-equity/
├── wikipedia_analyzer_corrected.py  # Main analysis script
├── visualize_results.py             # Visualization generator
├── target_languages_40.txt          # 40 target languages
├── topics_critical_50.txt           # 56 critical topics
├── data/
│   ├── language_equity_analysis_v2.csv
│   ├── language_equity_analysis_v2.xlsx
│   └── language_equity_analysis_v2.parquet
├── visualizations/                  # 6 interactive charts
│   └── summary_dashboard.html
└── cache/                           # API response cache
```

---

## Challenges & Limitations

### Challenges
* **API Rate Limiting**: Requires polite delays (0.5-1s) between requests
* **Runtime**: Complete analysis takes approximately 2 hours (caching speeds up subsequent runs)
* **Data Quality**: Some wikis have inconsistent data or are less maintained

### Limitations
* **Timestamp ≠ Quality**: Latest edit time is a proxy; doesn't measure content accuracy
* **Coverage ≠ Completeness**: Page existence doesn't mean information is adequate
* **English Baseline**: Assumes English Wikipedia is the "gold standard" (Western bias)

---

## Policy Recommendations

Based on the findings:

1. **Emergency Response Protocol**: Critical health topics should be translated to all 40 languages within 7 days
2. **Support Low-Resource Languages**: Provide funding and tools to Burmese, Hausa, Nepali communities
3. **Automated Monitoring**: Build real-time dashboard tracking update lags
4. **Governance Reform**: Establish "Language Equity Committee" with binding standards

---

## License

This project is open source under MIT License.  
Wikipedia content is licensed under CC BY-SA 3.0.

---

## Acknowledgments

* Wikipedia community for maintaining multilingual knowledge
* Wikimedia Foundation for API access
* Open source libraries: pandas, plotly, requests

---

**Project Status**: Complete  
**Data Collection Date**: January 26, 2026  
**Total Analysis Time**: Approximately 2 hours  
**Recommended Re-run**: Quarterly for updated metrics
