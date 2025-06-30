#pages/detect_deviation.py

import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 
import joblib 
import base64 
import os

st.set_page_config(page_title="📊 كشف الانحراف وتوقع الأعطال", layout="wide") st.title("📊 كشف انحراف قراءات الحساسات وتوقع الأعطال")

st.markdown("""

🚗 ارفع الملفات المطلوبة:

1. النموذج المدرب .pkl


2. ملف قراءات الحساسات .csv """)



model_file = st.file_uploader("📥 ارفع النموذج المدرب (model.pkl)", type=["pkl"]) data_file = st.file_uploader("📥 ارفع قراءات الحساسات الفعلية (.csv)", type=["csv"])

threshold = st.slider("📏 اختر الحد الحرج للانحراف", 0.0, 1.0, 0.5, step=0.01)

if st.button("🚀 تحليل وتوقع الأعطال"): if model_file is None or data_file is None: st.error("❌ الرجاء رفع كلا الملفين أولاً.") else: try: # تحميل النموذج والبيانات model = joblib.load(model_file) df = pd.read_csv(data_file) st.success("✅ تم تحميل البيانات") st.dataframe(df.head())

# محاولة جلب أسماء الأعمدة المطلوبة
        try:
            model_features = model.feature_names_in_
        except AttributeError:
            model_features = df.columns  # fallback

        if not all(col in df.columns for col in model_features):
            st.error("⚠️ ملف البيانات لا يحتوي على نفس الأعمدة التي تم تدريب النموذج عليها")
        else:
            df = df[model_features]

            # إزالة القيم غير الرقمية إن وجدت
            df = df.select_dtypes(include=[np.number])
            df = df.dropna()

            # توقع الانحرافات
            prediction = model.predict_proba(df)[:, 0]
            deviation_scores = 1 - prediction
            avg_deviation = np.mean(deviation_scores)

            st.markdown(f"### 🔍 متوسط درجة الانحراف: **{avg_deviation:.2f}** من 1.0")
            status = "⚠️ يوجد انحراف واضح عن القيم الطبيعية" if avg_deviation > threshold else "✅ القيم ضمن النطاق الطبيعي"
            st.markdown(f"### النتيجة: {status}")

            st.subheader("📉 رسم بياني للانحرافات")
            try:
                fig, ax = plt.subplots(figsize=(12, 5))
                sns.lineplot(x=range(len(deviation_scores)), y=deviation_scores, marker="o", ax=ax)
                ax.axhline(threshold, color='blue', linestyle='--', label='الحد الحرج')
                ax.set_title("درجة الانحراف عن النموذج السليم")
                ax.set_ylabel("درجة الانحراف")
                ax.set_xlabel("رقم القراءة")
                ax.legend()
                st.pyplot(fig)
            except Exception as e:
                st.warning(f"⚠️ لم يتم عرض الرسم البياني: {e}")

            # عرض القيم المنحرفة
            df_with_dev = df.copy()
            df_with_dev["deviation_score"] = deviation_scores
            outliers_df = df_with_dev[df_with_dev["deviation_score"] > threshold]

            st.subheader("📋 القراءات المنحرفة")
            st.dataframe(outliers_df)

            # تقرير نصي مفصل
            st.subheader("🧾 تقرير نصي")
            report_lines = [
                f"متوسط الانحراف: {avg_deviation:.2f}",
                f"الحد الحرج: {threshold}",
                f"النتيجة: {status}",
                "\n---\nتفاصيل القيم المنحرفة:" if not outliers_df.empty else "\nلا توجد قراءات منحرفة."
            ]

            for i, row in outliers_df.iterrows():
                report_lines.append(f"- قراءة رقم {i+1}:")
                for col in model_features:
                    report_lines.append(f"    • {col}: {row[col]}")
                report_lines.append(f"    ⚠️ درجة الانحراف: {row['deviation_score']:.2f}\n")

            report_text = "\n".join(report_lines)
            st.code(report_text, language="text")

            # تحميل التقرير
            b64 = base64.b64encode(report_text.encode()).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="fault_report.txt">⬇️ تحميل التقرير على الموبايل</a>'
            st.markdown("### 📥 تحميل التقرير النهائي")
            st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error("❌ حدث خطأ أثناء التحليل:")
        st.exception(e)

