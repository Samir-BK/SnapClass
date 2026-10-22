import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import create_subject_client

@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):
    student_id = st.session_state.student_data["student_id"]

    client = create_subject_client()
    res = (
        client.table('subjects')
        .select('subject_id, name')
        .eq('subject_code', subject_code)
        .limit(1)
        .execute()
    )

    if not res.data:
        st.error('Subject Code not found!')
        if st.button('Close'):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]

    check = (
        client.table('subject_students')
        .select('student_id')
        .eq('subject_id', subject['subject_id'])
        .eq('student_id', student_id)
        .limit(1)
        .execute()
    )
    if check.data:
        st.info('Youre already enrolled!')
        if st.button('Got it!'):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f'Would you like to enroll in **{subject['name']}**?')

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Yes enroll now!', type='primary', width='stretch'):
            try:
                enroll_student_to_subject(subject['subject_id'], student_id)
            except ValueError as error:
                st.info(str(error))
                return
            except Exception as error:
                st.error(f"Could not enroll in this subject: {error}")
                return

            st.success('Joined successfully!')
            st.query_params.clear()
            st.rerun()
