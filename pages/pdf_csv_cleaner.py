import streamlit as st
import pandas as pd
import re
import base64
import fitz  # PyMuPDF

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
        pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        all_text = ""
        for page in pdf_doc:
            all_text += page.get_text()

        st.success("✅ تم استخراج النص من ملف PDF")
        st.subheader("📝 جزء من النص:")
        st.code(all_text[:1000])

        # استخراج جميع الأسطر المهمة (بعد Data Stream)
        relevant_text = all_text.split("Data Stream")[-1]
        lines = [line.strip() for line in relevant_text.split("\n") if len(line.strip()) > 3]

        structured_rows = []
        for i in range(len(lines) - 1):
            headers = re.split(r"\s{2,}|\t+", lines[i])
            values = re.split(r"\s{2,}|\t+", lines[i + 1])

            if len(headers) == len(values) and all(re.search(r"\d", val) for val in values):
                structured_rows.append((headers, values))

        if not structured_rows:
            st.warning("⚠️ لم يتم العثور على بيانات منظمة داخل الملف.")
        else:
            final_data = []
            for headers, values in structured_rows:
                for h, v in zip(headers, values):
                    match = re.match(r"([\d\-.]+)\s*([a-zA-Z%°]+)?", v)
                    if match:
                        val = match.group(1)
                        unit = match.group(2) if match.group(2) else ""
                        final_data.append([h, val, unit])
            df = pd.DataFrame(final_data, columns=["Sensor", "Value", "Unit"])
            st.success("✅ تم تحويل النص إلى جدول منظم")
            st.dataframe(df.head())

            # تحميل الملف
            csv = df.to_csv(index=False).encode('utf-8-sig')
            b64 = base64.b64encode(csv).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="Cleaned_Sensor.csv">⬇️ تحميل الملف المنظم (CSV)</a>'
            st.markdown("### 📥 تحميل الملف النهائي")
            st.markdown(href, unsafe_allow_html=True)

    except Exception as e:
        st.error("❌ حدث خطأ أثناء المعالجة")
        st.exception(e)
else:
    st.info("📤 من فضلك ارفع ملف PDF أولاً")