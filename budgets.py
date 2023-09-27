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
    
def add_transaction(income, expense, income_category, expense_category, message):
    """function to add transactions continously to selected budget"""

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
            """"INSERT INTO budgets (income, expense, income_category, expense_category, message)
            VALUES(:income, :expense, :income_category, :expense_category, :message)""")
        db.session.execute(sql,{"income":income, "expense":expense, 
                                "income_category":income_category, 
                                "expense_category":expense_category, "message":message})
        db.session.commit()
        return True
    except:
        return False
    
def calculate_net_result():
    """function to calculate the net result and inserting it to results table"""
    try:
        sql = text(
        """INSERT INTO results (budget_id, result)
        SELECT b.id AS budget_id, SUM(b.income - b.expense) AS net_result
        FROM budgets AS b
        GROUP BY b.id""")
        db.session.execute(sql)
        db.session.commit()
        return True
    except:
        return False

def get_net_result(budget_id):
    """function to retrieve the net result for a selected budget"""
    
    sql = text("SELECT result FROM results WHERE budget_id=:budget_id")
    result = db.session.execute(sql, {"budget_id":budget_id}).scalar()
    
    return result

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