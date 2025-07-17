import streamlit as st
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
import os

# تحميل النموذج المدرب من مجلد models
MODEL_PATH = "models/model.pkl"

# عنوان الصفحة
st.set_page_config(page_title="كشف الأعطال", layout="wide")

st.markdown("## 👨‍🔧 أهلاً بيك في صفحة *كشف الأعطال*")
st.write("ارفع ملف الحساسات من العربية المشتبه في وجود عطل فيها، وشوف النتيجة فورًا مقارنة بالبيانات السليمة اللي اتدرب عليها النموذج.")

# تحميل النموذج المدرب
@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as file:
        model_data = pickle.load(file)
    return model_data  # نفترض إنه dict فيه {'mean': df_mean, 'std': df_std}

model_data = load_model()
ref_mean = model_data['mean']
ref_std = model_data['std']
expected_columns = ref_mean.columns.tolist()

# رفع ملف جديد للمقارنة
uploaded_file = st.file_uploader("📤 ارفع ملف قراءات الحساسات (CSV)", type="csv")

if uploaded_file:
    try:
        new_data = pd.read_csv(uploaded_file)

        st.markdown("### ✅ تم تحميل البيانات بنجاح")
        st.dataframe(new_data.head(), use_container_width=True)

        # التحقق من الأعمدة
        missing_cols = list(set(expected_columns) - set(new_data.columns))
        extra_cols = list(set(new_data.columns) - set(expected_columns))

        if missing_cols:
            st.warning(f"⚠️ الأعمدة التالية غير موجودة في الملف المرفوع: {missing_cols}")
        if extra_cols:
            st.info(f"ℹ️ الأعمدة التالية موجودة في الملف لكنها مش مطلوبة: {extra_cols}")

        # مطابقة الأعمدة المطلوبة فقط
        valid_columns = [col for col in expected_columns if col in new_data.columns]
        if len(valid_columns) == 0:
            st.error("❌ الملف لا يحتوي على أي من الحساسات المطلوبة.")
        else:
            input_data = new_data[valid_columns].mean()

            # حساب نسبة الانحراف عن المرجع
            deviation = abs((input_data - ref_mean[valid_columns].iloc[0]) / (ref_std[valid_columns].iloc[0] + 1e-6)) * 100
            deviation_df = pd.DataFrame({
                'حساس': valid_columns,
                'نسبة الانحراف (%)': deviation.values
            }).sort_values(by='نسبة الانحراف (%)', ascending=False)

            st.markdown("### 📊 نتيجة التحليل")
            st.dataframe(deviation_df, use_container_width=True)

            # رسم بياني
            st.markdown("### 🔍 تحليل بصري للانحراف")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(deviation_df['حساس'], deviation_df['نسبة الانحراف (%)'], color='orange')
            ax.axhline(100, color='red', linestyle='--', label='نسبة خطرة')
            plt.xticks(rotation=45, ha='right')
            plt.ylabel("نسبة الانحراف (%)")
            plt.title("مقارنة قراءات الحساسات مع القيم المرجعية")
            plt.legend()
            st.pyplot(fig)

            # توصية بناءً على النتائج
            max_dev = deviation_df['نسبة الانحراف (%)'].max()
            if max_dev > 100:
                st.error("🚨 الانحراف عالي جدًا! محتمل وجود عطل كبير في النظام.")
            elif max_dev > 50:
                st.warning("⚠️ في بعض الحساسات عندها انحراف ملحوظ. راجعها.")
            else:
                st.success("✅ الوضع جيد جدًا. مفيش انحرافات مقلقة.")

    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {str(e)}")