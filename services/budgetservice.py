def empty(income, expense, income_category, expense_category, message):
    income = 0 if income in ["", " "] else income
    expense = 0 if expense in ["", " "] else expense
    income_category = "Not selected" if income_category in ["", " "] else income_category
    expense_category = "Not selected" if expense_category in ["", " "] else expense_category
    message = "Not selected" if message in ["", " "] else message
    
    return income, expense, income_category, expense_category, message