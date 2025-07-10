import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="تشخيص الأعطال",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ======= عرض اللوجو =======
logo_path = "assets/logo1.png"
logo = Image.open(logo_path)
st.image(logo, width=180)

# ======= العنوان =======
st.markdown("""
    <div style="text-align:center; padding: 30px; background: linear-gradient(to right, #f8cdda, #1fc8db); border-radius: 15px;">
        <h1 style="color:#4B0082;">System Check by AI 💪</h1>
        <h3 style="color:#2f2f2f;">اختر الصفحة التي تريد الانتقال إليها من القائمة الجانبية</h3>
    </div>
""", unsafe_allow_html=True)

# ======= نبذة مختصرة مع أيقونات جذابة =======
st.markdown("### 🚀 نظرة سريعة على المشروع")
st.info("📘 StopEngine AI هو نظام ذكي بيحلل قراءات الحساسات ويقارنها بالموديل السليم للكشف المبكر عن الأعطال.\n\n📄 لشرح مفصل، توجه إلى صفحة **📘 دليل الاستخدام** من القائمة الجانبية.")

# ======= القائمة الجانبية =======
st.sidebar.title("📁 صفحات المشروع")
st.sidebar.page_link("pages/landing.py", label="🏁 الصفحة الافتتاحية", icon="🏁")
st.sidebar.page_link("pages/train_ai.py", label="🧠 تدريب النموذج", icon="🧠")
st.sidebar.page_link("pages/detect_deviation.py", label="📉 تحليل الانحراف", icon="📉")
st.sidebar.page_link("pages/final_report.py", label="📄 التقرير النهائي", icon="📄")
st.sidebar.page_link("pages/clean_and_merge.py", label="🧹 دمج وتنظيف البيانات", icon="🧹")
st.sidebar.page_link("pages/upload_zip_files.py", label="🗜️ رفع ملف ZIP", icon="🗜️")
st.sidebar.page_link("pages/readme_viewer.py", label="📘 دليل الاستخدام", icon="📘")  # ✅ صفحة الشرح

# ======= التوقيع =======
st.markdown("""
    <br><hr style="border-top: 1px solid #bbb;">
    <div style="text-align:center; font-size:18px; color:#FF1493;">
        تنفيذ: Eng. Nabil Elmasry &nbsp; | &nbsp; Powered by AI 🚀
    </div>
""", unsafe_allow_html=True)