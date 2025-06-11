# StopEngine/app.py

import streamlit as st

# إعداد الصفحة الرئيسية
st.set_page_config(page_title="تشخيص الأعطال", layout="wide")

# ======= واجهة العنوان الرئيسية =======
st.markdown("""
    <div style="text-align:center; padding: 30px; background: linear-gradient(to right, #f8cdda, #1fc8db); border-radius: 15px;">
        <h1 style="color:#4B0082;">System Check by AI 💪</h1>
        <h3 style="color:#2f2f2f;">اختر الصفحة التي تريد الانتقال إليها من القائمة الجانبية</h3>
    </div>
""", unsafe_allow_html=True)

# ======= القائمة الجانبية =======
st.sidebar.title("📂 قائمة التنقل")

st.sidebar.page_link("landing/landing.py", label="🏁 الصفحة الافتتاحية", icon="🏁")
st.sidebar.page_link("training/train_Ai_V3.py", label="🧠 تدريب النموذج", icon="🧠")
st.sidebar.page_link("deviation_check/detect_deviation.py", label="📉 تحليل الانحراف", icon="📉")
st.sidebar.page_link("reports/generate_report.py", label="📄 توليد التقارير", icon="📄")
st.sidebar.page_link("tools/cleanup.py", label="🧹 تنظيف المشروع", icon="🧹")
st.sidebar.page_link("tools/zip_uploader.py", label="🗜️ رفع ملفات ZIP", icon="🗜️")

# ======= التوقيع السفلي =======
st.markdown("""
    <br><hr style="border-top: 1px solid #bbb;">
    <div style="text-align:center; font-size:18px; color:#FF1493;">
        تنفيذ: Eng. Nabil Elmasry &nbsp; | &nbsp; Powered by AI
    </div>
""", unsafe_allow_html=True)