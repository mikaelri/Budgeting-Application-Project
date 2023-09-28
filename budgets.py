#module to handle when budget is created
from db import db
from sqlalchemy import text

def new_budget(name, creator_id, income, expense, income_category, expense_category, message):
    """function for creating a new budget"""
    try:
        if income == "":
            income = None
        if expense == "":
            expense = None
        if income_category == "":
            income_category = None
        if expense_category == "":
            expense_category = None

        sql = text(
            """INSERT INTO budgets (name, creator_id, income, expense, 
            income_category, expense_category, message)
            VALUES(:name, :creator_id, :income, :expense, 
            :income_category, :expense_category, :message)""")

        db.session.execute(sql, {"name": name, "creator_id": creator_id, "income": income, 
                                "expense": expense, "income_category": income_category,
                                "expense_category": expense_category, "message": message})
        db.session.commit()
        return True
    except:
        return False

def budget_exists(name):
    """function to check if username exists"""
    sql = text("SELECT name from budgets WHERE name=:name")
    result = db.session.execute(sql, {"name": name})
    existing_budget = result.fetchone()

    if existing_budget:
        return True
    else:
        return False

def see_budgets(creator_id):
    """function to view budgets"""
    sql = text("SELECT id, name FROM budgets WHERE creator_id=:creator_id")
    result = db.session.execute(sql, {"creator_id":creator_id})
    budgets = result.fetchall()
    return budgets

def get_budget_count(creator_id):
    """function to count the budgets per user"""
    sql = text("SELECT COUNT(*) FROM budgets WHERE creator_id = :creator_id")
    result = db.session.execute(sql, {"creator_id": creator_id})
    count = result.scalar()
    return count

def get_budget_id(budget_id):
    """function to get the budget id's. Used in select_budget"""
    sql = text("SELECT id, name FROM budgets WHERE id=:budget_id")
    result = db.session.execute(sql, {"budget_id":budget_id})
    budget = result.fetchone()
    return budget