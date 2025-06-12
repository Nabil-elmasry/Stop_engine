# pages/upload_zip_files.py

import streamlit as st
import zipfile
import os
import pandas as pd

st.set_page_config(page_title="📦 رفع وتحضير ملفات ZIP", layout="wide")
st.title("📦 رفع وتجميع ملفات حساسات من ZIP")

uploaded_zip = st.file_uploader("📁 ارفع ملف مضغوط يحتوي على ملفات CSV", type=["zip"])

if uploaded_zip:
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        extract_dir = "data/extracted_files"
        os.makedirs(extract_dir, exist_ok=True)
        zip_ref.extractall(extract_dir)

    st.success("✅ تم فك الضغط بنجاح")
    
    csv_files = [f for f in os.listdir(extract_dir) if f.endswith(".csv")]
    if not csv_files:
        st.warning("⚠️ لم يتم العثور على ملفات CSV داخل الملف المضغوط.")
    else:
        st.markdown(f"### 🗂️ عدد الملفات المستخرجة: {len(csv_files)}")
        st.code("\n".join(csv_files[:10]), language="text")