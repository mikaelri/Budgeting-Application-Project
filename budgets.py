#module to handle when budget is created + other supporting functions for budgets
from db import db
from sqlalchemy import text

def new_budget(name: str, creator_id: int):
    """function for creating a new budget"""
    try:
        sql = text("INSERT INTO budgets (name, creator_id) VALUES(:name, :creator_id)")
        db.session.execute(sql, {"name": name, "creator_id": creator_id})
        db.session.commit()
        return True
    except:
        return False

def budget_exists(name: str):
    """function to check if username exists"""
    sql = text("SELECT name from budgets WHERE name=:name")
    result = db.session.execute(sql, {"name": name})
    existing_budget = result.fetchone()

    if existing_budget:
        return True
    else:
        return False

def see_budgets(creator_id: int):
    """function to view budgets"""
    sql = text("SELECT id, name FROM budgets WHERE creator_id=:creator_id")
    result = db.session.execute(sql, {"creator_id":creator_id})
    budgets = result.fetchall()
    return budgets

def get_budget_count(creator_id: int):
    """function to count the budgets per user"""
    sql = text("SELECT COUNT(*) FROM budgets WHERE creator_id = :creator_id")
    result = db.session.execute(sql, {"creator_id": creator_id})
    count = result.scalar()
    return count

def get_budget_id(budget_id: int):
    """function to get the budget id's. Used in select_budget function"""
    sql = text("SELECT id, name FROM budgets WHERE id=:budget_id")
    result = db.session.execute(sql, {"budget_id":budget_id})
    budget = result.fetchone()
    return budget