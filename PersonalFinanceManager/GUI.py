'''
Author - 
Date - 25-10-2025
Desc - A clean and interactive Tkinter-based interface that allows users to easily add, view, and search financial transactions. The design focuses on simplicity and usability, with organized windows, dropdowns, and summaries to make expense tracking intuitive and visually clear
'''
import tkinter as tk
from tkinter import ttk,messagebox
import pft 
import pandas as pd 
import datetime
from decimal import Decimal
import sys
from tkcalendar import DateEntry



def start_gui():
    root = tk.Tk()
    root.title("Personal Finance Tracker")
    tk.Label(root, text = "Personal Finance Tracker", font =("helvetica",20)).pack(pady=10)

    transactions = pft.load_transaction()  

    def open_win1():
        win1 = tk.Toplevel(root)
        win1.title("Adding transaction ")
        win1.geometry("400x150")

        tk.Label(win1,text="Enter the date of transactions :").grid(row=0)
        tk.Label(win1,text ="Enter the Amount (in INR-rupees) :").grid(row=1)
        tk.Label(win1, text = "Enter the type of transaction :").grid(row=2)
        tk.Label(win1,text = "Enter the Description of transaction :").grid(row =3)
        
        date_entry = DateEntry(win1, date_pattern="dd-mm-yyyy", background="darkblue",foreground="white", borderwidth=2,state = "readonly")
        date_entry.grid(row=0,column=1)

        e2 = tk.Entry(win1)
        e2.grid(row=1, column=1)

        e3 = ttk.Combobox(win1,values=["Credit","Debit"],state= "readonly")
        e3.set("Select Expense")
        e3.grid(row=2,column=1)

        e4 = ttk.Combobox(win1,values = ["salary","takeout","travel","rent","grocery","bills","medicine","gifting","fun","shopping","others"],state = "readonly",width = 25)
        e4.set("Select Transaction Type")
        e4.grid(row=3,column=1)

        
        def submit():
            pft.add_transaction(transactions,
                date_entry.get(), e2.get(),e3.get(),e4.get(),
                info_callback = lambda msg : messagebox.showinfo("Info",msg)
            )        

            win1.destroy()

        tk.Button(win1, text="Submit", command=submit, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), activebackground="#45a049").grid(row=4, column=1)


    def open_win2():
        win2 = tk.Toplevel(root)
        win2.title("View summary")
        win2.geometry("400x300")

        results = pft.view_summary(transactions,info_callback = lambda msg : messagebox.showinfo("Info",msg))

        tk.Label(win2 , text = f"Net Income : {results[0]}" , font = ("Arial", 15 )).pack(pady=15)
        tk.Label(win2 , text = f"Net Expense : {results[1]}" , font = ("Arial", 15 )).pack(pady=15)
        tk.Label(win2 , text = f"Net Balance : {results[2]}" , font =("Arial", 15 )).pack(pady=15)

        

    def open_win3():
        win3 = tk.Toplevel(root)
        win3.title("View Transaction based on Type")
        win3.geometry("500x100")

        tk.Label(win3, text ="Enter the type of transaction you are looking for :").grid(row=0)
        e1 = ttk.Combobox(win3,values=["Credit","Debit"],state= "readonly")
        e1.set("Select Expense")
        e1.grid(row=0,column= 1)

        def open_win301():
            selected_type = e1.get()

            win3.destroy()

            win301 = tk.Toplevel(root)
            win301.title("Transaction based on type")
            win301.geometry("500x600")

            result = pft.search_by_type(transactions,selected_type,info_callback = lambda msg : messagebox.showinfo("Info",msg))

            if not result:
                tk.Label(win301, text = "No transactions records were found on the given type").pack(pady=20)
                return 
            
            column = ("Date","Amount","Type","Description")
            tree = ttk.Treeview(win301,columns = column , show ="headings")

            for col in column:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor="center")

            for row in result:
                if isinstance(row, dict):
                    date_val = row.get("Date", "")
                    if isinstance(date_val, datetime.date):
                        date_val = date_val.strftime("%d-%m-%Y")

                    amount_val = row.get("Amount", "")
                    if isinstance(amount_val, Decimal):
                        amount_val = str(amount_val)

                    values = (
                        date_val,
                        amount_val,
                        row.get("Type", ""),
                        row.get("Description", "")
                    )
                else:
                    values = row  # In case it’s already a tuple/list

                tree.insert("", tk.END, values=values)

            scrollbar = ttk.Scrollbar(win301, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")


        tk.Button(win3, text="Search", command = open_win301, bg="#B82222", fg="white", font=("Arial", 12, "bold"), activebackground="#45a049").grid(row=5, column=2)


    def open_win4():
        win4 = tk.Toplevel(root)
        win4.title("View Transaction based on Description")
        win4.geometry("550x100")

        tk.Label(win4, text ="Enter the Description of transaction you are looking for :").grid(row=0)
        e1 = ttk.Combobox(win4,values = ["salary","takeout","travel","rent","grocery","bills","medicine","gifting","fun","shopping","others"],state = "readonly",width = 25)
        e1.set("Select Transaction Type")
        e1.grid(row=0,column= 1)

        def open_win401():
            selected_desc = e1.get()

            win4.destroy()

            win401 = tk.Toplevel(root)
            win401.title("Transaction based on Description")
            win401.geometry("500x600")

            result = pft.search_by_desc(transactions,selected_desc,info_callback = lambda msg : messagebox.showinfo("Info",msg))

            if not result:
                tk.Label(win401, text = "No transactions records were found on the given Description").pack(pady=20)
                return 
            
            column = ("Date","Amount","Type","Description")
            tree = ttk.Treeview(win401,columns = column , show ="headings")

            for col in column:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor="center")

            for row in result:
                if isinstance(row, dict):
                    date_val = row.get("Date", "")
                    if isinstance(date_val, datetime.date):
                        date_val = date_val.strftime("%d-%m-%Y")

                    amount_val = row.get("Amount", "")
                    if isinstance(amount_val, Decimal):
                        amount_val = str(amount_val)

                    values = (
                        date_val,
                        amount_val,
                        row.get("Type", ""),
                        row.get("Description", "")
                    )
                else:
                    values = row  # In case it’s already a tuple/list

                tree.insert("", tk.END, values=values)

            scrollbar = ttk.Scrollbar(win401, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y")

        tk.Button(win4, text="Search", command = open_win401, bg="#B82222", fg="white", font=("Arial", 12, "bold"), activebackground="#45a049").grid(row=5, column=2)


    def open_win5():
        win5 = tk.Toplevel(root)
        win5.title("Delete Transaction")
        win5.geometry("600x500")

        win5.grid_rowconfigure(1, weight=1)
        win5.grid_columnconfigure(0, weight=1)

        # --- Input and Delete Button Row ---
        tk.Label(win5, text="Enter the Index to delete the transaction:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w"
        )

        e1 = tk.Entry(win5)
        e1.grid(row=0, column=1, padx=5, pady=10, sticky="w")

        delete_btn = tk.Button(win5, text="Delete", bg="red", fg="white")
        delete_btn.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        # --- Table (Treeview) Setup ---
        d1 = pd.DataFrame(transactions)
        columns = ["Index"] + list(d1.columns)

        tree = ttk.Treeview(win5, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=110)
        tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(win5, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=3, sticky='ns')

        # --- Load All Data At Once ---
        for idx, row in d1.iterrows():
            tree.insert("", "end", values=[idx] + list(row))

        # --- Backend Functions ---
        def info_callback(msg):
            messagebox.showinfo("Info", msg)

        def reload_table():
            tree.delete(*tree.get_children())
            new_df = pd.DataFrame(transactions)
            for idx, row in new_df.iterrows():
                tree.insert("", "end", values=[idx] + list(row))

        def delete_from_backend():
            try:
                idx = e1.get().strip()
                if idx == "":
                    messagebox.showinfo("Error", "Please enter an Index to delete")
                    return
                confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete transaction {idx}?")
                if confirm:
                    pft.delete_transaction(transactions, int(idx), info_callback)
                    reload_table()
            except ValueError:
                messagebox.showinfo("Error", "Please enter a valid numeric Index")

        delete_btn.config(command=delete_from_backend)


    def open_win6():
        def info_callback(msg):
            messagebox.showinfo("Info", msg)
        confirm = messagebox.askyesno("Confirm Delete", "Are you Sure you want to delete all the transactions")
        if confirm:
            pft.delete_all(transactions, info_callback)
        


    btn_frame = tk.Frame(root)
    btn_frame.pack(pady = 10)

    #linked buttons are added to the button frame 
    tk.Button(btn_frame,text ="Add Transaction", command = open_win1).grid(row=0,column = 0,padx = 10)
    tk.Button(btn_frame,text = "View Summary", command =open_win2).grid(row =0, column = 1,padx = 10)
    tk.Button(btn_frame,text ="Search by Expense",command= open_win3).grid(row = 0,column = 2,padx = 10)
    tk.Button(btn_frame,text ="Search by Type", command = open_win4).grid(row=1,column = 0,padx = 10, pady = 10)
    tk.Button(btn_frame,text ="Delete", command = open_win5).grid(row=1,column = 1,padx = 10, pady = 10)
    tk.Button(btn_frame,text ="Delete All", command = open_win6).grid(row=1,column = 2,padx = 10, pady = 10)


    root.mainloop()



if __name__ == "__main__":
    start_gui()
