train_modelv2.py

import streamlit as st import pandas as pd import base64 from sklearn.model_selection import train_test_split from sklearn.ensemble import RandomForestClassifier from sklearn.metrics import classification_report

إعداد الصفحة

st.set_page_config(page_title="تدريب النموذج - الإصدار 2", layout="wide") st.title("✨ 🛠️ صفحة تدريب النموذج الإصدار الثاني")

دالة لتحويل DataFrame إلى رابط تحميل

def convert_df_to_download_link(df, filename): csv = df.to_csv(index=False) b64 = base64.b64encode(csv.encode()).decode() href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">⬇️ اضغط هنا لتحميل الملف: {filename}</a>' return href

---------------------------- 1 -----------------------------

st.subheader("1️⃣ رفع ملفات البيانات الأصلية (قبل إضافة record_id)") sensor_file = st.file_uploader("ارفع ملف الحساسات الأصلي", type="csv", key="sensor") carset_file = st.file_uploader("ارفع ملف الأعطال الأصلي", type="csv", key="carset")

if sensor_file and carset_file: sensor_df = pd.read_csv(sensor_file) carset_df = pd.read_csv(carset_file) st.success("✅ تم رفع الملفين بنجاح") st.write("معاينة ملف الحساسات:") st.dataframe(sensor_df.head()) st.write("معاينة ملف الأعطال:") st.dataframe(carset_df.head())

if st.button("➕ أضف عمود record_id تلقائيًا"):
    sensor_df["record_id"] = range(1, len(sensor_df) + 1)
    carset_df["record_id"] = range(1, len(carset_df) + 1)
    st.success("✅ تم إضافة عمود record_id")

    st.markdown("### 📥 روابط تحميل الملفات بعد التعديل")
    st.markdown(convert_df_to_download_link(sensor_df, "sensor_with_id_v2.csv"), unsafe_allow_html=True)
    st.markdown(convert_df_to_download_link(carset_df, "carset_with_id_v2.csv"), unsafe_allow_html=True)

---------------------------- 2 -----------------------------

st.markdown("---") st.subheader("2️⃣ رفع الملفات المعدّلة (بعد إضافة record_id) للدمج")

sensor_with_id = st.file_uploader("ارفع ملف الحساسات المعدل", type="csv", key="sensor_id") carset_with_id = st.file_uploader("ارفع ملف الأعطال المعدل", type="csv", key="carset_id")

if sensor_with_id and carset_with_id: sensor_id_df = pd.read_csv(sensor_with_id) carset_id_df = pd.read_csv(carset_with_id)

if st.button("🔗 دمج الملفين بناءً على record_id"):
    try:
        merged_df = pd.merge(sensor_id_df, carset_id_df, on="record_id", how="inner")
        st.success("✅ تم الدمج بنجاح")
        st.write("معاينة البيانات بعد الدمج:")
        st.dataframe(merged_df.head())

        st.markdown("### 📥 رابط تحميل ملف الدمج:")
        st.markdown(convert_df_to_download_link(merged_df, "merged_data_v2.csv"), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء الدمج: {e}")

---------------------------- 3 -----------------------------

st.markdown("---") st.subheader("3️⃣ رفع ملف الدمج للتدريب")

merged_upload = st.file_uploader("ارفع ملف الدمج النهائي للتدريب", type="csv", key="merged")

if merged_upload: merged_df = pd.read_csv(merged_upload) st.success("✅ تم رفع ملف الدمج بنجاح") st.write("معاينة ملف الدمج:") st.dataframe(merged_df.head())

st.subheader("4️⃣ ابدأ التدريب على البيانات")
if st.button("🚀 ابدأ التدريب"):
    try:
        X = merged_df.drop(columns=["fault_code", "record_id"], errors='ignore')
        y = merged_df["fault_code"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred)

        st.success("✅ تم التدريب بنجاح")
        st.text("نتائج التقييم:")
        st.code(report)

        st.markdown("### 📥 رابط تحميل نتائج التقييم:")
        report_bytes = report.encode()
        b64_report = base64.b64encode(report_bytes).decode()
        href = f'<a href="data:file/txt;base64,{b64_report}" download="model_results_v2.txt">⬇️ اضغط هنا لتحميل تقرير التقييم</a>'
        st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء التدريب: {e}")

