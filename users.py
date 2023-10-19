"""modules to create user log-in requirements"""
import os
from db import db
from flask import session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

def login(username: str, password: str):
    """login function for database"""
    sql = text("SELECT password, id, role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_username"] = username
    session["user_role"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    return True

def logout():
    """log-out function for database"""
    del session["user_id"]
    del session["user_username"]
    del session["user_role"]
    del session["budget_id"]
    del session["creator_id"]

def create_user(username: str, password: str, role: int):
    """function for registering a new user to database"""
    hash_value = generate_password_hash(password)
    try:
        sql = text("""
            INSERT INTO users (username, password, role) 
            VALUES (:username, :password, :role)
                   """)
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    
    return login(username, password)

def user_exists(username: str):
    """function to check if username exists"""
    sql = text("SELECT username from users WHERE username=:username")
    result = db.session.execute(sql, {"username": username})
    existing_user = result.fetchone()

    if existing_user:
        return True
    else:
        return False

def get_user_role(user_id: int):
    """function to get the user role for session"""
    sql = text("SELECT role FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id":user_id})
    user = result.fetchone()
    if user:
        return user.role
    return None

def get_user_list():
    """function to get the list of all users and their roles"""
    sql = text("SELECT id, username, role FROM users")
    result = db.session.execute(sql).fetchall()
    return result

def get_username(user_id: int):
    """function to get username based on user id"""
    sql = text("SELECT username FROM users WHERE id=:user_id")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    if result:
        return result[0]
    return None