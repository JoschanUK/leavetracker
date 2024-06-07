# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

#Spreadsheet weblink
"""
https://docs.google.com/spreadsheets/d/1C379qhO_6zp1L4n5kI8mIFIw0OEbyhBfbOJqzV9FH-0/edit?pli=1#gid=1106879757
"""


import gspread
from google.oauth2.service_account import Credentials
import os
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('annual_leave')

#sales = SHEET.worksheet('grade')

#data = sales.get_all_values()

#print(data)

def get_user_selection():

    sys_values = ["1", "2", "3", "4", "5", "00"]

    while True:
        print("\033[92m" + f"Please select one of the following {sys_values} : \n")
        print("\033[92m" + "< 1 >" + " - Create New Staff Record")
        print("\033[92m" + "< 2 >" + " - Take Leave")
        print("\033[92m" + "< 3 >" + " - Email Details")
        print("\033[92m" + "< 4 >" + " - Retrieve Details")
        print("\033[92m" + "< 5 >" + " - Delete Staff Record")
        print("\033[92m" + "< 00 >" + " - Exit System\n")

        user_input = input(">> " + "\033[0m")
        if validate_data(sys_values, user_input):
            print ("Entry is correct ...")
            break
        else:
            print ("Wrong!")
            os.system('clear')
    return user_input
    
def validate_data(sys_values, user_value):
    """
    To check if the user entry and the system values are correct
    """
    x = 0
    for value in sys_values:
         if int(user_value) == int(sys_values[x]):
            return True
         x+=1
    return False

def create_new_record():

    """
    This is a function to create a new staff record and to append into the staff_details
    tab of the spreasheet
    """
    new_list = []
    grade_list = []
    

    """
    Call a function to get the next staff number from the spreadsheet
    """
    # Get new staff number from the spreadsheet and append it to the new list
    last_staff_number = get_new_staff_number()
    new_staff_number = int(last_staff_number) + 1
    new_list.append(int(new_staff_number))

    # Retrieve staff grade from spreadsheet
    detail = SHEET.worksheet("grade")
    grade_list = detail.col_values(1)

    while True:
        # Get user input for staff grade
        print("\033[92m" + f"Enter staff grade {grade_list[1:5]}")
        user_input = input(">> " + "\033[0m")
        user_input = user_input.upper()

    # Retrieve grade and total leave from spreadsheet and validate that the user entry is correct and return the total 
    # number of annual leave the staff is entitled
        annual_leave = get_grade_total_leave(user_input)
        print(annual_leave)

        if annual_leave != False:
            break

    new_list.append(user_input)

    # Get user input for first name, last name, email
    print("\033[92m" + "Enter staff first name")
    user_input = input(">> " + "\033[0m")
    new_list.append(user_input)

    print("\033[92m" + "Enter staff last name")
    user_input = input(">> " + "\033[0m")
    new_list.append(user_input)

    print("\033[92m" + "Enter staff email address")
    user_input = input(">> " + "\033[0m")
    new_list.append(user_input)

    # Add annual leave to new list
    new_list.append(annual_leave)
    
    #Append new staff details to spreadsheet
    print(f"Updating rew record...\n")
    worksheet_to_update = SHEET.worksheet("staff_details")
    worksheet_to_update.append_row(new_list)
    print(f"New staff details updated successfully\n")

def get_new_staff_number():

    """
    A function to retrieve the next staff number from the spreadsheet
    """
    detail = SHEET.worksheet("staff_details")
    new_staff_number = detail.col_values(1)
    return new_staff_number[-1]

def get_grade_total_leave(user_input):

    detail = SHEET.worksheet("grade")
    grade_leave = detail.get_all_values()

    for col_1, col_2 in grade_leave:
        if str(user_input) == str(col_1):
            return col_2
    
    return False

def main():
    """
    Creating a Main function to run all the program functions
    1. Get user selection
    """
    option_selected = get_user_selection()
    
    if int(option_selected) == 00:
        print("Exiting Tracking System ...")
    
    elif int(option_selected) == 1:
        print ("Create New Staff Record")
        create_new_record()
    


print("\033[1m" + "Welcome to Leave Tracking System 1.0\n\n" + "\033[0m")
main()