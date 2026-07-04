# 🩸 Anaemia Detection System

A machine learning-based clinical decision support system for detecting and classifying anaemia severity in pediatric patients.

---

## 📌 Project Overview

This project analyzes a pediatric anaemia dataset containing 300 patient records with demographic details, clinical pallor observations, haematological parameters, and investigation results. It builds machine learning models to predict anaemia severity and deploys them as a professional web application.

---

## 🎯 Objectives

- Perform data cleaning and preprocessing
- Conduct exploratory data analysis (EDA) to discover clinical patterns
- Build machine learning models to predict anaemia severity
- Analyze feature importance to identify key predictors
- Deploy a Streamlit-based web application for real-time prediction

---

## 📊 Dataset

- **Records:** 300 pediatric patients
- **Features:** Age, Gender, Pallor observations (Conjunctival, Tongue, Nailbed, Palmar), Haemoglobin, Blood indices (MCV, MCH, MCHC, RDW), Peripheral Smear
- **Target:** Anaemia severity (No Anemia, Mild, Moderate, Severe)

---

## 🤖 Machine Learning Models

| Model | Features | Accuracy | Use Case |
|-------|----------|----------|----------|
| Model 1 | Without HB | 76.67% | Field screening without lab |
| Model 2 | With HB | 100% | Clinical setting with lab |

**Algorithm:** Random Forest Classifier

---

## 🔑 Key Insights from EDA

- **54.9%** of patients have anaemia
- **Iron Deficiency** is the dominant cause — 81% of all cases
- **Palmar pallor** is the most reliable clinical indicator (95.6% accuracy)
- **HB drops consistently** with anaemia severity
- Males tend to have more **severe** anaemia; females more **mild** anaemia

---

## 🏥 Web Application Features

- **Login System** — Admin and Doctor roles
- **Prediction Page** — Two modes: Screening and Clinical
- **Patient Records** — Persistent SQLite database, search, download
- **Analytics Dashboard** — Visual insights from predictions
- **Doctor Management** — Admin can register and remove doctors

---

## 🛠️ Tech Stack

- **Language:** Python
- **ML Library:** Scikit-learn
- **Web App:** Streamlit
- **Database:** SQLite
- **Data Processing:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn

---

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/PokhrajSarkar/anemia-detection-app.git
cd anemia-detection-app
```

2. Install dependencies:
```bash
pip install streamlit joblib scikit-learn pandas numpy matplotlib seaborn bcrypt
```

3. Run the app:
```bash
streamlit run app.py
```

---

## 🔐 Default Login

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |

---

## 📁 Project Structure
