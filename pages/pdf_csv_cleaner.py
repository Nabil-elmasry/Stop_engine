# pages/pdf_to_csv_cleaner.py

import streamlit as st
import pandas as pd
import os
import base64
import tabula
from PyPDF2 import PdfReader

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV نظيف", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
### 📌 خطوات الاستخدام:
1. ارفع ملف PDF يحتوي على قراءات الحساسات (من جهاز Lunch مثلاً).
2. سيتم استخراج وتنظيف البيانات وتحويلها إلى CSV.
3. يمكنك تحميل الملف النهائي واستخدامه في صفحة كشف الأعطال.

💡 يدعم ملفات PDF المحتوية على جداول متعددة أو صفحة واحدة.
""")

# رفع ملف PDF
uploaded_pdf = st.file_uploader("📄 ارفع ملف PDF", type=["pdf"])

if uploaded_pdf:
    pdf_path = "data/temp_sensors.pdf"
    os.makedirs("data", exist_ok=True)
    
    # حفظ الملف المرفوع
    with open(pdf_path, "wb") as f:
        f.write(uploaded_pdf.read())

    st.success("✅ تم رفع الملف بنجاح. جاري المعالجة...")

    try:
        # استخراج الجداول باستخدام tabula (يتطلب Java مثبت)
        dfs = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)

        if dfs and len(dfs) > 0:
            combined_df = pd.concat(dfs, ignore_index=True)
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
            st.warning("⚠️ لم يتم العثور على أي جداول داخل الملف PDF.")
    except Exception as e:
        st.error("❌ فشل في تحويل PDF إلى CSV")
        st.exception(e)
else:
    st.info("📂 من فضلك ارفع ملف PDF للبدء.")