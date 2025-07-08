# pages/pdf_to_cleaned_csv.py
import streamlit as st
import pandas as pd
import re
from io import StringIO
from pdf2image import convert_from_bytes
import pytesseract
import tempfile
import base64

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV منظم", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
### 📌 خطوات الاستخدام:

1. ارفع ملف PDF يحتوي على قراءات الحساسات (مثل من جهاز Launch).
2. سيتم استخراج وتحليل الجدول وتحويله إلى CSV.
3. سيتم تنظيف البيانات وفصل القيمة عن الوحدة.
4. يمكنك تحميل الملف النهائي لاستخدامه في كشف الأعطال.

💡 يدعم ملفات PDF التي تحتوي على جداول مطبوعة أو على شكل صور.
""")

uploaded_pdf = st.file_uploader("📄 ارفع ملف PDF", type=["pdf"])

if uploaded_pdf:
    try:
        with tempfile.TemporaryDirectory() as path:
            images = convert_from_bytes(uploaded_pdf.read(), output_folder=path)
            st.success(f"✅ تم استخراج {len(images)} صفحة من ملف PDF")

            all_text = ""
            for img in images:
                text = pytesseract.image_to_string(img, lang='eng')
                all_text += text + "\n"

        st.subheader("📝 معاينة النص المستخرج (أول 1000 حرف)")
        st.code(all_text[:1000])

        st.markdown("### 📊 تحليل البيانات وتحويلها إلى جدول")

        rows = [line for line in all_text.split("\n") if len(line.strip()) > 5 and re.search(r"\d", line)]
        data = [re.split(r"\s{2,}|\t+", row.strip()) for row in rows]
        max_len = max(len(row) for row in data)
        data = [row for row in data if len(row) == max_len]

        if len(data) >= 2:
            df = pd.DataFrame(data[1:], columns=data[0])
            st.success("✅ تم تحويل النص إلى جدول منظم")
            st.dataframe(df.head())

            # تنظيف الأعمدة: فصل القيمة عن الوحدة
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

            # محاولة تحويل القيم الرقمية
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except:
                    continue

            st.subheader("📋 البيانات بعد التنظيف")
            st.dataframe(df.head())

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ تحميل الملف بعد التنظيف (CSV)",
                data=csv,
                file_name="Cleaned_Sensor.csv",
                mime="text/csv"
            )
        else:
            st.error("❌ لم يتم العثور على بيانات قابلة للتحليل داخل PDF.")
    except Exception as e:
        st.error("❌ حدث خطأ أثناء التحليل أو التنظيف")
        st.exception(e)
else:
    st.info("📤 من فضلك ارفع ملف PDF أولاً للبدء")