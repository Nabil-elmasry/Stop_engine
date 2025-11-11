#test for save

import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# 🎨 (اختياري) تفعيل التنسيق المخصص إذا حابب تفعل لاحقًا
# from tools.auto_theme_injector import apply_custom_theme
# apply_custom_theme()

# دالة: اكتشاف القيم المنحرفة
def detect_deviation(uploaded_df, model, threshold=0.1):
    try:
        predicted = model.predict(uploaded_df)
        predicted_df = pd.DataFrame(predicted, columns=uploaded_df.columns)
        deviation_df = uploaded_df - predicted_df
        deviation_df["Deviation_Score"] = deviation_df.abs().mean(axis=1)

        # استخراج القيم المنحرفة فقط
        deviated_only = deviation_df[deviation_df["Deviation_Score"] > threshold]
        return deviated_only
    except Exception as e:
        st.error(f"خطأ أثناء المقارنة: {e}")
        return pd.DataFrame()

# 🎯 واجهة المستخدم
st.title("🔍 مقارنة ملف به عطل مع النموذج المدرب")

# رفع الملفات
uploaded_model = st.file_uploader("📦 ارفع النموذج المدرب (pkl)", type=["pkl"])
uploaded_file = st.file_uploader("📂 اختر ملف الحساسات (CSV)", type=["csv"])

if uploaded_model and uploaded_file:
    try:
        # تحميل النموذج
        model = joblib.load(uploaded_model)
        st.success("✅ تم تحميل النموذج بنجاح.")

        # قراءة بيانات الحساسات
        sensor_data = pd.read_csv(uploaded_file)

        with st.expander("📄 عرض ملف الحساسات الأصلي"):
            st.dataframe(sensor_data)

        # تحليل القيم المنحرفة
        deviations = detect_deviation(sensor_data, model)

        if not deviations.empty:
            st.subheader("📉 القيم المنحرفة المكتشفة")
            st.dataframe(deviations)
            st.markdown(f"🔢 عدد القراءات المنحرفة: `{len(deviations)}`")
            st.info("✅ تم الاكتشاف بنجاح (دون تسجيل في ملف لوج).")
        else:
            st.info("✅ لا توجد قيم منحرفة تتجاوز العتبة المحددة.")

    except Exception as e:
        st.error("❌ حدث خطأ أثناء المعالجة.")
        st.exception(e)
else:
    st.warning("📌 برجاء رفع كلا الملفين: النموذج وملف الحساسات.")