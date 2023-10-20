"""module app to run the app.py file and flask used to handle the routing of the application"""
from flask import render_template, redirect, request, session, flash, url_for
from app import app
import users, budgets, user_budgets, category_search, services.budget_service, services.user_service

@app.route('/')
def index():
    """Function routing to login page"""
    return redirect("/login")

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
            flash("Username should be between 1-25 characters.")
            return render_template("register.html")
    
        if users.user_exists(username):
            flash("Username is already taken.")
            return render_template("register.html")
    
        if len(password1) < 5 or len(password1) > 25:
            flash("Password should be between 5-25 characters.")
            return render_template("register.html")
        if password1 != password2:
            flash("Given passwords are not the same.")
            return render_template("register.html")
        if password1 == "":
            flash("Password is empty.")
            return render_template("register.html")

        if role not in ("1", "2"):
            flash("Unknown user type.")
            return render_template("register.html")
    
        if not users.create_user(username, password1, role):
            flash("Registration not succesfull, check username and password.")
            return render_template("register.html")
    
        flash("User created succesfully, you can login now!", "success")
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Function handling the login"""
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password1"]

    if not users.login(username, password):
        return render_template("error.html", message="Wrong username, password or no user created.")

    """store the user role and creator_id in session if the login was succesful"""
    user_id = session.get("user_id")
    user_role = users.get_user_role(user_id)
    session["creator_id"] = user_id
    if user_role:
        session["role"] = user_role

    return redirect("/profile")
    
@app.route("/logout")
def logout():
     """Function to log out from your personal pages"""
     users.logout()
     return redirect("/login")

@app.route("/profile", methods=["GET"])
def profile():
    """function to view the profile page"""
    return render_template("profile.html")

@app.route("/profile/admin", methods=["GET", "POST"])
def admin_list():
    """Route to admin user page and functionalities"""
    if request.method == "GET":
        user_id = session.get("user_id")
        user_role = users.get_user_role(user_id)
        if user_role and user_role == 2:
            all_users = users.get_user_list()
            all_budgets = user_budgets.get_all_budgets() 
            return render_template("admin.html", users=all_users, budgets=all_budgets)
        else:
            flash("Access denied. The page is only for admin users.", "error")
            return redirect("/profile")
           
    """Remove existing budget if exists"""
    if request.method == "POST":
        services.user_service.require_role(2)
        services.user_service.check_csrf()

        budget_id = request.form.get("budget_id")

        creator_id = user_budgets.get_budget_creator(budget_id)
        creator_name = users.get_username(creator_id)

        budget_exists = user_budgets.check_budget_exists(budget_id)
        if not budget_exists:
            flash ("No budgets to delete.", "error")  
            return redirect("/profile/admin")  

        success = user_budgets.delete_budget(budget_id)
        if success:
            flash (f"Budget was removed successfully! You deleted a budget from username {creator_name}", "success") 
            return redirect("/profile/admin")     
        else:
            flash ("Failed to delete the budget, try again.", "error")  
            return redirect("/profile/admin")  

@app.route("/profile/newbudget", methods=["GET", "POST"])
def create_new_budget():
    """function handling to create a new budget"""
    if request.method == "GET":
        return render_template("new_budget.html")

    if request.method == "POST":
        services.user_service.check_csrf()

        name = request.form["name"]
        if len(name) < 1 or len(name) > 25:
            flash("Should be between 1-25 characters.")
            return redirect("/profile/newbudget")

        creator_id = session.get("user_id")
        budget_count = budgets.get_budget_count(creator_id)

        if budgets.budget_exists(name):
            flash("The name of the budget already exists, create a new one.", "error")
            return redirect("/profile/newbudget")

        if budget_count >= 5:
            flash("You have reached the maximum limit of 5 budgets.", "error")
            return redirect("/profile/newbudget")

        if budgets.new_budget(name, creator_id): 
            flash("Budget created successfully, you can now add transactions to it!", "success")
            return redirect("/profile")
        else:
            flash("Failed to create the budget, try again!")
            return redirect("/profile/newbudget")

    return render_template("new_budget.html")

@app.route("/profile/mybudgets", methods=["GET"])
def view_budgets():
    """function to view all personal budgets"""
    creator_id = session.get("user_id")
    budgets_list = budgets.see_budgets(creator_id)

    #store the budget_id in session for GET or POST
    if 'budget_id' in request.args:
        budget_id = request.args.get('budget_id')
        session['budget_id'] = budget_id
    elif 'budget_id' in request.form:
        budget_id = request.form['budget_id']
        session['budget_id'] = budget_id

    if len(budgets_list) < 1:
        return render_template("error_transactions.html", 
                               message_transactions="No budgets created yet. Please add a budget.")
            
    return render_template("my_budgets.html", budgets=budgets_list)

@app.route("/profile/mybudgets/addtransactions", methods=["GET", "POST"])
def add_new_transactions():
    """add transactions to a selected budget"""   
     
    #get the budget id from session and select it for front-end in html view
    budget_id = session.get("budget_id")
    selected_budget = budgets.get_budget_id(budget_id)

    #check that the session creator is the creator of the budget
    creator_id = session.get("user_id")
    if selected_budget.creator_id != creator_id:
        flash("Error, please use the budgets you have created")
        return redirect("/profile/mybudgets")
    
    if request.method == "POST":
        services.user_service.check_csrf()

        income = request.form["income"]
        expense = request.form["expense"]
        income_category = request.form["income_category"]
        expense_category = request.form["expense_category"]
        message = request.form.get("message") 
       
        #process the add transaction form so that all necessary fields are added
        is_valid, error_message = services.budget_service.validate_fields(income, expense, 
                                    income_category, expense_category)
        if not is_valid:
            flash(error_message, "error")
            return redirect(f"/profile/mybudgets/addtransactions?budget_id={budget_id}")
                
        # add the transaction if all of the mandatory fields where added
        if user_budgets.add_transaction(budget_id, income, expense, income_category, 
                                       expense_category, message):
            flash("Transaction added succesfully!", "success")
            return redirect("/profile/mybudgets")
            
    return render_template("add_transactions.html", selected_budget=selected_budget)

@app.route("/profile/mybudgets/netresult", methods=["POST"])
def view_net_result():
    """function to show the net result for selected budget"""
    services.user_service.check_csrf()
    budget_id = request.form.get("budget_id")
    select_budget = budgets.get_budget_id(budget_id)
    net_result = user_budgets.calculate_net_result(budget_id)

    return render_template("net_result.html", 
                           selected_budget=select_budget, budget_id=budget_id, 
                           net_result=net_result)

@app.route("/profile/mybudgets/searchtransactions", methods= ["POST"])
def route_search():
    """Routes to category search page and functionalities""" 
    services.user_service.check_csrf()
    budget_id = request.form.get('budget_id')
    session['budget_id'] = budget_id

    income_category = category_search.view_income_category(budget_id)
    expense_category = category_search.view_expense_category(budget_id)
        
    select_budget = budgets.get_budget_id(budget_id)

    return render_template("search_transactions.html", 
                        selected_budget=select_budget, budget_id=budget_id, 
                        income_category=income_category, expense_category=expense_category)


@app.route("/profile/mybudgets/searchtransactions/category", methods= ["GET"])
def search_transactions():
    """Routes to categorylisting page and shows the transactions for selected category"""
    budget_id = session.get('budget_id')
    category = request.args.get("category")
    select_budget = budgets.get_budget_id(budget_id)

    if category:
        transactions = category_search.search_by_category(budget_id, category)
        return render_template("category.html", transactions=transactions, 
                               selected_budget=select_budget, category=category)
    


    