import streamlit as st
import pandas as pd
import os
import pickle

# تنسيق الواجهة حسب التنسيق المخصص
from tools.auto_theme_injector import apply_custom_theme
apply_custom_theme()

st.title("🚗 Smart Maker Final - Format Sensor Data for AI Model")

uploaded_file = st.file_uploader("📤 ارفع ملف الحساسات الخام", type=["csv", "txt"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("📄 البيانات الأصلية:")
        st.dataframe(df.head())

        # الاحتفاظ بالقيم كما هي + الاحتفاظ بـ Unit و Volume
        required_columns = ['Sensor Name', 'Value', 'Unit', 'Volume']
        df_cleaned = df[[col for col in required_columns if col in df.columns]]

        if df_cleaned.empty:
            st.error("❌ الملف لا يحتوي على الأعمدة المطلوبة.")
        else:
            # تحميل النموذج للتأكد من مطابقة الأعمدة فقط
            model_path = "modules/trained_model.pkl"
            if os.path.exists(model_path):
                with open(model_path, "rb") as f:
                    model = pickle.load(f)
                st.success("✅ النموذج تم تحميله بنجاح.")

                # افترضنا أن الأعمدة المطلوبة من النموذج هي أسماء الحساسات فقط
                expected_sensors = model.feature_names_in_

                df_filtered = df_cleaned[df_cleaned['Sensor Name'].isin(expected_sensors)]

                pivot_df = df_filtered.pivot_table(index=None, 
                                                   columns='Sensor Name', 
                                                   values='Value', 
                                                   aggfunc='first')

                st.subheader("📊 البيانات بعد التجهيز:")
                st.dataframe(pivot_df)

                # حفظ الملف الناتج
                pivot_df.to_csv("final_sensor_data.csv", index=False)
                st.success("✅ تم تجهيز الملف بنجاح وحفظه باسم `final_sensor_data.csv`")
                st.download_button("📥 تحميل الملف", data=pivot_df.to_csv(index=False), file_name="final_sensor_data.csv", mime="text/csv")
            else:
                st.warning("⚠️ لم يتم العثور على نموذج مدرب داخل 'modules/trained_model.pkl'. يرجى التأكد من وجود الملف.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
else:
    st.info("👆 من فضلك ارفع ملف الحساسات لتجهيزه.")