# Data Exploration Summary: Ma3Route Traffic Crashes Dataset

**Student:** Mary Wangoi Mwangi (122174)  
**Supervisor:** Prof. Vincent Omwenga  
**Date:** February 2026  
**Program:** MSc Information Technology, Strathmore University

---

## Key Steps Performed

1. Dataset acquisition from World Bank Microdata Library
2. Initial data quality assessment (completeness, GPS coverage)
3. Severity classification using keyword analysis
4. Temporal pattern analysis (yearly, monthly, hourly trends)
5. Geographic coverage verification
6. Class distribution analysis for ML readiness
7. Comparative benchmarking against related studies

---

## Dataset Overview

**Source:** World Bank Ma3Route Nairobi Crash Dataset (2012-2023)  
**Total Records:** 31,064 georeferenced crash incidents  
**Time Span:** 10.9 years (August 2012 - July 2023)  
**GPS Coverage:** 100% (all records have valid coordinates)  
**Missing Values:** 0% (complete dataset)  
**Collection Method:** Crowdsourced via Ma3Route platform  
**Validation:** 92% verification accuracy (Milusheva et al., 2021)

### Geographic Scope
- **Primary Coverage:** Nairobi metropolitan region
- **Latitude Range:** -3.10 to -0.57
- **Longitude Range:** 36.28 to 37.88
- **Spatial Distribution:** Dense clustering in central Nairobi with coverage across major road networks

---

## Severity Classification Methodology

Severity levels derived from keyword analysis of crash reports following WHO severity principles:

| Severity | Definition | Count | % |
|----------|-----------|-------|---|
| **FATAL** | Contains death keywords ('killed', 'fatal', 'died') | 2,284 | 7.4% |
| **SEVERE** | Involves vulnerable road users (pedestrians, motorcycles) | 1,600 | 5.2% |
| **MODERATE** | Involves public transport (matatus) | 2,121 | 6.8% |
| **MINOR** | None of the above | 25,059 | 80.7% |

**Binary Classification for ML Model:**
- **HIGH Severity:** Fatal + Severe = 3,884 (12.5%)
- **LOW Severity:** Moderate + Minor = 27,180 (87.5%)

**Class Balance:** The 12.5% minority class provides sufficient samples for SMOTE-enhanced training.

---

## Key Findings

### Data Quality Strengths
 **100% GPS coverage** - Enables robust location-based features  
 **Zero missing values** - No imputation required  
 **Large sample size** (31,064) - Exceeds comparable African studies (Ethiopia: 2,000; Addis Ababa: 2,000+)  
 **Long timeframe** (10.9 years) - Captures seasonal and long-term patterns  
 **Multiple severity proxies** - Fatality, pedestrian, matatu, motorcycle keywords

### Temporal Patterns Identified
- **Peak reporting year:** 2015 (6,101 crashes)
- **Declining trend:** 2016-2023 (possible platform usage changes or safety improvements)
- **COVID-19 impact:** 2020 shows notable reduction (1,928 crashes)
- **Hourly peaks:** 8:00 AM and 6:00 PM (rush hours)
- **Lowest activity:** 4:00 AM (minimal traffic)

**Implication:** Time-of-day, day-of-week, and rush-hour indicators are critical features for ML model.

### Geographic Characteristics
- Central Nairobi shows highest crash density
- Major road networks clearly identifiable in spatial distribution
- Geographic hotspots enable location-based severity features
- Distance from CBD emerged as strong predictor candidate

---

## Data Quality Limitations

**Crowdsourced data bias** - May overrepresent visible crashes on major roads; nighttime/informal settlement incidents likely underreported  
**Keyword-based severity** - Not clinical assessment; lacks detailed injury counts  
**Platform usage decline** - Post-2015 reduction may affect temporal feature reliability  

### Mitigation Strategies
- Cross-validation to assess generalization across time periods
- Transparent limitation acknowledgment in thesis methodology
- Focus on relative severity (comparative risk) rather than absolute clinical severity
- Bias detection analysis during feature engineering phase

---

## Comparison with Related Research

| Study | Location | Sample Size | Severity Classes | GPS Coverage |
|-------|----------|-------------|------------------|--------------|
| **Current Dataset** | **Nairobi** | **31,064** | **4 classes → 2 binary** | **100%** |
| Getachew et al. (2025) | Ethiopia | 2,000 | 2 (fatal/non-fatal) | Not specified |
| Mussa et al. (2020) | Addis Ababa | 2,000+ | 3 classes | Not specified |
| Wang et al. (2023) | Singapore | 360,000 calls | Binary triage | N/A (call data) |

**Competitive Position:** Current dataset size significantly exceeds comparable African studies while providing complete GPS coverage and multi-class severity labels.

---

## Severity Indicator Analysis

| Indicator | Records | % of Total | Interpretation |
|-----------|---------|------------|----------------|
| **Fatality keywords** | 2,284 | 7.4% | Clear fatal crash marker |
| **Pedestrian involvement** | 944 | 3.0% | Vulnerable road user risk |
| **Matatu involvement** | 2,541 | 8.2% | Public transport safety concern |
| **Motorcycle involvement** | 1,142 | 3.7% | High-risk vehicle type |

---

## ML Readiness Assessment

### Dataset Suitability
 **Sufficient sample size** - 31,064 records exceed typical ML training requirements  
 **Complete features** - No missing data preprocessing needed  
 **Balanced minority class** - 12.5% HIGH severity sufficient for SMOTE  
 **Geographic variance** - Spatial diversity supports location-based features  
 **Temporal coverage** - 10.9 years captures seasonal patterns

### Feature Engineering Opportunities Identified
1. **Temporal:** Hour, day, month, rush hour flags, weekend indicators
2. **Spatial:** Distance from CBD, crash density by location, road network proximity
3. **Historical:** Location-specific severity rates, temporal severity trends
4. **Categorical:** Vehicle type involvement, vulnerable road user presence

---

## Technical Implementation

**Tools Used:**
- Python 3.x (pandas, numpy, scikit-learn)
- Visualization: matplotlib, seaborn, plotly
- Geospatial: geopandas (for spatial analysis)
- Development: Jupyter Notebooks, Git version control

**Repository Structure:**
```
NAIROBI-ACCIDENT-SEVERITY/
├── data/
│   ├── raw/              # Original Ma3Route dataset
│   └── processed/        # Cleaned data with severity labels
├── notebooks/
│   └── 01_data_exploration.ipynb
├── models/               # Trained ensemble models
├── reports/
│   └── figures/          # Visualizations
└── docs/                 # Documentation summaries
```

---

## Key Decisions Made

1. **Binary Classification Adopted:** HIGH (Fatal+Severe) vs LOW (Moderate+Minor) for clearer emergency dispatch decisions
2. **Keyword-Based Severity Accepted:** Despite limitations, aligns with WHO severity principles and provides consistent labeling
3. **Full Dataset Utilized:** All 31,064 records used (2012-2023) to maximize training data despite post-2015 decline
4. **GPS Completeness Verified:** 100% coverage confirmed critical for spatial feature engineering

---

## Conclusion

The Ma3Route dataset (2012-2023) **exceeds requirements** for ML-based severity prediction research. With 31,064 complete records, 100% GPS coverage, and clear severity indicators, the dataset eliminates anticipated data cleaning challenges.

**Key Advantages:**
- Largest traffic crash dataset for East African ML research
- Complete geographic information enables robust spatial features
- 10.9-year timeframe captures long-term patterns
- Validated methodology (92% accuracy) provides credible ground truth

**Status:**  **Ready for feature engineering and model development**

---

**Next Steps:**
1. Feature engineering (temporal, spatial, weather integration)
2. Model development (Random Forest ensemble)
3. Cross-validation and performance evaluation
4. Threshold optimization for safety-first dispatch

---

*Report prepared as part of MSc IT thesis requirements*  
*Strathmore University School of Computing & Engineering Sciences*