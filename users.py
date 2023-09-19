"""modules to create user log-in requirements"""
import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash

def login(username, password):
    """login function for database"""

def register(username, password, role):
    """function for registering a new user to database"""
    hash_value = generate_password_hash(password)



