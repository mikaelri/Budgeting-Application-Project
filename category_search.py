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
    
def search_by_category(budget_id, category):
    # Adjust this SQL based on your exact database schema.
    sql = text("""SELECT income, income_category, expense, expense_category, 
                    message from transactions WHERE budget_id=:budget_id AND
                    (income_category=:category OR expense_category=:category)""")
    result = db.session.execute(sql, {"budget_id":budget_id, "category": category})
    transactions = result.fetchall()
    return transactions