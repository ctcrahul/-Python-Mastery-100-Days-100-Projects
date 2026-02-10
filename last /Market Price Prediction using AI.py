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

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, shuffle=False, test_size=0.2
)

# -----------------------------
# Model Training
# -----------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -----------------------------
# Prediction
# -----------------------------
data.loc[X_test.index, "Predicted"] = model.predict(X_test)

# -----------------------------
# Visualization
# -----------------------------
plt.figure()
plt.plot(data["Date"], data["Close"], label="Actual Price")
plt.plot(data["Date"], data["Predicted"], label="Predicted Price")
plt.xlabel("Date")
plt.ylabel("Market Price")
plt.legend()
plt.show()

# -----------------------------
# Next Day Prediction
# -----------------------------
last_row = data.iloc[-1]
next_day_features = [[
    last_row["Close"],
    data["Close"].tail(3).mean(),
    data["Close"].tail(7).mean()
]]

next_price = model.predict(next_day_features)[0]
print("Predicted Next Day Price:", round(next_price, 2))
