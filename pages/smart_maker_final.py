import streamlit as st
import pandas as pd
import pickle
import os

# عنوان الصفحة
st.title("📊 Smart Maker Final - التحقق من فورمات ملف الحساسات")

# رفع ملف الحساسات
sensor_file = st.file_uploader("📁 ارفع ملف الحساسات (CSV)", type="csv")

# رفع ملف النموذج المدرب
model_file = st.file_uploader("🤖 ارفع ملف النموذج المدرب (.pkl)", type="pkl")

if sensor_file and model_file:
    try:
        # قراءة ملف الحساسات
        df_sensor = pd.read_csv(sensor_file)

        # تحميل النموذج المدرب
        model = pickle.load(model_file)

        # محاولة استخراج الأعمدة المستخدمة أثناء التدريب
        if hasattr(model, 'feature_names_in_'):
            model_columns = list(model.feature_names_in_)
        elif hasattr(model, 'columns'):
            model_columns = list(model.columns)
        else:
            st.warning("❗ لم نتمكن من استخراج أسماء الأعمدة من النموذج.")
            model_columns = []

        # مقارنة الأعمدة
        sensor_columns = df_sensor.columns.tolist()
        missing_in_sensor = [col for col in model_columns if col not in sensor_columns]
        extra_in_sensor = [col for col in sensor_columns if col not in model_columns]

        st.subheader("📌 مقارنة الأعمدة:")

        if not missing_in_sensor and not extra_in_sensor:
            st.success("✅ الأعمدة متطابقة مع النموذج المدرب.")
        else:
            if missing_in_sensor:
                st.error("❌ الأعمدة التالية مفقودة في ملف الحساسات:")
                st.write(missing_in_sensor)

            if extra_in_sensor:
                st.warning("⚠️ الأعمدة التالية زائدة في ملف الحساسات:")
                st.write(extra_in_sensor)

        # عرض الملف
        with st.expander("📄 عرض البيانات المحمّلة"):
            st.dataframe(df_sensor)

        # تصدير الملف المعدل إن أردت (نفسه هنا بدون تعديل فعلي)
        if st.button("📥 تحميل نسخة من الملف"):
            st.download_button(
                label="⬇️ اضغط لتحميل الملف",
                data=df_sensor.to_csv(index=False).encode('utf-8'),
                file_name="formatted_sensor.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"❌ حصل خطأ أثناء تحميل النموذج أو البيانات: {e}")
else:
    st.info("⬆️ من فضلك ارفع ملف الحساسات وملف النموذج المدرب أولاً.")