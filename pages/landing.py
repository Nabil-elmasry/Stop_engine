
import streamlit as st

st.set_page_config(page_title="Welcome", layout="centered")

st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #1f1c2c, #928DAB);
    }
    h1 {
        text-align: center;
        font-size: 3em;
        font-family: 'Arial Black', sans-serif;
        color: #FF4B2B;
        animation: pulse 2s infinite;
        text-shadow: 2px 2px 10px #000;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    .footer {
        position: fixed;
        bottom: 15px;
        width: 100%;
        text-align: center;
        font-size: 1.1em;
        color: #f8f8f8;
        font-weight: bold;
        text-shadow: 1px 1px 3px #000;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>AI Car Diagnosis System</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color:white;'>نظام التشخيص الذكي بالذكاء الاصطناعي</h1>", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        Eng. Nabil Almasry<br>By AI
    </div>
""", unsafe_allow_html=True)
