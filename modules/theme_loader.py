# modules/theme_loader.py

import streamlit as st

def apply_custom_theme():
    try:
        with open("assets/custom.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("⚠️ لم يتم العثور على ملف custom.css داخل مجلد assets.")