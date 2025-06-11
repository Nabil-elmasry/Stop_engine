# app.py

import streamlit as st

# إعداد واجهة الصفحة
st.set_page_config(page_title="تشخيص الأعطال", layout="wide")

# ======= تصميم العنوان الرئيسي =======
st.markdown("""
    <div style="text-align:center; padding: 30px; background: linear-gradient(to right, #f8cdda, #1fc8db); border-radius: 15px;">
        <h1 style="color:#4B0082;">System Check by AI 💪</h1>
        <h3 style="color:#2f2f2f;">اختر الصفحة التي تريد الانتقال إليها من القائمة الجانبية</h3>
    </div>
""", unsafe_allow_html=True)

# ======= القائمة الجانبية =======
st.sidebar.title("🧭 قائمة التنقل")

# ✅ روابط الصفحات (بعد مسح المجلدات الفرعية)
st.sidebar.page_link("pages/landing.py", label="🏁 الصفحة الافتتاحية", icon="🏁")
st.sidebar.page_link("pages/train_ai.py", label="🧠 تدريب النموذج", icon="🧠")
st.sidebar.page_link("pages/detect_deviation.py", label="📉 تحليل الانحراف", icon="📉")
st.sidebar.page_link("pages/final_report.py", label="📄 التقرير النهائي", icon="📄")
st.sidebar.page_link("pages/cleanup.py", label="🧹 تنظيف المشروع", icon="🧹")
st.sidebar.page_link("pages/zip_uploader.py", label="🗜️ رفع ملفات ZIP", icon="🗜️")

# ======= توقيع أسفل الصفحة =======
st.markdown("""
    <br><hr style="border-top: 1px solid #bbb;">
    <div style="text-align:center; font-size:18px; color:#FF1493;">
        تنفيذ: Eng. Nabil Elmasry &nbsp; | &nbsp; Powered by AI
    </div>
""", unsafe_allow_html=True)