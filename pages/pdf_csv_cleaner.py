import streamlit as st
import pandas as pd
import re
import fitz  
# PyMuPDF
import base64

st.set_page_config(page_title="🧾 تحويل PDF إلى CSV منظم", layout="wide")
st.title("🧾 تحويل ملف PDF لقراءات الحساسات إلى CSV نظيف ومنظم")

st.markdown("""
### 📌 خطوات الاستخدام:
1. ارفع ملف PDF يحتوي على قراءات الحساسات (مثل من جهاز Lunch أو Launch).
2. سيتم استخراج كل القيم - حتى القيم مثل `0`, `Not Available`, `Available`, إلخ.
3. سيتم توليد جدول باسم + القيمة + الوحدة.
4. يمكنك تحميل الملف النهائي لاستخدامه في صفحة كشف الأعطال.

💡 يدعم فقط ملفات PDF النصية (وليس المصورة).
""")

uploaded_file = st.file_uploader("📄 ارفع ملف PDF", type=["pdf"])

if uploaded_file:
    try:
        # استخراج النص من PDF باستخدام PyMuPDF
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        all_text = ""
        for page in doc:
            all_text += page.get_text()

        st.success("✅ تم استخراج النص من ملف PDF")
        st.markdown("### 📝 جزء من النص المستخرج:")
        st.code(all_text[:1000])

        # استخراج أسماء الحساسات والقيم والوحدات بناءً على نمط (Name, Value, Unit)
        lines = all_text.split("\n")
        sensor_data = []
        i = 0
        while i < len(lines) - 2:
            name = lines[i].strip()
            value = lines[i+1].strip()
            unit = lines[i+2].strip()

            # فلتر مبدأي: تجاهل الأسطر الفارغة فقط
            if name and value:
                sensor_data.append({
                    "Sensor Name": name,
                    "Value": value,
                    "Unit": unit if unit.lower() not in ["value", "unit", name.lower()] else ""
                })
                i += 3
            else:
                i += 1

        if sensor_data:
            df = pd.DataFrame(sensor_data)
            st.success(f"✅ تم استخراج {len(df)} قراءة حساسات")
            st.subheader("📊 البيانات المنظمة")
            st.dataframe(df)

            # تحميل الملف
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="⬇️ تحميل ملف CSV المنظم",
                data=csv,
                file_name="Cleaned_Sensors.csv",
                mime="text/csv"
            )
        else:
            st.warning("⚠️ لم يتم العثور على جدول منظم داخل الملف.")

    except Exception as e:
        st.error("❌ حدث خطأ أثناء التحويل")
        st.exception(e)
else:
    st.info("📤 من فضلك ارفع ملف PDF أولاً")