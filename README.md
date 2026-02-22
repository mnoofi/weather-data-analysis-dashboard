# 🌦 Rainfall Prediction System & Weather Analytics Dashboard

## 📌 Project Overview
An end-to-end Machine Learning project for predicting rainfall using Australian weather data.

The system combines:
- Data Cleaning & Feature Engineering
- Exploratory Data Analysis (EDA)
- Interactive Dashboard (Dash)
- Random Forest Classification Model
- Real-time Rain Prediction Interface

---

## 🚀 Model Performance

| Model | Accuracy |
|-------|----------|
| Logistic Regression | 85.2% |
| Random Forest | 85.6% |

Random Forest was selected as the final deployed model.

---

## 🔍 Key Features

- Feature Engineering (TempDiff, PressureDiff, HumidityDiff)
- Seasonal classification
- One-Hot Encoding
- Model comparison
- Feature importance analysis
- Live prediction system inside dashboard

---

## 🛠 Technologies Used

- Python
- Pandas & NumPy
- Scikit-learn
- Plotly
- Dash
- Joblib

---

## 📊 Dataset

Australian Weather Dataset (~145,000 records)

---

## ▶ How to Run

1. Clone the repository
2. Install dependencies:
pip install -r requirements.txt
3. Run the app:
python app.py

---

## 🔮 Live Prediction

The dashboard includes a Machine Learning section where users can input weather conditions and predict rainfall for the next day in real-time.

---

## 📈 Future Improvements

- Hyperparameter tuning
- Model probability visualization
- Cloud deployment (Render / Railway)
- CI/CD pipeline
