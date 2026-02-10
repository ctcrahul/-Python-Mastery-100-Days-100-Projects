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
# =============================
# TRAIN DEMAND MODEL
# =============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, shuffle=False, test_size=0.2
)

model = LinearRegression()
model.fit(X_train, y_train)

data.loc[X_test.index, "Predicted_Demand"] = model.predict(X_test)

# =============================
# INVENTORY PARAMETERS
# =============================
LEAD_TIME = 5               # days
HOLDING_COST = 2            # per unit per day
ORDER_COST = 50             # per order
SHORTAGE_COST = 10          # per unit
CURRENT_STOCK = 400

# =============================
# INVENTORY FORMULAS
# =============================
avg_daily_demand = data["Sales"].mean()
demand_std = data["Sales"].std()

# Safety Stock
safety_stock = int(1.65 * demand_std * np.sqrt(LEAD_TIME))

# Reorder Point
reorder_point = int(avg_daily_demand * LEAD_TIME + safety_stock)

# Economic Order Quantity (EOQ)
annual_demand = avg_daily_demand * 365
EOQ = int(np.sqrt((2 * annual_demand * ORDER_COST) / HOLDING_COST))

# =============================
# DECISION LOGIC
# =============================
decision = "DO NOT reorder yet"
if CURRENT_STOCK <= reorder_point:
    decision = f"REORDER {EOQ} units now"

# =============================
# OUTPUT
# =============================
print("\n--- DEMAND & INVENTORY DECISION ---")
print("Average Daily Demand:", round(avg_daily_demand, 2))
print("Safety Stock:", safety_stock)
print("Reorder Point:", reorder_point)
print("Current Stock:", CURRENT_STOCK)
print("EOQ:", EOQ)
print("Decision:", decision)

# =============================
# VISUALIZATION
# =============================
plt.figure()
plt.plot(data["Date"], data["Sales"], label="Actual Sales")
plt.plot(data["Date"], data["Predicted_Demand"], label="Predicted Demand")
plt.axhline(reorder_point, linestyle="--", label="Reorder Point")
plt.xlabel("Date")
plt.ylabel("Units")
plt.legend()
plt.show()
