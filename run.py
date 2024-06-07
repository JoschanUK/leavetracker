# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
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

    print("\033[92m" + f"Please select one of the following {sys_values} : \n")
    print("\033[92m" + "< 1 >" + " - Create New Staff Record")
    print("\033[92m" + "< 2 >" + " - Take Leave")
    print("\033[92m" + "< 3 >" + " - Email Details")
    print("\033[92m" + "< 4 >" + " - Retrieve Details")
    print("\033[92m" + "< 5 >" + " - Delete Staff Record")
    print("\033[92m" + "< 00 >" + " - Exit System\n")

    user_input = input(">> ")
    if validate_data(sys_values, user_input):
        print ("Entry is correct ...")
    else:
        print ("Wrong!")
       # break
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

def main():
    """
    Creating a Main function to run all the program functions
    1. Get user selection
    """
    option_selected = get_user_selection()
    print ([option_selected])
    


print("\033[1m" + "Welcome to Leave Tracking System 1.0\n\n" + "\033[0m")
main()