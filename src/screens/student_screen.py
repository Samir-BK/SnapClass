import streamlit as st
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout, style_bg_dashboard
from src.database.db import teacher_login, check_teacher_exist, create_teacher, get_all_students, create_student
from PIL import Image
import numpy as np
from src.pipeplines.face_pipeline import predict_attendance, get_face_embeddings, trian_classifier
from src.pipeplines.voice_pipeline import get_voice_embedding
import time

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
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not found!")
            elif num_faces > 1:
                st.warning("Multiple faces found!")
            else:
                if detected:
                    student_id = next(iter(detected))
                    all_students = get_all_students()
                    student = next((s for s in all_students if s["student_id"] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back. {student["name"]}")
                        time.sleep(1)
                        st.rerun()

                else:
                    st.info("Face not recogoinized! You might be a new student!")
                    show_registration = True
    if show_registration:
        with st.container(border=True):
            st.header("Register new profile")
            new_name = st.text_input("Enter you name", placeholder="Samir Smith")

            st.subheader("Optional : Voice Enrollment")
            st.info("Enroll your voice onyl attedance")

            audio_data = None

            try:
                audio_data = st.audio_input("Record a short pharse like I am present, My name is Samir.")
            except Exception:
                st.error("Audio Data failed!")

            if st.button("Create Account", type = "primary"):
                if new_name:
                    with st.spinner("Creating Profile.."):
                        img = np.array(Image.open(photo_source))
                        encodings = get_face_embeddings(img)
                        if encodings:
                            face_emb = encodings[0].tolist()

                            voice_emb = None

                            if audio_data is not None:
                                voice_emb = get_voice_embedding(audio_data.getvalue())
                            response_data = create_student(new_name, face_embedding = face_emb, voice_embedding = voice_emb)

                            if response_data:
                                trian_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("Couldn't capture your facial features for registration.")   
                else:
                    st.error("Please enter your name first")







