"""
Utility Functions for Emergency Severity Prediction System

This module contains helper functions for:
- Loading model artifacts (model, scaler, config)
- Fetching real-time weather data
- Extracting temporal features from timestamps
- Preparing features for prediction
- Analyzing feature importance
"""

# ============================================================================
# IMPORTS
# ============================================================================
import pickle
import json
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import os


# ============================================================================
# MODEL LOADING FUNCTIONS
# ============================================================================
"""
    Load trained Random Forest model and configuration files.
    
    This function handles loading the model saved during training and
    ensures all necessary metadata (feature names, hyperparameters) is available.
    
    Args:
        model_path (str): Path to saved model file (.pkl)
        scaler_path (str): Path to scaler file (None for Random Forest)
        config_path (str): Path to model configuration (.json)
    
    Returns:
        tuple: (model, scaler, config)
            - model: Trained RandomForestClassifier
            - scaler: None (Random Forest doesn't require scaling)
            - config: Dict with feature_names and hyperparameters
    
    Note: Model was saved using joblib.dump() during training
    """
def load_model_artifacts(model_path, scaler_path, config_path):
    
    try:
        import joblib
        
        # Load model (saved with joblib.dump in Notebook 03)
        model = joblib.load(model_path)
        
        # Load scaler if it exists (not used for Random Forest)
        scaler = None
        if scaler_path and os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
        
        # Load model configuration (hyperparameters, metadata)
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Feature names might be in separate file - load if needed
        if 'feature_names' not in config:
            feature_names_path = config_path.replace('model_config.json', 'feature_names.json')
            
            if os.path.exists(feature_names_path):
                with open(feature_names_path, 'r') as f:
                    feature_data = json.load(f)
                    config['feature_names'] = feature_data['feature_names']
            else:
                raise FileNotFoundError("feature_names not found in config or separate file")
        
        return model, scaler, config
    
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Model file not found: {str(e)}")
    except Exception as e:
        raise Exception(f"Error loading model artifacts: {str(e)}")


# ============================================================================
# WEATHER DATA FUNCTIONS
# ============================================================================
"""
    Fetch current weather conditions using Open-Meteo API (free, no key required).
    
    Weather is a critical severity predictor - rain increases severe accident
    probability by ~15% according to model training results.
    
    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate
    
    Returns:
        dict: Weather data with keys:
            - temperature: Current temp in °C
            - precipitation: Current rainfall in mm
            - is_raining: Boolean (True if precipitation > 0)
            - weather_code: WMO weather code
        None: If API call fails
    
    API: Open-Meteo (https://open-meteo.com)
    Typical response time: 1-2 seconds
    """

def get_weather_data(lat, lon):
    
    try:
        # Build API request URL
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,precipitation,weather_code"
            f"&timezone=Africa/Nairobi"
        )
        
        # Make API call with timeout
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            current = data.get('current', {})
            
            # Extract weather metrics
            temp = current.get('temperature_2m', 20)
            precip = current.get('precipitation', 0)
            weather_code = current.get('weather_code', 0)
            
            # Determine rain status (most important weather feature)
            is_raining = precip > 0
            
            return {
                'temperature': temp,
                'precipitation': precip,
                'is_raining': is_raining,
                'weather_code': weather_code
            }
        else:
            return None
            
    except Exception as e:
        print(f"Weather API error: {str(e)}")
        return None


# ============================================================================
# TEMPORAL FEATURE EXTRACTION
# ============================================================================
"""
Extract time-based risk factors from accident timestamp.
Temporal features are the second most important predictor category
after location. Key patterns:
    - Rush hours (7-9 AM, 5-7 PM): 23% higher severe accident rate
    - Night time (10 PM - 5 AM): 31% higher severe accident rate
    - Weekends: Different traffic patterns

Args:
        dt (datetime): Accident timestamp
    
Returns:
    dict: Temporal features
            - hour: Hour of day (0-23)
            - day_of_week: Day (0=Monday, 6=Sunday)
            - month: Month (1-12)
            - is_weekend: Binary (1 if Sat/Sun)
            - is_rush_hour: Binary (1 if peak traffic)
            - is_night: Binary (1 if late night/early morning)
    """
def extract_temporal_features(dt):
    
    return {
        'hour': dt.hour,
        'day_of_week': dt.weekday(),
        'month': dt.month,
        'is_weekend': 1 if dt.weekday() >= 5 else 0,
        'is_rush_hour': 1 if (7 <= dt.hour <= 9) or (17 <= dt.hour <= 19) else 0,
        'is_night': 1 if (dt.hour >= 22 or dt.hour <= 5) else 0
    }


# ============================================================================
# FEATURE PREPARATION FOR PREDICTION
# ============================================================================
"""
Convert raw inputs into model-ready feature vector.
    
This function creates the exact 41 features the model was trained on,
ensuring correct order and format. Missing engineered features
(e.g., historical_severity_rate) are set to 0 as defaults.
    
    Args:
        lat (float): Accident latitude
        lon (float): Accident longitude
        dt (datetime): Accident timestamp
        weather_data (dict): Weather conditions
        feature_names (list): Expected feature names from training (41 features)
    
    Returns:
        pd.DataFrame: Single row with 41 features in correct order
    
    Note: The model expects features in a specific order matching training.
        Any missing engineered features default to 0.
    """

def prepare_features(lat, lon, dt, weather_data, feature_names):
    
    # Extract temporal risk factors
    temporal = extract_temporal_features(dt)
    
    # Extract weather features
    is_raining = weather_data['is_raining'] if weather_data else 0
    temperature = weather_data['temperature'] if weather_data else 20
    
    # Build basic feature dictionary
    features = {
        'latitude': lat,
        'longitude': lon,
        'hour': temporal['hour'],
        'day_of_week': temporal['day_of_week'],
        'month': temporal['month'],
        'is_weekend': temporal['is_weekend'],
        'is_rush_hour': temporal['is_rush_hour'],
        'is_night': temporal['is_night'],
        'is_raining': is_raining,
        'temperature': temperature
    }
    
    # Create DataFrame from features
    df = pd.DataFrame([features])
    
    # Add any missing engineered features with default value 0
    # (e.g., rain_risk_score, historical_severity_rate, etc.)
    for feature in feature_names:
        if feature not in df.columns:
            df[feature] = 0
    
    # Reorder columns to match training data exactly
    df = df[feature_names]
    
    return df


# ============================================================================
# FEATURE IMPORTANCE ANALYSIS
# ============================================================================
"""
Identify which features most influenced this specific prediction.
    
This provides transparency and helps dispatchers understand the model's
reasoning. For example: "Rain risk score contributed 30% to this HIGH
severity prediction."
    
    Args:
        model: Trained RandomForestClassifier
        feature_names (list): All feature names (41 features)
        features_df (pd.DataFrame): Current prediction features
        top_n (int): Number of top features to return (default: 5)
    
    Returns:
        pd.DataFrame: Top N features sorted by importance
            Columns: feature, importance, value
    
Note: Importance scores come from Random Forest's built-in
    feature_importances_ attribute (mean decrease in impurity)
    """
def get_feature_importance_top_n(model, feature_names, features_df, top_n=5):
    
    # Get global feature importances from trained model
    importances = model.feature_importances_
    
    # Get actual feature values for this prediction
    feature_values = features_df.iloc[0]
    
    # Combine into DataFrame for analysis
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances,
        'value': feature_values
    })
    
    # Sort by importance (highest first)
    importance_df = importance_df.sort_values('importance', ascending=False)
    
    # Return top N most influential features
    return importance_df.head(top_n)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
"""
Convert technical feature names to human-readable labels.
    
    Example: 'is_rush_hour' → 'Rush Hour'
    
    Args:
        feature_name (str): Raw feature name from model
    
    Returns:
        str: User-friendly feature label
    """

def format_feature_name(feature_name):
    
    # Map common features to readable names
    replacements = {
        'latitude': 'Location (Latitude)',
        'longitude': 'Location (Longitude)',
        'hour': 'Hour of Day',
        'day_of_week': 'Day of Week',
        'month': 'Month',
        'is_weekend': 'Weekend',
        'is_rush_hour': 'Rush Hour',
        'is_night': 'Night Time',
        'is_raining': 'Rainy Weather',
        'temperature': 'Temperature',
        'rain_risk_score': 'Rain Risk Score',
        'historical_severity_rate': 'Historical Severity Rate',
        'nearby_severe_count': 'Nearby Severe Accidents'
    }
    
    # Return mapped name or format raw name
    if feature_name in replacements:
        return replacements[feature_name]
    else:
        # Default: replace underscores and title case
        return feature_name.replace('_', ' ').title()

# ============================================================================
# VALIDATION
# ============================================================================
"""
Check if coordinates fall within Nairobi County boundaries.
    
    Nairobi County Bounds:
    - Latitude: -1.44 to -1.16 (South to North)
    - Longitude: 36.65 to 37.10 (West to East)
    
    Args:
        lat (float): Latitude
        lon (float): Longitude
        bounds (dict): Boundary dictionary with lat_min, lat_max, lon_min, lon_max
    
    Returns:
        bool: True if coordinates within Nairobi, False otherwise
    """
def validate_coordinates(lat, lon, bounds):
    
    return (
        bounds['lat_min'] <= lat <= bounds['lat_max'] and
        bounds['lon_min'] <= lon <= bounds['lon_max']
    )