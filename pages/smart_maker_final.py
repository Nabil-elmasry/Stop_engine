import streamlit as st
import pandas as pd
from io import BytesIO

# تحميل الملف المرجعي (اللي اتدرب عليه النموذج)
@st.cache_data
def load_reference_file():
    ref = pd.read_csv("reference_dataset.csv")  # عدّل المسار حسب مكان الملف المرجعي
    return ref[['Sensor Name', 'Unit']]

# معالجة الملف الجديد
def process_file(uploaded_file, reference_units):
    df = pd.read_csv(uploaded_file)

    # حذف الأعمدة الغير مطلوبة زي volume لو مش موجودة في المرجع
    allowed_sensors = reference_units['Sensor Name'].tolist()
    df = df[df['Sensor Name'].isin(allowed_sensors)]

    # ملء الوحدات المفقودة من المرجع
    df = df.merge(reference_units, on='Sensor Name', how='left', suffixes=('', '_ref'))
    df['Unit'] = df['Unit'].fillna(df['Unit_ref'])
    df.drop(columns=['Unit_ref'], inplace=True)

    return df

# لتحميل الملف بعد المعالجة
def generate_download_link(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()

# واجهة ستريمليت
st.title("📊 Smart Maker Final - تنسيق ملف الحساسات")

uploaded_file = st.file_uploader("📁 اختر ملف الحساسات لتحويله", type=["csv"])

if uploaded_file:
    reference_units = load_reference_file()
    df_processed = process_file(uploaded_file, reference_units)

    st.success("✅ تم تحويل الملف بنجاح!")
    st.dataframe(df_processed.head())

    st.download_button(
        label="⬇️ تحميل الملف بعد المعالجة",
        data=generate_download_link(df_processed),
        file_name="sensor_data_final.csv",
        mime="text/csv"
    )