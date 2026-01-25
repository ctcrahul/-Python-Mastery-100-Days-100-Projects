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
