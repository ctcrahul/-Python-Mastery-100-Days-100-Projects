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
    st.subheader("Uploaded Data")
    st.dataframe(df)

    required_cols = ['study_hours','distractions','sleep','goals_completed']

    if not all(col in df.columns for col in required_cols):
        st.error("CSV must contain: study_hours, distractions, sleep, goals_completed")
        st.stop()

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df[required_cols])

    df_scaled = pd.DataFrame(scaled, columns=required_cols)

    # Consistency Score
    df['Consistency Score'] = (
        df_scaled['study_hours'] * 0.4 +
        (1 - df_scaled['distractions']) * 0.3 +
        df_scaled['sleep'] * 0.1 +
        df_scaled['goals_completed'] * 0.2
    ) * 100

    # Effort Stability
    df['Effort Stability'] = df['study_hours'].rolling(3).std().fillna(0)
