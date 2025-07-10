import streamlit as st
from pathlib import Path

# إعداد عنوان الصفحة وإغلاق الشريط الجانبي في البداية
st.set_page_config(page_title="شرح الاستخدام", layout="wide", initial_sidebar_state="collapsed")

# ترويسة
st.title("📘 شرح استخدام تطبيق StopEngine AI")

# تحديد مكان ملف README
readme_path = Path(__file__).parent.parent / "README.md"

# التحقق إذا الملف موجود
if readme_path.exists():
    with readme_path.open(encoding="utf-8") as f:
        readme_content = f.read()
    # عرض المحتوى بصيغة Markdown
    st.markdown(readme_content, unsafe_allow_html=True)
else:
    st.error("لم يتم العثور على ملف README.md")