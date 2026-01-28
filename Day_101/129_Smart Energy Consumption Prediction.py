# # Smart Energy Consumption Prediction (Single File)
# # IoT + Machine Learning + Sustainability

# import numpy as np
# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_absolute_error

# # -----------------------------
# # SAMPLE ENERGY DATA
# # -----------------------------
# data = {
#     "hour": [6, 9, 12, 18, 22, 2, 15, 20],
#     "temperature": [22, 28, 32, 30, 26, 20, 34, 29],
#     "humidity": [60, 55, 40, 45, 50, 70, 35, 48],
#     "device_count": [3, 6, 8, 10, 7, 2, 9, 8],
#     "is_weekend": [0, 0, 0, 0, 1, 1, 0, 1],
#     "energy_kwh": [1.2, 2.8, 3.6, 5.2, 4.1, 0.9, 4.8, 4.3]
# }
# df = pd.DataFrame(data)

# # -----------------------------
# # FEATURES / TARGET
# # -----------------------------
# X = df.drop("energy_kwh", axis=1)
# y = df["energy_kwh"]

# # -----------------------------
# # TRAIN MODEL
# # -----------------------------
# model = RandomForestRegressor(
#     n_estimators=200,
#     random_state=42
# )

# model.fit(X, y)

# # -----------------------------
# # PREDICTION FUNCTION
# # -----------------------------
# def predict_energy(hour, temp, humidity, devices, weekend):
#     features = np.array([[hour, temp, humidity, devices, weekend]])
#     return model.predict(features)[0]

# # -----------------------------
# # USER INPUT
# # -----------------------------
# if __name__ == "__main__":
#     print("\n⚡ Smart Energy Consumption Predictor\n")

#     hour = int(input("Hour (0–23): "))
#     temp = float(input("Temperature (°C): "))
#     humidity = float(input("Humidity (%): "))
#     devices = int(input("Active Devices: "))
#     weekend = int(input("Weekend? (1=yes, 0=no): "))

#     prediction = predict_energy(
#         hour, temp, humidity, devices, weekend
#     )
#      humidity = float(input("Humidity (%): "))
#     devices = int(input("Active Devices: "))
#     weekend = int(input("Weekend? (1=yes, 0=no): "))

#     prediction = predict_energy(
#         hour, temp, humidity, devices, weekend
#     )

#     print(f"\n🔋 Predicted Energy Usage: {prediction:.2f} kWh")
# Smart Energy Consumption Prediction (Single File)
# IoT + Machine Learning + Sustainability

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# -----------------------------
# SAMPLE ENERGY DATA
# -----------------------------
data = {
    "hour": [6, 9, 12, 18, 22, 2, 15, 20],
    "temperature": [22, 28, 32, 30, 26, 20, 34, 29],
    "humidity": [60, 55, 40, 45, 50, 70, 35, 48],
    "device_count": [3, 6, 8, 10, 7, 2, 9, 8],
    "is_weekend": [0, 0, 0, 0, 1, 1, 0, 1],
    "energy_kwh": [1.2, 2.8, 3.6, 5.2, 4.1, 0.9, 4.8, 4.3]
}

df = pd.DataFrame(data)

# -----------------------------
# FEATURES / TARGET
# -----------------------------
X = df.drop("energy_kwh", axis=1)
y = df["energy_kwh"]

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

# -----------------------------
# PREDICTION FUNCTION
# -----------------------------
def predict_energy(hour, temp, humidity, devices, weekend):
    features = np.array([[hour, temp, humidity, devices, weekend]])
    return model.predict(features)[0]

# -----------------------------
# USER INPUT
# -----------------------------
if __name__ == "__main__":
    print("\n⚡ Smart Energy Consumption Predictor\n")

    hour = int(input("Hour (0–23): "))
    temp = float(input("Temperature (°C): "))
    humidity = float(input("Humidity (%): "))
    devices = int(input("Active Devices: "))
    weekend = int(input("Weekend? (1=yes, 0=no): "))

    prediction = predict_energy(
        hour, temp, humidity, devices, weekend
    )

    print(f"\n🔋 Predicted Energy Usage: {prediction:.2f} kWh")


####### output like this

Hour (0–23): 19
Temperature (°C): 31
Humidity (%): 44
Active Devices: 9
Weekend? (1=yes, 0=no): 0

Predicted Energy Usage: 4.87 kWh
