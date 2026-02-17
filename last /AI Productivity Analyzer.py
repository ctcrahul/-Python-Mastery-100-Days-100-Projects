import time
import win32gui
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from flask import Flask, render_template_string

log_file = "activity_log.csv"

# ---------- TRACK ACTIVE WINDOW ----------
def get_active_window():
    window
