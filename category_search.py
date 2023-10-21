""" Module to handle user search functions functions"""
from db import db
from sqlalchemy import text

def view_income_category(budget_id: int):
    """Function to view budgets"""
    sql = text("""
               SELECT DISTINCT income_category as name 
               FROM transactions 
               WHERE budget_id=:budget_id
               """)
    
    result = db.session.execute(sql, {"budget_id": budget_id})
    income_categories = result.fetchall()
    return income_categories

def view_expense_category(budget_id: int):
    """Function to view budgets"""
    sql = text("""
               SELECT DISTINCT expense_category as name 
               FROM transactions 
               WHERE budget_id=:budget_id
               """)
    
    result = db.session.execute(sql, {"budget_id": budget_id})
    expense_categories = result.fetchall()
    return expense_categories
    
def search_by_category(budget_id:int, category:str):
    """Function to select transaction categories"""
    sql = text("""
               SELECT income, income_category, expense, expense_category, message 
               FROM transactions 
               WHERE budget_id=:budget_id 
               AND (income_category=:category OR expense_category=:category)
               """)
    
    result = db.session.execute(sql, {"budget_id":budget_id, "category": category})
    transactions = result.fetchall()
    return transactions

def get_category_totals(budget_id:int, category: str):
    """Function to get selected category's total income and expense"""
    sql = text(""" 
               SELECT sum(expense) AS total_expense, sum(income) AS total_income 
               FROM transactions 
               WHERE budget_id=:budget_id 
               AND (income_category=:category OR expense_category=:category)
               """)
    
    result = db.session.execute(sql, {"budget_id": budget_id, 
                                      "category": category}).first()
    
    if result:
        return {"total_income": result.total_income, "total_expense": result.total_expense}
    else:
        return {"total_income": 0, "total_expense": 0}