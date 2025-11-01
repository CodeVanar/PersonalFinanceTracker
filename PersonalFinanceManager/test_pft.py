'''
Author - CodeVaanar
Date - 25-10-2025
Desc - A pytest test file to integrate unittesting for the file - pft.py
'''

import pft 
from pft import FILENAME
import pytest
import csv
from unittest.mock import patch,mock_open
from decimal import Decimal
from datetime import date,timedelta,datetime

@pytest.fixture
def info_msg():
    message = []
    def callback(msg):
        message.append(msg)
    return message



class TestValidAmount: 
    
    def test_empty_amount(self, info_msg):
        result = pft.valid_amount("",info_msg.append)
        assert result is None 
        assert "Amount cannot be Empty" in info_msg

    def test_zero_amount(self,info_msg):
        result = pft.valid_amount("0",info_msg.append)
        assert result is None
        assert "Amount cannot be zero" in info_msg

    def test_negative_amount(self,info_msg):
        result = pft.valid_amount("-1",info_msg.append)
        assert result is None 
        assert "Amount cannot be Negative" in info_msg 

    def test_invalid_amount(self,info_msg):
        result = pft.valid_amount("abdjfh##",info_msg.append)
        assert result is None 
        assert "Invalid Amount !! enter only numbers " in info_msg 

    def test_amount_size(self,info_msg):
        result = pft.valid_amount("1e29",info_msg.append)
        assert result is None 
        assert "Amount too huge! Maximum allowed is 1e20." in info_msg

    def test_simple_amount(self,info_msg):
        result = pft.valid_amount("$1023",info_msg.append)
        assert result == Decimal("1023")
        assert not info_msg


class TestValidDate:

    def test_tommorow(self,info_msg):
        tommorow = date.today() + timedelta(days=1)
        format_tommorow = str(tommorow.strftime("%d-%m-%Y"))
        result = pft.valid_date(format_tommorow,info_msg.append)
        assert result is None 
        assert "Invalid date : cannot be ahead of today" in info_msg

    def test_empty_date(self,info_msg):
        result =  pft.valid_date(None,info_msg.append)
        assert result is None 
        assert "Date cannot be empty" in info_msg

    def test_year_range(self,info_msg):
        result = pft.valid_date("10-09-1782",info_msg.append)
        assert result is None 
        assert "Invalid date :  too way back in the past" in info_msg

    def test_date_format(self,info_msg):
        result = pft.valid_date("2025-1-1",info_msg.append)
        assert result is None 
        assert "Invalid date : Use DD-MM-YYYY (e.g., 25-12-2024)." in info_msg

    def test_invalid_date(self,info_msg):
        result = pft.valid_date("abcd",info_msg.append)
        assert result is None 
        assert "Invalid date : Use DD-MM-YYYY (e.g., 25-12-2024)." in info_msg

    def test_valid_date(self,info_msg):
        result = pft.valid_date("17-10-2024",info_msg.append)
        assert result == datetime.strptime("17-10-2024", "%d-%m-%Y").date()
        assert not info_msg

class TestValidChoice:

    def test_empty_choice(self,info_msg):
        result = pft.valid_choice(None,info_msg.append)
        assert result is None 
        assert "Choice cannot be empty" in info_msg

    def test_special_char(self,info_msg):
        result = pft.valid_choice("$",info_msg.append)
        assert result is None 
        assert "Invalid choice" in info_msg

    def test_invalid_choice(self,info_msg):
        result = pft.valid_choice("a",info_msg.append)
        assert result is None 
        assert "Invalid choice" in info_msg

    def test_choice_number(self,info_msg):
        result = pft.valid_choice("4",info_msg.append)
        assert result is None 
        assert "Invalid choice" in info_msg 

    def test_choice_length(self,info_msg):
        result = pft.valid_choice("abc",info_msg.append)
        assert result is None 
        assert "Invalid choice" in info_msg 

class TestAddTransaction:
    @patch("pft.call_info")
    @patch("pft.save_transaction")
    @patch("pft.valid_amount")
    @patch("pft.valid_date")
    
    

    def test_add_transaction_sucess(self,mock_valid_date,mock_valid_amount,mock_save_transaction,mock_call_info,info_msg):

        mock_valid_date.return_value = datetime(2025,10,17)
        mock_valid_amount.return_value = 1000

        transactions = []

        pft.add_transaction([],"17-10-2025","1000","CREDIT","travel",info_callback=info_msg.append)

        mock_valid_date.assert_called_once_with("17-10-2025",info_msg.append)
        mock_valid_amount.assert_called_once_with("1000",info_msg.append)

        

        expected_transaction = {
            "Date" : "17-10-2025",
            "Amount" : 1000,
            "Type" : "CREDIT",
            "Description" : "travel"
        }

        mock_save_transaction.assert_called_once_with(expected_transaction,info_msg.append)

        mock_call_info.assert_called_once_with("transaction added successfully ",info_msg.append)

class TestViewSummary:

    def test_empty(self,info_msg):
        result = pft.view_summary(None,info_msg.append)
        assert result is None
        assert "No transaction records found" in info_msg

    def test_decimal_value(self,info_msg):
        result = pft.view_summary([{"Date":"17-10-2025","Amount" :"12","Type":"DEBIT","Description": "travel"}],info_msg.append)
        assert result[1] == Decimal("12.00")

    def test_correct_value(self,info_msg):
        result = pft.view_summary([{"Date":"17-10-2025","Amount" :"100","Type":"DEBIT","Description": "travel"}],info_msg.append)
        assert result[0] == Decimal("0.00")
        assert result[1] == Decimal("100.00")
        assert result[2] == Decimal("-100.00")

    def test_invalid_value(self,info_msg):
        pft.view_summary([{"Date":"17-10-2025","Amount" :"abc","Type":"DEBIT","Description": "travel"}],info_msg.append)
        assert "1 corrupted transactions skipped" in info_msg

class TestSearchByType:


    def test_correct_result(self,info_msg):
        test_list = [{"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"fun"},{"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}]

        result = pft.search_by_type(test_list,"CREDIT",info_msg.append)


        correct_result = [{"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}]

        assert result == correct_result

    def test_empty_list(self,info_msg):
        result = pft.search_by_type(None,"CREDIT",info_msg.append)
        assert result == None 
        assert "No transaction found" in info_msg


    def test_no_match(self,info_msg):

        test_list = [{"Date":"16-10-2025","Amount":"100","Type":"CREDIT","Description":"fun"},{"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}]

        result = pft.search_by_type(test_list,"DEBIT",info_msg.append)

        

        assert result == None 
        assert "No records found of the type" in info_msg


class TestSearchByDesc:


    def test_correct_result(self,info_msg): 
        test_list = [{"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"travel"},{"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}]

        result = pft.search_by_desc(test_list,"travel",info_msg.append)

        correct_result = [{"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"travel"}]

        assert result == correct_result

    def test_empty_list(self,info_msg):
        result = pft.search_by_desc(None,"travel",info_msg.append)
        assert result == None 
        assert "No transaction found" in info_msg

    def test_no_match(self,info_msg):

        test_list = [{"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"shopping"},{"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}]

        result = pft.search_by_desc(test_list,"salary",info_msg.append)

        assert result == None 
        assert "No records found of the given decription" in info_msg

class TestValidChoice:

    def test_empty_choice(self,info_msg):
        result = pft.valid_choice(None,info_msg.append)
        assert result is None 
        assert "Choice cannot be empty" in info_msg

    def test_choice_len(self,info_msg):
        result = pft.valid_choice("yes",info_msg.append)
        assert result is None 
        assert "Invalid choice" in info_msg

    def test_choice_invalid(self,info_msg):
        result = pft.valid_choice("1",info_msg.append)
        assert result is None 
        assert "Invalid choice" in info_msg

    def test_choice_valid(self,info_msg):
        result = pft.valid_choice("y",info_msg.append)
        assert result == "y"

class TestDeleteTransaction:

    def test_empty_transactions(self, info_msg):
        result = pft.delete_transaction(None, 1, info_msg.append)
        assert result is None 
        assert "No records are found" in info_msg

    def test_index_len(self, info_msg):
        test_list = [
            {"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"travel"},
            {"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}
        ]
        result = pft.delete_transaction(test_list, "1 2", info_msg.append)
        assert result is None 
        assert "Index cannot have spaces" in info_msg

    def test_index_greater_than_length(self, info_msg):
        test_list = [
            {"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"travel"},
            {"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}
        ]
        result = pft.delete_transaction(test_list, 5, info_msg.append)
        assert result is None
        assert "Invalid Index: Index is greater than the length of transaction" in info_msg

    def test_negative_index(self, info_msg):
        test_list = [
            {"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"travel"},
            {"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}
        ]
        result = pft.delete_transaction(test_list, -1, info_msg.append)
        assert result is None
        assert "Invalid Index : Index cannot be special characters or negative characters" in info_msg

    def test_alphabet_index(self, info_msg):
        test_list = [
            {"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"travel"},
            {"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}
        ]
        result = pft.delete_transaction(test_list, "a", info_msg.append)
        assert result is None
        assert "Invalid Index : Index cannot be aplhabets" in info_msg

    def test_special_char_index(self, info_msg):
        test_list = [
            {"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"travel"},
            {"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}
        ]
        result = pft.delete_transaction(test_list, "@", info_msg.append)
        assert result is None
        assert "Invalid Index : Index cannot be special characters or negative characters" in info_msg

    def test_successful_deletion(self, info_msg, mocker):
        test_list = [
            {"Date":"16-10-2025","Amount":"100","Type":"DEBIT","Description":"travel"},
            {"Date":"17-10-2025","Amount":"200","Type":"CREDIT","Description":"fun"}
        ]

        # mock file writing and csv.writer
        mocker.patch("builtins.open", mocker.mock_open())
        mocker.patch("csv.writer")

        result = pft.delete_transaction(test_list, 0, info_msg.append)
        assert result is None
        assert "Transaction deleted successfully" in info_msg
        assert len(test_list) == 1


class Testdelete_all:

    def test_empty_transaction(self,info_msg):
        result = pft.delete_all([],info_msg.append)
        assert result is None
        assert "No transactions found" in info_msg

    def test_successful_delete_all(self, info_msg, mocker):
        test_list = [
            {"Date": "16-10-2025", "Amount": "100", "Type": "DEBIT", "Description": "travel"},
            {"Date": "17-10-2025", "Amount": "200", "Type": "CREDIT", "Description": "fun"}
        ]

        mocker.patch("builtins.open", mocker.mock_open())
        mock_csv_writer = mocker.patch("csv.writer")

        result = pft.delete_all(test_list, info_msg.append)

        assert result is None
        assert len(test_list) == 0  # should be cleared
        assert "All transactions deleted successfully " in info_msg
        mock_csv_writer.assert_called_once()

class TestLoadTransaction:

    def test_file_not_exist(self,info_msg):
        with patch("os.path.exists",return_value = False):
            result = pft.load_transaction(info_msg.append)
        assert result == []
        assert "No file was found - Starting Fresh"

    def test_empty_file(self,info_msg):
        m = mock_open(read_data = "")
        with patch ("os.path.exists",return_value = True),patch("builtins.open",m):
            result = pft.load_transaction(info_msg.append)
            assert result  == []
            assert any("No header found" in msg for msg in info_msg)

    def test_invalid_header(self,info_msg):
        csv_data = "Wrong,Header\n1,2"
        m = mock_open(read_data=csv_data)
        with patch("os.path.exists", return_value=True), patch("builtins.open", m):
            result = pft.load_transaction(info_msg.append)
        assert result == []
        assert any("Invalid header" in msg for msg in info_msg)

    def test_missing_value(self,info_msg):
        csv_data = "Date,Amount,Type,Description\n,,I,food\n01-01-2025,100,I,cake"
        m = mock_open(read_data = csv_data)
        with patch ("os.path.exists", return_value = True), patch("builtins.open", m):
            result = pft.load_transaction(info_msg.append)
        
        assert len(result) == 1
        assert result[0]["Amount"] == Decimal("100")
        assert any("missing values are skipped"in msg for msg in info_msg)

    def test_invalid_amount_or_date(self, info_msg):
        csv_data = (
            "Date,Amount,Type,Description\n"
            "01-01-2025,abc,Type1,Desc1\n"
            "32-01-2025,100,Type2,Desc2\n"
            "01-01-2025,50,Type3,Desc3"
        )
        m = mock_open(read_data=csv_data)
        with patch("os.path.exists", return_value=True), patch("builtins.open", m):
            result = pft.load_transaction(info_msg.append)
        assert len(result) == 1
        assert result[0]["Amount"] == Decimal("50")
        assert any("error with amounts" in msg for msg in info_msg)
        assert any("Error with date" in msg for msg in info_msg)

    def test_permission_error(self, info_msg):
        with patch("os.path.exists", return_value=True), patch("builtins.open", side_effect=PermissionError):
            result = pft.load_transaction(info_msg.append)
        assert result == []
        assert any("No permission granted" in msg for msg in info_msg)

    def test_corrupted_csv_error(self, info_msg):
        with patch("os.path.exists", return_value=True), patch("builtins.open", mock_open(read_data="bad\ndata")):
            with patch("csv.DictReader", side_effect=csv.Error("corrupted")):
                result = pft.load_transaction(info_msg.append)
        assert result == []
        assert any("possibly corrupted csv" in msg for msg in info_msg)

class TestSaveTransaction:

    def test_save_valid_transaction(self, info_msg):
        transaction = {
            "Date": date(2025, 1, 1),
            "Amount": 100,
            "Type": "CREDIT",
            "Description": "Test"
        }
        m = mock_open()
        with patch("os.path.exists", return_value=False), patch("builtins.open", m):
            pft.save_transaction(transaction, info_msg.append)
        
        # Check if file was opened
        m.assert_called_once_with(FILENAME, mode="a", newline="", encoding="utf-8")
        # Check that header and row were written
        handle = m()
        written_text = "".join(call.args[0] for call in handle.write.call_args_list)
        assert "Date,Amount,Type,Description" in written_text
        assert "01-01-2025,100,CREDIT,Test" in written_text


    def test_permission_error(self, info_msg):
        transaction = {
            "Date": date(2025, 1, 1),
            "Amount": 100,
            "Type": "CREDIT",
            "Description": "Test"
        }
        with patch("os.path.exists", return_value=True), patch("builtins.open", side_effect=PermissionError):
            pft.save_transaction(transaction, info_msg.append)
        assert any("Permission not granted" in msg for msg in info_msg)

    def test_memory_error(self, info_msg):
        transaction = {
            "Date": date(2025, 1, 1),
            "Amount": 100,
            "Type": "CREDIT",
            "Description": "Test"
        }
        with patch("os.path.exists", return_value=True), patch("builtins.open", side_effect=MemoryError):
            pft.save_transaction(transaction, info_msg.append)
        assert any("Too many transaction" in msg for msg in info_msg)

    def test_os_error(self, info_msg):
        transaction = {
            "Date": date(2025, 1, 1),
            "Amount": 100,
            "Type": "CREDIT",
            "Description": "Test"
        }
        with patch("os.path.exists", return_value=True), patch("builtins.open", side_effect=OSError("disk full")):
            pft.save_transaction(transaction, info_msg.append)
        assert any("OS error occured" in msg for msg in info_msg)      