
# Processed Dataset Documentation
Generated: 2026-02-10 01:16:30.371928

## Overview
These datasets are ready for machine learning model training and evaluation.
All features are dispatch-time available (no data leakage).

## Files Generated
1. train_balanced.csv - Training set with SMOTE balancing
2. validation.csv - Validation set with natural class distribution
3. test.csv - Test set with natural class distribution
4. *.npy - Numpy array versions for sklearn
5. feature_metadata.pkl - Feature names and metadata

## Dataset Sizes
- Training:   38,072 samples (38,072) - SMOTE-balanced 1:1
- Validation: 4,648 samples (4,648) - Natural 7:1
- Test:       4,660 samples (4,660) - Natural 7:1
- Total:      31,064 samples (31,064 original)

## Feature Set
Total features: 41
- Numeric features: 24
- Encoded categorical: 17

## Feature Categories
1. Location (2): latitude, longitude
2. Temporal (11): hour, day, month, year, weekend, severity rates, night, rush_hour
3. Spatial (6): crashes_at_location, high_rate_at_location, risk indicators
4. Weather (5): season, rain_risk, daylight_status, compound risks
5. Road Infrastructure (6): road_type, intersection, speed, zone, distance
6. Encoded Categorical (17): one-hot encoded versions

## Target Variable
- Binary classification: LOW (0) vs HIGH (1) severity
- Training distribution: 50/50 (after SMOTE)
- Val/Test distribution: 87.5% LOW, 12.5% HIGH (natural)

## Data Processing Applied
1. Missing value imputation (location_risk_category)
2. Data leakage removal (5 keyword flag features removed)
3. Feature engineering (8 temporal + 5 weather + 6 infrastructure)
4. Categorical encoding (one-hot encoding)
5. Train/val/test stratified split (70/15/15)
6. SMOTE applied to training set only

## Next Steps
Use these datasets in Notebook 03 for:
1. Model training (Random Forest as primary)
2. Hyperparameter tuning (using validation set)
3. Final evaluation (using test set)
4. Performance comparison with baseline models
