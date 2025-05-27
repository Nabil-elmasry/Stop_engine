# Stop_engine/app.py

import streamlit as st

st.set_page_config(page_title="تشخيص الأعطال", layout="wide")

# ======= واجهة العنوان الرئيسية =======
st.markdown("""
    <div style="text-align:center; padding: 30px; background: linear-gradient(to right, #f8cdda, #1fc8db); border-radius: 15px;">
        <h1 style="color:#4B0082;">System Check by AI 💪</h1>
        <h3 style="color:#2f2f2f;">اختر الصفحة التي تريد الانتقال إليها من القائمة الجانبية</h3>
    </div>
""", unsafe_allow_html=True)

# ======= القائمة الجانبية =======
st.sidebar.title("قائمة التنقل")
st.sidebar.page_link("Pages/0_🏠_Landing/landing.py", label="الصفحة الافتتاحية", icon="🏁")
st.sidebar.page_link("Pages/1_🧠_Training/train_Ai_V3.py", label="🧠 تدريب النموذج", icon="🧠")
st.sidebar.page_link("Pages/2_📉_Deviation_Check/detect_deviation.py", label="📉 تحليل الانحراف", icon="📉")
st.sidebar.page_link("Pages/3_📄_Reports/generate_report.py", label="📄 توليد التقارير", icon="📄")
st.sidebar.page_link("Pages/4_🧰_Tools/cleanup.py", label="🧹 تنظيف المشروع", icon="🧹")
st.sidebar.page_link("Pages/4_🧰_Tools/zip_uploader.py", label="🗜️ رفع ملفات ZIP", icon="🗜️")

# ======= توقيع أسفل الصفحة =======
st.markdown("""
    <br><hr style="border-top: 1px solid #bbb;">
    <div style="text-align:center; font-size:18px; color:#FF1493;">
        تنفيذ: Eng. Nabil Elmasry &nbsp; | &nbsp; Powered by AI
    </div>
""", unsafe_allow_html=True)