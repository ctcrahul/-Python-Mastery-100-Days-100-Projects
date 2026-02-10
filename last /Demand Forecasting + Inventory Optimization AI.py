import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

# =============================
# LOAD DATA
# =============================
data = pd.read_csv("sales_data.csv")
data["Date"] = pd.to_datetime(data["Date"])
data.sort_values("Date", inplace=True)

# =============================
# FEATURE ENGINEERING
# =============================
data["Prev_Sales"] = data["Sales"].shift(1)
data["MA_3"] = data["Sales"].rolling(3).mean()
data["MA_7"] = data["Sales"].rolling(7).mean()
data.dropna(inplace=True)

X = data[["Prev_Sales", "MA_3", "MA_7"]]
y = data["Sales"]
