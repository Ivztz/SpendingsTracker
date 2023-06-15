# My$pendingsTr@cker

## CS50 Final Project 2023
#

My$pendingsTr@cker is a web application that is implemented using Flask that helps user to track their spendings. User is able to set a spending budget and add individual spending based on its category and amount. The main page is able to display the overall spendings in a pie chart as well as tabular form.

The inspiration behind developing a personal spendings tracker is that it allows me to manage my finances better as I can keep tracker of how much I have spent in the month. This helps to encourage me to spend my money thriftily.

#### Video Demo:  <https://youtu.be/Y4JjBkKtc7Q>

# Framework Used
- HTML5, CSS
- Python
- SQLite

# Installation Guide
#### 1. Clone the repository into your machine.
#### 2. Run the command ```pip install -r requirements.txt``` to install Python dependencies.
#### 3. Extract sqlite.zip to "C:".
#### 4. Run the command ```python create_database.py``` to setup database.
#### 5. Run the command ```python app.py``` to start the local server and access the web app on your local browser.

# Usage Instructions
## Features:
### Personal Account
- User must first create a user account which can be done by clicking on "Register" on the navbar.
### Main Page
- Once logged in, user is prompted to set a budget and add new spendings by clicking on "Budget" and "Add Spendings" respectively.
- A pie chart and table will be shown if user has added at least one spending submission.
### Budget
- User is able to update their budget by entering a new amount.
### Add Spendings
- To submit a spending entry, user is to input the amount and category of the spending.
### History
- User is able to view all spending entries and delete them individually.

## More Details:
- User System: Users have unqiue sessions. User data are stored in database with passwords hashed and usernames are unique.
- Routing: All other routes are authenticated, user is unable to access main page without login in.
- Database contains 3 tables: 
    - users: username, password
    - budgets: user_id, budget
    - spendings: user_id, category, amount, timestamp

# Future Improvements
- Add feature to edit spendings amount and/or category without deleting entry and re-submiting it.
- Add feature for user customise profile: Edit username and/or password, add profile picture.
- Allow user to view spendings summary in different format other than pie-chart and tabular form.
- Add filter for spendings history table for year / month / day