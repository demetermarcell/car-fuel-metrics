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
WORKSHEET = SHEET.worksheet('fuel_data')


# Navigation functions:
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
    print("Latest Fueling Metrics:")
    trip_distance = calculate_latest_trip_distance()
    latest_gas_mileage = calculate_latest_gas_mileage()
    print(f"Latest Trip Distance: {trip_distance}km.")
    print(f"Latest Gas Mileage: {latest_gas_mileage}l/100km.\n")
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


# Latest metrics calculation functions:
def calculate_latest_gas_mileage():
    """
    Function to calculate the latest gas mileage.
    """
    print("Calculating Latest Gas Mileage")
    latest_trip_distance = float(calculate_latest_trip_distance())
    fuel_quantity_data = validate_data(3)  # This is a list of floats
    latest_fuel_quantity = fuel_quantity_data[-1]  # type: ignore
    return round(latest_fuel_quantity / latest_trip_distance * 100, 2)


def calculate_latest_trip_distance():
    """
    Function to calculate the latest trip distance.
    Calls the validate_data() function to validate odometer readings data.
    Calculates the latest trip distance by subtracting the last two readings.
    """
    odo_data = validate_data(2)
    latest_trip_distance = odo_data[-1] - odo_data[-2]  # type: ignore
    return latest_trip_distance


# Validate data retrieval from Google Sheets:
def validate_data(col_num):
    """
    Function to validate data retrieval from Google Sheets.
    """
    try:
        data = WORKSHEET.col_values(col_num)
        # Check if there are no readings or only the header row.
        if not data or len(data) < 2:
            print("Not enough data available.")
            return None
        else:
            # Remove first item (header row).
            data = data[1:]
            if col_num == 1:  # Date column
                return (validate_date_data(data))
            elif col_num == 2:  # Odometer readings column
                return (validate_int_data(data))
            elif col_num == 3:  # Fuel quantity column
                return (validate_float_data(data, col_num))
            elif col_num == 4:  # Fuel cost column
                return (validate_float_data(data, col_num))
            else:
                print("Invalid column number.")
                return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def validate_int_data(int_data):
    """
    Function to validate if odometer readings data is integers.
    """
    # Converts all items to integers and checks if they are all digits.
    if all(str(item).isdigit() for item in int_data):
        # Converts all items to integers and returns them in a list.
        test_data = list(map(int, int_data))
        print(test_data)
        return list(map(int, int_data))   # type: ignore
    else:
        print("Odometer readings data is invalid.")
        return None


def validate_float_data(float_data, col_num):
    """
    Function to validate float data.
    """
    if all(str(item).replace('.', '', 1).isdigit() for item in float_data):
        test_data = list(map(float, float_data))
        print(test_data)
        return list(map(float, float_data))
    else:
        if col_num == 3:
            type_data = "Fuel quantity"
        elif col_num == 4:
            type_data = "Fuel cost"
        print(f"{type_data} data is invalid.")
        return None


def validate_date_data(date_data):
    """
    Function to validate date data.
    """
    # Check if all items are in the format yyyy.mm.dd.
    if all(item.count('.') == 2 for item in date_data):
        print(date_data)
        return date_data
    else:
        print("Date data is invalid.")
        return None


# Run the app:
print("Welcome to the Car Fuel Metrics App")
select_mode()
