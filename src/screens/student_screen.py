import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_bg_dashboard
from src.database.db import teacher_login, check_teacher_exist, create_teacher
from PIL import Image
import numpy as np

# def student_dashboard():

    # if "teacher_data" in st.session_state:
    #     student()
    # elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
    #     student()
    # elif st.session_state.teacher_login_type == "register":
    #     student()

def student_screen():
    style_bg_dashboard()
    style_base_layout()
    
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using FaceID', text_alignment='center')
    st.space()
    st.space()
    
    show_registration = False
    photo_source = st.camera_input("Position your face in the center")
    if photo_source:
        np.array(Image.open(photo_source))