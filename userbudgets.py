#module to handle users budget functions from the user view
from db import db
from sqlalchemy import text
import services.budgetservice as budgetservice


def add_transaction(budget_id: int, income: int, expense:int, income_category: str, 
                    expense_category: str, message: str):
    """function to add transactions continuously to selected budget"""

    try:
        income, expense, income_category, expense_category, message = budgetservice.process_fields(
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

def calculate_net_result(budget_id: int):
    """function to calculate the net result and inserting it to results table"""

    try:
    # First get the total of income and expense from transactions table
        sql_sum_income = text(""" 
        SELECT budget_id, sum(income) AS total_income from transactions where budget_id=:budget_id
        GROUP BY budget_id
                              """)
        
        sql_sum_expense = text(""" 
        SELECT budget_id, sum(expense) AS total_expense from transactions where budget_id=:budget_id
        GROUP BY budget_id
                               """)

        income_result = db.session.execute(sql_sum_income, {"budget_id": budget_id}).first()
        expense_result = db.session.execute(sql_sum_expense, {"budget_id": budget_id}).first()

        total_income = income_result.total_income if income_result else 0
        total_expense = expense_result.total_expense if expense_result else 0

        net_result = total_income - total_expense

        sql_check_existing = text("SELECT budget_id FROM results WHERE budget_id=:budget_id")
        existing_result = db.session.execute(sql_check_existing, {"budget_id": budget_id}).first()

        # Second, update or add the result to results table
        if existing_result:
            # Update records if there is already data stored
            sql_update = text("""
            UPDATE results SET total_income=:total_income, total_expense=:total_expense, 
            net_result=:net_result WHERE budget_id=:budget_id""")

            db.session.execute(sql_update, {
                "total_income": total_income, 
                "total_expense": total_expense, 
                "net_result": net_result, 
                "budget_id": budget_id
            })
        else:
            # Add new record if there is no data stored
            sql_insert = text("""
            INSERT INTO results (budget_id, total_income, total_expense, net_result) 
            VALUES (:budget_id, :total_income, :total_expense, :net_result)
                              """)
            
            db.session.execute(sql_insert, {
                "budget_id": budget_id, 
                "total_income": total_income,
                "total_expense": total_expense, 
                "net_result": net_result
            })

        db.session.commit()

        return net_result  #returns the net result so routes.py can handle it to html
    except:
        False

def get_all_budgets():
    """function to get all the budgets for selected user"""
    sql = text("SELECT id, name FROM budgets")
    result = db.session.execute(sql)
    all_budgets = result.fetchall()
    return all_budgets

def delete_budget(budget_id: int):
    """function for admin users to delete a budget"""

    try:
        """delete first the transactions table data for selected budget_id"""
        sql_transactions = text("DELETE from transactions WHERE budget_id=:budget_id")
        db.session.execute(sql_transactions, {"budget_id": budget_id})

        """delete second the results table data for selected budget_id"""
        sql_results = text("DELETE from results where budget_id=:budget_id")
        db.session.execute(sql_results, {"budget_id": budget_id})

        """delete last the the budgets table data for selected id"""
        sql_budgets = text("DELETE from budgets where id=:budget_id")
        db.session.execute(sql_budgets, {"budget_id":budget_id})
        db.session.commit()

        return True
    except:
        return False
    

