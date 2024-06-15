# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

#Spreadsheet weblink
"""
https://docs.google.com/spreadsheets/d/1eRzudCSUTXbOoQNGQWoZAAvzvJGvzIE8t3iOZxcQmvc/edit?gid=334103161#gid=334103161
"""


import gspread
from google.oauth2.service_account import Credentials
import os
import TableIt #To create the table in the terminal
import time
# To send email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import date 
from datetime import datetime
import pandas as pd

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

    sys_values = ["1", "2", "3", "4", "5", "6", "7", "00"]
    global user_input

    while True:
        print("\033[92m" + f"Please select one of the following {sys_values} : \n")
        print("\033[92m" + "< 1 >" + " - Create New Staff Record")
        print("\033[92m" + "< 2 >" + " - Take Leave")
        print("\033[92m" + "< 3 >" + " - Email Details")
        print("\033[92m" + "< 4 >" + " - Display All Staff Details")
        print("\033[92m" + "< 5 >" + " - Display Staff Leave Record")
        print("\033[92m" + "< 6 >" + " - Clear Screen")
        print("\033[92m" + "< 7 >" + " - Delete Staff Record")
        print("\033[92m" + "< 00 >" + " - Exit System\n")

        try:
            user_input = int(input(">> " + "\033[0m\n"))
        except ValueError:
            print("Invalid input : Please enter a valid integer.\n")
            get_user_selection()
        
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
        print("\033[92m" + f"Enter staff grade {grade_list[1:5]}\n")
        user_input = input(">> " + "\033[0m\n")
        user_input = user_input.upper()
        
        """
        Retrieve grade and total leave from spreadsheet and validate that the user entry is correct and return the total 
        number of annual leave the staff is entitled.
        """
        grade_list = detail.col_values(1)
    
        result = validate_data_str(grade_list, user_input)
        if result == True:
            annual_leave = get_grade_total_leave(user_input)
            if annual_leave == False:
                break

            new_list.append(user_input)
        else:
            print("Invalid input : Please enter correct grade.\n")
            create_new_record()
            break

        # Get user input for first name, last name, email
        print("\033[92m" + "Enter staff first name")
        user_input = input(">> " + "\033[0m\n")
        new_list.append(user_input)

        print("\033[92m" + "Enter staff last name")
        user_input = input(">> " + "\033[0m")
        new_list.append(user_input)

        print("\033[92m" + "Enter staff email address")
        user_input = input(">> " + "\033[0m\n")
        new_list.append(user_input)

        # Add annual leave to new list
        new_list.append(annual_leave)
        new_list.append(0)
    
        #Append new staff details to spreadsheet00
        
        print(f"Updating new record...\n")
        worksheet_to_update = SHEET.worksheet("staff_details")
        worksheet_to_update.append_row(new_list)
        print(f"New staff details updated successfully\n")
        print("Press Enter to continue...")
        input("\033[92m" + ">> " + "\033[0m")
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
    global selected_details
    selected_record = []
    reasons = []

   # global user_input_staff
    global user_input

    today = date.today()
    today = today.strftime("%d/%m/%Y")
    
    # Retrieve all staff details from spreadsheet function
    selected_details = []
    selected_details = retrieve_allstaff_details()
    
    while True:

        """
        Check how many staff are in the database. This number will be compare with the user input in case the user 
        enter a wrong number.
        """
        total_staff = get_new_staff_number()

        # Allow user to select which staff is taking leave by enter the staff number and checking that it is an int
        print("\033[92m" + "Please select staff number :")
        try:
            user_input_staff = int(input(">> " + "\033[0m\n"))
            
            if int(total_staff) >= user_input_staff:
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
                break
            
            else:
                print("Invalid input : Please enter correct staff number.\n")            
        except ValueError:
            print("Invalid input: Please enter a valid integer.\n")
     
    """
    Get user input on the start date and end date of the annual leave and then calculate the no of days taken
    """
    while True:
        try:
            print("\033[92m" + "Please enter a start date [DD/MM/YYYY] :")
            user_input_start = input(">> " + "\033[0m\n")
            user_input_start_dt = datetime.strptime(user_input_start, '%d/%m/%Y')
            result = validate_startend_date(user_input_start, user_input_staff)
            print(result)
            if result == False:
                final_input_list.append(user_input_start)
                break
            else:
                print("Invalid input: Staff has taken leave.\n")
        except ValueError:
            print("Invalid input: Please enter a valid start date.\n")
    
    while True:
        try:
            print("\033[92m" + "Please enter end date [DD/MM/YYYY] :")
            user_input_end = input(">> " + "\033[0m\n")
            user_input_end_dt = datetime.strptime(user_input_end, '%d/%m/%Y')
            final_input_list.append(user_input_end)
            break
        except ValueError:
            print("Invalid input: Please enter a valid end date.\n")

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
    
    while True:
        # Allow user to select which the leave code
        print("\033[92m" + "Please select the leave code :")
       
        try:
            user_input = int(input(">> " + "\033[0m\n"))
            """
            if user select 1 which is holiday or time off, the system will deduct the no of leave and update the staff details.
            if user select 2 which is sick leave, the system will update the sick leave column.
            """
            if int(user_input) <= 4:
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
                print("Press Enter to continue...")
                input("\033[92m" + ">> " + "\033[0m\n")
                break
            else:
                print("Invalid input : Please enter correct leave code.\n")  
        except ValueError:
            print("Invalid input: Please enter a valid integer.\n")

def validate_startend_date(user_date, staff_no):
    """
    When user input the start and end date when taking leave, the dates are checked against the records to ensure that there is
    no duplication
    """

    
    # Retrieve staff leave details from spreadsheet
    detail = SHEET.worksheet("records")
    all_leave_list = detail.get_all_values()
    print ("Retrieving data from database ...\n")
    
    for date_row in all_leave_list:
        
        data_date = date_row
        #print(data_date)
        if (str(data_date[1]) == str(staff_no)):
            
            if (str(user_date) == str(data_date[5]) or str(user_date) <= str(data_date[6])):
                print("YES")
                return True

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

def display_leave_record():

    # Retrieve all staff details from spreadsheet function
    selected_leave_details = []
    selected_details = []
    selected_details = retrieve_allstaff_details()
    
    while True:

        """
        Check how many staff are in the database. This number will be compare with the user input in case the user 
        enter a wrong number.
        """
        total_staff = get_new_staff_number()
    
        # Allow user to select which staff is taking leave by enter the staff number and checking that it is an int
        print("\033[92m" + "Please select staff number to display that staff records :")
        try:
            user_input_staff = int(input(">> " + "\033[0m\n"))
            
            if int(total_staff) >= user_input_staff:
                selected_record = selected_details[int(user_input_staff)]
                """
                Append retrieved information into new list and write to spreadsheet starting with
                date, staff number, fname, lname, email, date start, date end, leave taken and reason
                """
                
                # Retrieve staff leave details from spreadsheet
                detail = SHEET.worksheet("records")
                staff_leave_list = detail.get_all_values()
                print ("Retrieving data from database ...\n")
    
                for row in staff_leave_list:
                    staff_no = row
                    if (str(staff_no[1]) != "staff_no"):
                        if (int(staff_no[1]) == int(user_input_staff)):
                            selected_leave_details.append(row[0:9])

                if not selected_leave_details: 
                    print("Staff has not taken any leave. No record found")
                    print("\n")
                    print("Press Enter to continue...")
                    input("\033[92m" + ">> " + "\033[0m\n")
                    break
                else:
                    TableIt.printTable(selected_leave_details)
                    print("\n")
                    print("Press Enter to continue...")
                    input("\033[92m" + ">> " + "\033[0m\n")
                    break
            
            else:
                print("Invalid input : Please enter correct staff number.\n")            
        except ValueError:
            print("Invalid input: Please enter a valid integer.\n")

def delete_record():
    """
    This is a function to delete the row in the spreadsheet when the staff leave the company
    """
    # First to call the retrieve all staff details
    selected_details = []
    selected_details = retrieve_allstaff_details()
    while True:

        # Allow user to select which staff record to delete by enter the staff number
        print("\033[92m" + "Please select staff number :")
        try:
            user_input_staff = int(input(">> " + "\033[0m\n"))
            # Retrieve the total number of staffs in the database
            total_staff = get_new_staff_number()
            if int(total_staff) >= user_input_staff:
                selected_record = selected_details[int(user_input_staff)]
                worksheet_to_update = SHEET.worksheet("staff_details")
                worksheet_to_update.delete_rows(int(user_input_staff)+1)
                print(f"Record successfully deleted\n")
                print("Press Enter to continue...")
                input("\033[92m" + ">> " + "\033[0m\n")
                break
            else:
                print("Invalid input: Please enter correct staff number.\n")

        except ValueError:
            print("Invalid input: Please enter a valid integer.\n")
        
def send_email():
    
    # First to call the retrieve all staff details
    selected_details = []
    selected_details = retrieve_allstaff_details()
    
    while True:
        
        """ 
        Check how many staff are in the database. This number will be compare with the user input in case the user 
        enter a wrong number.
        """
        total_staff = get_new_staff_number()

        # Allow user to select which staff is taking leave by enter the staff number and checking that it is an int
        print("\033[92m" + "Please select staff number to email the staff :")
        try:
            user_input_staff = int(input(">> " + "\033[0m\n"))
            
            if int(total_staff) >= user_input_staff:
                selected_record = selected_details[int(user_input_staff)]
                break
            else:
                print("Invalid input : Please enter correct staff number.\n")            
        except ValueError:
            print("Invalid input: Please enter a valid integer.\n")


    """
    Setting up the system to send an email
    """    
    sender_email = "jctest018@gmail.com"
    receiver_email = selected_record[4]
    subject = "Leave Updated Record"

    # Creating email content
    email_content = ("**This is an auto-generated email**" + "\n\n" "Total leave remaining : " + selected_record[5] +"\n" + "Total sick leave taken : " + selected_record[6] + "\n\n" + "Thank you")
    print(email_content)

    message = email_content

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "jctest018"
    smtp_password = "hckq mhew altd seoe"
   
    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Add body to the email
    msg.attach(MIMEText(message, "plain"))

    try:
        # Create a secure SSL/TLS connection to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.ehlo()

        # Login to the SMTP server
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())

        # Close the SMTP connection
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email. Error:", str(e))


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
            print ("Display All Staff Details ...\n")
            retrieve_allstaff_details()
            print("\n")
            print("Press Enter to continue...")
            input("\033[92m" + ">> " + "\033[0m\n")
            option_selected = get_user_selection()

        elif int(option_selected) == 5:
            print ("Display Staff Leave Record ...\n")  
            display_leave_record()
            option_selected = get_user_selection()

        elif int(option_selected) == 6:
            print ("Clearing Screen ...\n")  
            os.system('clear')
            option_selected = get_user_selection()

        elif int(option_selected) == 7:
            print ("Delete Staff Records ...\n")  
            delete_record()
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