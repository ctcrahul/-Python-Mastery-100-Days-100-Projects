# Flood Risk Prediction System (Single File)
# Environment + ML + Decision System

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# -----------------------------
# SAMPLE DATASET
# -----------------------------
data = {
    "rainfall_mm": [20, 50, 120, 200, 80, 10, 160, 30],
    "river_level_m": [1.2, 2.1, 4.5, 6.2, 3.0, 1.0, 5.5, 1.8],
    "soil_moisture": [30, 45, 80, 95, 60, 25, 90, 40],
    "temperature": [35, 32, 28, 26, 30, 36, 27, 33],
    "flood_risk": ["Low", "Medium", "High", "High", "Medium", "Low", "High", "Low"]
}

df = pd.DataFrame(data)

# -----------------------------
# ENCODE TARGET
# -----------------------------
encoder = LabelEncoder()
df["flood_risk"] = encoder.fit_transform(df["flood_risk"])

X = df.drop("flood_risk", axis=1)
y = df["flood_risk"]

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)
