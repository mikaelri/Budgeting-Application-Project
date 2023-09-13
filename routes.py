"""module app to run the app.py file and flask used to handle the routing of the application"""
from flask import render_template, redirect, request, session
from app import app

#Front page of the application
@app.route('/')
def index():
    """Function creating bullet points in front page"""
    words = [
        'create your own budgets',
        'add income & expense transactions by categories',
        'search transactions by category & word'
        ]
    reasons = [
        'application is free of charge',
        'bugeting made simple',
        'personal savings for the future', 
        'better visibility on your financials', 
        'much more - register now and try!'
        ]
    return render_template('index.html', items1= words, items2=reasons)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    """Function handling the log-in"""
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # TO DO: check username and password
    session['username'] = username
    return render_template("login.html")

@app.route('/logout')
def logout():
    """Function to log out from your personal pages"""
    del session['username']
    return redirect('/')


@app.route('/register', methods = ["GET"])
def register():
    """Function to route to the registration page for sign-up"""
    return render_template("register.html")