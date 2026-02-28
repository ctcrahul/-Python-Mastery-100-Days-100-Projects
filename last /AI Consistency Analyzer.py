import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="AI Consistency Analyzer", layout="wide")

st.title("AI Consistency Analyzer")

st.markdown("Upload your daily performance data to analyze discipline patterns.")

uploaded_file = st.file_uploader("Upload CSV File")

if uploaded_file:

    df = pd.read_csv(uploaded_file)
