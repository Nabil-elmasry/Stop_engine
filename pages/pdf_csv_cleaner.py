# pages/pdf_csv_cleaner.py

import streamlit as st
import pandas as pd
import os
import base64
import pdfplumber

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV نظيف", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
### 📌 خطوات الاستخدام:
1. ارفع ملف PDF يحتوي على قراءات الحساسات (من جهاز Lunch مثلاً).
2. سيتم استخراج وتنظيف البيانات وتحويلها إلى CSV.
3. يمكنك تحميل الملف النهائي واستخدامه في صفحة كشف الأعطال.

💡 يدعم ملفات PDF المحتوية على جداول واضحة ومنسقة.
""")

# رفع ملف PDF
uploaded_pdf = st.file_uploader("📄 ارفع ملف PDF", type=["pdf"])

if uploaded_pdf:
    pdf_path = "data/temp_sensors.pdf"
    os.makedirs("data", exist_ok=True)

    # حفظ الملف المؤقت
    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.read())

    st.success("✅ تم رفع الملف بنجاح. جاري المعالجة...")

    try:
        extracted_tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                table = page.extract_table()
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    extracted_tables.append(df)

        if extracted_tables:
            combined_df = pd.concat(extracted_tables, ignore_index=True)
            combined_df.dropna(axis=1, how='all', inplace=True)
            combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

            output_path = "data/converted_clean.csv"
            combined_df.to_csv(output_path, index=False)

            st.success(f"✅ تم استخراج وتنظيف البيانات - عدد الصفوف: {len(combined_df)}")
            st.write("📋 عرض أول 5 صفوف:")
            st.dataframe(combined_df.head())

            with open(output_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="converted_clean.csv">⬇️ اضغط لتحميل الملف CSV على الموبايل</a>'
                st.markdown("### 📥 تحميل الملف")
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("⚠️ لم يتم العثور على جداول واضحة داخل الملف.")
    except Exception as e:
        st.error("❌ حدث خطأ أثناء استخراج البيانات من PDF")
        st.exception(e)
else:
    st.info("📂 من فضلك ارفع ملف PDF للبدء.")