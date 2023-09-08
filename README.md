**BUDGETING APPLICATION PROJECT**

***Background***

The idea of the budgeting application is that a user can create own budget, where it is possible to track income (i.e. salary, study grant) and expenses (i.e. rent, mortgage, electricity, groceries).

One example for the use case is that user can create an individual budget and to follow monthly income and expenses to see what is the net result for the month. 

The application will use a ready-to-use categories for income and expenses. This is for the reason that it helps the user to group, sort and analyze transactions.

- **Income:** *Salary, Study grant, Miscellanous income*
- **Expenses:** *Rent, Mortgage, Interest for mortgage, Travel, Groceries, Restaurant & Food,  Miscellanous expenses*

Miscellanous expenses could be i.e. Mobile phone bill, membership fees or electricity. The idea is that the user can add any income or expense even if there is not a category for this. 
If there is no category the user can write a message related to the expense.

Please not this is not the only use case for the application. The application could be used also only for expenses, thus, one other example could be a holiday trip for some group. This application could help to track down the fixed costs already known (or something to add during the trip) such as (flight,hotel, activity costs).

***Application functionalities***

1. User can log in and out and create a new user account
2. User can see a list of own individual budgets when logging in and a net result of the budgets (income - expenses) and the time when the budget was previously modified
3. User can select which budgets to view and/or modify from the front page
4. User can create a new budget (and at the same time add already new income or expenses, see below)
5. User can continously add income and expense transactions to the budget with a message and category
6. User can search income and expenses related to specific word or category (i.e. Salary or Rent)
7. Admin user can delete existing user accounts and add new admin users
8. Admin user can see a list of user accounts

***Database tables*** **(to be updated)**
1. Users
2. Budgets for the users
3. Income transactions (+)
4. Expense transacionts (-)
5. Income and expense transactions
6. Transactions based on category (See criterias above)
7. Transactions based on a word