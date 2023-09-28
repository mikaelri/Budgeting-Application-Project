"""module app to run the app.py file and flask used to handle the routing of the application"""
from flask import render_template, redirect, request, session, flash, url_for
from app import app
import users
from budgets import new_budget
from budgets import see_budgets
from budgets import get_budget_count
from budgets import get_budget_id
from userbudgets import add_transaction
from userbudgets import get_net_result
from userbudgets import calculate_net_result
from budgets import budget_exists

@app.route('/')
def index():
    """Function creating bullet points in front page"""
    words = [
        "create your own budgets",
        "add income & expense transactions by categories",
        "search transactions by category & word"
        ]
    reasons = [
        "application is free of charge",
        "bugeting made simple",
        "personal savings for the future", 
        "better visibility on your financials", 
        "much more - register now and try!"
        ]
    return render_template('index.html', items1= words, items2=reasons)

@app.route("/register", methods=["GET", "POST"])
def create_user():
    """Function handling when a new user is created"""

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form ["password2"]
        role = request.form["role"]

        if len(username) < 1 or len(username) > 25:
            return render_template("error.html", message="Username should be between 1-25 characters.")
        
        if users.user_exists(username):
            return render_template("error.html", message="Username is already taken.")
        
        if len(password1) < 1 or len(password1) > 25:
            return render_template("error.html", message="Password should be between 1-25 characters.")
        if password1 != password2:
            return render_template("error.html", message="Given passwords are not the same")
        if password1 == "":
            return render_template("error.html", message="Password is empty")
    
        if role not in ("1", "2"):
            return render_template("error.html", message="Unknown user type")
        
        if not users.create_user(username, password1, role):
            return render_template("error.html", message="Registration not succesfull, check username and password")
        
        flash("User created succesfully!", "success")
        return redirect("/register")
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Function handling the log-in"""
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password1"]

    if not users.login(username, password):
        return render_template("error.html", message="Wrong username or password")
    return redirect("/login")

@app.route("/logout")
def logout():
    """Function to log out from your personal pages"""
    users.logout()
    return redirect("/")

@app.route("/budget", methods=["GET", "POST"])
def create_new_budget():
    """function handling to create a new budget"""
    if request.method == "GET":
        flash("", "error")
        return render_template("budget.html")

    if request.method == "POST":
        name = request.form["name"]
        if len(name) < 1 or len(name) > 25:
            flash("Should be between 1-25 characters.")
            return redirect("/budget")

        income = request.form["income"]
        expense = request.form["expense"]
        income_category = request.form["income_category"]
        expense_category = request.form["expense_category"]
        message = request.form["message"] or ""

        if income == "":
            income = None
        if expense == "":
            expense = None

        if income_category == "":
            income_category = None
        if expense_category == "":
            expense_category = None

        creator_id = session.get("user_id")
        budget_count = get_budget_count(creator_id)

        if budget_exists(name):
            flash("The name of the budget already exists, create a new one", "error")
            return redirect("/budget")

        if budget_count >= 5:
            flash("You have reached the maximum limit of 5 budgets.", "error")
            return redirect("/budget")

        if new_budget(name, creator_id, income, expense, income_category, expense_category, message): 
            flash("Budget created successfully!", "success")
            return redirect("/budget")
        else:
            flash("Failed to create the budget, try again!")
            return redirect("/budget")

    return render_template("budget.html")

@app.route("/mybudgets", methods=["GET", "POST"])
def view_budgets():
    """function to view all personal budgets"""
    creator_id = session.get("user_id")
    budgets = see_budgets(creator_id)

    if len(budgets) < 1:
        return render_template("error_transactions.html", 
                               message_transactions="No budgets created yet. Please add a budget.")
        
    return render_template("mybudgets.html", budgets=budgets)

@app.route("/netresult", methods=["GET", "POST"])
def view_net_result():
    """function to route to net result view"""
    budget_id = request.args.get("budget_id")
    selected_budget = get_budget_id(budget_id)

    return render_template("netresult.html", selected_budget=selected_budget)

@app.route("/transactions", methods=["GET", "POST"])
def select_budget():
    """function to select the budget where user wants to add income or expense transactions"""
    budget_id = request.args.get("budget_id")
    selected_budget = get_budget_id(budget_id)

    return render_template("transactions.html", selected_budget=selected_budget)

def add_new_transactions():
    """function to add continously transactions to a selected budget"""

    if request.method == "GET":
        return render_template("transactions.html")

    if request.method == "POST":
        income = request.form["income"]
        expense = request.form["expense"]
        income_category = request.form["income_category"]
        expense_category = request.form["expense_category"]
        message = request.form["message"] or ""
        budget_id = session.get("budget_id")

        if income == "":
            income = None
        if expense == "":
            expense = None
        if income_category == "":
            income_category = None
        if expense_category == "":
            expense_category = None

        if add_transaction(budget_id, income, expense, income_category, expense_category, message):
            flash("Transaction added succesfully!", "success")
            return redirect("/transactions")
        else:
            flash("Failed to add transactions to the budget, try again!")
            return redirect("/transactions")

    return render_template("transactions.html")