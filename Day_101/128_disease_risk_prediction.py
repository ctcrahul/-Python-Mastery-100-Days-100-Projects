# Disease Risk Prediction System (Single File)
# Healthcare + Machine Learning

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# -----------------------------
# SAMPLE HEALTH DATA
# -----------------------------
data = {
    "age": [25, 45, 60, 35, 50, 70, 40, 30],
    "bmi": [22, 28, 31, 25, 29, 34, 27, 23],
    "blood_pressure": [110, 140, 160, 120, 145, 170, 135, 115],
    "cholesterol": [180, 220, 260, 190, 240, 280, 210, 185],
    "disease_risk": ["Low", "Medium", "High", "Low", "Medium", "High", "Medium", "Low"]
}

df = pd.DataFrame(data)

# -----------------------------
# ENCODE TARGET
# -----------------------------
encoder = LabelEncoder()
df["disease_risk"] = encoder.fit_transform(df["disease_risk"])

X = df.drop("disease_risk", axis=1)
y = df["disease_risk"]
# -----------------------------
# TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X, y)

# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def predict_risk(age, bmi, bp, cholesterol):
    features = np.array([[age, bmi, bp, cholesterol]])
    pred = model.predict(features)[0]
    return encoder.inverse_transform([pred])[0]
# -----------------------------
# USER INPUT
# -----------------------------
if __name__ == "__main__":
    print("\n🏥 Disease Risk Prediction System\n")

    age = int(input("Age: "))
    bmi = float(input("BMI: "))
    bp = int(input("Blood Pressure: "))
    cholesterol = int(input("Cholesterol: "))

    risk = predict_risk(age, bmi, bp, cholesterol)
    print("\n⚠️ Predicted Disease Risk:", risk)
