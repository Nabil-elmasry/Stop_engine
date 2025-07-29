import streamlit as st
import pandas as pd
import pickle
import os

# واجهة الصفحة
st.set_page_config(page_title="Smart Maker Final", layout="wide")
st.title("📊 Smart Maker Final")
st.write("قم برفع ملف الحساسات + ملف النموذج المدرب (.pkl)")

# رفع ملف الحساسات
sensor_file = st.file_uploader("📁 ارفع ملف الحساسات (CSV)", type=["csv"])

# رفع ملف النموذج المدرب
model_file = st.file_uploader("🤖 ارفع ملف النموذج المدرب (.pkl)", type=["pkl"])

if sensor_file and model_file:
    try:
        # تحميل النموذج من الملف المرفوع
        model = pickle.load(model_file)

        # قراءة ملف الحساسات
        sensor_df = pd.read_csv(sensor_file)

        # عرض البيانات
        st.success("✅ تم تحميل النموذج والبيانات بنجاح")
        st.subheader("بيانات الحساسات:")
        st.dataframe(sensor_df.head())

        # (اختياري) تنفيذ أي مقارنة أو تنسيق حسب مشروعك
        # ...

    except Exception as e:
        st.error(f"❌ حصل خطأ أثناء تحميل النموذج أو البيانات: {e}")

elif sensor_file and not model_file:
    st.warning("⚠️ من فضلك ارفع ملف النموذج المدرب (.pkl)")
elif model_file and not sensor_file:
    st.warning("⚠️ من فضلك ارفع ملف الحساسات (CSV)")