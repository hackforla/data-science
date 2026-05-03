# Representation Gaps in Wikipedia Biographies

## 🚀 Overview

This project measures **representation gaps in Wikipedia biographies** by **gender**, **region**, and **occupation**, and tracks how these shares evolve over time.

The data is pulled directly from the [MediaWiki Action API](https://www.mediawiki.org/wiki/API:Action_API) and [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page), cleaned and aggregated with Python, and analyzed using statistical and intersectional methods to reveal the mathematical structure of systemic bias.

Key goals:
* Quantify who is represented in English Wikipedia biographies
* Track how that representation changes over time
* **Mathematically prove** systemic bias through statistical methods
* **Measure intersectional compounding** - how disadvantages multiply
* Identify systemic gaps to inform targeted improvements for Wikipedia's editorial community
* Make the pipeline reproducible and auto-refreshable

---

## 🌐 Live Dashboard

The final dashboard is fully interactive, allowing for cross-filtering by gender, occupation, and region. It includes:
* **Intersectional analysis visualizations** showing how biases multiply
* **Birth cohort comparisons** demonstrating the "pipeline problem" myth
* **Statistical trend indicators** with significance markers
* **Trajectory analysis** showing which fields are improving vs frozen

*(Update with dashboard preview image and live link once hosted)*

**[➡️ View the Interactive Dashboard Live]()**
*(Update this link once hosted on GitHub Pages)*

---

## 📊 Key Insights & Conclusions

Analysis of English Wikipedia biographies from 2015–2025 shows that representation gaps are not random noise — they are systemic, predictable, and mathematically quantifiable. The total number of new biographies rises and falls over time, but the *proportions* of who gets written about barely move.

### **Structural Bias is Stable and Measurable:**  

The volume of new biographies spiked before 2020 and then fell by ~45% post-pandemic, but gender and regional proportions barely changed. **Concentration indices (Herfindahl-Hirschman Index)** prove this mathematically:
- **Occupational concentration improved slightly** (HHI: 3081 → 2123, -31%)
- **Geographic concentration worsened dramatically** (HHI: 508 → 2159, +325% increase)

This means that even as Wikipedia slowed down, it didn't rebalance who it chooses to document. In fact, coverage became *more* concentrated in Western regions. Bias is baked into the rules of inclusion, not just a side effect of "not enough articles."

### **Gender Gap is Real — and Politically Reactive, Not Steadily Improving:**  

Men still dominate at roughly a 2:1 ratio. **Statistical time series analysis** confirms female representation was improving at **+3.2 percentage points/year** (p = 0.033) even before #MeToo, showing Wikipedia responds to cultural pressure. The female share rose quickly during the #MeToo era (2017–2019), when women's stories were culturally prioritized, but then plateaued in the 2020–2025 period despite high-profile milestones like Kamala Harris becoming the first female, Black, and South Asian U.S. Vice President.

**Changepoint detection algorithms** independently identified **2017 and 2023 as structural breaks** in the data—mathematical confirmation that these aren't just narratives but detectable shifts in Wikipedia's coverage patterns. This matches the broader shift from peak feminist visibility to anti-"woke" backlash and attacks on DEI after 2020. Wikipedia is following cultural pressure, not leading it.

### **The "Pipeline Problem" is a Myth — Proven by Birth Cohort Analysis:**

A common defense of gender gaps claims they'll naturally close as younger, more gender-balanced cohorts enter the historical record. **Analysis of 715,000 biographies with birth year data definitively disproves this hypothesis:**

- People born in the **1990s-2000s** (who came of age during #MeToo): **47.4 pp** gender gap
- People born in the **1970s-1980s** (their parents' generation): **47.2 pp** gender gap
- **The gap is statistically unchanged across 40 years of birth cohorts**

This proves bias is **ongoing, not historical**. Generational replacement won't fix the problem because each new cohort replicates the same 47pp male advantage. The issue is current editorial decisions, not just inherited from the past.

### **Occupational Gatekeeping is Extreme — and Gendered:**  

Four fields (Sports, Arts & Culture, Politics & Law, and STEM & Academia) make up ~98% of biographies and have for a decade. That narrow focus effectively defines who is "notable." Within those fields, the gender deltas are huge:

- Military: ~95% male (+91 pp) — **effectively frozen** at +0.05 pp/year
- Sports: ~90% male (+82 pp)
- Politics & Law: ~75% male (+51 pp) — **improving fastest** at +1.95 pp/year
- Religion: ~85% male (+71 pp) — **completely frozen** at +0.00002 pp/year

**Trajectory analysis** reveals which fields are improving versus frozen: Politics shows measurable progress (likely due to 2018-2020 electoral cycles with record women candidates), while Religion and Military show virtually zero movement. This proves change *is* possible when cultural attention focuses on specific domains, but passive "more articles" growth won't fix representation without targeted intervention.

### **Geography is Skewed — and That Skew Gets Exported Globally:**  

Europe and North America together make up ~60% of biographies. Asia holds only ~25% of biographies despite being ~60% of the world's population, and Africa sits in the single digits. **Location Quotient (LQ) analysis** provides precise statistical measures:

**Most Over-represented (2025):**
- Oceania: **LQ = 5.55** (5.5× over-represented relative to population)
- Europe: **LQ = 3.97** (4.0× over-represented)
- North America: **LQ = 2.81** (2.8× over-represented)

**Most Under-represented (2025):**
- Asia: **LQ = 0.34** (66% under-represented relative to population)
- Africa: **LQ = 0.39** (61% under-represented)

This basic hierarchy (Europe > North America ≫ Asia > Africa) barely shifts across the decade. English Wikipedia exports U.S./UK standards of notability to the rest of the world. If Western media hasn't covered you, you're less "citable," and therefore less "notable," even if you're hugely important in your own country.

### **Intersectional Penalty: The "Double Gap" is Mathematically Quantifiable:**

**Intersectional analysis using logistic regression** reveals how geographic and gender biases multiply rather than simply add:

- Female European military subjects are **10.5× less likely** than male counterparts to have Wikipedia biographies
- This is in a *privileged* region with a *high-visibility* occupation
- Women from underrepresented continents face exponentially worse odds
- Estimated **20× penalty** for female African subjects compared to male European subjects

The disadvantage stacks multiplicatively. A woman academic from Africa or Southeast Asia faces both the gender filter *and* the geographic filter. They need to be extraordinarily visible — often by Western media standards — just to qualify for inclusion at all. This exponential penalty means achieving "notability" requires far more recognition for marginalized groups.

### **Core Conclusion:**  

Wikipedia does not just reflect reality; it reflects which people and professions powerful cultures decide are worth documenting. The current rules systematically favor subjects who are male, Western, and embedded in historically male-coded power structures (military, elite politics, pro sports). 

**Mathematical evidence makes this bias undeniable:**
- 10.5× penalty for women even in favorable conditions
- 47pp gender gap unchanged across 40 years of birth cohorts  
- Geographic concentration quadrupled (2015-2025)
- Fields like Religion frozen at +0.00002 pp/year improvement

Real equity will not come from "more pages in general." It will require deliberate editorial effort to surface the missing kinds of people — especially women and non-Western subjects outside those legacy power domains.

---

## 🧭 Data Pipeline

The project runs in structured stages — both for the **initial build** and the **monthly refresh**.

### Full Analysis Pipeline

| Step | Notebook / Script | Purpose |
|:---|:---|:---|
| 00 | `00_project_setup.ipynb` | Project setup, folder structure, cache initialization |
| 01 | `01_api_seed.ipynb` | Pull initial biography page list from seed categories |
| 02 | `02_enrich_and_normalize.ipynb` | Map to Wikidata QIDs, fetch attributes, clean and normalize |
| 03 | `03_aggregate_and_qc.ipynb` | Build monthly aggregates and run quality checks |
| 04 | `04_visualization.ipynb` | Create core visualizations and charts |
| 05 | `05_statistical_analysis.ipynb` | Interrupted time series, changepoints, Location Quotients, concentration indices |
| 06 | `06_intersectional_analysis.ipynb` | Logistic regression, odds ratios, birth cohort analysis, trajectory analysis |
| 07 | `07_dashboard.ipynb` | Interactive dashboard combining all visualizations and analysis |

**Analysis Methods:**

**Statistical Analysis (Notebook 05):**
- **Interrupted Time Series:** Tests whether #MeToo (2017) and backlash (2020) caused significant trend changes
- **Changepoint Detection:** Algorithmically identifies structural breaks in time series
- **Location Quotients:** Quantifies regional over/under-representation relative to population
- **Concentration Indices (HHI):** Measures inequality in occupational and geographic coverage

**Intersectional Analysis (Notebook 06):**
- **Logistic Regression:** Predicts biography presence based on gender × occupation × region
- **Odds Ratios:** Quantifies multiplicative penalties for marginalized groups
- **Birth Cohort Analysis:** Compares gender gaps across generational cohorts
- **Trajectory Analysis:** Measures improvement rates by occupation field

**Dashboard (Notebook 07):**
- Reads outputs from statistical and intersectional analysis
- Interactive filters and cross-filtering capabilities
- Combines temporal trends, geographic patterns, and intersectional insights

### Monthly Refresh Pipeline

After the initial build, monthly updates follow this streamlined process:

| Step | Script | Purpose |
|:---|:---|:---|
| 1 | `pipelines/refresh_step_1.py` | Fetch new biographies with 2-week overlap |
| 2 | `pipelines/bootstrap_to_original_artifacts.py` | Transform to notebook-compatible format |
| 3 | `notebooks/03_aggregate_and_qc.ipynb` | Re-aggregate with new data |
| 4 | `notebooks/05_statistical_analysis.ipynb` | Update statistical measures |
| 5 | `notebooks/06_intersectional_analysis.ipynb` | Update intersectional metrics |
| 6 | `notebooks/04_visualization.ipynb` | Regenerate visualizations |
| 7 | `notebooks/07_dashboard.ipynb` | Update dashboard with new data |

**Or use the master script:**
```bash
python monthly_refresh.py  # Runs complete workflow automatically
```

**How it works:**
* The first seven notebooks build the complete dataset and perform all analysis from scratch.
* After that, monthly runs of the refresh pipeline keep everything up to date without rebuilding from zero.
* The **2-week overlap** ensures no biographies are missed at month boundaries.

---

## 📆 Monthly Refresh

The project is designed to **auto-refresh once a month** to pull in any newly created biographies without re-running the entire pipeline.

### Quick Start (Automated)

```bash
# Run complete monthly refresh (data collection + all notebooks)
python pipelines/monthly_refresh.py
```

### Manual Steps (If Preferred)

**Step 1: Collect New Data**
```bash
python pipelines/refresh_step_1.py
python pipelines/bootstrap_to_original_artifacts.py
```

**Step 2: Update Analysis** (run in order)
```bash
jupyter nbconvert --execute --inplace 03_aggregate_and_qc.ipynb
jupyter nbconvert --execute --inplace 05_statistical_analysis.ipynb
jupyter nbconvert --execute --inplace 06_intersectional_analysis.ipynb
jupyter nbconvert --execute --inplace 04_visualization.ipynb
jupyter nbconvert --execute --inplace 07_dashboard.ipynb
```

### The 2-Week Overlap Feature

The refresh pipeline includes an intelligent **14-day overlap** to catch articles that received late metadata updates:

```
Example Timeline:
┌──────────────┬──────────────┬──────────────┐
│   September  │   October    │   November   │
└──────────────┴──────────────┴──────────────┘
              ↑              ↑
         Oct 16         Oct 30
    (checkpoint       (run date)
     -14 days)

Run on Oct 30:
├─ Fetches: Jan 1 - Oct 30
└─ Saves checkpoint: Oct 16

Run on Nov 30:
├─ Fetches: Oct 16 - Nov 30
│  ├─ Oct 16-30: Overlap (catches late updates)
│  └─ Oct 30-Nov 30: New data
└─ Saves checkpoint: Nov 16
```

**Why?** Articles created near month boundaries may receive Wikidata properties days later. The overlap ensures these aren't missed, and the upsert logic automatically handles duplicates.

💡 *This ensures your dashboard always stays current without re-running the full historical API calls, while maintaining data integrity.*

---

## 🧾 Data Sources

The project builds on open data from:

* **🕸️ MediaWiki Action API**
    * Used to fetch newly created pages each month
    * Endpoint: `action=query&list=recentchanges`

* **🧠 Wikidata**
    * Used to enrich biographies with structured attributes such as gender, country, and occupation
    * Endpoint: `wbgetentities`
    * Properties used: P21 (gender), P27 (country), P106 (occupation), P569 (birth date)

* **📅 Initial seed categories** (e.g., "Living people", "Births by year", etc.)
    * Used once during the first bootstrap to pull the historical baseline.

📝 *All subsequent refreshes use the incremental fetch pipeline to only add new pages created since the last checkpoint.*

---

## ⚠️ Known Caveats & Limitations

### Data Quality Limitations

* **⏳ API rate limits:** The MediaWiki and Wikidata APIs throttle large bursts of requests.
    * The initial bootstrap took several hours/days because of the volume of pages.
    * Monthly refreshes are much faster since they only fetch new pages.

* **🕵️ Missing or incomplete attributes:**
    * Biographies missing *all three* key attributes (gender, country, occupation) are **excluded entirely** from the dataset.
    * Partial missingness (e.g., missing occupation but known gender) is allowed, and those fields are shown as `Unknown` in the dashboard.
    * A **significant number of biographies lack country values**, even after inferring from place of birth. This means geographic trends likely **underestimate** the true distribution.
    * Birth year data available for ~66% of dataset (715,000 biographies), limiting cohort analysis scope.

### Methodological Choices

* **🧭 Occupation bucketing:** Raw Wikidata occupations are mapped to broader categories (e.g., "actor", "singer", "musician" → *Arts & Culture*). Some specific occupations may be simplified or collapsed.

* **🗺️ Country-to-region mapping:** Countries are aggregated into continents (e.g., "Europe", "Asia") for trend analysis.

* **👥 Gender groups:** The "Other" gender category includes trans, non-binary, genderqueer, and other non-cis identities. Biographies with no stated gender are grouped as 'Unknown'.

* **🌍 English-only scope:** This project analyzes only *English Wikipedia biographies*, not other language editions. Findings reflect Anglophone bias.

* **🕰️ Timestamp gaps:** Pages without valid creation timestamps are excluded from time-based charts. This affects only a small fraction of biographies.

### Statistical & Analytical Limitations

* **📊 Interrupted time series analysis** could not definitively prove #MeToo effect magnitude (p > 0.05 for slope changes), though changepoint detection did identify 2017 as a structural break.

* **🔢 Location Quotients and concentration indices** are descriptive measures and do not establish causation.

* **🧬 Intersectional analysis** focuses on gender × occupation × region but does not capture other axes of marginalization (race, sexuality, disability).

* **⚖️ Odds ratios** assume independence of observations within categories and may not fully capture complex interaction effects.

* **📈 Dashboard reflects coverage, not reality:** Wikipedia data reflects *what is written*, not the real world. Representation gaps should be interpreted as editorial gaps, not population statistics.

### Pipeline Limitations

* **🧹 One-way append:** Monthly refreshes only append new pages; deletions or merges on Wikipedia are not currently reconciled.

* **🔄 Manual intervention required:** While data collection is automated, notebooks must be re-run manually (or via the master script) to update analysis.

📝 *These caveats and methodological notes are documented to maintain transparency and support responsible interpretation of the data. All limitations are disclosed in the final report (`representation_gaps.md`) and dashboard documentation.*

---

## 📁 Project Structure

```
wikipedia-representation-gaps/
├── conf/
│   └── project.json              # Project configuration
├── data/
│   ├── raw/
│   │   └── seed_enwiki_*.csv     # Initial + monthly seed files
│   ├── processed/
│   │   ├── tmp_normalized/
│   │   │   └── normalized_chunk_*.csv  # Chunked normalized data
│   │   └── df_for_charts.csv     # Final aggregated dataset
│   ├── entities/
│   │   └── entities.csv          # Incremental: pageid → QID + properties
│   ├── events/
│   │   └── creations.csv         # Incremental: creation timestamps
│   ├── cache/
│   │   └── id_labels.csv         # Wikidata ID → label cache
│   └── checkpoints.json          # Refresh pipeline checkpoint
├── notebooks/
│   ├── 00_project_setup.ipynb
│   ├── 01_api_seed.ipynb
│   ├── 02_enrich_and_normalize.ipynb
│   ├── 03_aggregate_and_qc.ipynb
│   ├── 04_visualization.ipynb
│   ├── 05_statistical_analysis.ipynb
│   ├── 06_intersectional_analysis.ipynb
│   └── 07_dashboard.ipynb
├── pipelines/
│   ├── refresh_step_1.py
│   ├── bootstrap_to_original_artifacts.py
│   └── monthly_refresh.py
├── outputs/
│   ├── statistical_analysis/      # HHI, LQ, changepoints
│   ├── intersectional_analysis/   # Odds ratios, cohorts
│   └── visualizations/            # Chart outputs
├── representation_gaps.md         # Full analysis report
└── README.md                      # This file
```

---

## 📚 Key Deliverables

* **`representation_gaps.md`** — Complete analytical report with all findings:
  - Statistical rigor throughout with p-values and significance tests
  - Intersectional analysis section quantifying multiplicative biases
  - Birth cohort analysis disproving the "pipeline problem"
  - Mathematical proofs of systemic bias
  - Quantified findings and policy implications

* **`REFRESH_SCRIPTS_README.md`** — Technical documentation of monthly refresh workflow:
  - How 2-week overlap works
  - Troubleshooting guide
  - Integration workflow
  - Expected file sizes and success indicators

* **Interactive Dashboard** — Combines all analysis in a user-friendly interface:
  - Temporal trends with statistical annotations
  - Geographic patterns with Location Quotients
  - Intersectional visualizations showing multiplicative penalties
  - Birth cohort comparisons
  - Trajectory analysis by occupation field

---

## 🔎 References & Useful Links

* 🕸️ [MediaWiki Action API](https://www.mediawiki.org/wiki/API:Action_API) — Documentation for fetching page metadata and revision timestamps.
* 🧠 [Wikidata API](https://www.wikidata.org/wiki/Wikidata:Data_access) — Documentation for structured data access (gender, country, occupation).
* 🗂️ [Wikipedia: Biography Categories](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Biography) — Seed categories used for the initial data collection.
* 📊 [Altair Documentation](https://altair-viz.github.io/) — For interactive charting and visualization.
* 🧰 [Pandas Documentation](https://pandas.pydata.org/docs/) — For data processing and transformations.
* 📈 [Statsmodels](https://www.statsmodels.org/) — For time series analysis and statistical tests.
* 🔬 [Scikit-learn](https://scikit-learn.org/) — For logistic regression and machine learning methods.
* 🌐 [Live Dashboard](#) — Link to the final interactive dashboard *(update once hosted)*.

---

## 🙏 Acknowledgments

This project was developed for **Hack for LA's Wikipedia Representation Gaps** initiative. 

**Methods Inspiration:**
- Interrupted time series analysis adapted from public health intervention studies
- Location Quotient methodology from economic geography literature
- Intersectional analysis frameworks from critical data studies

**Data Sources:**
- Wikimedia Foundation APIs (MediaWiki, Wikidata)
- Population baselines from UN World Population Prospects

---

## 📜 License

This project is released under the MIT License. Data from Wikipedia and Wikidata are available under their respective licenses (CC BY-SA 3.0).

---

**Last Updated:** October 2025  
**Project Status:** Active — Monthly refreshes ongoing  
**Contact:** [Your contact information]
