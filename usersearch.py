#module to handle user search functions functions
from db import db
from sqlalchemy import text

def view_income_category(budget_id: int):
    """function to view budgets"""
    sql = text("SELECT DISTINCT income_category as name FROM transactions WHERE budget_id=:budget_id")
    result = db.session.execute(sql, {"budget_id": budget_id})
    income_categories = result.fetchall()
    return income_categories

def view_expense_category(budget_id: int):
    """function to view budgets"""
    sql = text("SELECT DISTINCT expense_category as name FROM transactions WHERE budget_id=:budget_id")
    result = db.session.execute(sql, {"budget_id": budget_id})
    expense_categories = result.fetchall()
    return expense_categories
    
def search_income(budget_id, income_category):
    """function to search transactions based on income category"""
    
    try:
        """search based on income_category"""
        sql_income = text("""SELECT income, income_category, expense, expense_category, 
                          message from transactions WHERE budget_id=:budget_id AND
                          income_category=:income_category""")
        db.session.execute(sql_income, {"budget_id":budget_id, "income_category": income_category})
        db.session.commit
        return True
    except:
        return False

def search_expense(budget_id, expense_category):
    """function to search transactions based on expense category"""
    try:
        sql_income = text("""SELECT income, income_category, expense, expense_category, 
                          message from transactions WHERE budget_id=:budget_id AND
                          expensee_category=:expensee_category""")
        db.session.execute(sql_income, {"budget_id":budget_id, "income_category": expense_category})
        db.session.commit
        return True
    except:
        return False