traffic_congestion_prediction/
 ├── train_model.py
 ├── app.py
 ├── traffic_model.pkl
 └── traffic_data.csv


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

data = pd.read_csv("traffic_data.csv")

# Encode categorical
le_road = LabelEncoder()
le_cong = LabelEncoder()

data["road_type"] = le_road.fit_transform(data["road_type"])
data["congestion"] = le_cong.fit_transform(data["congestion"])

X = data.drop("congestion", axis=1)
y = data["congestion"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
model.fit(X_train, y_train)

joblib.dump(model, "traffic_model.pkl")
joblib.dump(le_road, "road_encoder.pkl")
joblib.dump(le_cong, "cong_encoder.pkl")

print("Traffic congestion model saved.")
