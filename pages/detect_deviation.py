import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime
from sklearn.metrics import mean_squared_error
from Tools.auto_theme_injector import apply_custom_theme

apply_custom_theme()

# المسارات
MODEL_PATH = "Modules/trained.pkl"
LOG_PATH = "Logs/deviation_log.txt"

# دالة لحساب الفروقات بين القيم المتوقعة والحقيقية
def detect_deviation(uploaded_df, model):
    try:
        predicted = model.predict(uploaded_df)
        predicted_df = pd.DataFrame(predicted, columns=uploaded_df.columns)
        deviation_df = uploaded_df - predicted_df
        deviation_df["Deviation_Score"] = deviation_df.abs().mean(axis=1)

        # اختيار القيم المنحرفة فقط
        threshold = 0.1  # يمكن تغييره حسب دقة البيانات
        deviated_only = deviation_df[deviation_df["Deviation_Score"] > threshold]

        return deviated_only
    except Exception as e:
        st.error(f"خطأ أثناء المقارنة: {e}")
        return pd.DataFrame()

# تسجيل القيم المنحرفة في ملف اللوج
def log_deviations(df):
    if df.empty:
        return
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"\n--- Deviation Detected @ {datetime.now()} ---\n")
        f.write(df.to_string(index=False))
        f.write("\n")

# واجهة المستخدم
st.title("🔍 مقارنة ملف به عطل مع النموذج المدرب")

uploaded_file = st.file_uploader("📂 اختر ملف الحساسات (CSV)", type=["csv"])

if uploaded_file:
    try:
        sensor_data = pd.read_csv(uploaded_file)

        # تحميل النموذج
        if not os.path.exists(MODEL_PATH):
            st.error("❌ النموذج المدرب غير موجود في المسار المحدد.")
        else:
            model = joblib.load(MODEL_PATH)
            st.success("✅ تم تحميل النموذج بنجاح.")

            # عرض البيانات الأصلية
            with st.expander("عرض ملف الحساسات الأصلي"):
                st.dataframe(sensor_data)

            # استخراج القيم المنحرفة فقط
            deviations = detect_deviation(sensor_data, model)

            if not deviations.empty:
                st.subheader("📉 القيم المنحرفة المكتشفة")
                st.dataframe(deviations)
                log_deviations(deviations)
                st.success("✅ تم تسجيل القيم المنحرفة في ملف اللوج.")
            else:
                st.info("✅ لا توجد قيم منحرفة تتجاوز العتبة المحددة.")

    except Exception as e:
        st.error("❌ حدث خطأ أثناء معالجة الملف. يرجى التحقق من التنسيق والمحاولة مرة أخرى.")
        st.exception(e)