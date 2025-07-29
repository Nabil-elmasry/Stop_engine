import streamlit as st
import os
import pickle

st.set_page_config(page_title="Smart Maker Final", layout="wide")

# عنوان الصفحة
st.title("📊 Smart Maker Final")

# التحقق من وجود ملف النموذج
model_path = "modules/trained_model.pkl"

if os.path.exists(model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    st.success("✅ تم تحميل النموذج بنجاح! يمكنك الآن البدء في استخدام الصفحة.")
    
    # ضع الكود الخاص بتحميل الملف وتشغيل النموذج هنا

else:
    st.warning("⚠️ لم يتم العثور على ملف النموذج المدرب.")
    
    # رسالة أنيقة باستخدام HTML
    st.markdown("""
        <div style='background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; padding: 15px; border-radius: 10px; font-size: 16px;'>
            <strong>ملف النموذج غير موجود!</strong><br>
            تأكد من وجود الملف <code>trained_model.pkl</code> داخل المجلد <code>modules</code> لتعمل هذه الصفحة بشكل صحيح.
        </div>
    """, unsafe_allow_html=True)