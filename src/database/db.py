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

def _require_current_student(student_id):
    current_student = st.session_state.get("student_data")
    current_student_id = current_student.get("student_id") if current_student else None
    if (
        current_student_id is None
        or student_id is None
        or str(current_student_id) != str(student_id)
    ):
        raise PermissionError("You are not authorized to access enrollment for this student.")

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

def get_subject_enrolled_students(subject_id):
    teacher = st.session_state.get("teacher_data")
    teacher_id = teacher.get("teacher_id") if teacher else None
    _require_current_teacher(teacher_id)

    client = create_subject_client()
    subject_response = (
        client.table("subjects")
        .select("subject_id")
        .eq("subject_id", subject_id)
        .eq("teacher_id", teacher_id)
        .limit(1)
        .execute()
    )
    if not subject_response.data:
        raise PermissionError("You are not authorized to view enrollment for this subject.")

    response = (
        client.table("subject_students")
        .select("*, students(*)")
        .eq("subject_id", subject_id)
        .execute()
    )
    return response.data

def enroll_student_to_subject(subject_id, student_id):
    _require_current_student(student_id)
    client = create_subject_client()
    check = (
        client.table("subject_students")
        .select("student_id")
        .eq("subject_id", subject_id)
        .eq("student_id", student_id)
        .limit(1)
        .execute()
    )
    if check.data:
        raise ValueError("You are already enrolled in this subject.")

    data = {"subject_id": subject_id, "student_id": student_id}
    response = client.table("subject_students").insert(data).execute()
    return response.data

def enroll_student_by_code(subject_code, student_id):
    _require_current_student(student_id)
    client = create_subject_client()
    response = (
        client.table("subjects")
        .select("subject_id, name, subject_code, section")
        .eq("subject_code", subject_code.strip())
        .limit(1)
        .execute()
    )
    if not response.data:
        raise ValueError("No subject was found with that code.")

    subject = response.data[0]
    enroll_student_to_subject(subject["subject_id"], student_id)
    return subject

def unenroll_student_to_subject(subject_id, student_id):
    _require_current_student(student_id)
    response = create_subject_client().table("subject_students").delete().eq("subject_id", subject_id).eq("student_id", student_id).execute()
    return response.data

def get_student_subjects(student_id):
    _require_current_student(student_id)
    response = create_subject_client().table("subject_students").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data

def get_student_attendance(student_id):
    _require_current_student(student_id)
    response = create_subject_client().table("attendence_logs").select("*, subjects(*)").eq("student_id", student_id).execute()
    return response.data

def create_attendance(logs):
    response = supabase.table("attendence_logs").insert(logs).execute()
    return response.data