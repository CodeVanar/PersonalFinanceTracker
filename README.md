# Personal Finance Tracker
Personal Finance Tracker is a Python-based application designed to help users efficiently manage their finances with ease and accuracy. It allows users to add, view, edit, and delete transactions, providing a clear overview of their financial activities.

The application stores transaction data in a CSV file containing date, amount, type, and description. A user-friendly GUI is built using Python's Tkinter, making finance tracking simple and interactive.

## Features
Load Transaction – Loads the CSV file containing previously recorded transactions for further operations.

Save Transaction – Saves new transactions or any changes made to existing transactions.

Add Transaction – Adds a new transaction with details like date, amount, type, and description, and updates the CSV file.

View Summary – Displays a financial summary including net income, total expenses, and balance.

Search by Expense or Type – Allows users to search for specific transactions based on expense(credit or debit) or type.

Delete Transaction – Deletes a particular transaction or clears the entire transaction history.

Delete All - Deletes all the available transactions.

When the program is launched, a GUI window appears with buttons corresponding to each function. Clicking a button executes the function, and inputs/outputs are displayed in the console

## Prerequisites
1. Python Environment
   - Python Version : 3.13.0 or higher
   - Download link : https://www.python.org/downloads/
   - Ensure that Python and pip are added to your system:
     - python --version
     - pip --version
2. Required Python Libraries
   - pip install pandas
   - pip install tkcalendar
   - pip install pytest

## Installation
1. Clone the Repository
   - git clone https://github.com/data-divaa/PersonalFinanceTracker
   - cd PersonalFinanceManager
2.  Launch the Application
   - python GUI.py    

## Testing with pytest
1. Automated testing in this project is handled using pytest
2. All test cases are stored inside the test_pft.py to maintain modularity and ensure code reliability .

   - For detailed test results : python -v
   - To see print statements and logs during testing: pytest -s
   - to combine both : pytest -v -s
   - to run specific class : pytest -v -k TestAddTransaction    (instead of TestAddTransaction it can be any class)
   - to run specific test fuction : pytest -v -k test_add_transaction_sucess  (instead of test_add_transaction_sucess it can be any test function)
  
## Code Quality & Analysis (SonarQube)
This project uses SonarQube (https://www.sonarsource.com/products/sonarqube/ )to ensure continuous code quality and maintainability.
SonarQube analyzes the repository for potential bugs, vulnerabilities, code smells, and test coverage after every code push.

## License
This project is licensed under the MIT License.


