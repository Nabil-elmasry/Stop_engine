# pages/clean_and_merge.py
import streamlit as st
import pandas as pd
import os
import glob
import base64

st.set_page_config(page_title="🧹 دمج وتنظيف ملفات الحساسات", layout="wide")
st.title("🧹 تنظيف وتجميع ملفات الحساسات")

st.markdown("""
### 📂 خطوات العمل:
1. ارفع ملفاتك من صفحة ZIP.
2. سيتم دمج وتنظيف كل الملفات داخل مجلد `data/extracted_files/`.
3. حمل الناتج على هيئة ملف واحد جاهز للتدريب.
""")

folder_path = "data/extracted_files/"
if not os.path.exists(folder_path):
    st.warning("⚠️ لا يوجد ملفات داخل المجلد data/extracted_files. ارفع ZIP أولاً.")
else:
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csv_files:
        st.warning("⚠️ لم يتم العثور على ملفات CSV داخل المجلد.")
    else:
        st.markdown(f"🔍 عدد الملفات الموجودة: **{len(csv_files)}**")
        dfs = []
        total_rows = 0
        for i, file in enumerate(csv_files):
            try:
                df = pd.read_csv(file)
                dfs.append(df)
                total_rows += len(df)
                if i < 3:
                    st.success(f"📄 ملف {os.path.basename(file)} تم تحميله - {len(df)} صف")
            except Exception as e:
                st.error(f"❌ خطأ في قراءة الملف {file}: {e}")

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            combined_df.dropna(axis=1, how='all', inplace=True)
            combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]
            
            # حفظ الملف النهائي
            os.makedirs("data", exist_ok=True)
            output_path = "data/merged_clean.csv"
            combined_df.to_csv(output_path, index=False)

            st.success(f"✅ تم الدمج والتنظيف بنجاح - عدد الصفوف: {len(combined_df)}")
            st.write("📋 عرض أول 5 صفوف من الملف:")
            st.dataframe(combined_df.head())

            # رابط التحميل
            with open(output_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="merged_clean.csv">⬇️ اضغط لتحميل الملف المدمج</a>'
                st.markdown("### 📥 تحميل الملف النهائي")
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.error("❌ لا توجد ملفات صالحة للدمج.")