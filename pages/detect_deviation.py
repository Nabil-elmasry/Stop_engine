import streamlit as st
import pandas as pd
import joblib
import os

from modules.logger import log_event
from modules.themes_leader import apply_custom_theme

apply_custom_theme()

st.title("🔍 StopEngine AI - كشف عن الأعطال بالذكاء الاصطناعي")

uploaded_file = st.file_uploader("ارفع ملف الحساسات هنا (CSV فقط)", type="csv")

if uploaded_file is not None:
    try:
        input_data = pd.read_csv(uploaded_file)

        model_path = os.path.join("modules", "trained_model.pkl")
        if not os.path.exists(model_path):
            st.error("⚠️ ملف النموذج المدرب غير موجود داخل مجلد modules.")
        else:
            model = joblib.load(model_path)

            # توقع القيم بناءً على النموذج المدرب
            predicted_values = model.predict(input_data)

            # حساب الفرق (الانحراف)
            deviation = abs(input_data.values - predicted_values)

            # إنشاء جدول بالنتائج
            deviation_df = pd.DataFrame(deviation, columns=input_data.columns)

            # عرض النتائج
            st.subheader("📊 نتائج التحليل (الانحراف لكل حساس):")
            st.dataframe(deviation_df)

            # مستوى الانحراف العام
            average_deviation = deviation_df.mean().mean()
            st.markdown(f"### ✅ متوسط الانحراف الكلي: `{average_deviation:.3f}`")

            # تفسير النتيجة
            threshold = 0.5  # تقدر تعدله حسب تجربتك
            if average_deviation > threshold:
                st.error("🚨 ⚠️ هناك احتمال بوجود عطل في أحد الأنظمة. يُفضل الفحص اليدوي.")
            else:
                st.success("✅ قراءات الحساسات تبدو طبيعية. لا يوجد علامات واضحة على الأعطال.")

            log_event("تم الكشف عن انحراف في البيانات بنجاح")

    except Exception as e:
        st.error(f"حدث خطأ أثناء تحليل البيانات: {e}")
        log_event(f"خطأ أثناء التحليل: {e}")