import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('cfmcred.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ci_car_fuel_metrics')


def select_mode():
    """
    Function to select the mode of the app.
    Run a while loop until the user selects a valid mode.
    Calls the data_input() function if mode is 1.
    Calls the select_metrics() function if mode is 2.
    """
    while True:
        print("Please select mode:")
        print("1: Input Fueling Data")
        print("2: View Metrics")

        mode = input("Enter your selected mode's number: \n")

        if mode == "1":
            data_input()
            break
        elif mode == "2":
            select_metrics()
            break
        else:
            print("Invalid input. Please try again.")


def data_input():
    print("Data Input Mode")


def select_metrics():
    print("Metrics Mode")


print("Welcome to the Car Fuel Metrics App")
select_mode()
