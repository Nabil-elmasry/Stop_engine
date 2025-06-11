
import streamlit as st
import os

st.set_page_config(page_title="📋 التقرير النهائي", layout="wide")
st.title("📋 التقرير النهائي لنتائج التحليل")

st.markdown("""
### 📂 تحميل التقرير الفني الأخير
""")

report_path = "log/fault_report.txt"  # تأكد إنه بيُحفظ هنا من صفحة التنبؤ

if os.path.exists(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    st.text_area("📄 محتوى التقرير:", report_text, height=400)

    # ✅ رابط تحميل مباشر
    st.download_button(
        label="📥 تحميل التقرير",
        data=report_text,
        file_name="fault_report.txt",
        mime="text/plain"
    )
else:
    st.warning("⚠️ لم يتم العثور على التقرير بعد. يرجى تنفيذ كشف الانحراف أولاً.")

# ✅ يمكنك لاحقًا إضافة زر لتحويله إلى PDF أو عرضه بشكل رسومي

