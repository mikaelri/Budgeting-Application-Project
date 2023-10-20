**Python FLASK API - Budgeting application project**

**SpendManager**

***Background***

The idea of SpendManager application is that a user can create own budget, where it is possible to track income (i.e. salary, study grant) and expenses (i.e. rent, groceries).

One example for the use case is that user can create an individual budget and to follow monthly income and expenses to see what is the net result for the month. 

The application will use a ready-to-use categories for income and expenses. This is for the reason that it helps the user to search transactions. The category groups for income and expenses are:

- **Income:** *salary, study grant & other*
- **Expenses:** *rent, mortgage, travel, groceries, food & other*

The idea for category "other" is that the user can add any income or expense transaction even if there is not a category for this. If there is no category the user can write a message related to the transaction.

The application could be used also only for expenses, thus, one other example could be a holiday trip for some group. This application could help to track down the fixed costs already known such as flight and hotel or something to add during the trip like activity costs.

***Application functionalities*** 

- **Functionalities 1,2,3,4,5,6,7,8, 9 are ready for testing**
- **Functionalities 10 are not ready for testing**

1. User can log in and out and create a new user account
2. User can view a list of own individual budgets after logging in (only if at least one exists)
3. User can select which budgets to modify from the list of budgets
4. User can create a new budget and add a name for it
5. User can continously add income and expense transactions to selected budget with a message and category
6. User can view the net result of the selected budget
7. User can search income and expenses related to selected category 
8. Admin user can see a list of user accounts, roles and budgets
9. Admin user can delete existing budgets
10. ~~User can leave comments to selected budgets~~

***Database tables***

1. users
2. budgets
3. transactions
4. results
5. comments

***Installing instructions / how to test the app locally***
```
Prerequisites: Python 3.10.12 and PostgreSQL.
```
**1. Clone this repository to your computer and navigate to the root folder.**

**2. Create .env file to the folder and add these:**
```
DATABASE_URL=<database-local-address> (I have: postgresql:///user)
```
```
SECRET_KEY=<your_secret_key>
```

**3. Next activate the virtual environment and install the requirements in terminal:**
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
pip install -r ./requirements.txt
```

**4. Create the database in psql with command:**
```
psql < schema.sql
```

**5. Start the application with command:**

```
flask run
```

***Possible future enhancements and ideas***

- Upgrade the front-end and make it visually more clear 
  
- Upgrade the UX with better navigation possibilities (this in link with point 2. above) and consider changes for the application to be more user friendly
  
- Modify the admin page table so it would show who is the creator for certain budget (i.e. dropdown) or make a double check asking if you really want to delete a budget from a selected user
  
- Add view, which would provide a better look for the user to see inside the budget (i.e. different functions to show more details of the budget, not only net result)