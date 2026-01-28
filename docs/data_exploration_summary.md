# Data Exploration Summary: Road Traffic Crashes 2012-2023
**Date:** January 27, 2026  
**Student:** Mary Wangoi Mwangi (122174)  
**Supervisor:** Prof. Vincent Omwenga



## Executive Summary

Successfully acquired and explored the Ma3Route Road Traffic Crashes dataset (2012-2023), containing **31,064 georeferenced crash records** spanning 10.9 years. The dataset demonstrates exceptional quality with **100% GPS coverage** and **zero missing values**, making it ideal for machine learning-based severity prediction.



## Dataset Overview

### Basic Statistics
- **Total Records:** 31,064 crash incidents
- **Time Period:** August 8, 2012 - July 12, 2023 (10.9 years)
- **Geographic Coverage:** Nairobi region (Lat: -3.10 to -0.57, Lon: 36.28 to 37.88)
- **GPS Coverage:** 100% (all records have valid coordinates)
- **Missing Values:** 0% (complete dataset)

### Data Structure
- **10 Variables:** crash_id, crash_datetime, crash_date, latitude, longitude, n_crash_reports, contains_fatality_words, contains_pedestrian_words, contains_matatu_words, contains_motorcycle_words
- **Data Source:** World Bank Microdata Library
- **Collection Method:** Crowdsourced reports from Ma3Route platform
- **Validation:** Algorithm-coded (Milusheva et al., 2021) with 92% verification accuracy



## Severity Classification

### Methodology
Severity levels derived from keyword analysis of crash reports:
- **FATAL:** Contains death-related keywords ('dead', 'died', 'killed', 'fatal', 'body')
- **SEVERE:** Involves vulnerable road users (pedestrians, motorcycles)
- **MODERATE:** Involves public transport (matatus)
- **MINOR:** None of the above

### Severity Distribution

| Severity | Count | Percentage |
|----------|-------|------------|
| **MINOR** | 25,059 | 80.7% |
| **FATAL** | 2,284 | 7.4% |
| **MODERATE** | 2,121 | 6.8% |
| **SEVERE** | 1,600 | 5.2% |

**Class Balance Assessment:** The distribution shows reasonable balance for machine learning, with 19.3% of crashes classified as moderate-to-fatal severity. This is sufficient for training robust classification models.



## Severity Indicators Analysis

| Indicator | Count | Percentage | Interpretation |
|-----------|-------|------------|----------------|
| Fatality keywords | 2,284 | 7.35% | Clear marker for fatal crashes |
| Pedestrian involvement | 944 | 3.04% | Vulnerable road user crashes |
| Matatu involvement | 2,541 | 8.18% | Public transport safety concern |
| Motorcycle involvement | 1,142 | 3.68% | High-risk vehicle type |



## Temporal Patterns

### Crashes by Year

| Year | Crashes | Notes |
|------|---------|-------|
| 2012 | 310 | Partial year (started Aug) |
| 2013 | 1,398 | - |
| 2014 | 4,014 | Increasing trend |
| **2015** | **6,101** | **Peak year** |
| 2016 | 4,219 | - |
| 2017 | 2,698 | Declining trend begins |
| 2018 | 3,194 | - |
| 2019 | 2,739 | - |
| 2020 | 1,928 | COVID-19 impact likely |
| 2021 | 1,937 | - |
| 2022 | 1,805 | - |
| 2023 | 721 | Partial year (Jan-Jul) |

**Key Observation:** Peak crash reporting in 2015 (6,101 crashes), followed by sustained decline. The 2020-2021 reduction likely reflects COVID-19 lockdown effects on traffic.

### Hourly Crash Patterns
- **Morning peak:** 8:00 AM (rush hour)
- **Evening peak:** 6:00 PM (rush hour)
- **Lowest:** 4:00 AM (minimal traffic)

**Implication:** Crash severity prediction models should incorporate time-of-day features, particularly rush hour indicators.



## Geographic Coverage

- **100% GPS coverage** - All 31,064 crashes have valid coordinates
- **Coverage area:** Primarily Nairobi metropolitan region
- **Spatial distribution:** Dense clustering in central Nairobi with crashes spread across major road networks
- **Hotspot identification:** Clear geographic patterns visible, enabling location-based severity features

**Comparison to Previous Dataset:**
- Old dataset (2017-2018): 44% GPS coverage (4,191/9,479)
- New dataset (2012-2023): **100% GPS coverage** (31,064/31,064)
- **Improvement:** +56 percentage points in GPS data availability



## Data Quality Assessment

### Strengths 
1. **Complete GPS coverage** (100%) - enables robust location-based features
2. **Zero missing values** - no need for imputation
3. **Large sample size** (31,064) - sufficient for ML training
4. **Long timeframe** (10.9 years) - captures seasonal and yearly patterns
5. **Validated methodology** - algorithm verified at 92% accuracy (Milusheva et al., 2021)
6. **Multiple severity proxies** - fatality, pedestrian, vehicle type keywords

### Limitations 
1. **Crowdsourced data bias** - may overrepresent visible crashes on major roads
2. **Keyword-based severity** - not clinical assessment (but aligns with WHO principles)
3. **Declining reports after 2015** - potential platform usage changes
4. **No injury count data** - severity inferred from keywords only

### Mitigation Strategies
- Use cross-validation to assess model generalization
- Compare algorithm-coded (31,064) with manual-coded subset (2,595) for validation
- Acknowledge limitations transparently in thesis methodology section
- Focus on relative severity (comparative) rather than absolute clinical severity



## Comparison with Related Research

| Study | Location | Sample Size | Severity Classes | Our Dataset |
|-------|----------|-------------|------------------|-------------|
| Getachew et al. (2025) | Ethiopia | 2,000 | 2 (fatal/non-fatal) | **31,064** |
| Mussa et al. (2020) | Addis Ababa | 2,000+ | 3 classes | **31,064** |
| Wang et al. (2023) | Singapore | 360,000 calls | Binary | **31,064 + severity** |

**Competitive Advantage:** Our dataset size exceeds similar African studies while providing multi-class severity labels.

---

## Next Steps

### Immediate (This Week)
1. ✅ Dataset acquired and explored
2. ✅ Severity classification implemented
3. ⏳ Feature engineering (temporal, spatial, historical features)
4. ⏳ Data preprocessing for ML (normalization, encoding)

### Short-term (Next 2 Weeks)
5. Model development (Random Forest, Gradient Boosting, Logistic Regression)
6. Hyperparameter tuning and cross-validation
7. Model evaluation and comparison

### Medium-term (Next 4 Weeks)
8. Results analysis and interpretation
9. Thesis writing (methodology, results, discussion chapters)
10. Prepare for final defense



## Technical Implementation

### Tools & Libraries
- **Python 3.x** with pandas, numpy, scikit-learn
- **Visualization:** matplotlib, seaborn
- **Geospatial:** geopandas (if needed for advanced spatial analysis)
- **Development:** Jupyter Notebooks, VS Code, Git

### Repository Structure

Nairobi-Accident-Severity/
├── data/
│   ├── raw/                    # Original datasets
│   └── processed/              # Cleaned data with severity labels
├── notebooks/
│   └── 02_new_dataset_exploration.ipynb
├── reports/
│   └── figures/                # Visualizations
└── src/                        # Python modules (future)
```



## Preliminary Findings

1. **Dataset Quality Exceeds Expectations**
   - 100% GPS coverage 
   - Zero missing values simplifies preprocessing pipeline

2. **Severity Distribution is ML-Friendly**
   - 19.3% severe/moderate/fatal crashes provides sufficient minority class samples
   - May still require SMOTE for optimal model training

3. **Clear Temporal Patterns**
   - Rush hour peaks align with expected traffic patterns
   - Yearly decline suggests possible safety improvements or reporting changes

4. **Geographic Hotspots Identifiable**
   - Central Nairobi shows highest density
   - Location-based features will be strong predictors


## Conclusion

The Ma3Route Road Traffic Crashes dataset (2012-2023) **exceeds requirements** for the thesis research. With 31,064 complete records, 100% GPS coverage, and clear severity indicators, we can proceed confidently to feature engineering and model development. The dataset's quality eliminates anticipated data cleaning challenges, potentially accelerating the research timeline.

**Status:** ✅ **Ready to proceed with feature engineering and model development**



**Prepared by:** Mary Wangoi Mwangi  
**Student ID:** 122174  
**Date:** January 27, 2026  
**Supervisor:** Prof. Vincent Omwenga  
**Program:** MSc Information Technology, Strathmore University