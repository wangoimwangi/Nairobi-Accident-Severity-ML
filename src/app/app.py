"""
Emergency Accident Severity Prediction System — Streamlit Interface
Nairobi County Emergency Dispatch Decision Support Tool

Author    : Mary Wangoi Mwangi (122174)
Supervisor: Prof. Vincent Omwenga
Institution: Strathmore University MSc IT, 2025

Addresses the 35% resource mismatch caused by subjective caller descriptions
(WHO, 2019) by providing an objective severity prediction within seconds of
receiving an accident report.

Model: Equal-weight ensemble (RF + XGBoost + LightGBM, threshold=0.13)
Test-set performance: 79.4% HIGH recall | 20.6% under-triage | AUC 0.633
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
NAIROBI_TZ = pytz.timezone("Africa/Nairobi")
import plotly.graph_objects as go
import plotly.express as px

from config import *
from utils  import (load_ensemble_models, get_weather_data, default_weather,
                    extract_temporal_features, prepare_features,
                    ensemble_predict, get_top_features,
                    validate_coordinates, get_distance_from_cbd)


# ============================================================================
# NEAREST HOSPITAL LOOKUP
# ============================================================================
# Major Nairobi trauma centres with coordinates.
# Used to recommend the closest facility based on accident location.
NAIROBI_HOSPITALS = [
    {"name": "Kenyatta National Hospital",    "lat": -1.3018, "lon": 36.8065},
    {"name": "Nairobi Hospital",              "lat": -1.2921, "lon": 36.8159},
    {"name": "Aga Khan University Hospital",  "lat": -1.2634, "lon": 36.8187},
    {"name": "MP Shah Hospital",              "lat": -1.2699, "lon": 36.8127},
    {"name": "Mathare Hospital",              "lat": -1.2621, "lon": 36.8597},
    {"name": "Karen Hospital",                "lat": -1.3173, "lon": 36.7145},
    {"name": "Gertrude's Children's Hospital","lat": -1.2603, "lon": 36.8225},
    {"name": "Nairobi West Hospital",         "lat": -1.3089, "lon": 36.8219},
    {"name": "Mater Misericordiae Hospital",  "lat": -1.3006, "lon": 36.8389},
]

def get_nearest_hospital(lat, lon):
    """Return the name of the closest hospital to the accident location."""
    import math
    def haversine(la1, lo1, la2, lo2):
        R = 6371.0
        dlat = math.radians(la2 - la1)
        dlon = math.radians(lo2 - lo1)
        a = (math.sin(dlat/2)**2 +
             math.cos(math.radians(la1)) *
             math.cos(math.radians(la2)) *
            math.sin(dlon/2)**2)
        return R * 2 * math.asin(math.sqrt(a))

    nearest = min(NAIROBI_HOSPITALS,
                key=lambda h: haversine(lat, lon, h["lat"], h["lon"]))
    return nearest["name"]


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Blue header for authority; red reserved exclusively for HIGH severity alerts
st.markdown("""
<style>
.block-container   { padding-top: 1.5rem !important; }
.main-header       { font-size:2.2rem; font-weight:700;
                    color:#1a5276; text-align:center; padding:.4rem 0; }
.sub-header        { font-size:1rem; color:#555;
                    text-align:center; padding-bottom:1rem; }
.severity-high     { background:#ffebee; border-left:6px solid #c0392b;
                    padding:.7rem 1.1rem; border-radius:8px; margin:.8rem 0; }
.severity-low      { background:#e8f5e9; border-left:6px solid #27ae60;
                    padding:.7rem 1.1rem; border-radius:8px; margin:.8rem 0; }
.stButton>button   { width:100%; background:#c0392b; color:white;
                    font-size:1.15rem; padding:.7rem;
                    border-radius:8px; font-weight:700; }
.stButton>button:hover { background:#96281b; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
for key, val in [('prediction_made', False),
                ('prediction_result', None),
                ('weather_data', None),
                ('selected_date', datetime.now(NAIROBI_TZ).date()),
                ('selected_time', datetime.now(NAIROBI_TZ).time())]:
    if key not in st.session_state:
        st.session_state[key] = val

# ============================================================================
# MODEL LOADING
# ============================================================================
@st.cache_resource
def load_models():
    try:
        return load_ensemble_models(
            RF_MODEL_PATH, XGB_MODEL_PATH, LGBM_MODEL_PATH,
            CONFIG_PATH, METADATA_PATH
        )
    except Exception as e:
        st.error(f"Model loading failed: {e}")
        st.stop()

rf_model, xgb_model, lgbm_model, ens_config, feature_names = load_models()


# ============================================================================
# HEADER
# ============================================================================
st.markdown(
    f'<div class="main-header">{APP_ICON} {APP_TITLE}</div>',
    unsafe_allow_html=True)
st.markdown(
    f'<div class="sub-header">{ORGANIZATION}</div>',
    unsafe_allow_html=True)


# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/ambulance.png", width=90)
    st.header("How to Use")
    st.info("""
    1. Enter the accident **location**
    2. Confirm **date & time**
    3. Check **weather** conditions
    4. Click **PREDICT SEVERITY**
    5. Follow recommended actions

    This is a decision support tool.
    Always combine with caller information and professional judgement.
    """)
    
    st.markdown("---")
    st.caption("**Prediction Drivers**")
    st.caption("Temporal: 51.4%")
    st.caption("Spatial: 33.6%")
    st.caption("Weather: 15.0%")
    
    st.markdown("---")
    st.caption("**Severity Classification**")
    st.caption("HIGH = Fatal + Severe crashes")
    st.caption("LOW  = Moderate + Minor crashes")

    st.markdown("---")
    st.caption(f"v{VERSION}  ·  © 2026 Nairobi County")

    st.markdown("---")
    # Demo weather simulation toggle
    simulate_adverse = st.checkbox(
        "Demo: Simulate Adverse Weather",
        help="Override live weather to demonstrate system response to adverse conditions"
    )


# ============================================================================
# INPUT SECTION
# ============================================================================
st.header("Accident Details")
col_loc, col_time = st.columns([2, 1])

# ----------------------------------------------------------------------------
# LOCATION INPUT
# ----------------------------------------------------------------------------
with col_loc:
    st.subheader(" Location")

    # GPS coordinates are required - all spatial features are derived from them.
    # In real deployment, these would be auto-populated from the caller's GPS or cell tower data via the CAD system.
    c1, c2 = st.columns(2)
    with c1:
        lat = st.number_input(
            "Latitude",
            min_value=NAIROBI_BOUNDS['lat_min'],
            max_value=NAIROBI_BOUNDS['lat_max'],
            value=DEFAULT_LOCATION['lat'],
            format="%.6f",
            help="Decimal degrees - e.g. -1.286389")
    with c2:
        lon = st.number_input(
            "Longitude",
            min_value=NAIROBI_BOUNDS['lon_min'],
            max_value=NAIROBI_BOUNDS['lon_max'],
            value=DEFAULT_LOCATION['lon'],
            format="%.6f",
            help="Decimal degrees - e.g. 36.817223")

    st.caption("Enter the GPS coordinates of the accident location as reported by the caller.")
    if lat and lon:
        dist = get_distance_from_cbd(lat, lon)
        st.success(f" {lat:.5f}, {lon:.5f}  ·  {dist:.1f} km from CBD")

# ----------------------------------------------------------------------------
# DATE & TIME INPUT (with session state to prevent reset)
# ----------------------------------------------------------------------------
with col_time:
    st.subheader(" Date & Time")

    st.caption("Auto-filled with current date and time. Adjust if the accident occurred earlier.")
    
    # Date input with session state
    accident_date = st.date_input("Date", value=st.session_state.selected_date or datetime.now(NAIROBI_TZ).date(), key="date_input")
    st.session_state.selected_date = accident_date
    
    # Time input with session state - prevents automatic reset to current time
    accident_time = st.time_input("Time", value=st.session_state.selected_time or datetime.now(NAIROBI_TZ).time(), key="time_input")
    st.session_state.selected_time = accident_time
    
    accident_dt = datetime.combine(accident_date, accident_time)

    temp   = extract_temporal_features(accident_dt)
    badges = []
    if temp['is_rush_hour']: badges.append(" Rush Hour")
    if temp['is_night']:     badges.append(" Night")
    if temp['is_weekend']:   badges.append(" Weekend")

    if badges:
        st.warning("  ".join(badges))
    else:
        st.success(" Regular hours")


# ----------------------------------------------------------------------------
# WEATHER INPUT (with compact dynamic contextual info + demo override)
# ----------------------------------------------------------------------------
st.markdown("---")
st.markdown('<h3 style="margin-bottom:0.3rem"> Weather Conditions</h3>',
            unsafe_allow_html=True)
st.caption("Automatically fetched from the accident location once coordinates are entered.")
w_col1, w_col2 = st.columns(2)

with w_col1:
    if lat and lon:
        # Only re-fetch if coordinates changed - prevents redundant API calls every time Streamlit reruns on button click
        current_coords = (round(lat, 4), round(lon, 4))
        if st.session_state.get('weather_coords') != current_coords:
            with st.spinner("Fetching live weather..."):
                weather = get_weather_data(lat, lon)
                st.session_state.weather_data   = weather
                st.session_state.weather_coords = current_coords
        else:
            weather = st.session_state.weather_data

        if not weather:
            weather = default_weather()
        
        # Apply demo weather override if checkbox is enabled
        if simulate_adverse:
            weather['is_adverse'] = True
            weather['is_raining'] = True
            weather['precipitation'] = 15.0
            weather['wind_speed'] = 45.0
            weather['temperature'] = 18.0

        if st.session_state.weather_data and not simulate_adverse:
            st.success(" Live weather retrieved")
        elif simulate_adverse:
            st.warning(" Demo mode: Simulated adverse conditions")
        else:
            st.warning(" API unavailable - using Nairobi average defaults")

        m1, m2, m3 = st.columns(3)
        m1.metric("Temp",  f"{weather['temperature']:.1f}°C")
        m2.metric("Rain",  f"{weather['precipitation']:.1f} mm")
        m3.metric("Wind",  f"{weather['wind_speed']:.1f} km/h")

        if weather['is_adverse']:
            st.error(" ADVERSE WEATHER - Higher severity risk")
        elif weather['is_raining']:
            st.warning(" Rainy conditions")
        else:
            st.info(" Clear conditions")
    else:
        st.warning("Enter location first to fetch weather")
        weather = default_weather()

# Compact dynamic contextual weather info
with w_col2:
    if lat and lon and weather:
        if weather['is_adverse']:
            st.error("""
            **ADVERSE CONDITIONS**  
            Reduced visibility/vehicle control • Extended response times • Consider additional units
            """)
        elif weather['is_raining']:
            st.warning("""
            **RAINY CONDITIONS**  
            Slippery surfaces • Increased severity risk
            """)
        else:
            st.success("""
            **CLEAR CONDITIONS**  
            Standard protocols • No weather complications
            """)
    else:
        st.info("""
        **Weather Impact**  
        Affects vehicle control, visibility, road conditions, and response times
        """)


# ============================================================================
# PREDICT BUTTON
# ============================================================================
st.markdown("---")
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    predict_clicked = st.button("PREDICT SEVERITY",
                                type="primary",
                                use_container_width=True)



# ============================================================================
# PREDICTION LOGIC
# ============================================================================
if predict_clicked:
    if lat is None or lon is None:
        st.error("Please provide accident location first.")
    else:
        weather = st.session_state.weather_data or default_weather()
        
        # Apply demo weather override if checkbox is enabled
        if simulate_adverse:
            weather['is_adverse'] = True
            weather['is_raining'] = True
            weather['precipitation'] = 15.0
            weather['wind_speed'] = 45.0
            weather['temperature'] = 18.0

        with st.spinner("Analysing accident data..."):
            # Build 44-feature vector (mirrors Notebook 02 pipeline)
            features_df = prepare_features(
                lat, lon, accident_dt, weather, feature_names)

            # Weighted ensemble probability + 0.13 threshold
            result = ensemble_predict(
                rf_model, xgb_model, lgbm_model,
                features_df,
                ENSEMBLE_WEIGHTS,
                ENSEMBLE_THRESHOLD
            )

            result['top_features']     = get_top_features(rf_model, feature_names)
            result['location']         = (lat, lon)
            result['datetime']         = accident_dt
            result['weather']          = weather
            # Nearest hospital computed once per prediction
            result['nearest_hospital'] = get_nearest_hospital(lat, lon)

            st.session_state.prediction_result = result
            st.session_state.prediction_made   = True


# ============================================================================
# RESULTS DISPLAY
# ============================================================================
if st.session_state.prediction_made and st.session_state.prediction_result:
    st.markdown("---")
    st.header(" Dispatch Recommendation")

    res      = st.session_state.prediction_result
    severity = res['prediction']
    prob     = res['probability']


    # ----------------------------------------------------------------------------
    # SEVERITY BANNER
    # ----------------------------------------------------------------------------
    if severity == 1:
        st.markdown(f"""
        <div class="severity-high">
            <h3 style="color:#c0392b;margin:0">
                HIGH SEVERITY ACCIDENT</h3>
            <p style="margin:.3rem 0;color:#555;font-size:0.95rem">
                Response type: <strong>Advanced Life Support (ALS)</strong>
            </p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="severity-low">
            <h3 style="color:#27ae60;margin:0">
                LOW SEVERITY ACCIDENT</h3>
            <p style="margin:.3rem 0;color:#555;font-size:0.95rem">
                Response type: <strong>Basic Life Support (BLS)</strong>
            </p>
        </div>""", unsafe_allow_html=True)


    # ----------------------------------------------------------------------------
    # RISK LEVEL (replaces raw probability confidence badge)
    # ----------------------------------------------------------------------------
    if prob >= 0.70:
        risk_level = "CRITICAL RISK"
        risk_icon = "🔴"
        risk_caption = "Assessment based on accident location, timing, and conditions. CRITICAL risk requires immediate ALS deployment."
    elif prob >= 0.40:
        risk_level = "HIGH RISK"
        risk_icon = "🔴"
        risk_caption = "Assessment based on accident location, timing, and conditions. HIGH risk indicates strong need for ALS response."
    elif prob >= 0.13:
        risk_level = "ELEVATED RISK"
        risk_icon = "🟡"
        risk_caption = "Assessment based on accident location, timing, and conditions. ELEVATED risk suggests ALS dispatch with dispatcher judgment."
    else:
        risk_level = "STANDARD RISK"
        risk_icon = "🟢"
        risk_caption = "Assessment based on accident location, timing, and conditions. STANDARD risk indicates BLS response sufficient."

    st.markdown(f"**Model confidence:** {risk_icon} {risk_level}",
                unsafe_allow_html=True)


    # ----------------------------------------------------------------------------
    # DISPATCH ACTIONS
    # ----------------------------------------------------------------------------
    # HIGH severity actions use the nearest hospital instead of a hardcoded name
    st.markdown('<h3 style="margin-top:1rem;margin-bottom:0.3rem"> Dispatch Actions</h3>',
                unsafe_allow_html=True)

    if severity == 1:
        high_actions = [
            "URGENT: Dispatch Advanced Life Support (ALS) unit immediately",
            f"Alert nearest trauma centre - {res['nearest_hospital']}",
            "Prepare receiving team for potential critical care",
            "Consider air ambulance if severe traffic congestion",
        ]
        for action in high_actions:
            st.error(f"• {action}")
    else:
        for action in RECOMMENDED_ACTIONS[0]:
            st.success(f"• {action}")


    # ----------------------------------------------------------------------------
    # DETAILED ANALYSIS (collapsed)
    # ----------------------------------------------------------------------------
    st.markdown("---")
    with st.expander(" View Detailed Analysis", expanded=False):

        d1, d2 = st.columns(2)

        # Risk stratification gauge - shows risk category instead of raw percentage
        with d1:
            st.subheader("Risk Assessment")
            
            # Create gauge with needle position but risk category text instead of percentage
            fig_g = go.Figure(go.Indicator(
                mode="gauge",
                value=prob * 100,
                title={'text': f"<b>{risk_level}</b>", 
                    'font': {'size': 28, 'color': '#c0392b' if severity == 1 else '#27ae60'}},
                gauge={
                    'axis': {'range': [0, 100], 'visible': True},
                    'bar':  {'color': '#c0392b' if severity == 1 else '#27ae60', 'thickness': 0.3},
                    'steps': [
                        {'range': [0,  13], 'color': '#e8f5e9', 'name': 'Standard'},
                        {'range': [13, 40], 'color': '#fff9c4', 'name': 'Elevated'},
                        {'range': [40, 70], 'color': '#ffcdd2', 'name': 'High'},
                        {'range': [70,100], 'color': '#ffebee', 'name': 'Critical'},
                    ],
                    'threshold': {
                        'line': {'color': 'black', 'width': 3},
                        'thickness': 0.85, 'value': 13
                    }
                }
            ))
            fig_g.update_layout(height=250, margin=dict(l=10,r=10,t=60,b=10))
            st.plotly_chart(fig_g, use_container_width=True)
            
            # Dynamic caption based on risk level
            st.caption(risk_caption)


        # Top features - what drove this specific prediction
        with d2:
            st.subheader("Top Risk Factors")
            st.caption("Variables that most influenced this prediction:")
            fig_f = px.bar(res['top_features'],
                        x='importance', y='feature',
                        orientation='h',
                        color='importance',
                        color_continuous_scale=(
                            'Reds' if severity == 1 else 'Greens'))
            fig_f.update_layout(
                yaxis={'categoryorder': 'total ascending'},
                height=250, showlegend=False,
                margin=dict(l=10,r=10,t=10,b=10),
                coloraxis_showscale=False)
            st.plotly_chart(fig_f, use_container_width=True)


# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption(
    "**Disclaimer:** Decision support tool only. "
    "Final dispatch decisions must be made by qualified emergency personnel.")