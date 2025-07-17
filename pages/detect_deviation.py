import streamlit as st
import pandas as pd
import joblib
import numpy as np
from modules.logger import logger  # ✅ تفعيل اللوج

st.set_page_config(page_title="Detect Deviation", layout="wide")

st.title("📊 Detect Sensor Deviation from Normal Behavior")

uploaded_model = st.file_uploader("🔍 Upload the trained model (.pkl)", type=["pkl"])
uploaded_file = st.file_uploader("📂 Upload sensor data to analyze (.csv)", type=["csv"])

if uploaded_model and uploaded_file:
    try:
        logger.info("🔁 Loading model...")  # ✅ سجل عملية تحميل الموديل
        model = joblib.load(uploaded_model)
        logger.info("✅ Model loaded successfully.")

        logger.info("📥 Reading sensor data file...")
        df = pd.read_csv(uploaded_file)
        logger.info(f"✅ Sensor data file read successfully. Shape: {df.shape}")

        if 'timestamp' in df.columns:
            df = df.drop(columns=['timestamp'])
            logger.info("🕒 'timestamp' column dropped.")

        logger.info("🧮 Starting prediction on input data...")
        reconstructed = model.inverse_transform(model.transform(df))
        reconstruction_error = np.mean((df - reconstructed) ** 2, axis=1)
        df['Deviation Score'] = reconstruction_error
        logger.info("✅ Deviation scores calculated.")

        threshold = st.slider("🚦 Deviation threshold", float(df['Deviation Score'].min()), float(df['Deviation Score'].max()), float(df['Deviation Score'].mean()))

        outliers = df[df['Deviation Score'] > threshold]
        st.subheader("⚠️ Detected Outliers")
        st.dataframe(outliers)

        st.subheader("📈 All Sensor Data with Deviation Scores")
        st.dataframe(df)

        logger.info(f"📊 {len(outliers)} outliers detected out of {len(df)} records.")

    except Exception as e:
        logger.error(f"❌ Error in processing: {e}")
        st.error("❌ An error occurred while processing the files. Please check the format and try again.")
else:
    st.info("📤 Please upload both a trained model and sensor data file to proceed.")