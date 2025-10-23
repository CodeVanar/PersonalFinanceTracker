import os 
import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime, date

FILENAME = "transaction.csv"

def call_info(msg,info_callback = None):
    if info_callback    :
        info_callback(msg)

def load_transaction(info_callback = None):
    
    # check if file exits 
    if not os.path.exists(FILENAME):
        call_info("No file was found - Starting Fresh",info_callback)
        return []
    
    expected_fields = ["Date", "Amount", "Type", "Description"]
    transactions = []

    try:
        #checks for different encoding type 
        try:
            file = open(FILENAME,mode ="r", newline = "", encoding ="utf-8")
            
        except UnicodeDecodeError:
             file = open(FILENAME, mode ="r", newline ="", encoding = "latin-1") 

        with file :
            reader = csv.DictReader(file)
            #check for header
            if not reader.fieldnames :
                call_info("No header found - Starting Fresh",info_callback)
                return []
                    
            #check for valid headers
            if not set(expected_fields).issubset(reader.fieldnames):
                call_info(f"Invalid header :{reader.fieldnames} - Starting Fresh!",info_callback)
                return []

            for row in reader :
            #skip missing fields
                if not all(row.get(field) and row.get(field).strip() != "" for field in expected_fields):
                    call_info("missing values are skipped",info_callback)
                    continue 

                #parsing amount field
                try:
                    row["Amount"] = Decimal(row["Amount"])
                except (ValueError, InvalidOperation):
                    call_info("error with amounts",info_callback)
                    continue

                #parsing date field
                try :
                    row["Date"] = datetime.strptime(row["Date"],"%d-%m-%Y").date()
                except (ValueError, TypeError):
                    call_info("Error with date",info_callback)
                    continue 

                filter_row = {field :row[field] for field in expected_fields}
                transactions.append(filter_row)

        return transactions 
    
    except PermissionError :
        call_info(f"Error : No permission granted to read {FILENAME}",info_callback)
        return []
    except csv.Error as e :
        call_info( f"Error : possibly corrupted csv - {e}",info_callback)
        return []
    except MemoryError:
        call_info(f"Error : File too huge to process !",info_callback)
        return []
    except Exception as e :
        call_info(f"Error : unexpected error : {e}",info_callback)
        return []

      

def save_transaction(new_transaction,info_callback = None):
    clean_transactions = []
    expected_fields = ["Date", "Amount", "Type", "Description"]


    if all(field in new_transaction and new_transaction[field] != "" for field in expected_fields):
        transaction_copy = new_transaction.copy()
    transaction_copy["Description"] = str(transaction_copy["Description"])
    if isinstance(transaction_copy["Date"], date):
        transaction_copy["Date"] = transaction_copy["Date"].strftime("%d-%m-%Y")
    clean_transactions.append(transaction_copy)
    try:
        file_exists = os.path.exists(FILENAME)
        with open (FILENAME, mode="a", newline = "", encoding = "utf-8") as file :
            writer = csv.DictWriter(file, fieldnames= expected_fields)

            if not file_exists:
                writer.writeheader()
            writer.writerows(clean_transactions)
        
    except PermissionError:
        call_info(f"Error : Permission not granted to write to the '{FILENAME}' ",info_callback)
        return None
    except MemoryError:
        call_info(f"Error : Too many transaction to save .. system overload.",info_callback)
        return None
    except OSError as e :
        call_info(f"OS error occured while saving the file : {e}",info_callback)
        return None
    except Exception as e :
        call_info(f"OS error occured while saving the file : {e}",info_callback)
        return None





def valid_date(date_input,info_callback = None):
    if not date_input:
        call_info("Date cannot be empty",info_callback)
        return None

    try :

        parsed_date = datetime.strptime(date_input , "%d-%m-%Y").date()
        today = date.today()

        

        if parsed_date > today :
            call_info("Invalid date : cannot be ahead of today",info_callback)
            return None

        if parsed_date.year < 1920:
            call_info("Invalid date :  too way back in the past",info_callback)
            return None
            

        return parsed_date

    except ValueError:
        call_info("Invalid date : Use DD-MM-YYYY (e.g., 25-12-2024).",info_callback)
        return None

def valid_amount(amt,info_callback = None):


    if not amt :
        call_info("Amount cannot be Empty",info_callback)
        return None
        

    amt_str = amt.replace(',','').replace("$","").replace("₹","").replace("£","")

    try:
        amt = Decimal(amt_str)
    except (InvalidOperation, ValueError):
        call_info("Invalid Amount !! enter only numbers ",info_callback)
        return None
        

    if amt == 0 :
        call_info("Amount cannot be zero",info_callback)
        return None
        
    if amt < 0 :
        call_info("Amount cannot be Negative",info_callback)
        return None
        
    if amt > Decimal("1e20") :
        call_info("Amount too huge! Maximum allowed is 1e20.",info_callback)
        return None
        

    return amt
    

def valid_type(type_,info_callback= None ):
    #keep asking for valid type as showed
    if not type_ :
        call_info("Type cannot be Empty",info_callback)
        return None
        
    if len(type_) != 1:
        call_info("Not a valid Type",info_callback)
        return None
        
    if not type_.isalpha():
        call_info("Not a valid Type",info_callback)
        return None

    if type_.upper() not in ["I", "E"]:
        call_info("Not a valid Type",info_callback)
        return None
        

    return type_.upper()
    

def valid_desc(desc,info_callback = None):
#keep asking for a valid description

    special_char = set("!@#$%^&*_,-+=/|><\\")

    if not desc :
        call_info("Description cannot be empty ",info_callback)
        return None

    if len(desc) > 50 :
        call_info("Description too long ",info_callback)
        return None

    if any(ch in special_char for ch in desc):
        call_info("Special Characters not allowed ",info_callback)
        return None

    if any(ch.isdigit() for ch in desc):
        call_info("Digits not allowed in Description",info_callback)
        return None

    return desc.lower()


def add_transaction(date_input,amt,type_,desc,info_callback = None):

    #storing the input with the help of helper function
    date_input = valid_date(date_input,info_callback)
    amt = valid_amount(amt,info_callback)
    type_ = valid_type(type_,info_callback)
    desc = valid_desc(desc,info_callback)

    new_transaction = {
        "Date" : date_input.strftime("%d-%m-%Y"),
        "Amount" : amt,
        "Type" : type_.upper(),
        "Description" : desc.lower()
    }
        
    
    save_transaction(new_transaction,info_callback)

    call_info("transaction added successfully ",info_callback)
        

def view_summary(transactions ,info_callback = None):
    '''
    displays a summary of total income, total expense and net balance.
    '''

    income = Decimal("0.00")
    expense = Decimal("0.00")

    if not transactions:
        call_info("No transaction records found",info_callback)
        return None
    
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
    

    if corrupted_transactions:
        call_info(f"{len(corrupted_transactions)} corrupted transactions skipped", info_callback) 
    result = [income, expense, (income- expense)]
    return result 
    

def search_by_type(transactions,type_,info_callback = None):
    '''search and print all transaction of the given type'''

    search_type = valid_type(type_,info_callback)
    if not transactions:
        call_info("No transaction found",info_callback)
        return None
    match = []
    found = False
    for transaction in transactions:
        try: 
            if transaction["Type"].upper() == search_type.upper():
                match.append(transaction)
                found = True
        except (KeyError, ValueError, TypeError) as e:
            call_info(f"Error occurred while searching by type: {e}",info_callback)
            return None
    if not found :
        call_info("No records found of the type",info_callback)
        return None

    return match


def search_by_desc(transactions,desc,info_callback= None):
    '''search and print all transaction of the given description'''

    desc_type = valid_desc(desc,info_callback)
    if not transactions:
        call_info("No transaction found",info_callback)
        return None
    match = []
    found = False
    for transaction in transactions:
        if desc_type == transaction["Description"]:
            match.append(transaction)
            found = True
    if not found :
        call_info("No records found of the given decription",info_callback)
        return  None
    
    return match 


def valid_choice(choice,info_callback = None):
    #take a choice from user
        if not choice :
            call_info("Choice cannot be empty",info_callback)
            return None
        if len(choice) != 1:
            call_info("Invalid choice",info_callback)
            return None
        if choice in ['y', 'n']:
            return choice
        else:
            call_info("Invalid choice",info_callback)
            return None

def delete_transaction(transactions,index_val,info_callback = None):
    index_val = str(index_val)

    for i in index_val:
        if i == " ":
            call_info("Index cannot have spaces",info_callback)
            return None

    if not transactions:
        call_info("No records are found",info_callback)
        return None
    
    if index_val.isalpha():
        call_info("Invalid Index : Index cannot be aplhabets", info_callback)
        return None
    
    if not index_val.isdigit():
        call_info("Invalid Index : Index cannot be special characters or negative characters", info_callback)
        return None
    
    index_val = int(index_val)

    if int(index_val) > len(transactions):
        call_info("Invalid Index: Index is greater than the length of transaction",info_callback)
        return None

    
    
    transactions.pop(int(index_val))

    with open(FILENAME, mode ="w", newline ="", encoding ="utf-8") as file :
        writer = csv.writer(file)
        writer.writerows(transactions)

    if info_callback:
        call_info("Transaction deleted successfully",info_callback)
        return None
    
    


def delete_all(transactions, info_callback = None):
    if not transactions:
        call_info("No transactions found", info_callback)
        return None
    transactions.clear()

    try :
        with open(FILENAME , mode ="w", newline = "", encoding ="utf-8") as file :
            writer = csv.writer(file)
            writer.writerow([])
        call_info("All transactions deleted successfully ",info_callback)
    except Exception as e :
        if info_callback:
            call_info(f"Error Delettion Error : {e}",info_callback)
            return None
if __name__ == "__main__":
    # load transactions when program starts
    transactions  = load_transaction()