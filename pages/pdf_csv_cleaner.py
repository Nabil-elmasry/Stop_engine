#premary test 
import streamlit as st
import pandas as pd

st.set_page_config(page_title="تنظيف ملف الحساسات", layout="wide")
st.title("AI Car Diagnosis - Sensor Data Cleaner")

# رفع ملف الحساسات
uploaded_file = st.file_uploader("ارفع ملف الحساسات (.csv)", type=["csv"])

if uploaded_file is not None:
    try:
        # قراءة الملف
        df = pd.read_csv(uploaded_file)

        st.subheader("البيانات الأصلية")
        st.dataframe(df)

        # ====== تنظيف البيانات ======
        # حذف الصفوف أو الأعمدة الفارغة
        df_cleaned = df.dropna(how='all')  # حذف الصفوف الفارغة كليًا
        df_cleaned = df_cleaned.dropna(axis=1, how='all')  # حذف الأعمدة الفارغة كليًا

        # إصلاح الفواصل العشرية (تحويل الفواصل إلى نقاط إن وجدت)
        df_cleaned = df_cleaned.applymap(
            lambda x: str(x).replace(',', '.') if isinstance(x, str) else x
        )

        # محاولة تحويل الأعمدة الرقمية إلى float أو int
        for col in df_cleaned.columns:
            try:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='ignore')
            except:
                pass

        st.success("تم تنظيف وتنظيم البيانات بنجاح!")

        st.subheader("البيانات بعد التنظيف")
        st.dataframe(df_cleaned)

        # ====== زر تحميل الملف ======
        csv = df_cleaned.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="تحميل ملف الحساسات المنظف",
            data=csv,
            file_name="Cleaned_Sensor.csv",
            mime='text/csv'
        )

    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة الملف: {e}")
else:
    st.info("يرجى رفع ملف الحساسات أولاً للبدء.")

