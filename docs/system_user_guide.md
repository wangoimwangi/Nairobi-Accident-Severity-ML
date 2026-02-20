# Emergency Severity Prediction System - User Guide

**Decision Support Tool for Emergency Dispatchers in Nairobi County**

---

## What This System Does

This tool provides **objective severity predictions** to assist emergency dispatchers in making resource allocation decisions. 

It requires only GPS coordinates and timestamp from the caller, then automatically enriches this minimal input with 44 predictive features including temporal patterns (rush hour, day of week), spatial risk factors (location history, hospital proximity), and real-time weather conditions (rain, temperature, wind). 

The system predicts whether an accident is **HIGH severity** (requiring advanced life support) or **LOW severity** (manageable with basic units).

**Important:** 

This is a **decision support tool that works alongside your current dispatch system** - it provides recommendations to inform your decisions, but does not replace dispatcher expertise or judgment.

---

## System Requirements

- Internet connection
- Web browser (Chrome, Firefox, Safari, Edge)
- Access to accident GPS coordinates (from caller or CAD system)

---

## Step-by-Step Usage Guide

### **Step 1: Open the System**

1. Navigate to: https://nairobi-accident-severity-ml.streamlit.app/
2. Wait for the interface to load (2-3 seconds)
3. You'll see the main prediction form

---

### **Step 2: Enter Accident Location**

**Latitude Input:**
- Enter the north-south GPS coordinate
- Example: `-1.2864` (City Centre area)
- Valid range for Nairobi: `-1.44` to `-1.16`
- **How to get:** From caller's smartphone GPS, Google Maps, or known landmark coordinates

**Longitude Input:**
- Enter the east-west GPS coordinate  
- Example: `36.8172` (City Centre area)
- Valid range for Nairobi: `36.66` to `37.10`
- **How to get:** From caller's smartphone GPS, Google Maps, or known landmark coordinates

**Coordinate Format:**
- Use decimal format (not degrees/minutes/seconds)
- Negative values are normal for Nairobi (southern hemisphere, east of prime meridian)
- 4-6 decimal places provide sufficient accuracy

---

### **Step 3: Set Date and Time**

**Default Behavior:**
- System automatically uses **current date and time**
- This is correct for real-time emergency calls

**When to Adjust:**
- Historical analysis of past accidents
- Training scenarios
- Testing system behavior at different times

**How to Adjust:**
1. Click the **date picker** to change date
2. Click the **time picker** to change time
3. System automatically updates temporal features (hour, day of week, rush hour status)

---

### **Step 4: Weather Data (Automatic)**

**How It Works:**
- System **automatically fetches real-time weather as soon as you enter valid GPS coordinates**
- No button click needed - happens in the background immediately
- Weather data retrieved from Open-Meteo API for the exact accident location
- Includes: temperature, precipitation, wind speed, weather conditions
- Takes <1 second to fetch and display
- **Status indicator shows:**  "Live weather retrieved"

**What You'll See:**
- **Temperature** (°C)
- **Precipitation** (mm/hour) - Current rainfall at accident location
- **Wind Speed** (km/h)
- **Weather Status:** Live, Demo, or Fallback mode

**Demo Mode Toggle (Training Only):**
- Enable this **only for training purposes**
- Overrides real weather with simulated adverse conditions (heavy rain 15mm/hr, strong wind 45km/h)
- **Status shows:**  "Demo mode: Simulated adverse conditions"
- **Do NOT use during real emergency calls** (always use real weather)

**When to Use Demo Mode:**
- Training new dispatchers on weather-related decisions
- Comparing same location under different weather conditions (dry vs rainy)
- Understanding how rain increases severity risk
- Teaching about weather's impact on accident outcomes

**If Weather Fetch Fails:**
- System uses Nairobi historical averages as fallback
- **Status shows:**  "API unavailable - using Nairobi average defaults"
- Prediction still works, but may be slightly less accurate
- Try refreshing if this happens frequently

---

### **Step 5: Generate Prediction**

1. Click the **"Predict Severity"** button (bottom of form)
2. System processes the request in **under 1 second**:
   - Fetches **real-time weather data** from Open-Meteo API (unless Demo Mode enabled)
   - Generates **44 predictive features** from GPS, timestamp, and weather
   - Runs ensemble model (Random Forest + XGBoost + LightGBM)
   - Applies optimized threshold (0.13) for safety-first dispatch

---

### **Step 6: Interpret the Results**

The system displays **four key pieces of information:**

---

#### **A. Severity Prediction**

**🔴 HIGH Severity**
- Fatal or severe injuries expected
- **Action:** Dispatch advanced life support (ALS) units immediately
- Equivalent to: Major trauma, multiple casualties, critical injuries

**🟢 LOW Severity**
- Moderate or minor injuries expected  
- **Action:** Basic life support (BLS) units appropriate
- Equivalent to: Minor injuries, single vehicle, property damage only

---

#### **B. Risk Category**

Operational classification for dispatch prioritization:

**🔴 CRITICAL** (Model confidence >80%)
- Very high probability of HIGH severity
- **Action:** Immediate ALS response, consider backup units

**🟠 HIGH RISK** (Model confidence 60-80%)
- Strong probability of HIGH severity
- **Action:** Prioritize ALS units, notify trauma center

**🟡 ELEVATED RISK** (Model confidence 40-60%)
- Moderate probability of HIGH severity  
- **Action:** Consider ALS backup, monitor situation

**🟢 STANDARD** (Model confidence <40%)
- Lower probability of HIGH severity
- **Action:** BLS units sufficient, ALS on standby if needed

---

#### **C. Confidence Score**

- **Percentage value (0-100%)** showing model certainty
- **Higher confidence** = More reliable prediction
- **Lower confidence** = More dispatcher judgment required

**Interpretation:**
- **>70%:** High model confidence - prediction is reliable
- **50-70%:** Moderate confidence - use with caller information
- **<50%:** Low confidence - rely more heavily on dispatcher expertise

**When confidence is low:** Dispatcher should give extra weight to:
- Caller's description of injuries
- Number of vehicles involved
- Caller's tone/urgency
- Known hazards at location

---

#### **D. Weather Context**

The system **automatically fetched real-time weather** for the accident location when you clicked "Predict Severity" (using the Open-Meteo weather API). 

This happened in the background - no manual input was needed.

**Displayed Information:**
- **Temperature** (°C)
- **Precipitation** (mm/hour) - Shows if it's currently raining
- **Weather Condition** (Clear/Rainy/Cloudy)
- **Wind Speed** (km/h)

**Why Weather Matters:**
- Rain increases accident severity risk by 15-20%
- Wet roads contribute to loss of control and multi-vehicle crashes
- Poor visibility reduces reaction time
- Weather features are among the top 5 predictive factors in the model

**Weather Risk Guidance:**
- **Heavy rain (>5mm/hr):** Increases HIGH severity probability
- **Moderate rain (2-5mm/hr):** Consider weather in decision
- **Light rain (<2mm/hr):** Minor factor
- **Dry conditions:** No weather-related risk increase

**If Demo Mode Was Enabled:**
- Weather shown is simulated (rainy conditions)
- Useful for training, not for real emergency decisions

---

## Integration with Current Dispatch System

**This tool is designed to COMPLEMENT your existing workflow:**

### **How It Fits:**

1. **Receive emergency call** (existing process)
2. **Gather GPS location** from caller (existing process)
3. **Enter coordinates into this tool** (NEW step - takes 10 seconds)
4. **Review prediction + risk category** (NEW information)
5. **Make dispatch decision** using:
   - ✅ Severity prediction from this tool
   - ✅ Caller's injury description
   - ✅ Your dispatcher expertise
   - ✅ Available unit locations
6. **Dispatch appropriate resources** (existing process)

### **NOT a Replacement For:**

- Caller interviews and injury assessment
- Dispatcher training and protocols
- CAD (Computer-Aided Dispatch) system
- Unit tracking and availability systems
- Communication with field units

### **Works Best When:**

- Combined with caller information
- Used by experienced dispatchers
- Integrated into decision workflow (not standalone)
- Predictions are questioned when they conflict with clear caller descriptions

---

## Understanding System Limitations

**The system CANNOT:**
- Detect multiple casualties (relies on single-point GPS)
- Know about hazmat, fire, or entrapment (no caller interview data)
- Account for traffic delays or unit availability
- Predict injuries from caller descriptions or witness statements

**The system CAN:**
- Provide objective severity estimate when caller descriptions are unclear
- Identify high-risk locations and times based on historical patterns  
- Factor in weather conditions automatically
- Reduce bias in resource allocation decisions

---

## System Performance

**Validated on 4,660 test accidents:**
- **HIGH Severity Recall:** 79.4% (catches 79 out of 100 HIGH severity cases)
- **Under-Triage Rate:** 20.6% (sends insufficient resources to 21 out of 100 HIGH cases)
- **ROC-AUC:** 0.633 (moderate discriminative ability)
- **Processing Time:** <1 second

**What This Means:**
- System is **optimized for safety** (minimizing missed severe accidents)
- Trade-off: Higher false alarm rate (sends ALS to some LOW severity cases)
- Better than dispatcher-only decisions (35% resource mismatch in current system)
- **188% improvement** over simple rule-based classification

---

## Technical Details

**Model Architecture:**
- Weighted ensemble: Random Forest (40%) + XGBoost (40%) + LightGBM (20%)
- 44 auto-generated features from GPS, timestamp, and weather
- Optimized threshold: 0.13 (favors safety over efficiency)

**Feature Categories:**
- Temporal (11 features): Hour, day, month, rush hour, weekend
- Spatial (8 features): Location risk, hospital proximity, road type
- Historical (15 features): Crash frequency, severity patterns
- Weather (10 features): Rain, temperature, wind, visibility

**Training Data:**
- 31,064 crashes from Ma3Route dataset (2012-2023)
- 70% training / 15% validation / 15% test split
- SMOTE balancing for HIGH severity class

---

## Troubleshooting

**"Invalid coordinates" error:**
- Check latitude is between -1.44 and -1.16
- Check longitude is between 36.66 and 37.10
- Ensure decimal format (not degrees/minutes/seconds)

**"Weather data unavailable":**
- System uses historical average weather
- Prediction still works, but less accurate
- Try again in 30 seconds (API rate limit)

**Prediction seems wrong:**
- Check coordinates are correct location
- Verify time is set correctly
- Remember: Model provides probability, not certainty
- Use dispatcher judgment when confident

**System not loading:**
- Check internet connection
- Try refreshing browser (Ctrl+F5 or Cmd+Shift+R)
- Try different browser
- Contact technical support if persistent

---

## Support and Feedback

**For technical issues:**
- GitHub Repository: https://github.com/wangoimwangi/Nairobi-Accident-Severity-ML
- Report bugs via GitHub Issues

**For research inquiries:**
- Mary Wangoi Mwangi (122174)
- MSc Information Technology
- Strathmore University

---

## Disclaimer

This system is a research prototype developed as part of a master's thesis at Strathmore University. It is intended as a decision support tool and should not be used as the sole basis for emergency dispatch decisions. Final responsibility for resource allocation remains with trained emergency dispatchers.

---

**Last Updated:** February 2026  
**Version:** 1.0 (Proof of Concept)