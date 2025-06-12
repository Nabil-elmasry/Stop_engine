# pages/clean_and_merge.py

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="🧹 تنظيف وتجميع الملفات", layout="wide")
st.title("🧹 تنظيف وتجميع ملفات الحساسات")

folder_path = "data/extracted_files"
output_file = "data/merged_clean_sensors.csv"

if not os.path.exists(folder_path):
    st.warning("⚠️ لا يوجد ملفات داخل المجلد data/extracted_files. ارفع ZIP أولاً.")
else:
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    if not csv_files:
        st.warning("⚠️ لا يوجد ملفات CSV في المجلد.")
    else:
        dfs = []
        for file in csv_files:
            try:
                df = pd.read_csv(os.path.join(folder_path, file))
                df.dropna(axis=1, how='all', inplace=True)  # حذف الأعمدة الفارغة
                dfs.append(df)
            except Exception as e:
                st.error(f"❌ خطأ في الملف: {file} — {e}")

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            combined_df.to_csv(output_file, index=False)
            st.success(f"✅ تم دمج {len(dfs)} ملف بنجاح")
            st.write(combined_df.head())

            with open(output_file, "rb") as f:
                st.download_button("⬇️ تحميل الملف المدمج", f, file_name="merged_clean_sensors.csv")