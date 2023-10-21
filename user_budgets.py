#module to handle users budget functions from the user view
from db import db
from sqlalchemy import text
import services.budget_service

def add_transaction(budget_id: int, income: int, expense:int, income_category: str, 
                    expense_category: str, message: str):
    """Function to add transactions continuously to selected budget"""

    try:
        income, expense, income_category, expense_category, message = services.budget_service.process_fields(
        income, expense, income_category, expense_category, message)
        
        sql = text("""
                   INSERT INTO transactions (budget_id, income, expense, 
                   income_category, expense_category, message)
                   VALUES(:budget_id, :income, :expense, :income_category, 
                   :expense_category, :message)
                   """)
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
    
def get_total_income(budget_id:int):
    sql_sum_income = text(""" 
                          SELECT budget_id, sum(income) AS total_income FROM transactions 
                          WHERE budget_id=:budget_id
                          GROUP BY budget_id
                          """)
    
    income_result = db.session.execute(sql_sum_income, {"budget_id": budget_id}).first()
    total_income = income_result.total_income if income_result else 0
    return total_income

def get_total_expense(budget_id:int):
    sql_sum_expense = text(""" 
                           SELECT budget_id, sum(expense) AS total_expense 
                           FROM transactions 
                           WHERE budget_id=:budget_id
                           GROUP BY budget_id
                           """)
    
    expense_result = db.session.execute(sql_sum_expense, {"budget_id": budget_id}).first()
    total_expense = expense_result.total_expense if expense_result else 0
    return total_expense


def calculate_net_result(budget_id: int):
    """Function to calculate the net result and inserting it to results table"""

    try:
    # First get the total of income and expense from transactions table
        total_income = get_total_income(budget_id)
        total_expense = get_total_expense(budget_id)
        net_result = total_income - total_expense

        sql_check_existing = text("SELECT budget_id FROM results WHERE budget_id=:budget_id")
        existing_result = db.session.execute(sql_check_existing, {"budget_id": budget_id}).first()

        # Second, update or add the result to results table
        if existing_result:
            # Update records if there is already data stored
            sql_update = text("""
                              UPDATE results SET 
                              total_income=:total_income, 
                              total_expense=:total_expense, 
                              net_result=:net_result WHERE budget_id=:budget_id
                              """)

            db.session.execute(sql_update, {
                "total_income": total_income, 
                "total_expense": total_expense, 
                "net_result": net_result, 
                "budget_id": budget_id
            })
        else:
            # Add new record if there is no data stored
            sql_insert = text("""
                              INSERT INTO results
                              (budget_id, total_income, total_expense, net_result) 
                              VALUES 
                              (:budget_id, :total_income, :total_expense, :net_result)
                              """)
            
            db.session.execute(sql_insert, {
                "budget_id": budget_id, 
                "total_income": total_income,
                "total_expense": total_expense, 
                "net_result": net_result
            })

        db.session.commit()

        return net_result  # Returns the net result so routes.py can handle it to html
    except:
        False

def get_all_budgets():
    """Function to get all the budgets for selected user"""
    sql = text("SELECT id, name FROM budgets")
    result = db.session.execute(sql)
    all_budgets = result.fetchall()
    return all_budgets

def delete_budget(budget_id: int):
    """Function for admin users to delete a budget"""
    try:
        # Delete first the transactions table data for selected budget_id
        sql_transactions = text("DELETE FROM transactions WHERE budget_id=:budget_id")
        db.session.execute(sql_transactions, {"budget_id": budget_id})

        # Delete second the results table data for selected budget_id
        sql_results = text("DELETE FROM results WHERE budget_id=:budget_id")
        db.session.execute(sql_results, {"budget_id": budget_id})

        # Delete last the the budgets table data for selected id
        sql_budgets = text("DELETE FROM budgets WHERE id=:budget_id")
        db.session.execute(sql_budgets, {"budget_id":budget_id})
        db.session.commit()

        return True
    except:
        return False
    
def check_budget_exists(budget_id: int):
    """Function to check if budget exists"""
    sql = text("SELECT id FROM budgets WHERE id=:budget_id")
    result = db.session.execute(sql, {"budget_id": budget_id})
    existing_budget = result.fetchone()

    if existing_budget:
        return True

def get_budget_creator(budget_id: int):
    """Function to get the creator of a budget based on ID"""
    sql = text("SELECT creator_id FROM budgets WHERE id=:budget_id")
    result = db.session.execute(sql, {"budget_id": budget_id})
    creator = result.fetchone()
    if creator:
        return creator[0]
    else:
        return None
