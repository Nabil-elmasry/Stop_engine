import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Smart Maker Final", layout="wide")

st.title("🔧 Smart Maker Final – تحويل فورمات ملفات الحساسات")

uploaded_file = st.file_uploader("📂 حمّل ملف الحساسات بأي فورمات", type=["csv", "xlsx"])

if uploaded_file:
   # قراءة الملف بناءً على النوع
    if uploaded_file.name.endswith(".csv"):
        df_raw = pd.read_csv(uploaded_file)
    else:
        df_raw = pd.read_excel(uploaded_file)

    st.subheader("📄 عرض البيانات الأصلية")
    st.dataframe(df_raw, use_container_width=True)

    # المعالجة الأساسية (مثال بسيط قابل للتعديل حسب النموذج المدرب)
    try:
        df_processed = df_raw.copy()

        # إعادة تسمية الأعمدة إن أمكن (تأكد من أسماء أعمدتك الحقيقية)
        if "Sensor Name" in df_processed.columns:
            df_processed.rename(columns={"Sensor Name": "Sensor", "Value": "Reading"}, inplace=True)

        # إزالة الأعمدة غير المفيدة للنموذج (مثال فقط)
        columns_to_keep = ["Sensor", "Reading"]
        df_processed = df_processed[[col for col in columns_to_keep if col in df_processed.columns]]

        st.subheader("✅ البيانات بعد المعالجة (جاهزة للنموذج)")
        st.dataframe(df_processed, use_container_width=True)

        # إعداد الملف للتحميل
        def convert_df_to_csv(df):
            output = BytesIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return output

        csv_data = convert_df_to_csv(df_processed)

        st.download_button(
            label="⬇️ تحميل الملف المعالج",
            data=csv_data,
            file_name="converted_sensors.csv",
            mime="text/csv",
            use_container_width=True
        )

    except Exception as e:
        st.error(f"حدث خطأ أثناء المعالجة: {e}")