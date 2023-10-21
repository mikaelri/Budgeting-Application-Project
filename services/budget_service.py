"""Module to support exception situations for other modules functions"""

def process_fields(income, expense, income_category, expense_category, message):
    # Function to process and validate transaction fields in SQL query
    income = 0 if not income or income.strip() == "" else income
    expense = 0 if not expense or expense.strip() == "" else expense
    income_category = "Not selected" if not income_category or income_category.strip() == "" else income_category
    expense_category = "Not selected" if not expense_category or expense_category.strip() == "" else expense_category
    message = "Not selected" if not message or message.strip() == "" else message
    
    return income, expense, income_category, expense_category, message

def validate_fields(income, expense, income_category, expense_category):
    # Function to validate fields in the add transaction form
    if not income and not expense:
        return False, "Failed to submit the transaction, either income or expense has to be added."

    elif (income and float(income) < 0) or (expense and float(expense) < 0):
        return False, "Negative values cannot be used when adding transactions."
    
    elif (income and float(income) > 2147483647) or (expense and float(expense) > 2147483647):
        return False, "Failed to add transaction. The entered amount exceeds the maximum limit of 2 147 483 647."
    
    elif (income and not income_category) or (expense and not expense_category):
        return False, "Failed to submit the transaction, please select income and/or expense and related categories."
    
    return True, ""