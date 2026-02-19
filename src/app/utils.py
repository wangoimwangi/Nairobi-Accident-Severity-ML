"""
Utility Functions — Emergency Severity Prediction System
Mary Wangoi Mwangi (122174) 

All feature engineering here mirrors Notebook 02 exactly.
Any divergence would cause silent prediction errors at inference time.
"""

import os, pickle, json
import numpy as np
import pandas as pd
from datetime import datetime
import requests


# ============================================================================
# MODEL LOADING
# ============================================================================

def load_ensemble_models(rf_path, xgb_path, lgbm_path,
                        config_path, metadata_path):
    """
    Load all three trained models and feature metadata.
    feature_metadata.pkl is the single source of truth for
    the 44 feature names and their exact order.
    """
    import joblib

    rf_model   = joblib.load(rf_path)
    xgb_model  = joblib.load(xgb_path)
    lgbm_model = joblib.load(lgbm_path)

    with open(config_path, 'r') as f:
        config = json.load(f)

    with open(metadata_path, 'rb') as f:
        metadata = pickle.load(f)

    feature_names = metadata['feature_names']  # 44 features

    return rf_model, xgb_model, lgbm_model, config, feature_names


# ============================================================================
# WEATHER DATA
# ============================================================================

def get_weather_data(lat, lon):
    """
    Fetch current weather from Open-Meteo API (free, no key required).
    Uses the same API and variables as training — ensures consistency.
    Weather contributed 15% of total feature importance in the model.
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current=temperature_2m,precipitation,"
            f"wind_speed_10m,relative_humidity_2m,"
            f"surface_pressure,weather_code"
            f"&timezone=Africa/Nairobi"
        )
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None

        c      = r.json().get('current', {})
        precip = c.get('precipitation', 0)
        wcode  = c.get('weather_code', 0)

        # WMO codes 51+ indicate precipitation or storms
        adverse_codes = {51,53,55,61,63,65,71,73,75,80,81,82,95,96,99}

        return {
            'temperature':  c.get('temperature_2m',       20.0),
            'precipitation': precip,
            'wind_speed':   c.get('wind_speed_10m',        10.0),
            'humidity':     c.get('relative_humidity_2m',  65.0),
            'pressure':     c.get('surface_pressure',    1013.0),
            'weather_code': wcode,
            'is_raining':   precip > 0,
            'is_adverse':   precip > 1.0 or wcode in adverse_codes,
        }
    except Exception:
        return None


def default_weather():
    """Nairobi annual averages — used when API is unavailable."""
    return {
        'temperature': 20.0, 'precipitation': 0.0,
        'wind_speed':  10.0, 'humidity':      65.0,
        'pressure':  1013.0, 'weather_code':   0,
        'is_raining': False, 'is_adverse':    False,
    }


# ============================================================================
# TEMPORAL FEATURE EXTRACTION
# ============================================================================

def extract_temporal_features(dt):
    """
    Extract temporal fields matching those computed in Notebook 02.
    Temporal features were the strongest predictor category (51.4% importance).
    Rush hour and night flags capture severity patterns found in EDA.
    """
    hour = dt.hour
    dow  = dt.weekday()  # 0 = Monday, 6 = Sunday

    return {
        'hour':         hour,
        'day_of_week':  dow,
        'month':        dt.month,
        'year':         dt.year,
        'is_weekend':   1 if dow >= 5 else 0,
        'is_rush_hour': 1 if (7 <= hour <= 9) or (17 <= hour <= 19) else 0,
        'is_night':     1 if (hour >= 22 or hour <= 5) else 0,
    }


# ============================================================================
# SPATIAL HELPERS
# ============================================================================

def get_distance_from_cbd(lat, lon):
    """Distance (km) from Nairobi CBD (City Hall)."""
    R            = 6371.0
    cbd_lat, cbd_lon = -1.286389, 36.817223
    dlat = np.radians(lat - cbd_lat)
    dlon = np.radians(lon - cbd_lon)
    a    = (np.sin(dlat/2)**2 +
            np.cos(np.radians(cbd_lat)) *
            np.cos(np.radians(lat))     *
            np.sin(dlon/2)**2)
    return R * 2 * np.arcsin(np.sqrt(a))


def get_geographic_zone(dist_km):
    """Map CBD distance to the four training-set zone categories."""
    if dist_km <= 3:    return 'CBD_CORE'
    elif dist_km <= 8:  return 'INNER_SUBURBS'
    elif dist_km <= 15: return 'OUTER_SUBURBS'
    else:               return 'PERIPHERAL'


def get_road_type(lat, lon):
    """
    Proxy road type from CBD distance.
    Used because Ma3Route data does not include road classification directly.
    """
    dist = get_distance_from_cbd(lat, lon)
    if dist <= 2:    return 'MAIN_ROAD'
    elif dist <= 5:  return 'MAJOR_HIGHWAY'
    elif dist <= 12: return 'SECONDARY_ROAD'
    else:            return 'RESIDENTIAL'


def get_location_risk(lat, lon):
    """
    Assign risk category from CBD proximity.
    CBD and inner-suburb locations had higher severe crash rates in training data.
    """
    dist = get_distance_from_cbd(lat, lon)
    if dist <= 2:    return 'HIGH_RISK'
    elif dist <= 5:  return 'MEDIUM_RISK'
    else:            return 'LOW_RISK'


# ============================================================================
# FEATURE VECTOR BUILDER
# ============================================================================

def prepare_features(lat, lon, dt, weather, feature_names):
    """
    Build the exact 44-feature vector the ensemble was trained on.

    This is the inference-time mirror of the Notebook 02 pipeline.
    Features requiring the full dataset (e.g. hour_severity_rate) use
    training-set global medians — a known limitation; production would
    replace these with live database lookups.

    Column order is enforced at the end using feature_names from
    feature_metadata.pkl to prevent train/inference mismatch.
    """
    t    = extract_temporal_features(dt)
    dist = get_distance_from_cbd(lat, lon)
    zone = get_geographic_zone(dist)
    road = get_road_type(lat, lon)
    risk = get_location_risk(lat, lon)
    w    = weather if weather else default_weather()

    # Risk interaction flags from feature engineering
    dangerous_time  = 1 if t['is_rush_hour'] or t['is_night'] else 0
    high_risk_loc   = 1 if risk in ('HIGH_RISK', 'VERY_HIGH_RISK') else 0
    high_risk_combo = 1 if (high_risk_loc and dangerous_time) else 0

    # Historical severity rates — global training-set medians as defaults
    MEDIAN_HOUR_RATE  = 0.118
    MEDIAN_DAY_RATE   = 0.122
    MEDIAN_MONTH_RATE = 0.120
    MEDIAN_CRASH_LOC  = 3.0
    HIGH_RATE_LOC     = 0.0

    daylight     = 'DAYLIGHT' if (6 <= dt.hour <= 18) else 'DARKNESS'
    weather_cond = 'RAIN' if w['is_raining'] else 'CLEAR'

    raw = {
        # Raw location
        'latitude':    lat,
        'longitude':   lon,
        # Temporal
        'hour':                     t['hour'],
        'day_of_week':              t['day_of_week'],
        'month':                    t['month'],
        'year':                     t['year'],
        'is_weekend':               t['is_weekend'],
        'is_night':                 t['is_night'],
        'is_rush_hour':             t['is_rush_hour'],
        # Historical rates (medians — top features by importance)
        'hour_severity_rate':       MEDIAN_HOUR_RATE,
        'day_severity_rate':        MEDIAN_DAY_RATE,
        'month_severity_rate':      MEDIAN_MONTH_RATE,
        # Location risk
        'crashes_at_location':      MEDIAN_CRASH_LOC,
        'high_rate_at_location':    HIGH_RATE_LOC,
        'high_risk_location':       high_risk_loc,
        'dangerous_time':           dangerous_time,
        'high_risk_location_dangerous_time': high_risk_combo,
        # Real-time weather from Open-Meteo API
        'actual_temperature_c':     w['temperature'],
        'actual_precipitation_mm':  w['precipitation'],
        'actual_wind_speed_kmh':    w['wind_speed'],
        'actual_humidity_percent':  w['humidity'],
        'actual_pressure_hpa':      w['pressure'],
        'weather_code':             w['weather_code'],
        'is_adverse_weather':       int(w['is_adverse']),
        # Infrastructure proxies
        'likely_intersection':      0,
        'high_speed_road':          1 if road == 'MAJOR_HIGHWAY' else 0,
        'distance_from_cbd_km':     dist,
        'high_risk_infrastructure': high_risk_loc,
        # One-hot: location risk category
        'location_risk_category_LOW_RISK':       1 if risk == 'LOW_RISK'       else 0,
        'location_risk_category_MEDIUM_RISK':    1 if risk == 'MEDIUM_RISK'    else 0,
        'location_risk_category_HIGH_RISK':      1 if risk == 'HIGH_RISK'      else 0,
        'location_risk_category_VERY_HIGH_RISK': 1 if risk == 'VERY_HIGH_RISK' else 0,
        # One-hot: daylight status
        'daylight_status_DARKNESS': 1 if daylight == 'DARKNESS' else 0,
        'daylight_status_DAYLIGHT': 1 if daylight == 'DAYLIGHT' else 0,
        # One-hot: weather condition
        'weather_condition_CLEAR':  1 if weather_cond == 'CLEAR' else 0,
        'weather_condition_RAIN':   1 if weather_cond == 'RAIN'  else 0,
        # One-hot: road type proxy
        'road_type_proxy_MAIN_ROAD':       1 if road == 'MAIN_ROAD'       else 0,
        'road_type_proxy_MAJOR_HIGHWAY':   1 if road == 'MAJOR_HIGHWAY'   else 0,
        'road_type_proxy_RESIDENTIAL':     1 if road == 'RESIDENTIAL'     else 0,
        'road_type_proxy_SECONDARY_ROAD':  1 if road == 'SECONDARY_ROAD'  else 0,
        # One-hot: geographic zone
        'geographic_zone_CBD_CORE':       1 if zone == 'CBD_CORE'       else 0,
        'geographic_zone_INNER_SUBURBS':  1 if zone == 'INNER_SUBURBS'  else 0,
        'geographic_zone_OUTER_SUBURBS':  1 if zone == 'OUTER_SUBURBS'  else 0,
        'geographic_zone_PERIPHERAL':     1 if zone == 'PERIPHERAL'     else 0,
    }

    df = pd.DataFrame([raw])

    # Enforce exact column order from training — prevents silent misalignment
    for col in feature_names:
        if col not in df.columns:
            df[col] = 0
    df = df[feature_names]

    return df


# ============================================================================
# ENSEMBLE PREDICTION
# ============================================================================

def ensemble_predict(rf, xgb, lgbm, features_df, weights, threshold):
    """
    Weighted average of three model probabilities, then apply threshold.

    Threshold 0.13 (vs default 0.50) reflects safety-first design:
    missing a HIGH severity case costs far more than a false alarm.
    Test set result: 79.4% HIGH recall, 20.6% under-triage.
    """
    rf_p   = rf.predict_proba(features_df)[0][1]
    xgb_p  = xgb.predict_proba(features_df)[0][1]
    lgbm_p = lgbm.predict_proba(features_df)[0][1]

    ensemble_p = (weights['rf']      * rf_p  +
                  weights['xgboost'] * xgb_p +
                  weights['lgbm']    * lgbm_p)

    prediction = 1 if ensemble_p >= threshold else 0

    return {
        'prediction':  prediction,
        'probability': ensemble_p,
        'rf_prob':     rf_p,
        'xgb_prob':    xgb_p,
        'lgbm_prob':   lgbm_p,
        'confidence':  ensemble_p * 100 if prediction == 1
                       else (1 - ensemble_p) * 100,
    }


# ============================================================================
# FEATURE IMPORTANCE
# ============================================================================

def get_top_features(rf_model, feature_names, top_n=5):
    """
    Top N features by Random Forest importance.
    RF used here (not LightGBM or ensemble) because its mean-decrease-in-
    impurity scores are stable and easy to explain to non-technical users.
    """
    imp = rf_model.feature_importances_
    df  = pd.DataFrame({'feature': feature_names, 'importance': imp})
    df  = df.sort_values('importance', ascending=False).head(top_n)
    df['feature'] = df['feature'].str.replace('_', ' ').str.title()
    return df


# ============================================================================
# VALIDATION
# ============================================================================

def validate_coordinates(lat, lon, bounds):
    """Check input coordinates fall within the Nairobi County study area."""
    return (bounds['lat_min'] <= lat <= bounds['lat_max'] and
            bounds['lon_min'] <= lon <= bounds['lon_max'])