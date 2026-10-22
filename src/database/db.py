import streamlit as st
from src.database.config import create_subject_client, supabase
import bcrypt # for hashing password

def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

def check_pass(pwd, hased):
    return bcrypt.checkpw(pwd.encode(), hased.encode())

def check_teacher_exist(username):
    # check for unique usename, returns false when username is already taken
    response = supabase.table("teachers").select("user_name").eq("user_name", username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
    data = {"user_name": username, "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data

def teacher_login(username, password):
    response = supabase.table("teachers").select("*").eq("user_name", username).execute()
    if (response.data):
        teacher = response.data[0]
        if check_pass(password, teacher["password"]):
            return teacher
    return None

def get_all_students():
    response = supabase.table('students').select('*').execute()
    return response.data

def create_student(new_name, face_embedding = None, voice_embedding = None):
    data = {"name": new_name, "face_embedding": face_embedding, "voice_embedding": voice_embedding}
    response = supabase.table("students").insert(data).execute()
    return response.data

def _require_current_teacher(teacher_id):
    current_teacher = st.session_state.get("teacher_data")
    current_teacher_id = current_teacher.get("teacher_id") if current_teacher else None
    if (
        current_teacher_id is None
        or teacher_id is None
        or str(current_teacher_id) != str(teacher_id)
    ):
        raise PermissionError("You are not authorized to access subjects for this teacher.")

def create_subject(sub_id, sub_name, section, teacher_id):
    _require_current_teacher(teacher_id)
    data = {"subject_code": sub_id, "name": sub_name, "section": section, "teacher_id": teacher_id}
    response = create_subject_client().table("subjects").insert(data).execute()
    return response.data

def get_teacher_subjects(teacher_id):
    _require_current_teacher(teacher_id)
    response = create_subject_client().table("subjects").select("*, subject_students(count), attendence_logs(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get('count', 0) if sub.get('subject_students') else 0
        attendance = sub.get('attendence_logs', [])
        unique_sessions = len(set(log['timestamp'] for log in attendance))
        sub['total_classes'] = unique_sessions

        sub.pop('subject_students', None)
        sub.pop('attendence_logs', None)

    return subjects