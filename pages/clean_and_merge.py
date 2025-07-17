
import streamlit as st
import pandas as pd
import os
import glob
import base64

st.set_page_config(page_title="🧹 دمج وتنظيف ملفات الحساسات", layout="wide")
st.title("🧹 تنظيف وتجميع ملفات الحساسات")

st.markdown("""
### 📂 خطوات العمل:
يمكنك اختيار إحدى الطريقتين:
- ✅ استخدام الملفات المفكوكة تلقائيًا من ملف ZIP (الموجودة في `data/extracted_files/`)
- 📥 أو رفع ملفات CSV يدويًا هنا في حالة وجود مشكلة في صفحة ZIP
""")

# ✅ اختيار طريقة الإدخال
method = st.radio("اختر طريقة رفع الملفات:", ["📁 من مجلد ZIP المفكوك", "📤 رفع ملفات CSV يدويًا"])

dfs = []
total_rows = 0

if method == "📁 من مجلد ZIP المفكوك":
    folder_path = "data/extracted_files/"
    if not os.path.exists(folder_path):
        st.warning("⚠️ لا يوجد مجلد data/extracted_files. ارفع ZIP أولاً.")
    else:
        csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
        if not csv_files:
            st.warning("⚠️ لا يوجد ملفات CSV داخل المجلد.")
        else:
            st.markdown(f"🔍 عدد الملفات الموجودة: **{len(csv_files)}**")
            for i, file in enumerate(csv_files):
                try:
                    df = pd.read_csv(file)
                    dfs.append(df)
                    total_rows += len(df)
                    if i < 3:
                        st.success(f"📄 {os.path.basename(file)} - عدد الصفوف: {len(df)}")
                except Exception as e:
                    st.error(f"❌ خطأ في قراءة {file}: {e}")

elif method == "📤 رفع ملفات CSV يدويًا":
    uploaded_files = st.file_uploader("ارفع ملفات CSV", type="csv", accept_multiple_files=True)
    if uploaded_files:
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                df = pd.read_csv(uploaded_file)
                dfs.append(df)
                total_rows += len(df)
                if i < 3:
                    st.success(f"📄 {uploaded_file.name} - عدد الصفوف: {len(df)}")
            except Exception as e:
                st.error(f"❌ خطأ في قراءة {uploaded_file.name}: {e}")
    else:
        st.info("📂 لم يتم رفع أي ملفات بعد.")

# ✅ مرحلة الدمج والتنظيف
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.dropna(axis=1, how='all', inplace=True)
    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]

    os.makedirs("data", exist_ok=True)
    output_path = "data/merged_clean.csv"
    combined_df.to_csv(output_path, index=False)

    st.success(f"✅ تم الدمج والتنظيف - عدد الصفوف النهائية: {len(combined_df)}")
    st.write("📋 عرض أول 5 صفوف:")
    st.dataframe(combined_df.head())

    with open(output_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="merged_clean.csv">⬇️ اضغط لتحميل الملف المدمج</a>'
        st.markdown("### 📥 تحميل الملف")
        st.markdown(href, unsafe_allow_html=True)
else:
    st.warning("⚠️ لم يتم دمج أي بيانات بعد.")