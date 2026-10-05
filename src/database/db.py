from src.database.config import supabase
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