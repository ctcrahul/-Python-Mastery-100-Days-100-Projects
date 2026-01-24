import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

# Load data
data = pd.read_csv("air_quality.csv")

X = data.drop("AQI", axis=1)
y = data["AQI"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
pred = model.predict(X_test)
mae = mean_absolute_error(y_test, pred)
print("Mean Absolute Error:", mae)

# Save model
joblib.dump(model, "aqi_model.pkl")
print("Model saved as aqi_model.pkl")





from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("aqi_model.pkl")

@app.route("/predict", methods=["POST"])
def predict_aqi():
    data = request.json

    features = np.array([[
        data["PM2.5"],
        data["PM10"],
        data["NO2"],
        data["SO2"],
        data["CO"],
        data["O3"]
    ]])

    prediction = model.predict(features)[0]

    return jsonify({
        "Predicted_AQI": round(prediction, 2)
    })

@app.route("/")
def home():
    return {"status": "AQI Prediction API running"}

if __name__ == "__main__":
    app.run(debug=True)
