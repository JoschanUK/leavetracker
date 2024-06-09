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
import TableIt #To create the table in the terminal
import time
import smtplib #To send emails out
from datetime import date 

#smtpObj = smtplib.SMTP( [live.smtp.mailtrap.io [587]] )

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('annual_leave')

def get_user_selection():

    sys_values = ["1", "2", "3", "4", "5", "6", "00"]

    while True:
        print("\033[92m" + f"Please select one of the following {sys_values} : \n")
        print("\033[92m" + "< 1 >" + " - Create New Staff Record")
        print("\033[92m" + "< 2 >" + " - Take Leave")
        print("\033[92m" + "< 3 >" + " - Email Details")
        print("\033[92m" + "< 4 >" + " - Retrieve All Staff Details")
        print("\033[92m" + "< 5 >" + " - Delete Staff Record")
        print("\033[92m" + "< 6 >" + " - Clear Screen")
        print("\033[92m" + "< 00 >" + " - Exit System\n")

        user_input = input(">> " + "\033[0m")
        if validate_data_int(sys_values, user_input):
            break
        else:
            os.system('clear')
    return user_input
    
def validate_data_int(sys_values, user_value):
    """
    To check if the user entry and the system values are correct
    """
    x = 0
    for value in sys_values:
         if int(user_value) == int(sys_values[x]):
            return True
         x+=1
    return False

def validate_data_str(sys_values, user_value):
    """
    To check if the user entry and the system values are correct
    """
    x = 0
    for value in sys_values:
         if str(user_value) == str(sys_values[x]):
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
        
        """
        Retrieve grade and total leave from spreadsheet and validate that the user entry is correct and return the total 
        number of annual leave the staff is entitled.
        """
        grade_list = detail.col_values(1)
    
        result = validate_data_str(grade_list, user_input)
        if result == True:
            annual_leave = get_grade_total_leave(user_input)
            print(annual_leave)

            if annual_leave == False:
                break

            new_list.append(user_input)
        else:
            print("Error : Please enter correct grade.")
            create_new_record()
            break

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
        break
    
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

def take_leave():
    """
    When user input to take leave. The system will retrieve the staff names from the spreadsheet and then ask user to 
    select the staff who wants to take leave. The system will also ask for the start and end date and the reason for 
    taking this leave
    """
    
    final_input_list = []
    selected_details = []
    selected_record = []
    reasons = []

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    
    # Retrieve all staff details from spreadsheet function
    selected_details = retrieve_allstaff_details()
    

    # Allow user to select which staff is taking leave by enter the staff number
    print("\033[92m" + "Please select staff number :")
    user_input_staff = input(">> " + "\033[0m")
        
    """
    Check how many staff are in the database. This number will be compare with the user input in case the user enter a wrong number.
    """
    total_staff = get_new_staff_number()

    if int(total_staff) <= 1:

        selected_record = selected_details[int(user_input_staff)]
        """
        Append retrieved information into new list and write to spreadsheet starting with
        date, staff number, fname, lname, email, date start, date end, leave taken and reason
        """
    
        final_input_list.append(today)
        final_input_list.append(selected_record[0])
        final_input_list.append(selected_record[2])
        final_input_list.append(selected_record[3])
        final_input_list.append(selected_record[4])
    else:
        print("Error : Please enter correct staff number.")
        take_leave()
    """
    Get user input on the start date and end date of the annual leave and then calculate the no of days taken
    """
    print("\033[92m" + "Please start date [DD/MM/YYYY] :")
    user_input_start = input(">> " + "\033[0m")
    final_input_list.append(user_input_start)

    print("\033[92m" + "Please end date [DD/MM/YYYY] :")
    user_input_end = input(">> " + "\033[0m")
    final_input_list.append(user_input_end)
      
    date_format = "%d/%m/%Y"
    a = time.mktime(time.strptime(user_input_start, date_format))
    b = time.mktime(time.strptime(user_input_end, date_format))
    total_leave = b - a
    total_leave = int(total_leave / 86400)
    final_input_list.append(total_leave)
    
    # Retrieve reasons for taking leave from spreadsheet
    detail = SHEET.worksheet("reason")
    reasons = detail.get_all_values()
    print ("Retrieving data from database ...\n")
    TableIt.printTable(reasons)
    
    # Allow user to select which the leave code
    print("\033[92m" + "Please select the leave code :")
    user_input = input(">> " + "\033[0m")
    """
    if user select 1 which is holiday or time off, the system will deduct the no of leave and update the staff details
    """
    if int(user_input) == 1:
        update_holidays_record(user_input_staff, selected_record[5],total_leave)
    elif int(user_input) == 2:
        update_sickness_record(user_input_staff, selected_record[6],total_leave)

    reasons = reasons[int(user_input)]
    final_input_list.append(reasons[1])
    
    #Append new leave details to spreadsheet
    print(f"Updating rew record...\n")
    worksheet_to_update = SHEET.worksheet("records")
    worksheet_to_update.append_row(final_input_list)
    print(f"New leave details updated successfully\n")

def update_holidays_record(staff_no, total_annual, total_leave):
    
    worksheet_to_update = SHEET.worksheet("staff_details")
    total_annual = int(total_annual) - int(total_leave)
    worksheet_to_update.update_cell(int(staff_no)+1, 6, total_annual)

def update_sickness_record(staff_no, total_sick, no_sick):

    worksheet_to_update = SHEET.worksheet("staff_details")
    total_sick = int(total_sick) + int(no_sick)
    worksheet_to_update.update_cell(int(staff_no)+1, 7, total_sick)


def retrieve_allstaff_details():

    selected_details = []
    # Retrieve staff details from spreadsheet
    detail = SHEET.worksheet("staff_details")
    staff_list = detail.get_all_values()
    print ("Retrieving data from database ...\n")
    
    for col_1 in staff_list:
        selected_details.append(col_1[0:7])
    TableIt.printTable(selected_details)
    print("\n")
    return selected_details


def delete_record():
    """
    This is a function to delete the row in the spreadsheet when the staff leave the company
    """
    # First to call the retrieve all staff details
    selected_details = []

    selected_details = retrieve_allstaff_details()
    
    # Allow user to select which staff record to delete by enter the staff number
    print("\033[92m" + "Please select staff number :")
    user_input_staff = input(">> " + "\033[0m")

    # Retrieve the total number of staffs in the database
    total_staff = get_new_staff_number()

    if int(total_staff) <= 1:
        selected_record = selected_details[int(user_input_staff)]
        worksheet_to_update = SHEET.worksheet("staff_details")
        worksheet_to_update.delete_rows(int(user_input_staff)+1)
        print(f"Record successfully deleted\n")
    else:
        print("Error : Please enter correct staff number.")
        delete_record()

def send_email():
    
    # First to call the retrieve all staff details
    selected_details = []

    selected_details = retrieve_allstaff_details()
    
    # Allow user to select which staff to send the email to by enter the staff number
    print("\033[92m" + "Please select staff number to email the staff :")
    user_input_staff = input(">> " + "\033[0m")
    selected_record = selected_details[int(user_input_staff)]
    

    sender = "Administrator <mailtrap@leavetracker.com>"
    receiver = "A Test User <jctest018@gmail.com>"

    message = f"""\
    Subject: Hi Mailtrap
    To: {receiver}
    From: {sender}

    This is a test e-mail message."""

    with smtplib.SMTP("live.smtp.mailtrap.io", 587) as server:
        server.starttls()
        server.login("api", "304db84d02f75d57cfc7dd73632fa378")
        server.sendmail(sender, receiver, message)
    
    print("Email sent")


def main():
    """
    Creating a Main function to run all the program functions
    1. Get user selection
    """
    option_selected = get_user_selection()
    while option_selected != 00:
        if int(option_selected) == 1:
            print ("Create New Staff Record ...\n")
            create_new_record()
            option_selected = get_user_selection()
    
        elif int(option_selected) == 2:
            print ("Take Leave ...\n")
            take_leave()
            option_selected = get_user_selection()
    
        elif int(option_selected) == 3:
            print ("Email Details ...\n")
            send_email()
            option_selected = get_user_selection()

        elif int(option_selected) == 4:
            print ("Retrieve All Staff Details ...\n")
            retrieve_allstaff_details()
            option_selected = get_user_selection()

        elif int(option_selected) == 5:
            print ("Delete Staff Records ...\n")  
            delete_record()
            option_selected = get_user_selection()

        elif int(option_selected) == 6:
            print ("Clearing Screen ...\n")  
            os.system('clear')
            option_selected = get_user_selection()
        
        else :
            print("Exiting Tracking System ...\n")
            break 

    
    
    
        

print("\033[1m" + "Welcome to Leave Tracking System \n" + "\033[0m")
print("\033[1m" + "System Version 1.0\n" + "\033[0m")
print("\033[1m" + "**Unauthorised use is strictly prohibited**\n\n" + "\033[0m")

today = date.today()
today = today.strftime("%d/%m/%Y")
print(f"Today date is {today}.\n\n")
main()