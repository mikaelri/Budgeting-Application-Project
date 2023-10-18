"""service function for sql query"""
def process_fields(income, expense, income_category, expense_category, message):
    """function to process and validate transaction fields"""
    income = 0 if not income or income.strip() == "" else income
    expense = 0 if not expense or expense.strip() == "" else expense
    income_category = "Not selected" if not income_category or income_category.strip() == "" else income_category
    expense_category = "Not selected" if not expense_category or expense_category.strip() == "" else expense_category
    message = "Not selected" if not message or message.strip() == "" else message
    
    return income, expense, income_category, expense_category, message

def validate_transaction_fields(income, expense):
    """function to validate the transaction fields form."""
    if not income and not expense:
        return False, "Failed to submit the transaction, either income or expense has to be added."
    
    try:
        #handling if the integer is negative or in case of value errors
        if (income and float(income) < 0) or (expense and float(expense) < 0):
            return False, "Negative values cannot be used when adding transactions."
    except ValueError:
        return False, "Please provide valid numbers for income or expense."

    return True, ""

def validate_category(income, expense, income_category, expense_category):
    if (income and not income_category) or (expense and not expense_category):
        return False, "Failed to submit the transaction, please select income or expense and related category."
    
    return True, ""