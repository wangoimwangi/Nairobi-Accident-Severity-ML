# Nairobi Traffic Accident Severity Prediction

Machine Learning-based system for predicting traffic accident severity to improve emergency dispatch in Nairobi.

## Project Structure
```
nairobi-accident-severity/
├── data/
│   ├── raw/                 # Original Ma3Route dataset
│   ├── processed/           # Cleaned, labeled data
│   └── features/            # Engineered features
├── notebooks/               # Jupyter notebooks for exploration
├── src/                     # Source code
│   ├── data/               # Data loading and preprocessing
│   ├── features/           # Feature engineering
│   ├── models/             # Model training and prediction
│   └── visualization/      # Plotting functions
├── models/                  # Saved trained models
├── reports/                 # Generated analysis and figures
└── docs/                    # Documentation
```

## Setup
```bash
# Create virtual environment
python -m venv venv --without-pip

# Activate virtual environment
source venv/Scripts/activate  # Git Bash
# OR
.\venv\Scripts\Activate       # PowerShell

# Install dependencies
pip install -r requirements.txt
```

## Dataset
World Bank Ma3Route Nairobi Crash Dataset (2012-2023)
https://microdata.worldbank.org/access_licensed/download/3124/97805


## Author
Mary Wangoi Mwangi (122174)
Master of Science in Information Technology
Strathmore University
