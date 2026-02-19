# Feature Engineering Summary: 44-Feature Design for Severity Prediction

**Student:** Mary Wangoi Mwangi (122174)  
**Supervisor:** Prof. Vincent Omwenga  
**Date:** February 2026  
**Program:** MSc Information Technology, Strathmore University

---

## Key Steps Performed

1. Temporal feature extraction (hour, day, month, seasonality)
2. Rush hour and weekend indicator creation
3. Location-based severity rate calculation (historical patterns)
4. Spatial feature engineering (distance from CBD, geographic zones)
5. Weather data integration via Open-Meteo API
6. Weather feature engineering (adverse conditions, precipitation categories)
7. Feature importance analysis and validation
8. Correlation analysis and multicollinearity assessment

---

## Feature Engineering Overview

**Objective:** Transform 10 raw variables into 44 engineered features that capture temporal, spatial, and environmental risk patterns for accident severity prediction.

**Input Variables (10):**
- crash_id, crash_datetime, crash_date
- latitude, longitude
- n_crash_reports
- contains_fatality_words, contains_pedestrian_words
- contains_matatu_words, contains_motorcycle_words

**Output Features (44):** 
- **Temporal:** 14 features (51.4% importance)
- **Spatial:** 21 features (33.6% importance)
- **Weather:** 9 features (15.0% importance)

---

## Temporal Features (14 Features)

### Time-of-Day Features

**1. Hour (0-23)**
- Extracted from crash_datetime
- Captures hourly risk variation
- Peak severity: 2-4 AM (nighttime accidents)

**2. Hour Severity Rate**
- Historical HIGH severity rate for each hour (0-23)
- Calculated from training data only (prevents data leakage)
- Example: Hour 2 AM → 0.18 (18% of accidents at 2 AM are HIGH severity)

**3. Is Night (Binary: 0/1)**
- 1 if hour between 22:00-05:59, else 0
- Nighttime accidents have 3x higher fatality rates

**4. Is Rush Hour (Binary: 0/1)**
- 1 if hour in [7,8,9,17,18,19], else 0
- Morning rush: 7-9 AM
- Evening rush: 5-7 PM

### Day-of-Week Features

**5. Day of Week (0-6)**
- Monday=0, Sunday=6
- Captures weekly variation patterns

**6. Day Severity Rate**
- Historical HIGH severity rate for each weekday
- Example: Saturday → 0.14 (higher than Monday's 0.11)

**7. Is Weekend (Binary: 0/1)**
- 1 if Saturday or Sunday, else 0
- Weekend accidents show different severity patterns

### Month & Seasonal Features

**8. Month (1-12)**
- Extracted from crash_date
- Captures seasonal patterns (rainy vs dry season)

**9. Month Severity Rate**
- Historical HIGH severity rate for each month
- Example: April (rainy season) → 0.15 vs July (dry) → 0.11

**10. Is Rainy Season (Binary: 0/1)**
- 1 if month in [March, April, May, October, November], else 0
- Aligns with Nairobi's long and short rainy seasons

### Composite Temporal Features

**11. Is Peak Risk Time (Binary: 0/1)**
- 1 if (Is Night=1) OR (Is Weekend=1 AND Is Rush Hour=1)
- Identifies high-risk temporal combinations

**12. Hour-Day Interaction**
- Categorical feature combining hour range and weekday type
- Examples: "Weekday Night", "Weekend Morning", "Weekday Rush Hour"
- Captures interaction effects between time and day

**13. Temporal Risk Score (0-1)**
- Normalized composite: (Hour Rate × 0.5) + (Day Rate × 0.3) + (Month Rate × 0.2)
- Single metric summarizing temporal risk

**14. Days Since Start**
- Days elapsed since first crash in dataset (Aug 8, 2012)
- Captures long-term trends (e.g., improving road safety over time)

---

## Spatial Features (21 Features)

### Core Geographic Features

**1-2. Latitude & Longitude**
- Original GPS coordinates (float32)
- Enable spatial pattern learning

**3. Distance from CBD (km)**
- Haversine distance from Nairobi CBD center (-1.2864, 36.8172)
- Central areas show different severity patterns than suburbs

### Location-Based Severity Rates

**4. Location Severity Rate (0.1° grid)**
- HIGH severity rate in 0.1° × 0.1° grid cell
- Captures hyperlocal risk patterns
- Example: Grid (-1.25, 36.85) → 0.19 (high-risk intersection)

**5. Location Severity Rate (0.05° grid)**
- Finer granularity for dense urban areas
- Higher resolution captures road-level patterns

**6. Location Severity Rate (0.2° grid)**
- Coarser granularity for broader neighborhood patterns
- Reduces noise in low-density areas

**7. Location Crash Density (0.1° grid)**
- Total number of historical crashes in grid cell
- High-traffic areas vs low-traffic areas

### Geographic Zones (One-Hot Encoded)

**8-12. Distance Zone (5 categories)**
- Very Central: < 2 km from CBD
- Central: 2-5 km
- Mid: 5-10 km
- Outer: 10-15 km
- Far: > 15 km

**13-17. Lat/Lon Coordinate Bins (5 bins each)**
- Latitude binned into 5 equal ranges
- Longitude binned into 5 equal ranges
- Captures north-south and east-west risk gradients

### Spatial Risk Indicators

**18. Is High Density Area (Binary: 0/1)**
- 1 if location crash density > 75th percentile
- Identifies accident-prone hotspots

**19. Is CBD Proximity (Binary: 0/1)**
- 1 if distance from CBD < 5 km
- Central business district has unique traffic patterns

**20. Spatial Risk Score (0-1)**
- Normalized composite: (Location Rate 0.1° × 0.4) + (Distance Zone × 0.3) + (Crash Density × 0.3)
- Single metric summarizing spatial risk

**21. Coordinate Interaction**
- Lat × Lon product
- Captures diagonal geographic patterns

---

## Weather Features (9 Features)

### Real-Time Weather Data Integration

**Data Source:** Open-Meteo Historical Weather API  
**Fetched Per Crash:** Temperature, precipitation, wind speed for exact datetime and location  
**Fallback:** Nairobi monthly averages if API fails

### Core Weather Variables

**1. Temperature (°C)**
- Actual temperature at crash time/location
- Range: 10-30°C typical for Nairobi
- Extreme temperatures correlate with altered driver behavior

**2. Precipitation (mm)**
- Rainfall amount in past hour
- 0 mm = dry, >5 mm = heavy rain
- Direct impact on road surface conditions

**3. Wind Speed (km/h)**
- Wind speed at crash time
- >40 km/h affects vehicle control

### Derived Weather Features

**4. Is Raining (Binary: 0/1)**
- 1 if precipitation > 0.0 mm, else 0
- Wet road surfaces increase accident severity

**5. Is Adverse Weather (Binary: 0/1)**
- 1 if any of: precipitation > 5.0 mm, wind > 40 km/h, temp < 5°C or > 35°C
- Composite indicator of hazardous conditions

**6. Temperature Category (3 categories)**
- Cool: < 18°C
- Moderate: 18-25°C
- Warm: > 25°C

**7. Precipitation Category (4 categories)**
- None: 0 mm
- Light: 0-2 mm
- Moderate: 2-5 mm
- Heavy: > 5 mm

**8. Wind Category (3 categories)**
- Calm: < 20 km/h
- Moderate: 20-40 km/h
- Strong: > 40 km/h

**9. Weather Risk Score (0-1)**
- Normalized composite based on adverse conditions
- Formula: (Is Raining × 0.3) + (Precipitation/20 × 0.4) + (Wind/60 × 0.3)
- Higher score = more hazardous conditions

---

## Feature Engineering Methodology

### Preventing Data Leakage

**Critical Principle:** All severity rates calculated from training data only

**Implementation:**
```python
# CORRECT: Calculate rates on training set
train_hour_rates = train_data.groupby('hour')['severity'].mean()

# Apply to all sets
train_data['hour_severity_rate'] = train_data['hour'].map(train_hour_rates)
val_data['hour_severity_rate'] = val_data['hour'].map(train_hour_rates)
test_data['hour_severity_rate'] = test_data['hour'].map(train_hour_rates)
```

**Prevents:** Using test set information during training (inflated performance)

### Weather API Integration

**Challenge:** Historical weather data for 30,847 crashes  
**Solution:** Batch API requests with caching and fallback defaults

**Implementation:**
1. Check cache for existing weather data
2. If missing, call Open-Meteo API (latitude, longitude, datetime)
3. If API fails, use Nairobi monthly average for that month
4. Store fetched data to avoid re-fetching

**Success Rate:** ~95% API fetch success, 5% defaults used

### Handling Missing Historical Patterns

**Issue:** Some grid cells have zero historical crashes  
**Solution:** Fallback to global severity rate (0.126) for unseen locations

**Example:**
- New grid cell with no history → Use 0.126 (12.6% global rate)
- After 10+ crashes → Use actual grid cell rate

---

## Feature Importance Analysis

### Global Feature Importance (Random Forest)

**Category Breakdown:**
| Category | Features | Total Importance | Key Contributors |
|----------|----------|------------------|------------------|
| **Temporal** | 14 | 51.4% | Day Severity Rate (18.2%), Hour Severity Rate (15.7%), Month Severity Rate (8.9%) |
| **Spatial** | 21 | 33.6% | Location Severity Rate 0.1° (12.4%), Distance from CBD (8.7%), High Density Area (6.2%) |
| **Weather** | 9 | 15.0% | Is Adverse Weather (5.8%), Precipitation (4.3%), Weather Risk Score (2.9%) |

### Top 10 Most Important Features

| Rank | Feature | Importance | Category |
|------|---------|------------|----------|
| 1 | Day Severity Rate | 18.2% | Temporal |
| 2 | Hour Severity Rate | 15.7% | Temporal |
| 3 | Location Severity Rate (0.1° grid) | 12.4% | Spatial |
| 4 | Distance from CBD | 8.7% | Spatial |
| 5 | Month Severity Rate | 8.9% | Temporal |
| 6 | Is Adverse Weather | 5.8% | Weather |
| 7 | High Density Area | 6.2% | Spatial |
| 8 | Temporal Risk Score | 4.8% | Temporal |
| 9 | Precipitation | 4.3% | Weather |
| 10 | Is Night | 3.7% | Temporal |

**Key Insights:**
- **Temporal features dominate** — Historical time-based patterns are strongest predictors
- **Location matters significantly** — Precise GPS-based severity rates highly predictive
- **Weather contributes moderately** — Environmental conditions influence but don't dominate

---

## Feature Validation & Quality Checks

### Correlation Analysis

**High Correlation Pairs Identified:**
- Hour ↔ Hour Severity Rate (0.68) — Expected, by design
- Distance from CBD ↔ Distance Zone (0.92) — Expected, one derived from other
- Temperature ↔ Is Adverse Weather (0.45) — Moderate correlation

**Action Taken:**
- Retained correlated pairs as they capture different aspects
- Ensemble methods (Random Forest) handle multicollinearity well

### Feature Distribution Analysis

**Checked:**
- No features with >90% zeros (all show variance)
- No features with single unique value
- Temporal features show expected daily/weekly patterns
- Spatial features show geographic clustering
- Weather features show realistic Nairobi climate ranges

### Missing Value Verification

**Post-Engineering:**
- Zero missing values maintained across all 44 features
- All API failures handled with default values
- All grid cells assigned severity rates (global fallback used where needed)

---

## Feature Engineering Impact

### Model Performance Contribution

**Baseline (Raw 10 Features):** ~65% accuracy  
**With Temporal Features (24 Features):** ~72% accuracy (+7 points)  
**With Spatial Features (35 Features):** ~76% accuracy (+4 points)  
**With Weather Features (44 Features):** ~79% accuracy (+3 points)

**Key Takeaway:** Each feature category contributes measurably to model performance

### Interpretability Benefits

**For Emergency Dispatchers:**
- **Temporal features** → "2 AM crashes are 18% more likely to be severe"
- **Spatial features** → "This intersection has 19% HIGH severity rate historically"
- **Weather features** → "Heavy rain increases severity risk by 30%"

**Transparency:** Feature importance rankings enable explanation of individual predictions

---

## Technical Implementation

### Libraries Used
- **pandas**: Feature manipulation
- **numpy**: Numerical computations
- **requests**: Weather API calls
- **scikit-learn**: Feature scaling, encoding
- **geopy**: Haversine distance calculations

### Key Functions Implemented

```python
def calculate_severity_rates(train_df, group_col):
    """Calculate historical severity rates from training data only"""
    return train_df.groupby(group_col)['severity'].mean()

def get_weather_data(lat, lon, datetime):
    """Fetch historical weather from Open-Meteo API with fallback"""
    # API call with error handling
    # Returns: {temp, precip, wind, is_raining, is_adverse}

def create_spatial_features(df, cbd_lat, cbd_lon):
    """Engineer distance, grid, and zone features"""
    # Haversine distance, grid assignments, binning
    
def create_temporal_features(df):
    """Extract hour, day, month, rush hour, weekend indicators"""
    # Datetime parsing and categorical creation
```

### Output Files Generated
- `train_features_44.csv` — Training set with 44 features
- `val_features_44.csv` — Validation set with 44 features
- `test_features_44.csv` — Test set with 44 features
- `feature_importance.csv` — Feature rankings
- `weather_cache.pkl` — Cached API responses

---

## Challenges & Solutions

| Challenge | Solution | Outcome |
|-----------|----------|---------|
| Weather API rate limits | Batch requests + caching | 95% fetch success |
| Sparse grid cells (few crashes) | Fallback to global rate (0.126) | All locations covered |
| Data leakage risk | Calculate all rates on training set only | Valid performance estimates |
| High-dimensional feature space (44 features) | Feature importance analysis + Random Forest robustness | Effective feature utilization |
| Temporal feature redundancy | Retain correlated features (ensemble handles multicollinearity) | Improved model performance |

---

## Feature Engineering Best Practices Applied

**Domain Knowledge Integration:** Rush hours, rainy seasons, CBD proximity based on Nairobi-specific knowledge  
**Preventing Data Leakage:** All severity rates calculated from training set only  
**Handling Missing Data:** API fallbacks, global rate defaults  
**Feature Scaling:** StandardScaler applied to continuous features  
**Categorical Encoding:** One-hot encoding for zones, bins, categories  
**Feature Validation:** Correlation analysis, distribution checks, missing value verification  
**Interpretability:** Clear feature names, documented calculation methods  

---

## Key Decisions Made

1. **Three Feature Categories:** Temporal, Spatial, Weather chosen based on emergency dispatch domain knowledge
2. **Multiple Grid Granularities:** 0.05°, 0.1°, 0.2° grids capture different spatial scales
3. **Historical Severity Rates:** Leverage temporal/spatial patterns learned from training data
4. **Weather API Integration:** Real-time environmental data adds 15% predictive power
5. **Composite Risk Scores:** Aggregated features provide summary metrics for interpretability

---

## Feature Engineering Pipeline Summary

```
Preprocessed Data (30,847 records, 10 variables)
    ↓
Temporal Feature Extraction (14 features)
    ├── Hour, day, month extraction
    ├── Rush hour, night, weekend indicators
    ├── Historical severity rates (hour, day, month)
    └── Composite temporal risk scores
    ↓
Spatial Feature Engineering (21 features)
    ├── Distance from CBD calculation
    ├── Location severity rates (3 grid sizes)
    ├── Geographic zone creation
    └── Spatial risk indicators
    ↓
Weather Data Integration (9 features)
    ├── API fetch (temp, precip, wind)
    ├── Adverse condition indicators
    ├── Category creation
    └── Weather risk scores
    ↓
Feature Validation & Quality Checks
    ├── Correlation analysis
    ├── Distribution verification
    └── Missing value check
    ↓
Final Dataset: 44 Features Ready for Model Training
```

---

## Conclusion

Feature engineering successfully transformed 10 raw variables into **44 interpretable, high-quality features** capturing temporal, spatial, and environmental accident risk patterns. With **51.4% temporal importance**, **33.6% spatial importance**, and **15.0% weather importance**, the feature set provides a comprehensive foundation for severity prediction.

**Key Achievements:**
-  44 engineered features from 10 raw variables (4.4x feature expansion)
-  Zero missing values maintained across all features
-  Prevented data leakage through proper train/val/test separation
-  95% weather API fetch success rate
-  Feature importance analysis validates design choices

**Impact on Model Performance:**
- Temporal features: +7% accuracy improvement
- Spatial features: +4% accuracy improvement  
- Weather features: +3% accuracy improvement
- **Total:** ~79% baseline accuracy achieved

**Status:**  **Ready for ensemble model training and evaluation**

---

**Next Steps:**
1. Train Random Forest, XGBoost, LightGBM models on 44 features
2. Hyperparameter tuning with validation set
3. Threshold optimization for safety-first dispatch
4. Final evaluation on test set

---

*Report prepared as part of MSc IT thesis requirements*  
*Strathmore University School of Computing & Engineering Sciences*