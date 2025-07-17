
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import base64
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="🧠 تدريب النموذج", layout="wide")
st.title("🧠 تدريب النموذج على قراءات الحساسات السليمة فقط")

st.markdown("""
### 🚗 ارفع ملف يحتوي على بيانات حساسات لعربيات سليمة فقط
""")

uploaded_file = st.file_uploader("📥 ارفع ملف CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ تم تحميل البيانات بنجاح")
    st.dataframe(df.head())

    st.subheader("📊 إحصائيات رقمية مختصرة")
    st.dataframe(df.describe())

    st.subheader("📈 رسم Boxplot لقياس التوزيع والانحرافات المحتملة")
    try:
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.boxplot(data=df.select_dtypes(include=['float64', 'int64']), ax=ax)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        ax.set_title("Boxplot لمقارنة توزيع الحساسات")
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"⚠️ لم يتم عرض الرسم البياني بسبب: {e}")

    st.subheader("🤖 تدريب النموذج على البيانات")

    if st.button("🚀 ابدأ التدريب"):
        try:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(df, [0] * len(df))  # كل البيانات سليمة، نصنفها بـ 0

            # حفظ النموذج
            joblib.dump(model, "model.pkl")
            st.success("✅ تم حفظ النموذج باسم model.pkl")

            # حفظ الإحصائيات
            df.describe().to_csv("normal_stats.csv")
            st.success("✅ تم حفظ الإحصائيات باسم normal_stats.csv")

            # روابط التحميل
            with open("model.pkl", "rb") as f:
                st.download_button("⬇️ تحميل النموذج المدرب", f, file_name="model.pkl")

            with open("normal_stats.csv", "rb") as f:
                st.download_button("⬇️ تحميل إحصائيات الحساسات", f, file_name="normal_stats.csv")

        except Exception as e:
            st.error(f"❌ حدث خطأ أثناء التدريب: {e}")
else:
    st.info("📂 من فضلك ارفع ملف CSV لبدء التدريب")