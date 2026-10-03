import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_bg_home
def home_screen():

    header_home()
    style_bg_home()
    style_base_layout()

    st.markdown(
        """
        <style>
            [data-testid="stHorizontalBlock"] > div {
                display: flex;
                flex-direction: column;
            }

            .role-card {
                background: rgba(255, 255, 255, 0.16);
                border-radius: 30px;
                padding: 1.5rem 1.25rem 1.25rem;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.05);
                margin-top: 0.5rem;
                width: 100%;
                min-height: 430px;
                height: 100%;
            }

            .role-title {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 4rem !important;
                line-height: 0.82 !important;
                letter-spacing: -0.06em;
                color: #2e3143 !important;
                margin: 0 0 1rem 0;
                text-align: left;
            }

            .role-figure {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0.25rem 0 1.5rem;
                flex: 1;
            }

            .role-figure img {
                max-width: 180px;
                width: 100%;
                height: auto;
                display: block;
            }

            .portal-button-wrap {
                margin-top: auto;
                width: 100%;
            }

            .portal-button-wrap button {
                width: 100% !important;
                border-radius: 999px !important;
                background-color: #5865F2 !important;
                color: white !important;
                border: none !important;
                padding: 0.95rem 1.3rem !important;
                font-size: 1.1rem !important;
                font-weight: 700 !important;
                box-shadow: none !important;
                min-height: 62px !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                gap: 0.5rem !important;
                cursor: pointer !important;
            }

            .portal-button-wrap button:hover {
                transform: scale(1.02);
                opacity: 0.98;
            }

            .portal-button-wrap button:focus,
            .portal-button-wrap button:active {
                outline: none !important;
                box-shadow: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large", vertical_alignment="top")

    with col1:
        st.markdown(
            """
            <div class="role-card">
                <div class="role-title">I’m<br>Student</div>
                <div class="role-figure">
                    <img src="https://i.ibb.co/844D9Lrt/mascot-student.png" alt="Student mascot" />
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="portal-button-wrap">', unsafe_allow_html=True)
        if st.button('Student Portal ↗', key='student_portal', use_container_width=True):
            st.session_state['login_type'] = 'student'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div class="role-card">
                <div class="role-title">I’m<br>Teacher</div>
                <div class="role-figure">
                    <img src="https://i.ibb.co/CsmQQV6X/mascot-prof.png" alt="Teacher mascot" />
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="portal-button-wrap">', unsafe_allow_html=True)
        if st.button('Teacher Portal ↗', key='teacher_portal', use_container_width=True):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
