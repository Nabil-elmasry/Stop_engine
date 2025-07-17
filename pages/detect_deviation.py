import streamlit as st
import pandas as pd
import joblib
import numpy as np
import os
import logging
from tools.apply_custom_theme import apply_custom_theme

apply_custom_theme()

# إعداد اللوج
log_file_path = "logs/deviation_log.txt"
os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

st.title("📉 كشف القيم المنحرفة في قراءات الحساسات")

# تحميل النموذج المدرب مسبقًا
MODEL_PATH = "models/sensor_model.pkl"
if not os.path.exists(MODEL_PATH):
    st.error("⚠️ ملف النموذج غير موجود. تأكد من وجوده داخل مجلد models.")
    st.stop()

model = joblib.load(MODEL_PATH)

uploaded_file = st.file_uploader("📤 ارفع ملف CSV به قراءات الحساسات (بها مشكلة):", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        if 'Sensor Name' not in df.columns or 'Value' not in df.columns:
            st.error("❌ تأكد أن الملف يحتوي على الأعمدة: Sensor Name و Value")
            st.stop()

        # تحويل القيم إلى float إذا أمكن
        df["Value"] = pd.to_numeric(df["Value"], errors='coerce')

        # معالجة البيانات
        X = df["Value"].values.reshape(-1, 1)
        y_pred = model.predict(X)
        error = np.abs(X.flatten() - y_pred.flatten())

        # حساب الانحراف بناءً على Threshold تلقائي
        threshold = np.percentile(error, 85)  # تعديل النسبة حسب دقة النموذج
        df["Predicted"] = y_pred
        df["Deviation"] = error
        df["Is Deviated"] = df["Deviation"] > threshold

        # عرض القيم المنحرفة فقط
        deviated_df = df[df["Is Deviated"]]

        if not deviated_df.empty:
            st.subheader("🔍 القيم المنحرفة المكتشفة:")
            st.dataframe(deviated_df[["Sensor Name", "Value", "Predicted", "Deviation"]])

            # حفظ في لوج
            for _, row in deviated_df.iterrows():
                logging.info(f"انحراف: {row['Sensor Name']} - القيمة: {row['Value']} - المتوقعة: {row['Predicted']:.2f} - الانحراف: {row['Deviation']:.2f}")

        else:
            st.success("✅ لا توجد قيم منحرفة واضحة في البيانات المرفوعة.")

    except Exception as e:
        st.error("❌ حدث خطأ أثناء معالجة الملف.")
        st.exception(e)