import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import hashlib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Student Performance Prediction System",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------
conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    sex TEXT,
    studytime INTEGER,
    failures INTEGER,
    absences INTEGER,
    G1 INTEGER,
    G2 INTEGER,
    predicted_grade REAL,
    risk_level TEXT
)
""")
conn.commit()

# -------------------------------------------------
# PASSWORD HASHING
# -------------------------------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Default teacher account
cursor.execute(
    "INSERT OR IGNORE INTO users VALUES (?, ?)",
    ("teacher", hash_password("admin123"))
)
conn.commit()

# -------------------------------------------------
# LOGIN SYSTEM
# -------------------------------------------------
def login():
    st.title("🔐 Teacher Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        hashed = hash_password(password)
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, hashed)
        )
        if cursor.fetchone():
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    login()
    st.stop()

# -------------------------------------------------
# LOAD & TRAIN MODELS
# -------------------------------------------------
@st.cache_data
def train_models():
    data = pd.read_csv("student-mat.csv", sep=";")
    encoded = pd.get_dummies(data, drop_first=True)

    X = encoded.drop("G3", axis=1)
    y_reg = encoded["G3"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    reg = LinearRegression().fit(X_scaled, y_reg)

    encoded["pass"] = (encoded["G3"] >= 10).astype(int)
    y_cls = encoded["pass"]

    cls = LogisticRegression(max_iter=1000).fit(X_scaled, y_cls)

    return data, X, scaler, reg, cls

data, X, scaler, reg_model, cls_model = train_models()

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
st.title("🎓 Student Performance Prediction Dashboard")
st.markdown("Developed by **Annastanciah Tong'i**")

col1, col2 = st.columns(2)

# -------------------------------------------------
# MANUAL INPUT
# -------------------------------------------------
with col1:
    st.subheader("🧾 Student Input")

    sex = st.selectbox("Gender", ["male", "female"])
    studytime = st.slider("Weekly Study Time", 1, 4, 2)
    failures = st.slider("Past Failures", 0, 4, 0)
    absences = st.slider("Absences", 0, 100, 5)
    G1 = st.slider("G1 Grade", 0, 20, 10)
    G2 = st.slider("G2 Grade", 0, 20, 10)

    input_df = pd.DataFrame(columns=X.columns)
    input_df.loc[0] = 0
    input_df.loc[0, ["studytime", "failures", "absences", "G1", "G2"]] = [
        studytime, failures, absences, G1, G2
    ]

    if sex == "male" and "sex_M" in input_df.columns:
        input_df.loc[0, "sex_M"] = 1

    input_scaled = scaler.transform(input_df)

    if st.button("🔍 Predict"):
        grade = reg_model.predict(input_scaled)[0]

        # Risk coding
        if grade >= 14:
            risk = "Low Risk"
            color = "green"
        elif grade >= 10:
            risk = "Medium Risk"
            color = "orange"
        else:
            risk = "High Risk"
            color = "red"

        st.markdown(
            f"<h3 style='color:{color}'>Predicted Grade: {grade:.2f}</h3>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<h4 style='color:{color}'>Risk Level: {risk}</h4>",
            unsafe_allow_html=True
        )

        cursor.execute(
            "INSERT INTO predictions VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (sex, studytime, failures, absences, G1, G2, grade, risk)
        )
        conn.commit()

# -------------------------------------------------
# ANALYTICS & CHARTS
# -------------------------------------------------
with col2:
    st.subheader("📊 School Performance Analytics")

    pred_df = pd.read_sql("SELECT * FROM predictions", conn)

    if not pred_df.empty:
        fig, ax = plt.subplots()
        ax.hist(pred_df["predicted_grade"], bins=10)
        ax.set_title("Predicted Grade Distribution")
        ax.set_xlabel("Grade")
        ax.set_ylabel("Students")
        st.pyplot(fig)

        risk_counts = pred_df["risk_level"].value_counts()
        st.bar_chart(risk_counts)

# -------------------------------------------------
# BATCH CSV UPLOAD
# -------------------------------------------------
st.markdown("---")
st.subheader("📂 Batch Prediction")

file = st.file_uploader("Upload CSV", type="csv")

if file:
    batch = pd.read_csv(file)
    batch_enc = pd.get_dummies(batch, drop_first=True)
    batch_enc = batch_enc.reindex(columns=X.columns, fill_value=0)
    batch_scaled = scaler.transform(batch_enc)

    batch["Predicted_G3"] = reg_model.predict(batch_scaled)
    batch["Risk"] = batch["Predicted_G3"].apply(
        lambda x: "Low" if x >= 14 else "Medium" if x >= 10 else "High"
    )

    st.dataframe(batch)

    st.download_button(
        "⬇ Download Results",
        batch.to_csv(index=False),
        "batch_predictions.csv",
        "text/csv"
    )

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")
st.caption("Secure ML-Based Academic Decision Support System")
