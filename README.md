**SpendManager - Budgeting application project**

***Background***

The idea of SpendManager application is that a user can create own budget, where it is possible to track income (i.e. salary, study grant) and expenses (i.e. rent, mortgage, electricity, groceries).

One example for the use case is that user can create an individual budget and to follow monthly income and expenses to see what is the net result for the month. 

The application will use a ready-to-use categories for income and expenses. This is for the reason that it helps the user to group, sort and analyze transactions. The category groups for income and expenses are:

- **Income:** *Salary, Study grant, Miscellanous income*
- **Expenses:** *Rent, Mortgage, Interest for mortgage, Travel, Groceries, Restaurant & Food,  Miscellanous expenses*

Miscellanous expenses could be i.e. Mobile phone bill, membership fees or electricity. The idea is that the user can add any income or expense even if there is not a category for this. 
If there is no category the user can write a message related to the expense.

Please note this is not the only use case for the application. The application could be used also only for expenses, thus, one other example could be a holiday trip for some group. This application could help to track down the fixed costs already known (or something to add during the trip) such as flight,hotel, activity costs.

***Application functionalities*** 

- **Functionalities 1,2,3,4 are ready for testing**
- **Functionalities 5,6,7,8,9,10 are not ready for testing**

1. User can log in and out and create a new user account
2. User can view a list of own individual budgets after logging in (only if at least one exists)
3. User can select which budgets to view and/or modify from the list of budgets
4. User can create a new budget and at the same time add already new income or expenses, category and message
5. ~~User can continously add income and expense transactions to the budget with a message and category~~
6. ~~User can view the net result of the selected budget~~
7. ~~User can leave comments to selected budgets~~
8. ~~User can search income and expenses related to specific category (i.e. Salary or Rent)~~
9.  ~~Admin user can delete existing user accounts and add new admin users~~
10. ~~Admin user can see a list of user accounts~~

***Database tables***

- **Database tables 1,2,3 are implemented to schema.sql**
- **Database tables 4,5,6 are not yet implemented to schema.sql**

1. Users
2. Budgets for the users
3. Transactions
4. Individual comments for budgets
5. ~~Transactions based on category (See criterias above)~~

***Installing instructions / how to test the app locally***

**1. Clone this repository to your computer and navigate to the root folder.**

**2. Create .env file to the folder and add these:**

    - DATABASE_URL=<database-local-address> (I have: postgresql:///user)
    - SECRET_KEY=<your_secret_key>
  
**3. Next activate the virtual environment and install the requirements in terminal:**
  
    - $ python3 -m venv venv
    - $ source venv/bin/activate
    - $ pip install -r ./requirements.txt
   
**4. Create the database in psql with command:**

    - $ psql < schema.sql
  
**5. Start the application with command:**

    - $ flask run
