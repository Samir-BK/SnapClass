import streamlit as st

from src.ui.base_layout import style_bg_home, style_base_layout
from src.components.header import header_home
def home_screen():

    header_home()
    style_base_layout()
    style_bg_home()
    
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Teacher portal"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
    with col2:
        if st.button("Student portal"):
            st.session_state['login_type'] = 'student'
            st.rerun()