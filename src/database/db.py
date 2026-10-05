from src.database.config import supabase
import bcrypt # for hashing logins


def check_teacher_exist(username):
    # check for unique usename, returns false when username is already taken
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0

def create_teacher(username, password, name):
