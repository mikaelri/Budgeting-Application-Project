"""Module to support creating a new user and security checks"""
from flask import abort, request, session

def user_id():
    return session.get("user_id", 0)

def require_role(role: int):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)