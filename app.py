# stop_engine/app.py

import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="تشخيص الأعطال", layout="wide")

# ✅ تصميم العنوان
st.markdown("""
    <div style="text-align:center; padding: 30px; background: linear-gradient(to right, #f8cdda, #1fc8db); border-radius: 15px;">
        <h1 style="color:#4B0082;">System Check by AI 💪</h1>
        <h3 style="color:#2f2f2f;">اختر الصفحة التي تريد الانتقال إليها من القائمة الجانبية</h3>
    </div>
""", unsafe_allow_html=True)

# ✅ القائمة الجانبية
st.sidebar.title("📂 الصفحات المتاحة")

# ✅ روابط الصفحات (استخدم المسارات الصحيحة)
st.sidebar.page_link("pages/landing.py", label="🏁 الصفحة الافتتاحية", icon="🏁")
st.sidebar.page_link("pages/training/train_Ai.py", label="🧠 تدريب النموذج", icon="🧠")
st.sidebar.page_link("pages/deviation_check/detect_deviation.py", label="📉 تحليل الانحراف", icon="📉")
st.sidebar.page_link("pages/reports/final_report.py", label="📄 التقرير النهائي", icon="📄")

# ✅ توقيع أسفل الصفحة
st.markdown("""
    <br><hr style="border-top: 1px solid #bbb;">
    <div style="text-align:center; font-size:18px; color:#FF1493;">
        تنفيذ: Eng. Nabil Elmasry | 🚗 Powered by StopEngine AI
    </div>
""", unsafe_allow_html=True)