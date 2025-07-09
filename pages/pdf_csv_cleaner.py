import streamlit as st
import pandas as pd
import re
from PyPDF2 import PdfReader
from io import StringIO

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV منظم", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
### 📌 خطوات الاستخدام:
1. ارفع ملف PDF يحتوي على قراءات الحساسات (من جهاز Lunch أو Launch).
2. سيتم تحويل النص واستخلاص القيم + الوحدة بدقة.
3. يمكنك تحميل الملف المنظم كـ CSV لاستخدامه في المقارنة النهائية.

💡 الكود يحافظ على كل القيم بما فيها 0 أو Not Available لأنها مهمة في التحليل.
""")

uploaded_pdf = st.file_uploader("📄 ارفع ملف PDF", type=["pdf"])

if uploaded_pdf:
    try:
        reader = PdfReader(uploaded_pdf)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        st.subheader("📝 جزء من النص المستخرج:")
        st.code(text[:1000])

        # استخراج الحساسات والقيم والوحدات
        pattern = re.compile(r"([A-Za-z0-9 \-\/\.,()%]+?)\s+([-+]?\d*\.?\d+|0|Not Fixed|Not Available|Available)\s*([a-zA-Z%μVkmhPaA]+)?")
        matches = pattern.findall(text)

        if not matches:
            st.warning("⚠️ لم يتم العثور على بيانات حساسات منظمة في الملف.")
        else:
            data = []
            for name, value, unit in matches:
                name = name.strip()
                value = value.strip()
                unit = unit.strip() if unit else ""
                data.append([name, value, unit])

            df = pd.DataFrame(data, columns=["Sensor Name", "Value", "Unit"])

            # تحويل الأرقام
            df["Value"] = df["Value"].apply(lambda x: x.replace(',', '.') if isinstance(x, str) else x)
            df["Value"] = pd.to_numeric(df["Value"], errors="ignore")

            st.success(f"✅ تم استخراج {len(df)} سجل من الحساسات.")
            st.dataframe(df)

            # حفظ الملف
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ تحميل الملف كـ CSV",
                data=csv,
                file_name="Cleaned_Sensor.csv",
                mime="text/csv"
            )

    except Exception as e:
        st.error("❌ حدث خطأ أثناء معالجة الملف")
        st.exception(e)
else:
    st.info("📤 من فضلك ارفع ملف PDF أولاً")