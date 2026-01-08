🎓 Student Performance Prediction System

Author: Annastanciah Tong'i
Project Type: Machine Learning Project
Deployment: Streamlit Web Application

📌 Project Overview

The Student Performance Prediction System is a machine learning–based web application designed to predict students’ academic performance and classify their academic risk level. The system supports both individual student prediction and batch prediction using CSV upload, making it suitable for use by teachers and academic institutions.

The application integrates data analytics, predictive modeling, secure authentication, and visual dashboards to support academic decision-making.

🎯 Objectives

Predict students’ final academic grades using machine learning

Classify students into Low, Medium, or High academic risk

Provide a secure teacher login system

Enable batch prediction via CSV upload

Visualize school-level performance analytics

Store prediction records persistently using a database

🧠 Technologies Used

Programming Language: Python

Web Framework: Streamlit

Machine Learning: Scikit-learn

Data Processing: Pandas, NumPy

Visualization: Matplotlib

Database: SQLite

Security: SHA-256 Password Hashing

Deployment: Streamlit Community Cloud

📂 Project Structure
student-performance-streamlit/
│
├── app.py                  # Main Streamlit application
├── student-mat.csv         # Dataset
├── students.db             # SQLite database (auto-generated)
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation

🔐 System Login Details (Demo)
Username: teacher
Password: admin123


Passwords are securely stored using SHA-256 hashing.

⚙️ Installation & Local Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/student-performance-streamlit.git
cd student-performance-streamlit

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run the Application
streamlit run app.py

🌐 Online Deployment (Streamlit Cloud)

Push the project to a public GitHub repository

Go to 👉 https://streamlit.io/cloud

Sign in with GitHub

Click New App

Select:

Repository

Branch: main

File: app.py

Click Deploy

You will receive a live URL such as:

https://student-performance-streamlit.streamlit.app

📊 System Features
✔ Manual Student Prediction

Sliders & dropdown inputs

Predicts final grade

Displays academic risk level with color coding

✔ Batch Prediction

Upload CSV file

Predict grades and risk for multiple students

Download results as CSV

✔ Visual Analytics

Grade distribution charts

Risk-level bar charts

School-level performance insights

✔ Secure Authentication

Teacher login

Password hashing

Session-based access control

✔ Persistent Storage

SQLite database stores predictions

Enables future analytics and reporting

📁 Dataset Information

Source: UCI Machine Learning Repository

Dataset: Student Performance Dataset

Attributes include:

Gender

Study time

Failures

Absences

G1, G2 grades

Final grade (G3)

🧪 Machine Learning Models

Linear Regression: Final grade prediction

Logistic Regression: Pass/Fail classification

StandardScaler: Feature normalization

📈 Risk Classification Logic
Predicted Grade	Risk Level
≥ 14	Low Risk
10 – 13	Medium Risk
< 10	High Risk
📚 Academic Use

This system is suitable for:

Final year project submission

Machine learning coursework

Academic analytics demonstrations

Student performance monitoring systems

🚀 Future Enhancements

Role-based user accounts

Cloud database integration

Model retraining via admin panel

Student historical tracking

Mobile-friendly UI

🏆 Author

Annastanciah Tong'i
Bachelor of Science in Computer Science / IT
Machine Learning Project
