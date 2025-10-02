'''
Date - 09: Sept:2025
Author - data-divaa
Desc - Personal Finance Manager - tracks finance by taking date of transaction, amount , type of transaction and 
description as input and stores it in a csv file . it is a backend for GUI application . it contains functions like
---> load transactions - to load previous transaction from csv file to a list of dictionary
---> save transactions - to save a new transaction into the csv file 
---> add transaction - to take a new transaction as input and store it in csv
---> view summary - to view the net expense, income and balance
---> search by type - it searches and print all transaction of the given type 
---> search by description - it searches and print all transaction of the given description
---> delete - it delete a particular transaction based on date, amount and type 
---> delete all - it deletes all the transaction 
---> various helper function are also defined .
'''

from datetime import datetime
from datetime import date
import csv
from decimal import Decimal, InvalidOperation
import os
import pandas as pd

FILENAME = "transaction.csv"


#clearing the console screen
def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


#loading a csvfile to check for previous transaction
def load_transactions():
    if not os.path.exists(FILENAME):
        print("No file found. Starting fresh!")
        return []

    expected_fields = {"Date", "Amount", "Type", "Description"}
    transactions = []

    try :
        try:
            file = open(FILENAME, mode = "r", newline = "", encoding ="utf-8")
        except UnicodeDecodeError:
            file = open(FILENAME, mode = "r", newline = "", encoding = "latin-1")

        with file :
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("CSV file has no headers. Starting with an empty list.")
                return []
            if not set(expected_fields).issubset(reader.fieldnames):
                print(f"CSV file headers invalid or missing. Found: {reader.fieldnames}")
                return []

            for row in reader :
                if not all(row.get(field) for field in expected_fields):
                    print(f"Skipping row with missing fields: {row}")
                    continue

                try :
                    row["Amount"] = Decimal(row["Amount"])
                except (ValueError, InvalidOperation):
                    print(f"Skipping row with invalid amount: {row}")
                    continue

                # Parse date string back to date object
                try:
                    row["Date"] = datetime.strptime(row["Date"], "%d-%m-%Y").date()
                except (ValueError, TypeError):
                    print(f"Skipping row with invalid date format: {row}")
                    continue

                filtered_row = {field : row[field] for field in expected_fields}

                transactions.append(filtered_row)

        print(f"Loaded {len(transactions)} valid transactions from file.")
        return transactions

    except PermissionError :
        print(f"Error : No permission to read '{FILENAME}'")
        return []
    except csv.Error as e :
        print(f"Error reading CSV file (possibly corrupted): {e}")
        return []
    except MemoryError:
        print(f"File too large to process!!")
        return []
    except Exception as e:
        print(f"An Unexpected Error occured while loading the file  : {e}")
        return []



#save new changes int the csv file
def save_transactions(transactions):
    expected_fields = ["Date", "Amount", "Type", "Description"]
    clean_transactions = []
    for row in transactions:
        if all(field in row and row[field] != "" for field in expected_fields):
            row_copy = row.copy()
            row_copy["Description"] = str(row_copy["Description"])
            # Ensure date is serialized as string before saving
            if isinstance(row_copy["Date"], date):
                row_copy["Date"] = row_copy["Date"].strftime("%d-%m-%Y")
            clean_transactions.append(row_copy)
        else:
            print(f" Skipping row with missing fields during save: {row}")

    try :
        with open(FILENAME, mode="w", newline="",encoding = "utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=expected_fields)
            writer.writeheader()
            writer.writerows(clean_transactions)

        print(f" Saved {len(clean_transactions)} transactions to file.")
    except PermissionError:
        print(f"Error : Permission not granted to write to the '{FILENAME}' ")
    except MemoryError:
        print("Error : Too many transaction to save .. system overload.")
    except OSError as e :
        print(f"OS error occured while saving the file : {e}")
    except Exception as e :
        print(f"An Unexpected Error occurred while saving the file : {e}")



#list to hold all transaction records
transactions = load_transactions()



def valid_date():
    #keep asking for a date until a valid date is entered
    while True:
        date_input = input("Enter the date of transaction(DD-MM-YYYY):    ").strip()
        if not date_input:
            print("Date cannot be empty")
            continue


        try :
            parsed_date = datetime.strptime(date_input , "%d-%m-%Y").date()
            today = date.today()

            if parsed_date > today :
                print("Invalid date : cannot be ahead of today")
                continue

            if parsed_date.year < 1920:
                print("Invalid date :  too way back in the past")
                continue

            return parsed_date

        except ValueError:
            print("Invalid date : Use DD-MM-YYYY (e.g., 25-12-2024).")

def valid_amount():
    #keep asking for a valid amount
    while True:
        amt = input("Enter the Amount:  ").strip()

        if not amt :
            print("Amount cannot be empty")
            continue
        amt_str = amt.replace(',','').replace("$","").replace("₹","").replace("£","")

        try:
            amt = Decimal(amt_str)
        except (InvalidOperation, ValueError):
            print("Invalid Amount !! enter only numbers ")
            continue

        if amt == 0 :
            print("Amount cannot be zero")
            continue
        if amt < 0 :
            print("Amount cannot be Negative")
            continue
        if amt > Decimal("1e20") :
            print("Amount too huge! Maximum allowed is 1e20.")
            continue

        return amt



def valid_type():
    #keep asking for valid type as showed
    while True:
        type_ = input("Enter the type of transaction (I for Income and E for Expense):      ").strip()
        if not type_ :
            print("Type cannot be Empty")
            continue
        if len(type_) != 1:
            print("Not a valid Type")
            continue
        if not type_.isalpha():
            print("Not a valid type ")
            continue

        if type_.upper() not in ["I", "E"]:
            print("Not a Valid Type")
            continue

        return type_.upper()



def valid_desc():
    #keep asking for a valid description
    while True:
        desc = input("Enter the Description (food, travel, subscriptions, rent, shopping, others):      ").strip()

        special_char = set("!@#$%^&*_-+=/|><\\")

        if not desc :
            print("Description cannot be empty ")
            continue

        if len(desc) > 50 :
            print("Description too long !")
            continue

        if any(ch in special_char for ch in desc):
            print("Special Characters not allowed ")
            continue

        if any(ch.isdigit() for ch in desc):
            print("Digits not allowed in Description")
            continue

        if "," in desc :
            print("Invalid Description : commas are not allowed")
            continue

        return desc.lower()



def add_transaction():
    clear_console()
    """
    Adds a new transaction to the transactions list after validating user input.
    Prompts the user for date, amount, type (Income/Expense), and description.
    Checks for duplicate transactions before adding and saves the updated list to the CSV file.
    """
    #storing the input with the help of helper function
    date_input = valid_date()
    amt = valid_amount()
    type_ = valid_type()
    desc = valid_desc()

    # Normalize types for comparison to avoid mismatches
    def normalize_transaction(tr):
        return {
            "Date": str(tr["Date"]),
            "Amount": float(tr["Amount"]),
            "Type": tr["Type"].upper(),
            "Description": str(tr["Description"]).lower()
        }

    #store transaction in a dictionary
    t = {"Date" : date_input.strftime("%d-%m-%Y"),
    "Amount" : amt,
    "Type" :type_,
    "Description" : desc}

    t_norm = normalize_transaction(t)
    for existing in transactions:
        if normalize_transaction(existing) == t_norm:
            print("Duplicate transaction rejected")
            return

    # Serialize date before appending to transactions list
    t_serialized = t.copy()
    t_serialized["Date"] = date_input.strftime("%d-%m-%Y")
    transactions.append(t_serialized)

    #confirmation message with transaction details
    print("-------Transaction Added Successfully--------")
    print("Date :",date_input)
    print("Amount :",amt)
    print("Type of Expense :","Expense" if type_.upper() == "E" else "Income")
    print("Description :",desc)

    save_transactions(transactions)



def view_summary():
    '''
    displays a summary of total income, total expense and net balance.
    '''
    clear_console()

    income = Decimal("0.00")
    expense = Decimal("0.00")

    if not transactions:
        print("No records found!")
        return
    
    corrupted_transactions = []
    for transaction in transactions:
        try:
            amt = Decimal(transaction["Amount"])
            if transaction["Type"].upper() == "I":
                income += amt
            elif transaction["Type"].upper() == "E":
                expense += amt
        except (KeyError, ValueError, InvalidOperation) as e:
            corrupted_transactions.append((transaction, str(e)))
    print("---------Transaction summary ---------")
    print(f"Net Income : ₹{income:,.2f}")
    print(f"Net Expense : ₹{expense:,.2f}")
    print(f"Net Balance : ₹{income - expense:,.2f}")

    if corrupted_transactions:
        print(f"\nSkipped {len(corrupted_transactions)} corrupted transaction(s):")
        for trans, err in corrupted_transactions:
            print(f"  {trans} ({err})")



def search_by_type():
    '''search and print all transaction of the given type'''
    clear_console()

    searchTYPE = valid_type()
    if not transactions:
        print("No records found!")
        return 
    print("-----Showing all",searchTYPE.upper(),"Transaction-----")
    found = False
    for transaction in transactions:
        try: 
            if transaction["Type"].upper() == searchTYPE.upper():
                print(f"Date : {transaction['Date']} | Amount : {transaction['Amount']} | Type : {transaction['Type']} | Description : {transaction['Description']}")
                found = True
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error occurred while searching by type: {e}")
    if not found :
        print("No Records found.")




def search_by_desc():
    '''search and print all transaction of the given description'''
    clear_console()

    descTYPE = valid_desc()
    print("-----Showing all",descTYPE.upper(),"Transaction-----")
    found = False
    for transaction in transactions:
        if descTYPE == transaction["Description"]:
            print(f"Date : {transaction['Date']} | Amount : {transaction['Amount']} | Type : {transaction['Type']} | Description : {transaction['Description']}")
            found = True
    if not found :
        print("No Records found")




def valid_choice():
    #take a choice from user
    while True :
        choice = input("Are you Sure(y/n) :     ").strip().lower()
        if not choice :
            print("Choice cannot be empty")
            continue
        if len(choice) != 1:
            print("Not a valid choice!!!")
            continue
        if choice in ['y', 'n']:
            return choice
        else:
            print("Not a valid choice!!!")


def choose_index(df):
    while True:
        index = input("Enter the index of the transaction to delete :   ").strip()
        if len(index) > 1 :
            print("Invalid Index ")
            continue
        if index.isalpha():
            print("Invalid value : Enter Numbers only ")
            continue
        if index in set("!@#$%^&*_-+=/|><\\"):
            print("Invalid Index : special charcter not allowed ")
            continue
        index = int(index) -1
        if index > df.index[-1]:
            print("Invalid Index : index exceeded !!")
            continue
        if index < 0 :
            print("Invalid Index : Index cannot be Negative")
            continue
        return index 
    
def print_transaction(df):
    df.index = df.index + 1
    print(df)

def delete_transaction():
    df = pd.DataFrame(transactions,columns =["Date","Amount","Type","Description"] )
    print_transaction(df)
    index_to_delete = choose_index(df)
    del transactions[index_to_delete]
    save_transactions(transactions)
    df1 = pd.DataFrame(transactions, columns = ["Date", "Amount", "Type", "Description"])
    print("\n")
    print(f"------------Transaction Number {index_to_delete} is Successfully Deleted---------")
    print("\n")
    print("----------------ALL THE TRANSACTION AFTER DELETION---------------------")
    print_transaction(df1)
    



def delete_all():
    #delete every transaction from the records after confirmation
    clear_console()
    if not transactions:
        print("No records found!")
        return 
    
    print("this will delete all the records permanently")
    choice = valid_choice()
    if choice == "y":
        transactions.clear()
        save_transactions(transactions)
        print("all records delete successfully")
    else:
        print("Deletion cancelled")




if __name__ == "__main__":
    # load transactions when program starts
    transactions = load_transactions()