import streamlit as st
import pandas as pd
import re
import fitz  # PyMuPDF
import base64

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV منظم", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
📌 **خطوات الاستخدام**:
1. ارفع ملف PDF يحتوي على قراءات الحساسات (من جهاز Launch مثلاً).
2. سيتم استخراج النص وتنظيمه في شكل جدول.
3. يمكنك تحميل الملف النهائي كـ CSV لاستخدامه في صفحة كشف الأعطال.

💡 يدعم ملفات PDF التي تحتوي على **نصوص قابلة للنسخ** وليس صور فقط.
""")

uploaded_pdf = st.file_uploader("📄 ارفع ملف PDF", type=["pdf"])

if uploaded_pdf is not None:
    try:
        # قراءة صفحات النص
        with fitz.open(stream=uploaded_pdf.read(), filetype="pdf") as doc:
            full_text = ""
            for page in doc:
                full_text += page.get_text()

        st.subheader("📝 النص المستخرج من ملف PDF")
        st.code(full_text[:1000])  # عرض أول جزء فقط

        # تحويل النص إلى جدول
        rows = [line.strip() for line in full_text.split("\n") if re.search(r"\d", line)]
        data = [re.split(r"\s{2,}|\t+", row) for row in rows]
        max_len = max(len(row) for row in data)
        data = [row for row in data if len(row) == max_len]

        if len(data) >= 2:
            df = pd.DataFrame(data[1:], columns=data[0])

            st.success("✅ تم تحويل النص إلى جدول")
            st.dataframe(df.head())

            # تنظيف الأعمدة (فصل القيمة عن الوحدة)
            for col in df.columns:
                unit_col = col.strip() + "_unit"

                def extract_value_and_unit(val):
                    if pd.isna(val): return pd.NA, pd.NA
                    match = re.match(r"([\d\-,\.E+]+)([^\d\s,\.%]+|%)?", str(val).strip())
                    if match:
                        value = match.group(1).replace(',', '.')
                        unit = match.group(2) if match.group(2) else ""
                        return value, unit
                    return val, ""

                values, units = zip(*df[col].map(extract_value_and_unit))
                df[col] = values
                df[unit_col] = units

            # تحويل القيم الرقمية
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    continue

            st.subheader("📋 البيانات بعد التنظيف")
            st.dataframe(df.head())

            # تحميل الملف
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ تحميل الملف كـ CSV",
                data=csv,
                file_name="Cleaned_Sensor.csv",
                mime="text/csv"
            )

        else:
            st.warning("⚠️ لم يتم العثور على بيانات قابلة للتحليل داخل PDF. تأكد أن الملف يحتوي على جدول نصي.")

    except Exception as e:
        st.error("❌ حدث خطأ أثناء قراءة الملف")
        st.exception(e)
else:
    st.info("📤 من فضلك ارفع ملف PDF أولاً")