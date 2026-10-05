import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_bg_dashboard
def teacher_screen():
    style_base_layout()
    style_bg_dashboard()
    header_dashboard()
    st.header('teacher screen')