"""
Configuration file for Streamlit application
"""
import os

# Get the project root directory (parent of app folder)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model paths
MODEL_DIR = os.path.join(PROJECT_ROOT, 'models', 'final_model')
MODEL_PATH = os.path.join(MODEL_DIR, 'rf_tuned_model.pkl')
SCALER_PATH = None  # No separate scaler file
CONFIG_PATH = os.path.join(MODEL_DIR, 'model_config.json')

# Nairobi boundaries (for validation)
NAIROBI_BOUNDS = {
    'lat_min': -1.444471,
    'lat_max': -1.163332,
    'lon_min': 36.650497,
    'lon_max': 37.103729
}

# Default location (Nairobi CBD - City Hall)
DEFAULT_LOCATION = {
    'lat': -1.286389,
    'lon': 36.817223,
    'name': 'Nairobi City Center'
}

# Severity labels
SEVERITY_LABELS = {
    0: 'LOW SEVERITY',
    1: 'HIGH SEVERITY'
}

# Color coding for UI
SEVERITY_COLORS = {
    0: 'green',
    1: 'red'
}

# Recommended actions for dispatchers
RECOMMENDED_ACTIONS = {
    0: [
        " Dispatch Basic Life Support (BLS) unit",
        " Standard response protocol",
        " Monitor situation for updates"
    ],
    1: [
        "🚨URGENT: Dispatch Advanced Life Support (ALS) unit",
        " Alert nearest trauma center (Kenyatta National Hospital)",
        " Prepare for potential critical care",
        " Consider air ambulance if severe traffic"
    ]
}

# App metadata
APP_TITLE = "Emergency Accident Severity Predictor"
APP_ICON = ""
ORGANIZATION = "Nairobi County Emergency Dispatch"
VERSION = "1.0.0"