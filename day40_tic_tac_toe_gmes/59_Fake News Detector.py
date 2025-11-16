"""
Fake News Detector (Single File)
--------------------------------
Features:
 - Load any CSV dataset with columns: "text" and "label"
 - Train TF-IDF + Logistic Regression model
 - Evaluate accuracy, precision, recall, F1
 - Predict single text or classify a full CSV
 - Export results to CSV
 - Tkinter GUI

Label format required:
 - "fake" or "real"
 - or 1 (fake) / 0 (real)

Run:
    python fake_news_detector.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import os
import time
from datetime 
