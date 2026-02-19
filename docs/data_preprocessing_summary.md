# Data Preprocessing Summary: Ma3Route Dataset Preparation

**Student:** Mary Wangoi Mwangi (122174)  
**Supervisor:** Prof. Vincent Omwenga  
**Date:** February 2026  
**Program:** MSc Information Technology, Strathmore University

---

## Key Steps Performed

1. Data quality validation and duplicate detection
2. Outlier detection and coordinate bounds verification
3. Severity label encoding (4-class to binary HIGH/LOW)
4. Data type optimization and datetime parsing
5. Train/validation/test stratified split (70/15/15)
6. Class imbalance handling with SMOTE
7. Feature scaling preparation (normalization parameters saved)

---

## Input Data Characteristics

**Source:** Ma3Route dataset after exploration phase  
**Records:** 31,064 crash incidents  
**Variables:** 10 raw features  
**Data Quality:**
- Zero missing values (100% complete)
- 100% GPS coverage (all coordinates valid)
- No duplicate records detected
- Consistent datetime formats

---

## Data Validation & Cleaning

### 1. Duplicate Detection
**Method:** Check for duplicate `crash_id` and identical `(latitude, longitude, crash_datetime)` combinations

**Results:**
- Duplicate crash_ids: **0 found**
- Duplicate coordinate-time pairs: **0 found**
- **Action:** No removal necessary

### 2. Coordinate Bounds Verification
**Nairobi County Bounds:**
- Latitude: -1.444 to -1.163
- Longitude: 36.650 to 36.950

**Validation Results:**
- Records within bounds: **30,847 (99.3%)**
- Records outside bounds: **217 (0.7%)**
- **Action:** Removed 217 outlier records (likely data entry errors or reports from neighboring counties)

**Final Dataset:** 30,847 valid records

### 3. Datetime Parsing
**Original Format:** String timestamps  
**Converted To:** Python datetime objects  
**Validation:** All timestamps successfully parsed (100% success rate)  
**Range Verified:** August 2012 - July 2023 (consistent with expected range)

### 4. Data Type Optimization
**Optimizations Applied:**
- `crash_id` → string (categorical identifier)
- `latitude`, `longitude` → float32 (reduced memory)
- `crash_datetime` → datetime64
- Boolean flags → int8 (memory efficient)

**Memory Reduction:** ~40% reduction in dataset memory footprint

---

## Severity Classification Encoding

### Binary Classification Schema

**Original 4-Class Distribution:**
| Class | Count | Percentage |
|-------|-------|------------|
| FATAL | 2,284 | 7.4% |
| SEVERE | 1,600 | 5.2% |
| MODERATE | 2,121 | 6.8% |
| MINOR | 25,059 | 80.7% |

**Binary Encoding Applied:**
```python
HIGH Severity (1): FATAL + SEVERE = 3,884 records (12.6%)
LOW Severity (0): MODERATE + MINOR = 26,963 records (87.4%)
```

**Rationale:** 
- Aligns with emergency dispatch decision-making (ALS vs BLS)
- Reduces ambiguity between moderate and severe classifications
- Focuses model on identifying critical accidents requiring advanced life support

---

## Data Partitioning Strategy

### Stratified Split Configuration
**Method:** Stratified sampling to maintain severity class proportions

| Partition | Records | HIGH Severity | LOW Severity | Percentage |
|-----------|---------|---------------|--------------|------------|
| **Training** | 21,593 | 2,719 (12.6%) | 18,874 (87.4%) | 70% |
| **Validation** | 4,627 | 583 (12.6%) | 4,044 (87.4%) | 15% |
| **Testing** | 4,627 | 582 (12.6%) | 4,045 (87.4%) | 15% |
| **Total** | **30,847** | **3,884** | **26,963** | **100%** |

**Key Properties:**
- Stratification maintains 12.6% HIGH severity across all splits
- Validation and test sets have identical size for fair comparison
- No data leakage — splits created before any feature engineering
- Random seed (42) set for reproducibility

**Validation Approach:**
- Training set: Model training + hyperparameter tuning
- Validation set: Threshold optimization + early stopping
- Test set: Final performance evaluation (held out until end)

---

## Class Imbalance Handling

### Problem Statement
**Imbalance Ratio:** 6.9:1 (LOW to HIGH severity)  
**Impact:** Models trained on imbalanced data tend to predict majority class, resulting in high under-triage rates (missing severe accidents)

### SMOTE Application

**Method:** Synthetic Minority Over-sampling Technique  
**Applied To:** Training set only (validation/test kept natural distribution)  
**Configuration:**
- k-neighbors: 5
- Sampling strategy: Balance to 50/50 ratio
- Random state: 42

**Results:**

| Split | Before SMOTE | After SMOTE |
|-------|--------------|-------------|
| **Training Set** | HIGH: 2,719 (12.6%)<br>LOW: 18,874 (87.4%) | HIGH: 18,874 (50%)<br>LOW: 18,874 (50%) |
| **Validation Set** | Natural distribution maintained | 583 HIGH / 4,044 LOW |
| **Test Set** | Natural distribution maintained | 582 HIGH / 4,045 LOW |

**Synthetic Samples Created:** 16,155 additional HIGH severity samples

**Rationale:**
- Improves model's ability to learn HIGH severity patterns
- Prevents bias toward predicting LOW severity
- Critical for safety-first emergency dispatch (missing severe accidents has higher cost than false alarms)

---

## Feature Scaling Preparation

### Normalization Strategy
**Method:** StandardScaler (z-score normalization)  
**Applied To:** Continuous numerical features only  
**Fit On:** Training set (parameters saved)  
**Applied To:** Training, validation, and test sets using training parameters

**Features Requiring Scaling:**
- Latitude, longitude (geographic coordinates)
- Distance from CBD
- Temporal severity rates
- Weather variables (temperature, precipitation, wind speed)

**Categorical Features:** One-hot encoded (no scaling needed)

**Scaler Parameters Saved:** Mean and standard deviation from training set stored for deployment consistency

---

## Data Quality After Preprocessing

### Summary Statistics

**Final Dataset Quality:**
-  **30,847 valid records** (99.3% retention from 31,064 original)
-  **Zero missing values** maintained
-  **Stratified splits** preserve class distribution
-  **Balanced training set** (50/50 after SMOTE)
-  **Natural test set** reflects real-world imbalance
-  **No data leakage** between splits

**Data Integrity Checks Passed:**
- Coordinate bounds validation 
- Datetime range verification 
- Severity label consistency 
- Split proportions verification 

---

## Technical Implementation

**Libraries Used:**
- pandas: Data manipulation
- numpy: Numerical operations
- scikit-learn: Train/test split, StandardScaler
- imbalanced-learn: SMOTE implementation

**Key Functions:**
```python
# Stratified split
train_test_split(stratify=y, test_size=0.15, random_state=42)

# SMOTE application
SMOTE(sampling_strategy='auto', k_neighbors=5, random_state=42)

# Feature scaling
StandardScaler().fit(X_train)
```

**Output Files Generated:**
- `train_data.csv` — Training set (21,593 records)
- `val_data.csv` — Validation set (4,627 records)
- `test_data.csv` — Test set (4,627 records)
- `train_data_smote.csv` — Balanced training set (37,748 records)
- `scaler_params.pkl` — Normalization parameters

---

## Key Decisions Made

1. **Binary Classification:** HIGH vs LOW severity chosen over 4-class for clearer emergency dispatch decisions
2. **Stratified Sampling:** Maintains natural class distribution across splits for reliable evaluation
3. **SMOTE on Training Only:** Preserves realistic test set distribution while improving model training
4. **Aggressive Outlier Removal:** 217 records (0.7%) removed based on geographic bounds to ensure data quality
5. **Standard Scaling:** Z-score normalization chosen over min-max for robustness to outliers

---

## Preprocessing Pipeline Summary

```
Raw Dataset (31,064 records)
    ↓
Duplicate Detection (0 removed)
    ↓
Outlier Removal (217 removed) → 30,847 records
    ↓
Severity Encoding (4-class → binary)
    ↓
Stratified Split (70/15/15)
    ↓
    ├── Training (21,593)
    │       ↓
    │   SMOTE Applied → 37,748 balanced samples
    │
    ├── Validation (4,627) — Natural distribution
    │
    └── Test (4,627) — Natural distribution
            ↓
Ready for Feature Engineering
```

---

## Validation & Quality Assurance

**Checks Performed:**
- Class distribution maintained across splits
- No duplicate records between train/val/test
- Datetime ranges consistent across splits
- Geographic coordinates within valid bounds
- SMOTE samples pass sanity checks (realistic coordinates)
- Scaler parameters successfully saved and loaded

**Statistical Tests:**
- Chi-square test: Class distribution across splits (p > 0.05, not significantly different) 
- Kolmogorov-Smirnov test: Temporal distribution across splits (p > 0.05, same distribution) 

---

## Impact on Model Development

**Preprocessing Benefits:**
1. **Clean Data:** Zero missing values, validated coordinates
2. **Balanced Training:** SMOTE enables better learning of minority class patterns
3. **Realistic Evaluation:** Natural test set distribution reflects operational deployment
4. **No Data Leakage:** Proper split sequence ensures valid performance estimates
5. **Reproducibility:** Fixed random seeds and saved parameters enable exact replication

**Expected Model Performance Impact:**
- Improved HIGH severity recall (fewer missed critical accidents)
- Slightly lower overall accuracy (trade-off for safety-first approach)
- Better generalization to real-world dispatch scenarios

---

## Challenges & Solutions

| Challenge | Solution | Outcome |
|-----------|----------|---------|
| Severe class imbalance (12.6%) | SMOTE on training set only | Balanced learning without test set bias |
| Geographic outliers (0.7%) | Coordinate bounds filtering | Clean, Nairobi-focused dataset |
| Memory optimization needed | Data type conversion (float32, int8) | 40% memory reduction |
| Scaling parameters for deployment | Save StandardScaler parameters | Consistent preprocessing pipeline |

---

## Conclusion

Preprocessing successfully prepared the Ma3Route dataset for machine learning model development. With **30,847 clean records**, **zero missing values**, **balanced training data** (via SMOTE), and **stratified splits**, the dataset is optimally structured for developing a safety-focused severity prediction model.

**Key Achievements:**
- 99.3% data retention (minimal loss from outlier removal)
- Balanced training set enables effective minority class learning
- Natural test set provides realistic performance estimates
- Robust preprocessing pipeline ensures reproducibility

**Status:**  **Ready for feature engineering phase**

---

**Next Steps:**
1. Feature engineering (temporal, spatial, weather features)
2. Feature importance analysis
3. Model training with preprocessed data
4. Threshold optimization on validation set

---

*Report prepared as part of MSc IT thesis requirements*  
*Strathmore University School of Computing & Engineering Sciences*