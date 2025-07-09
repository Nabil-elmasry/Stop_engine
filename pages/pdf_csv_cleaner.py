import streamlit as st
import pandas as pd
import re
import fitz  # PyMuPDF

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV منظم", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
### 📌 خطوات الاستخدام:
1. ارفع ملف PDF يحتوي على قراءات الحساسات (من جهاز Launch أو مشابهه).
2. سيتم تحليل النص واستخلاص أسماء الحساسات + القيم + الوحدات.
3. سيتم تنظيف وتنظيم البيانات تلقائيًا.
4. يمكنك تحميل الملف النهائي لاستخدامه في صفحة المقارنة مع النموذج.

💡 **يدعم ملفات PDF النصية فقط (غير المصورة)**.
""")

uploaded_pdf = st.file_uploader("📄 ارفع ملف PDF", type=["pdf"])

if uploaded_pdf:
    try:
        # قراءة النص من ملف PDF النصي
        with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        st.success("✅ تم استخراج النص من ملف PDF")

        st.markdown("### 📝 جزء من النص:")
        st.code(text[:1000])

        # استخراج القيم من النص بناءً على نمط: اسم الحساس -> القيمة -> الوحدة (أو نص)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        records = []
        current_sensor = None

        for i in range(len(lines) - 2):
            name_candidate = lines[i]
            value_candidate = lines[i + 1]
            unit_candidate = lines[i + 2]

            # تحقق أن السطر التالي يبدو رقم أو قيمة حساسات
            if re.match(r"^[-+]?[0-9]*\.?[0-9]+$", value_candidate) or value_candidate.lower() in [
                "not available", "available", "not fixed", "fixed", "0", "-", "null"
            ]:
                current_sensor = name_candidate.strip()
                records.append({
                    "Sensor Name": current_sensor,
                    "Value": value_candidate.strip(),
                    "Unit": unit_candidate.strip()
                })

        if records:
            df = pd.DataFrame(records)

            st.subheader("📋 البيانات بعد المعالجة:")
            st.dataframe(df)

            # حفظ كـ CSV
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="⬇️ تحميل الملف كـ CSV",
                data=csv,
                file_name="Cleaned_Sensor.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ لم يتم العثور على بيانات منظمة يمكن استخراجها من الملف.")

    except Exception as e:
        st.error("❌ حدث خطأ أثناء معالجة الملف:")
        st.exception(e)
else:
    st.info("📥 من فضلك ارفع ملف PDF أولاً")