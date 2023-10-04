#module to handle users budget functions from the user view
from db import db
from sqlalchemy import text
import services.budgetservice as budgetservice


def add_transaction(budget_id: int, income: int, expense:int, income_category: str, 
                    expense_category: str, message: str):
    """function to add transactions continuously to selected budget"""

    try:
        income, expense, income_category, expense_category, message = budgetservice.empty(
        income, expense, income_category, expense_category, message)
        
        sql = text(
            """INSERT INTO transactions (budget_id, income, expense, 
            income_category, expense_category, message)
            VALUES(:budget_id, :income, :expense, :income_category, 
            :expense_category, :message)""")
        db.session.execute(sql, {
                                "budget_id": budget_id,
                                "income": income,
                                "expense": expense,
                                "income_category": income_category,
                                "expense_category": expense_category,
                                "message": message
                                })
        db.session.commit()
        return True
    except:
        return False

def calculate_net_result():
    """function to calculate the net result and updating it to budgets table"""
    try:
        sql_update_result = text(
            """
            UPDATE budgets
            SET result = SUM(income, 0) - COALESCE(expense, 0);
            """
        )
        db.session.execute(sql_update_result)
        db.session.commit()

        return True
    except Exception as e:
        print(e)
        return False

def get_net_result(budget_id):
    """function to retrieve the net result for a selected budget"""
    
    sql = text("SELECT result FROM results WHERE budget_id=:budget_id")
    result = db.session.execute(sql, {"budget_id":budget_id}).scalar()
    
    return result