"""
Emergency Accident Severity Prediction System for Nairobi County Emergency Dispatch

Author: Mary Wangoi Mwangi (122174)
Supervisor: Prof. Vincent Omwenga

This system provides real-time severity predictions to support emergency
dispatch decision-making in Nairobi County.
"""

# ============================================================================
# IMPORTS
# ============================================================================
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

from config import *
from utils import *

# ============================================================================
# PAGE SETUP
# ============================================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        padding-bottom: 2rem;
    }
    .severity-high {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
.severity-low {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0d47a1;
    }
    </style>
""", unsafe_allow_html=True)



# ============================================================================
# SESSION STATE
# ============================================================================
# Track prediction state across user interactions
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None



# ============================================================================
# LOAD MODEL
# ============================================================================
@st.cache_resource
def load_models():
    """Load trained model and configuration (cached for performance)"""
    try:
        model, scaler, config = load_model_artifacts(MODEL_PATH, SCALER_PATH, CONFIG_PATH)
        return model, scaler, config
    except Exception as e:
        st.error(f" Error loading model: {str(e)}")
        st.stop()

model, scaler, config = load_models()



# ============================================================================
# HEADER
# ============================================================================
st.markdown(f'<div class="main-header">{APP_ICON} {APP_TITLE}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{ORGANIZATION}</div>', unsafe_allow_html=True)



# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/ambulance.png", width=100)
    
    st.header(" How to Use")
    st.info("""
    1. Enter accident location
    2. Confirm date & time
    3. Review weather conditions
    4. Click 'Predict Severity'
    5. Review recommendations
    
    **Note:** This is a decision support tool.
    Always combine with caller information and
    your professional judgment.
    """)
    
    st.markdown("---")
    
    st.header(" Model Performance")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Recall", "64%", help="Catches 64% of high-severity cases")
        st.metric("Precision", "67%", help="Accuracy of predictions")
    with col2:
        st.metric("Accuracy", "65%", help="Overall correctness")
        st.metric("F1-Score", "65%", help="Balance of precision & recall")
    
    st.markdown("---")
    st.caption(f"Version {VERSION}")
    st.caption("© 2025 Strathmore University")

# ============================================================================
# MAIN INTERFACE
# ============================================================================
st.header("Accident Severity Prediction")
st.markdown("Enter accident details below to get an instant severity assessment.")

# Layout: Location (left) and Time (right)
col_left, col_right = st.columns([2, 1])



# ----------------------------------------------------------------------------
# LOCATION INPUT
# ----------------------------------------------------------------------------
with col_left:
    st.subheader(" Location Information")
    
    location_method = st.radio(
        "How would you like to enter the location?",
        ["Enter Coordinates", "Enter Address"],
        horizontal=True
    )
    
    lat, lon = None, None
    
    if location_method == "Enter Coordinates":
        coord_col1, coord_col2 = st.columns(2)
        
        with coord_col1:
            lat = st.number_input(
                "Latitude",
                min_value=NAIROBI_BOUNDS['lat_min'],
                max_value=NAIROBI_BOUNDS['lat_max'],
                value=DEFAULT_LOCATION['lat'],
                format="%.6f",
                help="Latitude within Nairobi County"
            )
        
        with coord_col2:
            lon = st.number_input(
                "Longitude",
                min_value=NAIROBI_BOUNDS['lon_min'],
                max_value=NAIROBI_BOUNDS['lon_max'],
                value=DEFAULT_LOCATION['lon'],
                format="%.6f",
                help="Longitude within Nairobi County"
            )
        
        if lat and lon:
            st.success(f" Location: {lat:.6f}, {lon:.6f}")
    
    else:  # Address input
        st.info("Address geocoding requires internet connection")
        address = st.text_input(
            "Enter accident location:",
            placeholder="e.g., Uhuru Highway, Nairobi"
        )
        
        if address:
            st.warning("  Demo Mode: Please use coordinates for accurate predictions.")
            lat = DEFAULT_LOCATION['lat']
            lon = DEFAULT_LOCATION['lon']
            st.info(f"Using default: {DEFAULT_LOCATION['name']}")



# ----------------------------------------------------------------------------
# DATE & TIME INPUT
# ----------------------------------------------------------------------------
with col_right:
    st.subheader(" Date & Time")
    
    accident_date = st.date_input("Date", value=datetime.now())
    accident_time = st.time_input("Time", value=datetime.now().time())
    
    accident_datetime = datetime.combine(accident_date, accident_time)
    
    # Show temporal risk factors (more compact)
    temporal = extract_temporal_features(accident_datetime)

    risk_badges = []
    if temporal['is_rush_hour']:
        risk_badges.append(" Rush Hour")
    if temporal['is_night']:
        risk_badges.append(" Night Time")
    if temporal['is_weekend']:
        risk_badges.append(" Weekend")

    if risk_badges:
        st.warning(" | ".join(risk_badges))
    else:
        st.success(" Regular hours")

# ----------------------------------------------------------------------------
# WEATHER CONDITIONS
# ----------------------------------------------------------------------------
st.markdown("---")
st.subheader(" Weather Conditions")

weather_col1, weather_col2 = st.columns(2)

with weather_col1:
    if lat and lon:
        with st.spinner("Fetching weather data..."):
            weather = get_weather_data(lat, lon)
            
            if weather:
                st.success(" Weather data retrieved")
                st.metric(" Temperature", f"{weather['temperature']:.1f}°C")
                st.metric(" Precipitation", f"{weather['precipitation']:.1f} mm")
                
                if weather['is_raining']:
                    st.warning(" **RAINY CONDITIONS**")
                else:
                    st.info(" No rain")
            else:
                st.warning(" Using default weather values")
                weather = {'temperature': 20, 'precipitation': 0, 'is_raining': False}
    else:
        st.warning(" Enter location first")
        weather = None

with weather_col2:
    st.info("""
    **Weather Impact:**
    
    Rain increases severity by affecting:
    - Vehicle control
    - Visibility
    - Road conditions
    - Response time
    """)



# ----------------------------------------------------------------------------
# PREDICT BUTTON
# ----------------------------------------------------------------------------
st.markdown("---")

predict_col1, predict_col2, predict_col3 = st.columns([1, 2, 1])

with predict_col2:
    predict_button = st.button(
        " PREDICT SEVERITY",
        type="primary",
        use_container_width=True
    )
    st.caption("Tip: Complete all fields and click above")



# ============================================================================
# PREDICTION LOGIC
# ============================================================================
if predict_button:
    # Validate inputs
    if lat is None or lon is None:
        st.error(" Please provide accident location")
    elif weather is None:
        st.error(" Please wait for weather data")
    else:
        with st.spinner(" Analyzing accident data..."):
            try:
                # Prepare features for model
                features_df = prepare_features(
                    lat, lon, accident_datetime, weather, config['feature_names']
                )
                            
                # Scale if needed (Random Forest doesn't need scaling)
                if scaler is not None:
                    features_scaled = scaler.transform(features_df)
                else:
                    features_scaled = features_df
                
                # Make prediction
                prediction = model.predict(features_scaled)[0]
                prediction_proba = model.predict_proba(features_scaled)[0]
                
                # Get top features
                top_features = get_feature_importance_top_n(
                    model, config['feature_names'], features_df, top_n=5
                )
                
                # Store results
                st.session_state.prediction_result = {
                    'severity': prediction,
                    'confidence': prediction_proba[prediction] * 100,
                    'probabilities': prediction_proba,
                    'top_features': top_features,
                    'location': (lat, lon),
                    'datetime': accident_datetime
                }
                st.session_state.prediction_made = True
                
            except Exception as e:
                st.error(f" Prediction error: {str(e)}")



# ============================================================================
# DISPLAY RESULTS
# ============================================================================
if st.session_state.prediction_made and st.session_state.prediction_result:
    st.markdown("---")
    st.header("Prediction Results")
    
    result = st.session_state.prediction_result
    severity = result['severity']
    confidence = result['confidence']
    
    # Display severity level
    if severity == 1:  # HIGH
        st.markdown(f"""
            <div class="severity-high">
                <h3 style="color: #d32f2f; margin: 0; font-size: 1.5rem;"> HIGH SEVERITY ACCIDENT</h3>
                <p style="font-size: 1.1rem; margin: 0.3rem 0; color: #333;">
                    <strong>Confidence: {confidence:.1f}%</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)

    else:  # LOW
        st.markdown(f"""
            <div class="severity-low">
                <h3 style="color: #388e3c; margin: 0; font-size: 1.5rem;"> LOW SEVERITY ACCIDENT</h3>
                <p style="font-size: 1.1rem; margin: 0.3rem 0; color: #333;">
                    <strong>Confidence: {confidence:.1f}%</strong>
                </p>
            </div>
        """, unsafe_allow_html=True)
    

    # Recommended actions
    st.subheader("Recommended Actions")
    actions = RECOMMENDED_ACTIONS[severity]

    for action in actions:
        if severity == 1:
            st.error(f"• {action}")
        else:
            st.success(f"• {action}")


    # Collapse detailed analysis into expander
    st.markdown("---")
    with st.expander("View Detailed Analysis (Optional)", expanded=False):


    # Confidence visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Confidence Level")
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=confidence,
                title={'text': "Confidence (%)"},
                number={'font': {'size': 40}},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': SEVERITY_COLORS[severity]},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "lightblue"},
                        {'range': [75, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            
            fig_gauge.update_layout(
                height=200,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
        


        with col2:
            st.subheader("Probabilities")
            
            prob_df = pd.DataFrame({
                'Severity': ['LOW', 'HIGH'],
                'Probability': result['probabilities'] * 100
            })
            
            fig_bar = px.bar(
                prob_df, x='Severity', y='Probability',
                color='Severity',
                color_discrete_map={'LOW': 'green', 'HIGH': 'red'},
                text='Probability'
            )
            fig_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_bar.update_layout(
                showlegend=False, 
                height=200,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    

    # Feature importance
        st.subheader("Key Risk Factors")
        
        fig_features = px.bar(
            result['top_features'],
            x='importance', y='feature', orientation='h',
            color='importance',
            color_continuous_scale='Reds' if severity == 1 else 'Greens'
        )
        fig_features.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=200,
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_features, use_container_width=True)
    

        # Explanation
        st.info("""
        **Understanding This Prediction:**
        - Higher confidence (>75%) = more certain prediction
        - Lower confidence (<60%) = borderline case, use extra caution
        - Risk factors show which features influenced this prediction
        - Always combine with caller information and your judgment
        """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("""
 **Disclaimer:** This is a decision support tool. All emergency decisions 
must be made by qualified personnel considering all available information.
""")