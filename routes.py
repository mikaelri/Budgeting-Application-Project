"""module app to run the app.py file and flask used to handle the routing of the application"""
from flask import render_template, redirect, request, session, flash, url_for
from app import app
import users, budgets, userbudgets, services.budgetservice, services.userservice

@app.route('/')
def index():
    """Function for index page"""
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def create_user():
    """Function handling when a new user is created"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        services.userservice.check_csrf()

        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form ["password2"]
        role = request.form["role"]

        if len(username) < 1 or len(username) > 25:
            return render_template("error.html", message="Username should be between 1-25 characters.")
        
        if users.user_exists(username):
            return render_template("error.html", message="Username is already taken.")
        
        if len(password1) < 5 or len(password1) > 25:
            return render_template("error.html", message="Password should be between 5-25 characters.")
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
        return render_template("error.html", message="Wrong username, password or no user created.")
    
    """store the user role in session if the login was succesful"""
    user_id = session.get("user_id")
    user_role = users.get_user_role(user_id)
    if user_role:
        session["role"] = user_role
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
        services.userservice.check_csrf()

        name = request.form["name"]
        if len(name) < 1 or len(name) > 25:
            flash("Should be between 1-25 characters.")
            return redirect("/budget")

        creator_id = session.get("user_id")
        budget_count = budgets.get_budget_count(creator_id)

        if budgets.budget_exists(name):
            flash("The name of the budget already exists, create a new one.", "error")
            return redirect("/budget")

        if budget_count >= 5:
            flash("You have reached the maximum limit of 5 budgets.", "error")
            return redirect("/budget")

        if budgets.new_budget(name, creator_id): 
            flash("Budget created successfully!", "success")
            return redirect("/budget")
        else:
            flash("Failed to create the budget, try again!")
            return redirect("/budget")

    return render_template("budget.html")

@app.route("/mybudgets", methods=["GET"])
def view_budgets():
    """function to view all personal budgets"""
    creator_id = session.get("user_id")
    budgets_list = budgets.see_budgets(creator_id)

    if len(budgets_list) < 1:
        return render_template("error_transactions.html", 
                               message_transactions="No budgets created yet. Please add a budget.")
        
    return render_template("mybudgets.html", budgets=budgets_list)

@app.route("/transactions", methods=["GET"])
def select_budget():
    """function to select the budget where user wants to add income or expense transactions"""
    budget_id = request.args.get("budget_id")
    selected_budget = budgets.get_budget_id(budget_id)

    return render_template("transactions.html", selected_budget=selected_budget, budget_id=budget_id)

@app.route("/transactions/<int:budget_id>", methods=["GET", "POST"])
def add_new_transactions(budget_id: int):
    """function to add continously transactions to a selected budget"""

    session['budget_id'] = budget_id

    if request.method == "GET":
        budget_id = request.args.get("budget_id")
        if budget_id:
            session['budget_id'] = budget_id
        return render_template("transactions.html")

    if request.method == "POST":
        services.userservice.check_csrf()

        budget_id = session.get('budget_id')
        income = request.form.get("income")
        expense = request.form.get("expense")
        income_category = request.form.get("income_category")
        expense_category = request.form.get("expense_category")
        message = request.form.get("message") 
       
        is_valid, message = services.budgetservice.validate_transaction_fields(income, expense)
        if not is_valid:
            flash(message, "error")
            return redirect(f"/transactions?budget_id={session.get('budget_id')}")

        if userbudgets.add_transaction(budget_id, income, expense, income_category, 
                                       expense_category, message):
            flash("Transaction added succesfully!", "success")
            return redirect(f"/transactions?budget_id={session.get('budget_id')}")
        else:
            flash("Failed to add transaction. The entered amount exceeds the maximum limit of 2 147 483 647.", 
                  "error")
            return redirect(f"/transactions?budget_id={session.get('budget_id')}")
        
    return render_template("transactions.html", budget_id=budget_id)

@app.route("/netresult", methods=["GET"])
def view_net_result():
    """function to show the net result for selected budget"""
    budget_id = request.args.get("budget_id")
        
    budget_id = int(budget_id)
    select_budget = budgets.get_budget_id(budget_id)
    
    net_result = userbudgets.calculate_net_result(budget_id)

    return render_template("netresult.html", 
                           selected_budget=select_budget, budget_id=budget_id, net_result=net_result)

@app.route("/admin", methods=["GET", "POST"])
def admin_list():
    """Route to admin user page and functionalities"""
    if request.method == "GET":
        user_id = session.get("user_id")
        user_role = users.get_user_role(user_id)
        if user_role and user_role == 2:
            all_users = users.get_user_list()
            all_budgets = userbudgets.get_all_budgets() 
            return render_template("admin.html", users=all_users, budgets=all_budgets)
        else:
            flash("Access denied. The page is only for admin users.", "error")
            return redirect("/login")
           
    """Remove existing budget if there is at least 1 budget created"""
    if request.method == "POST":
        services.userservice.require_role(2)
        services.userservice.check_csrf()

        creator_id = session.get("user_id")
        budget_count = budgets.get_budget_count(creator_id)

        budget_id = request.form.get("budget_id")
        success = userbudgets.delete_budget(budget_id)

        if not budget_count:
            flash ("No budgets to delete.", "error")        
            return redirect("/admin")   
        
        elif success:
            flash ("Budget was removed successfully!", "success") 
            return redirect("/admin")     

@app.route("/usersearch", methods= ["GET"])
def search_transactions():
    """Routes to usersearch page and functionalities"""
    budget_id = request.args.get("budget_id")
        
    budget_id = int(budget_id)
    select_budget = budgets.get_budget_id(budget_id)

    return render_template("usersearch.html", 
                           selected_budget=select_budget, budget_id=budget_id)

    
