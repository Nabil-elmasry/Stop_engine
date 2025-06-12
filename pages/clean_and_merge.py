import streamlit as st
import zipfile
import os
import pandas as pd
import base64

st.set_page_config(page_title="🧹 تنظيف وتجميع البيانات", layout="wide")
st.title("🧹 تنظيف وتجميع ملفات الحساسات")

upload_folder = "data"
os.makedirs(upload_folder, exist_ok=True)

# 1️⃣ رفع ملف ZIP
zip_file = st.file_uploader("📦 ارفع ملف ZIP الذي يحتوي على ملفات CSV", type="zip")

# 2️⃣ استخراج الملفات داخل data مباشرة
if zip_file:
    try:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            zf.extractall(upload_folder)
        st.success("✅ تم استخراج الملفات داخل مجلد data بنجاح.")
    except Exception as e:
        st.error(f"❌ خطأ أثناء فك الضغط: {e}")

# 3️⃣ جمع كل ملفات CSV الموجودة في مجلد data
csv_files = [f for f in os.listdir(upload_folder) if f.endswith(".csv")]

if not csv_files:
    st.warning("⚠️ لا يوجد ملفات CSV داخل مجلد data. تأكد من رفع ZIP يحتوي على ملفات CSV.")
else:
    st.info(f"📄 تم العثور على {len(csv_files)} ملف CSV داخل data.")

    if st.button("🔄 دمج وتنظيف الملفات"):
        try:
            all_dfs = [pd.read_csv(os.path.join(upload_folder, f)) for f in csv_files]
            merged_df = pd.concat(all_dfs, ignore_index=True)
            st.success("✅ تم دمج جميع الملفات بنجاح.")
            st.dataframe(merged_df.head())

            # حفظ الملف داخل data
            output_path = os.path.join(upload_folder, "merged_clean.csv")
            merged_df.to_csv(output_path, index=False)

            # رابط التحميل
            with open(output_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="merged_clean.csv">⬇️ اضغط هنا لتحميل الملف المدمج</a>'
                st.markdown("### 💾 تحميل الملف المدمج:")
                st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ فشل الدمج: {e}")