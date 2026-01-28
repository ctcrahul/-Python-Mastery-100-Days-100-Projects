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
