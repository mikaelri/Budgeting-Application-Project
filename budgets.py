from db import db
from sqlalchemy import text

def new_budget(name, creator_id):
    """function for creating a new budget"""
    try:
        sql = text(
            """INSERT INTO budgets (name, creator_id)
            VALUES(:name, :creator_id)""")
        db.session.execute(
            sql, {"name": name, "creator_id": creator_id})
        db.session.commit()
        return True  # Return True on success
    except:
        return False

def see_budgets(creator_id):
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