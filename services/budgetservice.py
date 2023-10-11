"""service function for sql query"""
def process_fields(income, expense, income_category, expense_category, message):
    """function to process and validate transaction fields"""
    income = 0 if not income or income.strip() == "" else income
    expense = 0 if not expense or expense.strip() == "" else expense
    income_category = "Not selected" if not income_category or income_category.strip() == "" else income_category
    expense_category = "Not selected" if not expense_category or expense_category.strip() == "" else expense_category
    message = "Not selected" if not message or message.strip() == "" else message
    
    return income, expense, income_category, expense_category, message