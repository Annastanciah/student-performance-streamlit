
import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

st.title("Student Performance Prediction App")

data = pd.read_csv("student-mat.csv", sep=';')
data_encoded = pd.get_dummies(data, drop_first=True)

X = data_encoded.drop('G3', axis=1)
y = data_encoded['G3']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LinearRegression()
model.fit(X_scaled, y)

st.write("Prediction uses average student data as demo")
sample = X.mean().values.reshape(1, -1)
sample_scaled = scaler.transform(sample)
prediction = model.predict(sample_scaled)

st.success(f"Predicted Final Grade: {prediction[0]:.2f}")
