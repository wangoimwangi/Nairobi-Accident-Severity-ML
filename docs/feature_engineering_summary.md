# Feature Engineering Summary

**Date:** January 28, 2026  
**Student:** Mary Wangoi Mwangi (122174)  
**Supervisor:** Prof. Vincent Omwenga  
**Notebook:** `03_feature_engineering.ipynb`



## Executive Summary

Successfully engineered **26 new features** from the Ma3Route Road Traffic Crashes dataset (2012-2023), expanding from 10 original columns to 36 features optimized for machine learning severity prediction. Feature engineering focused on temporal patterns, geographic characteristics, crash frequency hotspots, and historical severity indicators.



## Feature Engineering Overview

### Original Dataset
- **Records:** 31,064 crashes
- **Columns:** 10 (raw crash data)
- **Target:** Severity (Fatal/Severe/Moderate/Minor)

### Processed Dataset
- **Records:** 31,064 crashes (unchanged)
- **Columns:** 36 features
- **New Features:** 26 engineered features
- **File:** `data/processed/crashes_with_features.csv`



## Feature Categories

### 1. Temporal Features (11 features)

**Basic Time Components:**
- `hour` (0-23): Hour of day when crash occurred
- `day_of_week` (0-6): Day of week (0=Monday, 6=Sunday)
- `day_name`: Day name (Monday-Sunday)
- `month` (1-12): Month of year
- `month_name`: Month name
- `year`: Year (2012-2023)

**Derived Temporal Features:**
- `is_morning_rush` (Boolean): 7-9 AM indicator
- `is_evening_rush` (Boolean): 5-7 PM indicator
- `is_rush_hour` (Boolean): Morning OR evening rush hour
- `is_weekend` (Boolean): Saturday or Sunday
- `time_of_day` (Categorical): Morning/Afternoon/Evening/Night

**Key Insights:**
- **41.6%** of crashes occur during rush hours
- **75.7%** occur on weekdays
- Morning period has most crashes (12,081)
- Peak hours: 7-8 AM (morning rush), 5-7 PM (evening rush)

**Why These Matter for ML:**
Rush hour crashes may be more severe due to higher traffic density and speed. Weekend patterns differ from weekday commuting patterns.



### 2. Location Features (5 features)

**Distance-Based:**
- `distance_from_center_km` (Continuous): Distance from Nairobi CBD
- `distance_category` (Categorical): 0-5km, 5-10km, 10-15km, 15-20km, 20+km

**Geographic Grid:**
- `lat_grid`: Latitude rounded to 2 decimals (~1km precision)
- `lon_grid`: Longitude rounded to 2 decimals
- `location_grid`: Combined lat_lon identifier for spatial grouping

**Key Insights:**
- **Nairobi CBD:** -1.2864°, 36.8172°
- **Average distance from center:** 11.7 km
- **Crash distribution:** 31.9% within 5km, 31.8% within 5-10km
- **Geographic coverage:** 895 unique grid cells

**Why These Matter for ML:**
Distance from city center correlates with road types (highways vs local streets), traffic density, and emergency response times.



### 3. Hotspot Features (3 features)

**Crash Frequency:**
- `crashes_at_location` (Count): Total crashes at each grid cell
- `is_hotspot` (Boolean): Location in top 10% by crash frequency
- `frequency_category` (Categorical): Isolated/Low/Moderate/High

**Key Insights:**
- **895 unique locations** identified
- **Average 246 crashes per location** (highly concentrated)
- **Top hotspot:** 764 crashes at (-1.29, 36.83)
- **10.6%** of crashes in designated hotspots
- **92.7%** classified as "High" frequency locations

**Top 5 Crash Hotspots:**
1. -1.29, 36.83: 764 crashes
2. -1.28, 36.82: 697 crashes
3. -1.20, 36.92: 664 crashes
4. -1.26, 36.84: 608 crashes
5. -1.28, 36.83: 574 crashes

**Why These Matter for ML:**
Historical crash frequency is a strong predictor of future crashes and severity. Hotspots often indicate dangerous intersections, poor road design, or high-risk areas.



### 4. Historical Severity Features (7 features)

**Severity Metrics:**
- `severity_numeric` (1-4): Numeric encoding (Minor=1, Moderate=2, Severe=3, Fatal=4)
- `avg_severity_at_location` (Continuous): Mean severity at grid cell
- `max_severity_at_location` (1-4): Worst crash severity observed at location
- `fatal_rate_at_location` (0-1): Proportion of fatal crashes at location
- `pedestrian_rate_at_location` (0-1): Proportion with pedestrian involvement
- `location_risk` (Categorical): Low/Moderate/High/Very High Risk

**Key Insights:**
- **Average severity:** 1.39 (mostly minor crashes)
- **Fatal crash rate:** 7.4% average per location
- **Risk distribution:** 86.6% Low Risk, 12.2% Moderate, 1.2% High/Very High
- **Some locations:** 50% fatal crash rate (extremely dangerous)

**Why These Matter for ML:**
Past severity patterns at specific locations strongly predict future severity. Some locations consistently produce more severe crashes due to speed limits, road design, or traffic mix.



## Feature Statistics Summary

| Category | Features | Purpose |
|----------|----------|---------|
| **Original** | 10 | Raw crash data from Ma3Route |
| **Temporal** | 11 | Time-based patterns (rush hour, weekends) |
| **Location** | 5 | Geographic patterns (distance, grid) |
| **Hotspot** | 3 | Crash frequency and concentration |
| **Severity** | 7 | Historical severity patterns |
| **TOTAL** | 36 | Ready for ML model training |



## Data Quality Assessment

### Completeness
- **Total Records:** 31,064
- **Missing Values:** 0 (fixed - all values present)
- **Duplicate Rows:** 0
- **GPS Coverage:** 100%

### Feature Value Ranges

**Temporal:**
- Hour: 0-23
- Day of week: 0-6
- Month: 1-12
- Year: 2012-2023

**Location:**
- Distance from center: 0.02-225 km
- Latitude: -3.10 to -0.57
- Longitude: 36.28 to 37.88

**Hotspot:**
- Crashes at location: 1-764
- Average: 246 crashes per location

**Severity:**
- Average severity: 1.0-4.0
- Fatal rate: 0-100%
- Pedestrian rate: 0-100%



## Machine Learning Readiness

### Features Ready for Model Training

**Categorical Features (Need Encoding):**
- day_name, month_name, time_of_day
- distance_category, frequency_category, location_risk
- severity (TARGET)

**Numerical Features (Can Use Directly):**
- hour, day_of_week, month, year
- distance_from_center_km
- crashes_at_location
- avg_severity_at_location, max_severity_at_location
- fatal_rate_at_location, pedestrian_rate_at_location
- severity_numeric

**Boolean Features (Already 0/1):**
- is_morning_rush, is_evening_rush, is_rush_hour
- is_weekend, is_hotspot
- contains_fatality_words, contains_pedestrian_words
- contains_matatu_words, contains_motorcycle_words



## Next Steps for Model Development

### 1. Data Preprocessing
- Missing values handled (0 remaining)
- Encode categorical variables (one-hot or label encoding)
- Normalize/standardize numerical features
- Split into train/validation/test sets (70/15/15)

### 2. Feature Selection
- Calculate feature importance with Random Forest
- Remove highly correlated features if necessary
- Consider dimensionality reduction if needed

### 3. Handle Class Imbalance
- Apply SMOTE if needed for minority classes
- Use class weighting in model training
- Monitor under-triage rate (target <10%)

### 4. Model Training
- Random Forest (primary)
- Gradient Boosting (comparison)
- Logistic Regression (baseline)



## Expected Model Performance

Based on similar studies and feature quality:

**Target Metrics:**
- Overall Accuracy: >75%
- Fatal Crash Recall: >70% (minimize under-triage)
- Weighted F1-Score: >0.72
- Under-triage Rate: <10%

**Strongest Predictive Features (Expected):**
1. `avg_severity_at_location` (historical patterns)
2. `is_rush_hour` (temporal patterns)
3. `crashes_at_location` (hotspot indicator)
4. `contains_fatality_words` (direct severity proxy)
5. `fatal_rate_at_location` (location risk)



## Comparison with Literature

| Study | Location | Features | Our Work |
|-------|----------|----------|----------|
| Getachew et al. (2025) | Ethiopia | 15 features | 36 features |
| Mussa et al. (2020) | Addis Ababa | 20 features | 36 features |
| Wang et al. (2023) | Singapore | Basic features | Rich historical features |

**Advantage:** Comprehensive temporal, spatial, and historical features engineered from 11 years of data.



## Technical Implementation

### Tools Used
- **Python 3.x** with pandas, numpy
- **Geospatial:** Haversine distance calculations
- **Feature Engineering:** Custom functions for aggregation
- **Development:** Jupyter Notebook, VS Code

### Code Quality
- ✅ Well-documented functions
- ✅ Modular feature creation
- ✅ Quality checks at each step
- ✅ Reproducible pipeline

### Files Generated
- **Input:** `data/raw/ma3route_crashes_2012_2023/ma3route_crashes_algorithmcode.csv`
- **Output:** `data/processed/crashes_with_features.csv`
- **Notebook:** `notebooks/03_feature_engineering.ipynb`



## Conclusion

Feature engineering successfully transformed raw crash data into a rich, ML-ready dataset with 26 new features capturing temporal patterns, geographic characteristics, crash hotspots, and historical severity trends. The engineered features provide multiple angles for the machine learning model to identify severity patterns, significantly improving upon the original 10-column dataset.

**Status:** ✅ **Ready for data preprocessing and model training**

---

**Prepared by:** Mary Wangoi Mwangi  
**Student ID:** 122174  
**Date:** January 28, 2026  
**Supervisor:** Prof. Vincent Omwenga  
**Program:** MSc Information Technology, Strathmore University