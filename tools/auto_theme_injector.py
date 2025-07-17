import streamlit as st
from streamlit.components.v1 import html

def apply_custom_theme():
    custom_css = """
    <style>
        /* تغيير لون الخلفية */
        .stApp {
            background-color: #f5f5f5;
        }

        /* تنسيق العناوين */
        h1 {
            color: #2e7d32;
            font-size: 36px;
            border-bottom: 2px solid #2e7d32;
            padding-bottom: 10px;
        }

        /* تحسين شكل الجداول */
        .stDataFrame {
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            background-color: #ffffff;
        }

        /* تنسيق أزرار Streamlit */
        .stButton > button {
            background-color: #2e7d32;
            color: white;
            padding: 0.5em 1em;
            border-radius: 8px;
            border: none;
        }

        .stButton > button:hover {
            background-color: #1b5e20;
        }

        /* تنسيق البطاقات */
        .stCard {
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
    </style>
    """
    html(custom_css, unsafe_allow_html=True)