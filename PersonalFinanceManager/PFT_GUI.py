'''
Date - 20: Sept:2025
Author - Data-Divaa
Desc - Personal Finance Manager GUI using tkinter 
'''

import tkinter as tk 
import PersonalFinanceTracker as pft  


#main window 
root = tk.Tk()
root.title("Personal Finace Tracker")

#label added
tk.Label(root, text = "Personal Finance Tracker", font =("helvetica",20)).pack(pady=10)

#creating a frame for buttons 
btn_frame = tk.Frame(root)
btn_frame.pack(pady = 10)

#linked buttons are added to the button frame 
tk.Button(btn_frame,text ="Add Transaction", command = pft.add_transaction).grid(row=0,column = 0,padx = 10)
tk.Button(btn_frame,text = "View Summary", command =pft.view_summary).grid(row =0, column = 1,padx = 10)
tk.Button(btn_frame,text ="Search by Type",command= pft.search_by_type).grid(row = 0,column = 2,padx = 10)
tk.Button(btn_frame,text ="Search by Description", command = pft.search_by_desc).grid(row=1,column = 0,padx = 10, pady = 10)
tk.Button(btn_frame,text ="Delete", command = pft.delete_transaction).grid(row=1,column = 1,padx = 10, pady = 10)
tk.Button(btn_frame,text ="Delete All", command = pft.delete_all).grid(row=1,column = 2,padx = 10, pady = 10)

root.mainloop()