traffic_congestion_prediction/
 ├── train_model.py
 ├── app.py
 ├── traffic_model.pkl
 └── traffic_data.csv


###               train_model.py

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





###             app.py

from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

model = joblib.load("traffic_model.pkl")
road_encoder = joblib.load("road_encoder.pkl")
cong_encoder = joblib.load("cong_encoder.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    road = road_encoder.transform([data["road_type"]])[0]

    features = np.array([[
        data["hour"],
        data["day"],
        data["vehicle_count"],
        data["temperature"],
        data["rain"],
        road
    ]])

    pred = model.predict(features)[0]
    congestion = cong_encoder.inverse_transform([pred])[0]

    return jsonify({
        "Predicted_Congestion": congestion
    })

@app.route("/")
def home():
    return {"status": "Traffic Congestion API running"}

if __name__ == "__main__":
    app.run(debug=True)

        data["day"],
        data["vehicle_count"],
        data["temperature"],
