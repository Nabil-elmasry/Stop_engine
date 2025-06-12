# pages/clean_and_merge.py

import streamlit as st
import pandas as pd
import os
import glob
import base64

st.set_page_config(page_title="🧹 دمج وتنظيف ملفات الحساسات", layout="wide")
st.title("🧹 تنظيف وتجميع ملفات الحساسات")

# تعليمات
st.markdown("""
### 📂 خطوات العمل:
1. ارفع ملفات CSV الخاصة بقراءات الحساسات (تدعم رفع عدة ملفات دفعة واحدة).
2. سيتم دمج الملفات وتنظيف الأعمدة الفارغة والمتكررة.
3. يمكنك تحميل الملف المدمج على موبايلك لاستخدامه في التدريب.
""")

# رفع الملفات
uploaded_files = st.file_uploader("📤 ارفع ملفات الحساسات (CSV)", type="csv", accept_multiple_files=True)

if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        try:
            df = pd.read_csv(uploaded_file)
            dfs.append(df)
            st.success(f"✅ تم تحميل: {uploaded_file.name}")
        except Exception as e:
            st.error(f"❌ خطأ في قراءة الملف {uploaded_file.name}: {e}")

    if dfs:
        # دمج وتنظيف
        combined_df = pd.concat(dfs, ignore_index=True)
        combined_df.dropna(axis=1, how='all', inplace=True)  # حذف الأعمدة الفارغة تماماً
        combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]  # حذف الأعمدة المكررة

        # حفظ داخل مجلد data/
        os.makedirs("data", exist_ok=True)
        merged_path = "data/merged_clean.csv"
        combined_df.to_csv(merged_path, index=False)

        st.success("✅ تم دمج وتنظيف البيانات وحفظها في data/merged_clean.csv")
        st.dataframe(combined_df.head())

        # زر تحميل الملف
        with open(merged_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="merged_clean.csv">⬇️ اضغط هنا لتحميل الملف المدمج على موبايلك</a>'
            st.markdown("### 📥 تحميل الملف بعد الدمج")
            st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("⚠️ لم يتم تحميل أي ملف صالح بعد.")
else:
    st.info("📌 الرجاء رفع ملفات CSV الخاصة بقراءات الحساسات للبدء.")