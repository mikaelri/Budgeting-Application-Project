"""module os for database url fetching, app to run the app and sql for DB creation"""
from flask import Flask
from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
# End-of-file (EOF)
