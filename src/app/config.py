"""
Configuration - Emergency Severity Prediction System
Mary Wangoi Mwangi (122174) 
Supervisor: Prof. Vincent Omwenga
"""
import os

# Resolve paths from project root so app works from any launch directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_DIR    = os.path.join(PROJECT_ROOT, 'models', 'final_model')


# ============================================================================
# MODEL PATHS
# ============================================================================
# Three model files saved with joblib.dump() in Notebook 03
RF_MODEL_PATH   = os.path.join(MODEL_DIR, 'rf_model.pkl')
XGB_MODEL_PATH  = os.path.join(MODEL_DIR, 'xgb_model.pkl')
LGBM_MODEL_PATH = os.path.join(MODEL_DIR, 'lgbm_model.pkl')

# ensemble_config.json stores locked weights and threshold from training
CONFIG_PATH   = os.path.join(MODEL_DIR, 'ensemble_config.json')

# feature_metadata.pkl stores the exact 44 feature names and order from training
METADATA_PATH = os.path.join(
    PROJECT_ROOT, 'data', 'features', 'feature_metadata.pkl')


# ============================================================================
# ENSEMBLE CONFIGURATION
# ============================================================================
# Equal weights chosen because the 0.52% gap between equal-weight and
# best single model (LightGBM) was not statistically meaningful
ENSEMBLE_WEIGHTS = {'rf': 0.33, 'xgboost': 0.33, 'lgbm': 0.34}

# Threshold of 0.13 optimised on validation set only (not test set)
# Default 0.50 produced only 10.5% recall — unusable for emergency dispatch
ENSEMBLE_THRESHOLD = 0.13


# ============================================================================
# NAIROBI GEOGRAPHIC BOUNDARIES
# ============================================================================
# Used to validate input coordinates match the Ma3Route training dataset extent
NAIROBI_BOUNDS = {
    'lat_min': -1.444471, 'lat_max': -1.163332,
    'lon_min': 36.650497, 'lon_max': 37.103729
}

DEFAULT_LOCATION = {
    'lat': -1.286389, 'lon': 36.817223,
    'name': 'Nairobi City Centre'
}

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
SEVERITY_LABELS = {0: 'LOW SEVERITY',  1: 'HIGH SEVERITY'}
SEVERITY_COLORS = {0: '#4caf50',       1: '#f44336'}


# Actions aligned with Kenya Red Cross and St John Ambulance dispatch protocols
RECOMMENDED_ACTIONS = {
    0: [
        "Dispatch Basic Life Support (BLS) unit",
        "Standard response protocol applies",
        "Monitor situation for any updates from caller",
    ],
    1: [
        "URGENT: Dispatch Advanced Life Support (ALS) unit immediately",
        "Alert nearest trauma centre — Kenyatta National Hospital",
        "Prepare receiving team for potential critical care",
        "Consider air ambulance if severe traffic congestion",
    ]
}


# ============================================================================
# APP METADATA
# ============================================================================
APP_TITLE    = "Emergency Accident Severity Predictor"
APP_ICON     = " "
ORGANIZATION = "Nairobi County Emergency Dispatch"
VERSION      = "2.0.0"