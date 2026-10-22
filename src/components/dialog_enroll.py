import streamlit as st
from src.database.db import enroll_student_by_code


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.write('Enter the subject code provided by your teacher to enroll')
    join_code = st.text_input('Subject Code', placeholder='Eg. CS101')

    if st.button('Enroll now', type='primary', width='stretch'):
        if not join_code.strip():
            st.warning('Please enter a subject code')
            return

        student_id = st.session_state.student_data['student_id']
        try:
            subject = enroll_student_by_code(join_code, student_id)
            st.success(f"Successfully enrolled in {subject['name']}!")
            st.rerun()
        except ValueError as error:
            st.warning(str(error))
        except Exception as error:
            st.error(f"Could not enroll in the subject: {error}")
