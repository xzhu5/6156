# -*- coding: utf-8 -*-
"""6156.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MyA-GFssKOUPmhFPDE1L3TgDXTT4liVR
"""

import pandas as pd

# Load the data
data = pd.read_csv("natality2023ps.csv")

# Drop rows where apgar5 is 99
data = data[data['apgar5'] != 99]

# Keep only relevant variables
data = data[['mager', 'mrace31', 'meduc', 'pwgt_r', 'wtgain', 'bmi', 'cig_0',
    'precare', 'previs', 'rf_pdiab', 'rf_phype', 'dplural', 'pay']]

#Look at data spread including object variables (transposed)
data.describe(include='all').T

#Look at data types, non-null counts and data types
data.info()

import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib


# Load the data
data = pd.read_csv("natality2023ps.csv")

# Select relevant features based on the previous list (adjust column names as needed)
features = [
    'mager', 'mrace6', 'meduc', 'pwgt_r', 'wtgain', 'bmi', 'cig_0',
    'precare', 'previs', 'rf_pdiab', 'rf_phype', 'dplural', 'pay'
]

target = 'apgar5'  # Set the target column name for the APGAR score

# Separate features and target
X = data[features]
y = data[target]

# Handle missing values
X = X.dropna()

# Encode categorical variables with LabelEncoder for rf_pdiab and rf_phype
label_encoder = LabelEncoder()

for column in ['rf_pdiab', 'rf_phype']:
    X[column] = label_encoder.fit_transform(X[column].astype(str))  # Ensure all data is string before encoding

# Standardize numerical features (excluding other categorical variables)
numerical_features = ['mager', 'pwgt_r', 'wtgain', 'bmi', 'cig_0', 'precare', 'previs']
scaler = StandardScaler()
X[numerical_features] = scaler.fit_transform(X[numerical_features])

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
print(f"Mean Absolute Error: {mae}")

# Optional: feature importance analysis
importances = model.feature_importances_
feature_importances = pd.DataFrame({'feature': X.columns, 'importance': importances})
feature_importances = feature_importances.sort_values(by='importance', ascending=False)
print(feature_importances)

# Save the model
joblib.dump(model, "apgar5_model.pkl")

import streamlit as st
import joblib
import numpy as np

# Load the trained model
model = joblib.load("apgar5_model.pkl")

# Define the Streamlit app
st.title("APGAR Score Prediction")

st.header("Enter Pregnancy and Maternal Details")
mother_age = st.number_input("Mother's Age", min_value=12, max_value=50, step=1)
mother_race = st.selectbox("Mother's Race", ["White (only)", "Black (only)", "AIAN (only)", "Asian (only)", "NHOPI (only)", "More than one race"])
mother_education = st.selectbox("Mother's Education", ["8th grade or less", "9th through 12th grade with no diploma", "High school graduate or GED completed", "Some college credit, but no degree", "Associate degree", "Bachelor's degree", "Master's degree", "Doctorate"])
mother_prepregnancy_weight = st.number_input("Mother's Prepregnancy Weight", min_value=75, max_value=375, step=1)
mother_weight_gain = st.number_input("Mother's Weight Gain", min_value=0, max_value=98, step=1)
mother_bmi = st.number_input("Mother's BMI", min_value=13.0, max_value=69.9, step=0.1)
smoking_before_pregnancy = st.number_input("Number of Cigarettes Daily Before Pregnancy", min_value=0, max_value=98, step=1)
prenatal_care_began = st.number_input("Month Prenatal Care Began", min_value=0, max_value=10, step=1)
prenatal_care_visits = st.number_input("Number of Prenatal Care Visits", min_value=0, max_value=98, step=1)
mother_diabetes = st.selectbox("Pre-pregnancy Diabetes Status", ["Yes", "No"])
mother_hypertension = st.selectbox("Pre-pregnancy Hypertension Status", ["Yes", "No"])
plurality = st.selectbox("Plurality", ["Single", "Twin", "Triplet", "Quadruplet or higher"])
pay = st.selectbox("Payment Source for Delivery", ["Medicaid", "Private Insurance", "Self-Pay", "Indian Health Service", "CHAMPUS/TRICARE", "Other government", "Other non-government"])

# Convert inputs to a format suitable for prediction
input_features = np.array([
     mother_age,
    {"White (only)": 0, "Black (only)": 1, "AIAN (only)": 2, "Asian (only)": 3, "NHOPI (only)": 4, "More than one race": 5}[mother_race],
    {"8th grade or less": 0, "9th through 12th grade with no diploma": 1, "High school graduate or GED completed": 2, "Some college credit, but no degree": 3, "Associate degree": 4, "Bachelor's degree": 5, "Master's degree": 6, "Doctorate": 7}[mother_education],
    mother_prepregnancy_weight,
    mother_weight_gain,
    mother_bmi,
    smoking_before_pregnancy,
    prenatal_care_began,
    prenatal_care_visits,
    1 if mother_diabetes == "Yes" else 0,
    1 if mother_hypertension == "Yes" else 0,
    {"Single": 1, "Twin": 2, "Triplet": 3, "Quadruplet or higher": 4}[plurality],
    {"Medicaid": 0, "Private Insurance": 1, "Self-Pay": 2, "Indian Health Service": 3, "CHAMPUS/TRICARE": 4, "Other government": 5, "Other non-government": 6}[pay]
]).reshape(1, -1)


# Predict APGAR score
if st.button("Predict APGAR Score"):
    prediction = model.predict(input_features)
    st.subheader(f"Predicted APGAR Score: {prediction[0]:.1f}")
