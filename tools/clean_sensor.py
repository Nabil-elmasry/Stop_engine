
import streamlit as st
import pandas as pd

st.set_page_config(page_title="تنظيف وتحميل بيانات الحساسات", layout="wide")
st.title("تنظيف وتحميل بيانات الحساسات - Sensor Data Cleaning")

# رفع ملف الحساسات
uploaded_file = st.file_uploader("ارفع ملف الحساسات (CSV)", type=["csv"])

if uploaded_file is not None:
    # قراءة البيانات
    df = pd.read_csv(uploaded_file)

    st.subheader("عرض البيانات الأصلية")
    st.dataframe(df)

    # تنظيف الأعمدة (إزالة الفراغات والمسافات)
    df.columns = df.columns.str.strip()

    # إزالة الصفوف الفارغة إن وجدت
    df.dropna(how="all", inplace=True)

    # إزالة الأعمدة الفارغة إن وجدت
    df.dropna(axis=1, how="all", inplace=True)

    # عرض البيانات بعد التنظيف
    st.subheader("عرض البيانات بعد التنظيف")
    st.dataframe(df)

    # تحويل الداتا إلى CSV وتحميلها إجباري
    csv = df.to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        label="اضغط هنا لتحميل ملف الحساسات بعد التنظيف (CSV)",
        data=csv,
        file_name='Cleaned_Sensor.csv',
        mime='text/csv'
    )

else:
    st.info("برجاء رفع ملف الحساسات للبدء في التنظيف.")

