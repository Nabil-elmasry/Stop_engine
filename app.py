
import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="Vehicle Diagnosis App", layout="wide")
st.title("Upload & View Reports")

def extract_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

sensor_file = st.file_uploader("Upload Sensor Report (PDF)", type="pdf")
code_file = st.file_uploader("Upload Fault Report (PDF)", type="pdf")

if sensor_file:
    st.subheader("Sensor Report Content")
    sensor_text = extract_text(sensor_file)
    st.text(sensor_text)

if code_file:
    st.subheader("Fault Report Content")
    fault_text = extract_text(code_file)
    st.text(fault_text)

if not sensor_file and not code_file:
    st.info("Please upload both PDF reports to preview content.")

