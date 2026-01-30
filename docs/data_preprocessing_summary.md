# Data Preprocessing Summary

**Date:** January 30, 2026  
**Student:** Mary Wangoi Mwangi (122174)  
**Supervisor:** Prof. Vincent Omwenga  
**Notebook:** `04_data_preprocessing.ipynb`



## Executive Summary

Successfully preprocessed the engineered Ma3Route dataset, transforming 31,064 crash records with 36 features into a machine learning-ready format with 40 encoded features. Applied categorical encoding, numerical normalization, train/validation/test splitting (70/15/15), and SMOTE balancing to address severe class imbalance (15.66:1 ratio). Final datasets are saved in both CSV and pickle formats, ready for model training.



## Preprocessing Pipeline Overview

### Input Dataset
- **Source:** `data/processed/crashes_with_features.csv`
- **Records:** 31,064 crashes
- **Features:** 36 (engineered features)
- **Target:** severity (Fatal/Severe/Moderate/Minor)
- **Data Quality:** 0 missing values, 0 duplicates

### Output Datasets
- **Training Set:** 70,164 samples (with SMOTE) - 40 features
- **Validation Set:** 4,660 samples - 40 features
- **Test Set:** 4,660 samples - 40 features



## Preprocessing Steps

### Step 1: Feature Selection and Cleaning

**Features Dropped (8):**
- `crash_id` - Unique identifier (not predictive)
- `crash_datetime` - Already extracted as temporal features
- `crash_date` - Already extracted as temporal features
- `day_name` - Redundant with day_of_week
- `month_name` - Redundant with month
- `lat_grid` - Redundant with location_grid
- `lon_grid` - Redundant with location_grid
- `location_grid` - Already captured in aggregated features

**Result:** 36 features → 28 features

**Rationale:** Remove redundant and non-predictive features to reduce dimensionality and prevent multicollinearity.



### Step 2: Target Variable Encoding

**Original Target:** `severity` (categorical: FATAL, MINOR, MODERATE, SEVERE)

**Encoding Method:** Label Encoding

**Mapping:**
- FATAL → 0
- MINOR → 1
- MODERATE → 2
- SEVERE → 3

**Result:** Encoded target variable `y_encoded` for model training


### Step 3: Categorical Feature Encoding

**Features Encoded (4):**
1. `time_of_day` (4 categories) → 4 dummy columns
   - Morning, Afternoon, Evening, Night
2. `distance_category` (5 categories) → 5 dummy columns
   - 0-5km, 5-10km, 10-15km, 15-20km, 20+km
3. `frequency_category` (4 categories) → 4 dummy columns
   - Isolated, Low, Moderate, High
4. `location_risk` (4 categories) → 4 dummy columns
   - Low Risk, Moderate Risk, High Risk, Very High Risk

**Encoding Method:** One-Hot Encoding (no drop_first)

**Result:** 
- 4 categorical features → 17 dummy columns
- Total features: 23 + 17 = 40

**Rationale:** One-hot encoding prevents ordinal assumptions and allows models to learn non-linear relationships between categories.



### Step 4: Numerical Feature Normalization

**Features Normalized (14):**
- `latitude`, `longitude`
- `n_crash_reports`
- `hour`, `day_of_week`, `month`, `year`
- `distance_from_center_km`
- `crashes_at_location`
- `severity_numeric`
- `avg_severity_at_location`, `max_severity_at_location`
- `fatal_rate_at_location`, `pedestrian_rate_at_location`

**Normalization Method:** StandardScaler (z-score normalization)

**Formula:** `z = (x - μ) / σ`

**Result:**
- Mean ≈ 0 (actual: -0.000000)
- Standard deviation ≈ 1 (actual: 1.000016)

**Rationale:** Standardization ensures features are on similar scales, preventing distance-based algorithms from being dominated by large-magnitude features.



### Step 5: Boolean Features (No Processing)

**Features Already Binary (9):**
- `contains_fatality_words`
- `contains_pedestrian_words`
- `contains_matatu_words`
- `contains_motorcycle_words`
- `is_morning_rush`
- `is_evening_rush`
- `is_rush_hour`
- `is_weekend`
- `is_hotspot`

**Action:** None required (already 0/1 encoded)



### Step 6: Train/Validation/Test Split

**Split Strategy:**
- **Training:** 70% (21,744 samples)
- **Validation:** 15% (4,660 samples)
- **Test:** 15% (4,660 samples)

**Method:** Stratified sampling (maintains class distribution)

**Random State:** 42 (for reproducibility)

**Class Distribution (Before SMOTE):**

| Class | Training | Validation | Test |
|-------|----------|------------|------|
| FATAL | 1,599 (7.35%) | 342 (7.34%) | 343 (7.36%) |
| MINOR | 17,541 (80.67%) | 3,759 (80.67%) | 3,759 (80.67%) |
| MODERATE | 1,484 (6.82%) | 319 (6.85%) | 318 (6.82%) |
| SEVERE | 1,120 (5.15%) | 240 (5.15%) | 240 (5.15%) |

**Rationale:** 70/15/15 split balances training data volume with sufficient validation/test samples. Stratification ensures representative class distributions.



### Step 7: Class Imbalance Handling (SMOTE)

**Problem Identified:**
- Imbalance ratio: **15.66:1** (MINOR to SEVERE)
- Majority class (MINOR): 17,541 samples
- Minority class (SEVERE): 1,120 samples

**Decision:** SMOTE HIGHLY RECOMMENDED (ratio > 10:1)

**SMOTE Configuration:**
- Method: Synthetic Minority Over-sampling Technique
- Strategy: Balance all classes to majority class size
- k_neighbors: 5
- Random state: 42

**Results:**

**Before SMOTE:**
- Total training samples: 21,744
- FATAL: 1,599 (7.35%)
- MINOR: 17,541 (80.67%)
- MODERATE: 1,484 (6.82%)
- SEVERE: 1,120 (5.15%)

**After SMOTE:**
- Total training samples: 70,164
- FATAL: 17,541 (25.00%)
- MINOR: 17,541 (25.00%)
- MODERATE: 17,541 (25.00%)
- SEVERE: 17,541 (25.00%)

**Synthetic Samples Created:** 48,420

**IMPORTANT:** SMOTE applied ONLY to training set. Validation and test sets retain original class distributions to evaluate real-world performance.

**Rationale:** Training on balanced data prevents model bias toward majority class. Evaluating on imbalanced data assesses real-world performance where crashes are predominantly minor.


## Final Dataset Specifications

### Training Set (with SMOTE)
- **Samples:** 70,164
- **Features:** 40
- **Class Distribution:** Balanced (25% each class)
- **Files:** `X_train_smote.csv/.pkl`, `y_train_smote.csv/.pkl`

### Validation Set
- **Samples:** 4,660
- **Features:** 40
- **Class Distribution:** Original (80.67% MINOR)
- **Files:** `X_val.csv/.pkl`, `y_val.csv/.pkl`

### Test Set
- **Samples:** 4,660
- **Features:** 40
- **Class Distribution:** Original (80.67% MINOR)
- **Files:** `X_test.csv/.pkl`, `y_test.csv/.pkl`



## Feature Composition (40 Total)

| Category | Count | Details |
|----------|-------|---------|
| **Numerical (Normalized)** | 14 | Latitude, longitude, temporal, distance, severity metrics |
| **Boolean (0/1)** | 9 | Fatality, pedestrian, rush hour, weekend indicators |
| **Encoded Categorical** | 17 | Time of day, distance, frequency, risk categories |
| **TOTAL** | **40** | Ready for ML model training |



## Preprocessing Objects Saved

All preprocessing transformations saved for reproducibility:

1. **scaler.pkl** - StandardScaler (fitted on training data)
2. **label_encoder.pkl** - LabelEncoder for target variable
3. **feature_names.pkl** - List of 40 feature names
4. **preprocessing_metadata.pkl** - Complete preprocessing parameters

**Usage:** Load these objects when deploying model to ensure consistent preprocessing.



## Data Quality Validation

### Pre-Preprocessing
- Missing values: 0
- Duplicate rows: 0
- Data types: Verified and appropriate

### Post-Preprocessing
- Feature dimensions: Verified (40 features)
- Normalization: Mean ≈ 0, Std ≈ 1 
- Encoding: All categorical variables converted 
- Split ratios: 70/15/15 confirmed 
- SMOTE balance: 25% per class 



## Comparison with Literature

| Study | Preprocessing Approach | Our Approach |
|-------|------------------------|--------------|
| Getachew et al. (2025) | SMOTE, train/test 80/20 | SMOTE, train/val/test 70/15/15 |
| Mussa et al. (2020) | Normalization, no SMOTE | Normalization + SMOTE |
| Wang et al. (2023) | Basic encoding | One-hot encoding + normalization |

**Advantage:** Comprehensive preprocessing pipeline with validation set for hyperparameter tuning, addressing class imbalance while maintaining realistic evaluation conditions.


## Technical Implementation

### Tools & Libraries
- **Python 3.x** with pandas, numpy
- **scikit-learn:** StandardScaler, LabelEncoder, train_test_split
- **imbalanced-learn:** SMOTE
- **Development:** Jupyter Notebook, VS Code

### Code Quality
-  Reproducible (random_state=42 throughout)
-  Well-documented functions
-  Modular preprocessing steps
-  Quality checks at each stage

### Files Generated
- **Input:** `data/processed/crashes_with_features.csv`
- **Outputs:** 10 files (6 datasets + 4 preprocessing objects)
- **Location:** `data/processed/`
- **Formats:** CSV (human-readable) + Pickle (efficient)

---

## Model Training Readiness

### Ready for Training 
- [x] Data encoded and normalized
- [x] Train/val/test sets created
- [x] Class imbalance addressed
- [x] All datasets saved
- [x] Preprocessing pipeline documented

### Next Steps
1. Load preprocessed data from pickle files
2. Train Random Forest (primary model)
3. Train Gradient Boosting (comparison)
4. Train Logistic Regression (baseline)
5. Hyperparameter tuning with GridSearchCV
6. Model evaluation and selection
7. Final testing on held-out test set


## Expected Model Performance

Based on preprocessing quality and similar studies:

**Target Metrics:**
- Overall Accuracy: >75%
- Per-class Recall: >70% (especially for FATAL)
- Weighted F1-Score: >0.72
- Under-triage Rate: <10%

**Strongest Factors for Success:**
1. Balanced training data (SMOTE)
2. Comprehensive feature engineering (40 features)
3. Proper normalization (prevents feature dominance)
4. Stratified splitting (representative samples)



## Conclusion

Data preprocessing successfully transformed the engineered dataset into a machine learning-ready format. The comprehensive pipeline addresses data encoding, normalization, imbalance handling, and proper train/validation/test splitting. With 70,164 balanced training samples, 40 well-engineered features, and validation/test sets maintaining realistic class distributions, the datasets are optimally prepared for robust model development and evaluation.

**Status:**  **Ready for model training**
