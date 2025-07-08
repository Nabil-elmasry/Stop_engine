# pages/pdf_csv_cleaner.py

import streamlit as st
import pandas as pd
import re
import base64

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV منظم", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
### 📌 خطوات الاستخدام:
1. ارفع ملف PDF يحتوي على قراءات الحساسات (مثل من جهاز Lunch أو Launch).
2. سيتم تحليل النص واستخلاص القيم والوحدات تلقائيًا.
3. يمكنك تحميل الملف النهائي لاستخدامه في صفحة كشف الأعطال.

💡 يدعم فقط ملفات PDF النصية (غير المصورة).
""")

uploaded_file = st.file_uploader("📄 ارفع ملف PDF", type=["pdf"])
if uploaded_file:
    try:
        import fitz  # PyMuPDF
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        all_text = ""
        for page in pdf_doc:
            all_text += page.get_text()

        st.success("✅ تم استخراج النص من ملف PDF")
        st.subheader("📝 جزء من النص:")
        st.code(all_text[:1000])

        # تحليل السطور المشتبه بها كجدول (بها أرقام و % أو وحدات)
        rows = [line.strip() for line in all_text.split("\n") if re.search(r"\d", line) and len(line.strip()) > 5]

        data = []
        for line in rows:
            # حاول فصل الجملة إلى: الاسم - القيمة - الوحدة
            parts = re.split(r"\s{2,}|\t+", line)
            if len(parts) >= 2:
                name = parts[0]
                rest = " ".join(parts[1:])
                # استخراج القيمة + الوحدة من بقية السطر
                match = re.match(r"([\d\-.]+)\s*([a-zA-Z%°]+)?", rest)
                if match:
                    value = match.group(1)
                    unit = match.group(2) if match.group(2) else ""
                    data.append([name, value, unit])

        if data:
            df = pd.DataFrame(data, columns=["Sensor", "Value", "Unit"])
            st.success("✅ تم تحويل النص إلى جدول منظم")
            st.dataframe(df.head())

            csv = df.to_csv(index=False).encode('utf-8-sig')
            b64 = base64.b64encode(csv).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="Cleaned_Sensor.csv">⬇️ تحميل الملف المنظم (CSV)</a>'
            st.markdown("### 📥 تحميل الملف النهائي")
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("⚠️ لم يتم العثور على بيانات حساسات منظمة داخل الملف.")

    except Exception as e:
        st.error("❌ حدث خطأ أثناء قراءة الملف:")
        st.exception(e)
else:
    st.info("📤 من فضلك ارفع ملف PDF أولاً")