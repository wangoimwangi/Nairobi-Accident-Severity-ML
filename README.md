# Traffic Accident Severity Prediction for Emergency Dispatch in Nairobi

Machine learning-based decision support system for predicting traffic accident severity to optimize emergency response resource allocation in Nairobi County, Kenya.

**Author:** Mary Wangoi Mwangi (122174)  
**Program:** MSc Information Technology  
**Institution:** Strathmore University  
**Supervisor:** Prof. Vincent Omwenga  
**Year:** 2025-2026

---

##  Project Overview

This research develops an ensemble machine learning model (Random Forest + XGBoost + LightGBM) that predicts accident severity by requiring only GPS coordinates and timestamp from emergency callers, then automatically deriving 44 predictive features including temporal patterns, spatial risk factors, historical crash data, and real-time weather conditions. 

The system addresses a critical 35% resource mismatch in Nairobi's fragmented emergency dispatch system by providing objective severity assessments without burdening callers for additional information.

**Key Achievement:** 79.42% HIGH severity recall with 20.58% under-triage rate on test data.

---

##  Project Structure
```
NAIROBI-ACCIDENT-SEVERITY/
├── data/
│   ├── raw/                        # Ma3Route dataset (2012-2023)
│   ├── processed/                  # Cleaned, labeled crashes
│   └── features/                   # Engineered features (44 features)
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning_feature_engineering.ipynb
│   └── 03_Model_Training___Evaluation.ipynb
│
├── src/
│   └── app/                        # Streamlit demo application
│       ├── app.py
│       ├── config.py
│       └── utils.py
│
├── models/                         # Trained ensemble models + configs
│
├── reports/
│   └── figures/
│       ├── 01_exploration/         # EDA visualizations
│       ├── 02_features/            # Feature importance charts
│       └── 03_model/               # Model performance plots
│
├── docs/                           # Thesis proposal & documentation
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

##  Quick Start

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Installation
```bash
# 1. Clone repository
git clone https://github.com/wangoimwangi/Accident-Severity-Prediction.git
cd Accident-Severity-Prediction

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows (Git Bash)
source venv/Scripts/activate

# Windows (PowerShell)
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the Demo
```bash
# Launch Streamlit demo app
streamlit run src/app/app.py
```

---

##  Dataset

**Source:** World Bank Ma3Route Nairobi Crash Dataset  
**Period:** 2012-2023  
**Records:** 31,064 crowdsourced crash reports  
**Access:** https://datacatalog.worldbank.org/search/dataset/0038043

**Citation:**  
Milusheva, S., Marty, R., Bedoya, G., Williams, S., Resor, E., & Legovini, A. (2021). Applying machine learning and geolocation techniques to social media data (Twitter) to develop a resource for urban planning. *PLOS ONE*, 16(2), e0244317.

---

##  Methodology

- **Framework:** CRISP-DM (Cross-Industry Standard Process for Data Mining)
- **Approach:** Binary classification (HIGH vs LOW severity)
- **Models:** Ensemble of Random Forest, XGBoost, and LightGBM
- **Features:** 44 engineered features (temporal, spatial, weather)
- **Data Split:** 70% train / 15% validation / 15% test
- **Class Balancing:** SMOTE on training set only
- **Optimization:** Threshold tuning for safety-first dispatch (0.13)

---

##  Results

### Test Set Performance (Threshold 0.13)

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **HIGH Recall** | **79.42%** | >75% |
| **Under-Triage** | **20.58%** | <30% |
| **ROC-AUC** | **0.6327** | >0.60 |
| **HIGH Precision** | **15.28%** | >15% | 

### Impact Estimation
- **Current system:** 35% resource mismatch (WHO, 2019)
- **With ML support:** 14.4% reduction in under-triage
- **Potential lives saved:** ~156 annually in Nairobi (estimated)

---

##  Key Technologies

**Core ML Stack:**
- Python 3.9+
- scikit-learn 1.8.0
- XGBoost
- LightGBM
- imbalanced-learn (SMOTE)

**Data Processing:**
- pandas 2.3.3
- numpy 2.4.1
- geopandas 1.1.2

**Visualization:**
- matplotlib 3.10.8
- seaborn 0.13.2
- folium 0.20.0

**Demo Interface:**
- Streamlit 1.41.0

---

##  Documentation

Comprehensive documentation available in `/docs/`:
- Data Exploration Summary
- Data Preprocessing Summary
- Feature Engineering Summary
- Model Development Summary
- Dataset README

---

##  Academic Context

This work is submitted in partial fulfillment of the requirements for the degree of Master of Science in Information Technology at Strathmore University, School of Computing & Engineering Sciences.

**Thesis Defense:** March 2026

---

##  License & Ethics

- Research conducted under Strathmore University ISERC ethical approval
- Dataset: World Bank Open Data (public access with microdata agreement)
- All data anonymized (no personally identifiable information)
- Model intended as decision support tool (requires human oversight)

---

##  Acknowledgments

- **Supervisor:** Prof. Vincent Omwenga, Strathmore University
- **Dataset:** World Bank Development Data Group
- **Platform:** Ma3Route crowdsourced traffic reporting
- **Emergency Services:** Kenya Red Cross, St. John Ambulance, Nairobi County EMS

---

##  Links

- [GitHub Repository](https://github.com/wangoimwangi/Accident-Severity-Prediction)
- [Ma3Route Dataset](https://datacatalog.worldbank.org/search/dataset/0038043)
- [Strathmore University](https://www.strathmore.edu/)

---

**Status:** Proof-of-concept validated 
