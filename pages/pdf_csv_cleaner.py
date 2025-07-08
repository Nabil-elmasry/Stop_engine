# pages/pdf_csv_cleaner.py

import streamlit as st
import pandas as pd
import re
import base64

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV منظم", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
### 📌 خطوات الاستخدام:
1. ارفع ملف PDF يحتوي على قراءات الحساسات (مثل من جهاز Lunch).
2. سيتم تحليل النص واستخلاص القيم والوحدات يدويًا.
3. يمكنك تحميل الملف النهائي لاستخدامه في صفحة كشف الأعطال.

💡 مناسب لملفات PDF النصية فقط (غير المصورة).
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

        # استخراج بيانات جدول القيم
        start_marker = "Name Value"
        if start_marker in all_text:
            table_text = all_text.split(start_marker)[1]
            rows = table_text.strip().split("\n")

            data = []
            for line in rows:
                if re.match(r"^[A-Za-z0-9\-/()#.,% ]+\s+[\S]+", line.strip()):
                    # فصل بين الاسم والقيمة أو النطاق
                    parts = re.split(r"\s{2,}", line.strip())
                    if len(parts) >= 2:
                        name = parts[0]
                        value_unit = " ".join(parts[1:])
                        # استخراج القيمة والوحدة
                        match = re.match(r"([\d\-.]+)\s*([a-zA-Z%°]+)?", value_unit)
                        if match:
                            value = match.group(1)
                            unit = match.group(2) if match.group(2) else ""
                        else:
                            value = value_unit
                            unit = ""
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
        else:
            st.warning("⚠️ لم يتم العثور على بداية جدول القيم داخل الملف.")

    except Exception as e:
        st.error("❌ حدث خطأ أثناء قراءة الملف:")
        st.exception(e)
else:
    st.info("📤 من فضلك ارفع ملف PDF أولاً")