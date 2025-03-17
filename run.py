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

        mode = input("Enter the number of your selected mode: \n")

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
    """
    Function to select metrics type.
    Run a while loop until the user selects a valid option.
    Calls the latest_metrics() function if user selection is 1.
    Calls the annual_metrics() function if user selection is 2.
    Calls the total_ownership_metrics() function if user selection is 3.
    Calls the select_mode() function if user selection is 4.
    """
    while True:
        print("Please select which metrics you would like to see:")
        print("1: Latest Fueling Metrics")
        print("2: Annual Metrics")
        print("3: Total Ownership Metrics")
        print("4: Back to Mode Selection")

        mode = input("Enter the number of your selected metrics: \n")

        if mode == "1":
            latest_metrics()
            break
        elif mode == "2":
            annual_metrics()
            break
        elif mode == "3":
            total_ownership_metrics()
            break
        elif mode == "4":
            select_mode()
            break
        else:
            print("Invalid input. Please try again.")


def latest_metrics():
    print("Latest Metrics")
    navigate_metrics()


def annual_metrics():
    print("Annual Metrics")
    navigate_metrics()


def total_ownership_metrics():
    print("Total Ownership Metrics")
    navigate_metrics()


def navigate_metrics():
    """
    Function to navigate back to the metrics or to mode selection menu.
    Run a while loop until the user selects a valid option.
    Calls the select_mode() function if user selection is 1.
    Calls the select_metrics() function if user selection is 2.
    """
    while True:

        print("To navigate back: \n")
        print("1: Select Mode Menu")
        print("2: Select Metrics Menu")
        navigate_metrics = input("Enter the number of your selected menu \n")
        if navigate_metrics == "1":
            select_mode()
            break
        elif navigate_metrics == "2":
            select_metrics()
            break
        else:
            print("Invalid input. Please try again.")


print("Welcome to the Car Fuel Metrics App")
select_mode()
