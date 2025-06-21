# pages/train_ai.py

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64
from sklearn.ensemble import IsolationForest

# إعداد الصفحة
st.set_page_config(page_title="🧠 تدريب نموذج الذكاء الاصطناعي", layout="wide")
st.title("🧠 تدريب النموذج على قراءات الحساسات السليمة فقط")

st.markdown("""
### 📥 ارفع ملف بيانات الحساسات السليمة (CSV)
يفضل أن يكون الملف مدمج ونظيف وخالي من الأعطال.
""")

uploaded_file = st.file_uploader("ارفع الملف", type=["csv"])

# اختيار نسبة التلوث (أي نسبة القيم الغير طبيعية أثناء التدريب)
contamination = st.slider("⚠️ نسبة التلوث المتوقعة في البيانات (قيم غير طبيعية)", 0.0, 0.2, 0.01, step=0.01)

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ تم تحميل البيانات بنجاح")
        st.dataframe(df.head())

        if st.button("🚀 ابدأ تدريب النموذج"):
            with st.spinner("جاري تدريب النموذج..."):
                model = IsolationForest(contamination=contamination, random_state=42)
                model.fit(df)

                joblib.dump(model, "model.pkl")
                st.success("✅ تم تدريب النموذج وحفظه باسم model.pkl")

                # رابط تحميل النموذج
                with open("model.pkl", "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                    href = f'<a href="data:file/pkl;base64,{b64}" download="model.pkl">📥 اضغط هنا لتحميل النموذج</a>'
                    st.markdown("### ⬇️ تحميل النموذج المدرب:")
                    st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ حدث خطأ أثناء المعالجة: {e}")
else:
    st.info("📌 يرجى رفع ملف CSV لبدء التدريب.")