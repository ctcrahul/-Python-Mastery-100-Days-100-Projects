# Titanic Survival Prediction (Single File)
# Classic ML Classification Problem

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("train.csv")

# -----------------------------
# SELECT FEATURES
# -----------------------------
features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
target = "Survived"

df = df[features + [target]]

# -----------------------------
# HANDLE MISSING VALUES
# -----------------------------
df["Age"].fillna(df["Age"].median(), inplace=True)
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

# -----------------------------
# ENCODE CATEGORICAL DATA
# -----------------------------
encoder = LabelEncoder()
df["Sex"] = encoder.fit_transform(df["Sex"])
df["Embarked"] = encoder.fit_transform(df["Embarked"])
# -----------------------------
# SPLIT DATA
# -----------------------------
X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# EVALUATION
# -----------------------------
predictions = model.predict(X_test)

print("\n🎯 Accuracy:", accuracy_score(y_test, predictions))
print("\n📊 Classification Report:\n")
print(classification_report(y_test, predictions))

# -----------------------------
# SINGLE PASSENGER PREDICTION
# -----------------------------
def predict_survival(pclass, sex, age, sibsp, parch, fare, embarked):
    sex = encoder.transform([sex])[0]
    embarked = encoder.transform([embarked])[0]

    sample = np.array([[pclass, sex, age, sibsp, parch, fare, embarked]])
    result = model.predict(sample)[0]
    return "Survived" if result == 1 else "Did Not Survive"

# -----------------------------
# USER INPUT
# -----------------------------
if __name__ == "__main__":
    print("\n🚢 Titanic Survival Predictor\n")

    pclass = int(input("Passenger Class (1/2/3): "))
    sex = input("Sex (male/female): ")
    age = float(input("Age: "))
    sibsp = int(input("Siblings/Spouses aboard: "))
    parch = int(input("Parents/Children aboard: "))
    fare = float(input("Fare: "))
    embarked = input("Embarked (C/Q/S): ")

    result = predict_survival(
        pclass, sex, age, sibsp, parch, fare, embarked
    )

    print("\n🧾 Prediction:", result)
