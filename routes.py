"""module app to run the app.py file and flask used to handle the routing of the application"""
from flask import render_template, redirect, request, session, flash, url_for
from app import app
import users, budgets, userbudgets, usersearch, services.budgetservice, services.userservice

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
            all_budgets = userbudgets.get_all_budgets() 
            return render_template("admin.html", users=all_users, budgets=all_budgets)
        else:
            flash("Access denied. The page is only for admin users.", "error")
            return redirect("/profile")
           
    """Remove existing budget if exists"""
    if request.method == "POST":
        services.userservice.require_role(2)
        services.userservice.check_csrf()

        budget_id = request.form.get("budget_id")

        creator_id = userbudgets.get_budget_creator(budget_id)
        creator_name = users.get_username(creator_id)

        budget_exists = userbudgets.check_budget_exists(budget_id)
        if not budget_exists:
            flash ("No budgets to delete.", "error")  
            return redirect("/profile/admin")  

        success = userbudgets.delete_budget(budget_id)
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
        return render_template("newbudget.html")

    if request.method == "POST":
        services.userservice.check_csrf()

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

    return render_template("newbudget.html")

@app.route("/profile/mybudgets", methods=["GET"])
def view_budgets():
    """function to view all personal budgets"""
    creator_id = session.get("user_id")
    budgets_list = budgets.see_budgets(creator_id)
    if len(budgets_list) < 1:
        return render_template("error_transactions.html", 
                               message_transactions="No budgets created yet. Please add a budget.")
            
    return render_template("mybudgets.html", budgets=budgets_list)

@app.route("/profile/mybudgets/addtransactions", methods=["GET", "POST"])
def add_new_transactions():
    """add transactions to a selected budget"""
    print(request.method) #debug print to be deleted

    #store the budget_id in session
    if 'budget_id' in request.form:
        budget_id = request.form['budget_id']
        session['budget_id'] = budget_id

    #get the budget_id for the session and check that it exists or is valid
    budget_id = session.get("budget_id")
    print("Budget_id:", budget_id) #debug print to be deleted
    if not budget_id:
        flash("Not a valid budget id, please try again")
        return redirect("/profile/mybudgets")
    
    #fetch the budget details for the session budget_id
    selected_budget = budgets.get_budget_id(budget_id)
    if not selected_budget:
        flash("Error, the selected budget does not exist")
        return redirect("/profile/mybudgets")

    #check that the session creator is the creator of the budget
    creator_id = session.get("creator_id")
    print("Session creator_id:", creator_id) #debug print to be deleted
    print("Selected budget's creator_id:", selected_budget.creator_id) #debug print to be deleted
    if selected_budget.creator_id != creator_id:
        flash("Error, please use the budgets you have created")
        return redirect("/profile/mybudgets")
    
    if request.method == "POST":
        print("Inside POST branch")
        services.userservice.check_csrf()

        income = request.form.get("income")
        expense = request.form.get("expense")
        income_category = request.form.get("income_category")
        expense_category = request.form.get("expense_category")
        message = request.form.get("message") 
       
        #must have income or expense inserted
        is_valid, error_message = services.budgetservice.validate_transaction_fields(income, expense)
        if not is_valid:
            print("Validation Result:", is_valid, error_message) #debug print to be deleted
            flash(error_message, "error")
            return redirect("/profile/mybudgets/addtransactions")
        
        #must have income or expense and the associated category
        is_category, error_message = services.budgetservice.validate_category(income, expense, 
                                    income_category, expense_category)
        if not is_category:
            flash(error_message, "error")
            return redirect("/profile/mybudgets/addtransactions")
        
        if userbudgets.add_transaction(budget_id, income, expense, income_category, 
                                       expense_category, message):
            flash("Transaction added succesfully!", "success")
            return redirect("/profile/mybudgets/addtransactions")
        else:
            flash("Failed to add transaction. The entered amount exceeds the maximum limit of 2 147 483 647.", 
                  "error")
            return redirect("/profile/mybudgets/addtransactions")
        
        
    return render_template("addtransactions.html", budget_id=budget_id, selected_budget=selected_budget)












@app.route("/profile/mybudgets/netresult", methods=["POST"])
def view_net_result():
    """function to show the net result for selected budget"""
    services.userservice.check_csrf()
    budget_id = request.form.get("budget_id")
    select_budget = budgets.get_budget_id(budget_id)
    net_result = userbudgets.calculate_net_result(budget_id)

    return render_template("netresult.html", 
                           selected_budget=select_budget, budget_id=budget_id, 
                           net_result=net_result)

@app.route("/profile/mybudgets/searchtransactions", methods= ["POST"])
def route_search():
    """Routes to usersearch page and functionalities""" 
    services.userservice.check_csrf()
    budget_id = request.form.get('budget_id')
    session['budget_id'] = budget_id

    income_category = usersearch.view_income_category(budget_id)
    expense_category = usersearch.view_expense_category(budget_id)
        
    select_budget = budgets.get_budget_id(budget_id)

    return render_template("searchtransactions.html", 
                        selected_budget=select_budget, budget_id=budget_id, 
                        income_category=income_category, expense_category=expense_category)


@app.route("/profile/mybudgets/searchtransactions/category", methods= ["GET"])
def search_transactions():
    """Routes to categorylisting page and shows the transactions for selected category"""
    budget_id = session.get('budget_id')
    category = request.args.get("category")
    select_budget = budgets.get_budget_id(budget_id)

    if category:
        transactions = usersearch.search_by_category(budget_id, category)
        return render_template("category.html", transactions=transactions, 
                               selected_budget=select_budget, category=category)
    


    