# شغل ممتاز - Enhanced UI Version
import streamlit as st
import pdfplumber
import pandas as pd
import re
import os
import shutil
import datetime

st.set_page_config(page_title="تحليل الحساسات والأكواد", layout="wide")

# ==== تصميم العنوان ====
st.markdown("""
    <h1 style='text-align: center; color: #FFFFFF; background-color: #FF0000; padding: 10px; border-radius: 15px;'>
        AI Car Diagnosis     
    </h1>
""", unsafe_allow_html=True)

# ======= زر مسح الملف والذاكرة =======
st.sidebar.markdown("""
    <div style='background-color:#f4cccc;padding:10px;border-radius:10px;'>
        <h4 style='color:#990000;'>تنظيف كامل للبيانات</h4>
    </div>
""", unsafe_allow_html=True)

if st.sidebar.button("احذف الملف وامسح الذاكرة"):
    try:
        if os.path.exists("Carset.csv"):
            os.remove("Carset.csv")
        if os.path.exists("backup"):
            shutil.rmtree("backup")
        st.session_state.clear()
        st.sidebar.success("تم حذف الملفات ومسح الذاكرة. أعد تشغيل الصفحة.")
    except Exception as e:
        st.sidebar.error(f"حدث خطأ أثناء الحذف: {e}")

# ======= دوال استخراج البيانات =======
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

def extract_dtcs(text):
    lines = text.split('\n')
    dtcs = []
    for line in lines:
        match = re.search(r"(P\d{4})", line)
        if match:
            code = match.group(1)
            desc = line.replace(code, "").strip(" :-–")
            dtcs.append([code, desc.strip()])
        elif line.strip():
            dtcs.append(["No Code", line.strip()])
    return dtcs

def extract_sensor_data(text):
    lines = text.split('\n')
    sensors = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 4:
            name = ' '.join(parts[:-3])
            value = parts[-3]
            standard = parts[-2]
            unit = parts[-1]
            sensors.append([name, value, standard, unit])
    return pd.DataFrame(sensors, columns=["Sensor", "Value", "Standard", "Unit"])

# ======= واجهة رفع الملفات =======
st.markdown("""
    <div style='background-color:#90EE90;padding:15px;border:2px dashed #2ecc71;border-radius:10px;'>
        <h4 style='color:#34495e;'> من فضلك ارفع تقرير الحساسات (PDF)</h4>
    </div>
""", unsafe_allow_html=True)
sensor_files = st.file_uploader("", type="pdf", accept_multiple_files=True)

st.markdown("""
    <div style='background-color:#FFFF66;padding:15px;border:2px dashed #f39c12;border-radius:10px;'>
        <h4 style='color:#34495e;'>من فضلك ارفع تقرير الأعطال (PDF)</h4>
    </div>
""", unsafe_allow_html=True)
code_file = st.file_uploader("", type="pdf")

if sensor_files and code_file:
    sensor_text = ""
    for file in sensor_files:
        sensor_text += extract_text_from_pdf(file)

    code_text = extract_text_from_pdf(code_file)

    df_sensors = extract_sensor_data(sensor_text)
    dtcs = extract_dtcs(code_text)
    df_dtcs = pd.DataFrame(dtcs, columns=["Code", "Description"])

    st.subheader("1. بيانات الحساسات المستخرجة")
    st.dataframe(df_sensors)

    st.subheader("2. الأكواد المستخرجة")
    st.dataframe(df_dtcs)

    st.subheader("3. تحليل الانحراف وربط الحساسات بالأكواد")
    matches = []
    for _, dtc_row in df_dtcs.iterrows():
        for _, sensor_row in df_sensors.iterrows():
            if sensor_row["Sensor"].lower() in dtc_row["Description"].lower():
                try:
                    value = float(sensor_row["Value"])
                    standard = float(sensor_row["Standard"])
                    deviation_percent = abs(value - standard) / standard * 100 if standard != 0 else 0
                    status = "High Deviation" if deviation_percent > 15 else "OK"
                except:
                    deviation_percent = "N/A"
                    status = "Cannot Evaluate"

                matches.append([
                    dtc_row["Code"],
                    dtc_row["Description"],
                    sensor_row["Sensor"],
                    sensor_row["Value"],
                    sensor_row["Standard"],
                    sensor_row["Unit"],
                    f"{deviation_percent:.1f}%" if isinstance(deviation_percent, float) else deviation_percent,
                    status
                ])

    if matches:
        df_matches = pd.DataFrame(matches, columns=[
            "Code", "Fault Description", "Sensor", "Value", "Standard", "Unit", "Deviation %", "Status"
        ])
        st.success("تم تحليل الانحراف وربط الحساسات بالأكواد بنجاح.")
        st.dataframe(df_matches)
    else:
        st.info("لم يتم العثور على تطابق مباشر بين الحساسات والأكواد.")

    # ======= زر يدوي لحفظ البيانات =======
    st.subheader("4. حفظ البيانات يدويًا")
    if st.button("احفظ البيانات الحالية"):
        try:
            sensor_dict = {row['Sensor']: row['Value'] for _, row in df_sensors.iterrows()}
            sensor_dict['Fault Codes'] = ','.join(df_dtcs['Code'].tolist())
            new_case_df = pd.DataFrame([sensor_dict])

            csv_filename = "Carset.csv"
            backup_dir = "backup"
            os.makedirs(backup_dir, exist_ok=True)

            if os.path.exists(csv_filename):
                # نسخ احتياطي قبل التعديل
                now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                backup_path = os.path.join(backup_dir, f"backup_{now}.csv")
                shutil.copyfile(csv_filename, backup_path)

                # قراءة البيانات القديمة ودمجها مع الجديدة
                existing_df = pd.read_csv(csv_filename)
                final_df = pd.concat([existing_df, new_case_df], ignore_index=True)
            else:
                final_df = new_case_df

            final_df.to_csv(csv_filename, index=False)
            st.success("تم حفظ البيانات في Carset.csv وتم إنشاء نسخة احتياطية في backup")

            with open(csv_filename, "rb") as f:
                st.download_button(
                    label="Download Carset.csv",
                    data=f,
                    file_name="Carset.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"خطأ في حفظ البيانات: {e}")

else:
    st.warning("يرجى رفع تقرير الحساسات وتقرير الأعطال للاستمرار.")