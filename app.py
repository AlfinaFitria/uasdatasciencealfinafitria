# -*- coding: utf-8 -*-
"""uasdatascience.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1GC3Dc7dQWLzyj3MBOe0soG-Bi0yrA9UA

# Import libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load dataset
data = pd.read_csv("/content/sample_data/winequality-red.csv", delimiter=";", quotechar='"')

# 2. Data Understanding
print("Dataset Shape:", data.shape)
print("\nData Types:\n", data.dtypes)
print("\nMissing Values:\n", data.isnull().sum())

# Exploratory Data Analysis (EDA)
print("\nDataset Description:\n", data.describe())

# Visualize the distribution of quality
sns.countplot(x="quality", data=data)
plt.title("Distribution of Wine Quality")
plt.show()

# Correlation heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()

# 3. Data Preparation
# Remove outliers (optional, based on EDA)
def remove_outliers(df, columns):
    for col in columns:
        upper_limit = df[col].mean() + 3 * df[col].std()
        lower_limit = df[col].mean() - 3 * df[col].std()
        df = df[(df[col] <= upper_limit) & (df[col] >= lower_limit)]
    return df

columns_to_check = ["residual sugar", "chlorides", "density"]
data = remove_outliers(data, columns_to_check)

# Categorize quality
def categorize_quality(value):
    if value <= 4:
        return "low"
    elif value <= 6:
        return "medium"
    else:
        return "high"

data["quality_label"] = data["quality"].apply(categorize_quality)

# Encode target variable
data["quality_label"] = data["quality_label"].map({"low": 0, "medium": 1, "high": 2})

# Drop original quality column
data = data.drop("quality", axis=1)

# Split dataset
X = data.drop("quality_label", axis=1)
y = data["quality_label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. Modeling
# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt="d", cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# Feature importance
importances = model.feature_importances_
feature_names = X.columns

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(feature_names, importances, color="skyblue")
plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.show()

# prompt: save model

import joblib

# Assuming 'model' is your trained RandomForestClassifier
# Save the model to a file
joblib.dump(model, 'wine_quality_model.pkl')

!pip install streamlit



import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
model = joblib.load('wine_quality_model.pkl')

# Define the app title
st.title("Wine Quality Prediction App")
st.markdown("This app predicts the quality of wine (low, medium, or high) based on its chemical properties.")

# Sidebar inputs
st.sidebar.header("Input Features")

def user_input_features():
    fixed_acidity = st.sidebar.slider('Fixed Acidity', 4.0, 16.0, 8.0)
    volatile_acidity = st.sidebar.slider('Volatile Acidity', 0.1, 1.5, 0.5)
    citric_acid = st.sidebar.slider('Citric Acid', 0.0, 1.0, 0.3)
    residual_sugar = st.sidebar.slider('Residual Sugar', 0.5, 15.0, 2.5)
    chlorides = st.sidebar.slider('Chlorides', 0.01, 0.1, 0.05)
    free_sulfur_dioxide = st.sidebar.slider('Free Sulfur Dioxide', 1.0, 72.0, 15.0)
    total_sulfur_dioxide = st.sidebar.slider('Total Sulfur Dioxide', 6.0, 289.0, 46.0)
    density = st.sidebar.slider('Density', 0.990, 1.004, 0.996)
    pH = st.sidebar.slider('pH', 2.9, 4.0, 3.3)
    sulphates = st.sidebar.slider('Sulphates', 0.3, 2.0, 0.6)
    alcohol = st.sidebar.slider('Alcohol', 8.0, 15.0, 10.0)

    data = {
        'fixed acidity': fixed_acidity,
        'volatile acidity': volatile_acidity,
        'citric acid': citric_acid,
        'residual sugar': residual_sugar,
        'chlorides': chlorides,
        'free sulfur dioxide': free_sulfur_dioxide,
        'total sulfur dioxide': total_sulfur_dioxide,
        'density': density,
        'pH': pH,
        'sulphates': sulphates,
        'alcohol': alcohol
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Display user input features
st.subheader("User Input Features")
st.write(input_df)

# Predict quality
prediction = model.predict(input_df)
prediction_proba = model.predict_proba(input_df)

# Map predictions to labels
quality_mapping = {0: "Low", 1: "Medium", 2: "High"}

# Display prediction
st.subheader("Prediction")
st.write(f"The predicted wine quality is: **{quality_mapping[prediction[0]]}**")

# Display prediction probabilities
st.subheader("Prediction Probabilities")
st.write("The probabilities for each quality label are:")
pred_proba_df = pd.DataFrame(prediction_proba, columns=['Low', 'Medium', 'High'])
st.write(pred_proba_df)

# Footer
st.markdown("---")
st.markdown("Developed with ❤️ Alfina Fitria")