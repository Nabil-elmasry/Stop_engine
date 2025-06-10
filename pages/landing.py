# landing.py

import streamlit as st
from modules.theme_loader import apply_custom_theme

apply_custom_theme()

st.image("assets/logo.png", width=180)


st.set_page_config(page_title="🚀 StopEngine AI - الصفحة الرئيسية", layout="wide")

# ✅ عرض الشعار
st.image("assets/logo.png", width=180)

# ✅ عنوان رئيسي
st.markdown("""
<h1 style='text-align: center; color: #2c3e50;'>مرحبًا بك في StopEngine AI 👋</h1>
<h3 style='text-align: center; color: #6c757d;'>نظام ذكي للكشف المبكر عن الأعطال باستخدام تحليل بيانات الحساسات</h3>
""", unsafe_allow_html=True)

# ✅ شرح مختصر للخطوات
st.markdown("""
---

## 🧭 خطوات استخدام النظام:

1. 🧠 **تدريب النموذج** على بيانات قراءات الحساسات السليمة  
2. 📊 **رفع بيانات عربية بها مشكلة** وتحليل الانحراف  
3. 📋 **تحميل التقرير النهائي** لحالة السيارة  
4. 🛠️ **تحويل PDF إلى CSV** وتحضير البيانات  
5. 🧼 **تنظيف الملفات أو السجلات القديمة**

---

> استخدم القائمة الجانبية للتنقل بين الصفحات المختلفة 🧭
""")

# ✅ توقيع ختامي
st.markdown("""
<hr>
<div style='text-align: center; font-size: 16px; color: #888;'>
    تنفيذ: Eng. Nabil Elmasry 🚗 | Powered by AI ⚙️
</div>
""", unsafe_allow_html=True)