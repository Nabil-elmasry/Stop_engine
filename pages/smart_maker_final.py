# pages/smart_maker_final.py

import streamlit as st
import pandas as pd
import joblib
import os

# تحميل تنسيق الواجهة
from tools.auto_theme_injector import apply_custom_theme
apply_custom_theme()

# عنوان الصفحة
st.title("🔧 تنسيق ملف الحساسات - Smart Maker Final")

# تحميل النموذج المدرب
MODEL_PATH = "modules/trained_model.pkl"
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    st.success("✅ تم تحميل النموذج المدرب بنجاح.")
else:
    st.error(f"❌ لم يتم العثور على النموذج في المسار: {MODEL_PATH}")

# تحميل ملف الحساسات
uploaded_file = st.file_uploader("📂 اختر ملف الحساسات (CSV)", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("📊 عرض أولي للبيانات الأصلية")
        st.dataframe(df.head())

        # التأكد من وجود نفس أعمدة النموذج
        if model and hasattr(model, 'feature_names_in_'):
            expected_columns = list(model.feature_names_in_)
            st.info(f"📋 الأعمدة المطلوبة بواسطة النموذج: {expected_columns}")

            # الاحتفاظ فقط بالأعمدة المطلوبة
            formatted_df = df.copy()
            formatted_df = formatted_df.loc[:, formatted_df.columns.isin(expected_columns)]

            # التحقق من وجود كل الأعمدة
            missing_cols = set(expected_columns) - set(formatted_df.columns)
            for col in missing_cols:
                formatted_df[col] = 0.0  # ملء القيم الناقصة بصفر

            # إعادة ترتيب الأعمدة
            formatted_df = formatted_df[expected_columns]

            st.subheader("📁 البيانات بعد التنسيق")
            st.dataframe(formatted_df.head())

            # تحميل الملف المنسق
            csv_download = formatted_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ تحميل الملف المنسق",
                data=csv_download,
                file_name="formatted_sensors.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ النموذج لا يحتوي على معلومات الأعمدة أو لم يتم تحميله.")
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")