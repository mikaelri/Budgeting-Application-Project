"""modules to create user log-in requirements"""
import os
from db import db
from flask import abort, request, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
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

def create_user(username, password, role):
    """function for registering a new user to database"""
    hash_value = generate_password_hash(password)
    try:
        sql = text(
            """INSERT INTO users (username, password, role) 
            VALUES (:username, :password, :role)""")
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    
    return login(username, password)

def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)