import streamlit as st
import pandas as pd
import pickle

# عنوان الصفحة
st.title("📊 Smart Maker Final - تجهيز ملف الحساسات للتنبؤ")

# رفع ملف الحساسات
sensor_file = st.file_uploader("📁 ارفع ملف الحساسات (CSV)", type="csv")

# رفع ملف النموذج المدرب
model_file = st.file_uploader("🤖 ارفع ملف النموذج المدرب (.pkl)", type="pkl")

if sensor_file and model_file:
    try:
        # قراءة ملف الحساسات
        df_sensor = pd.read_csv(sensor_file)

        # تحميل النموذج المدرب
        model = pickle.load(model_file)

        # استخراج الأعمدة المستخدمة في التدريب
        if hasattr(model, 'feature_names_in_'):
            model_columns = list(model.feature_names_in_)
        else:
            st.error("❌ النموذج لا يحتوي على أسماء الأعمدة. قد تحتاج إعادة التدريب بطريقة مختلفة.")
            st.stop()

        # مقارنة الأعمدة
        sensor_columns = df_sensor.columns.tolist()
        missing_in_sensor = [col for col in model_columns if col not in sensor_columns]
        extra_in_sensor = [col for col in sensor_columns if col not in model_columns]

        st.subheader("📌 مقارنة الأعمدة:")

        if not missing_in_sensor and not extra_in_sensor:
            st.success("✅ الأعمدة متطابقة مع النموذج المدرب. الملف جاهز للتنبؤ.")
            df_ready = df_sensor.copy()
        else:
            if missing_in_sensor:
                st.error("❌ الأعمدة التالية مفقودة في ملف الحساسات (تمت إضافتها بقيمة 0):")
                st.write(missing_in_sensor)

            if extra_in_sensor:
                st.warning("⚠️ الأعمدة التالية زائدة في ملف الحساسات (تم تجاهلها في نسخة التنبؤ):")
                st.write(extra_in_sensor)

            # تجهيز نسخة جاهزة للتنبؤ
            df_ready = df_sensor.copy()

            # إضافة الأعمدة الناقصة بقيمة 0
            for col in missing_in_sensor:
                df_ready[col] = 0

            # الاحتفاظ فقط بالأعمدة المطلوبة للتدريب
            df_ready = df_ready[model_columns]

        # عرض البيانات الأصلية
        with st.expander("📄 عرض البيانات الأصلية"):
            st.dataframe(df_sensor)

        # عرض البيانات الجاهزة للتنبؤ
        with st.expander("✅ عرض البيانات الجاهزة للتنبؤ"):
            st.dataframe(df_ready)

        # تحميل الملف الجاهز للتنبؤ
        st.download_button(
            label="⬇️ تحميل الملف الجاهز للتنبؤ",
            data=df_ready.to_csv(index=False).encode('utf-8'),
            file_name="ready_for_prediction.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"❌ حصل خطأ أثناء التحضير: {e}")
else:
    st.info("⬆️ من فضلك ارفع ملف الحساسات وملف النموذج المدرب أولاً.")