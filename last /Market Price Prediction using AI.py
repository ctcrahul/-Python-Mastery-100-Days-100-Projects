import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# -----------------------------
# Load Data
# -----------------------------
data = pd.read_csv("market_data.csv")
data["Date"] = pd.to_datetime(data["Date"])
data.sort_values("Date", inplace=True)

# -----------------------------
# Feature Engineering
# -----------------------------
data["Prev_Close"] = data["Close"].shift(1)
data["MA_3"] = data["Close"].rolling(3).mean()
data["MA_7"] = data["Close"].rolling(7).mean()

data.dropna(inplace=True)

X = data[["Prev_Close", "MA_3", "MA_7"]]
y = data["Close"]
