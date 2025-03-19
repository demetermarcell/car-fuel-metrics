import gspread
from google.oauth2.service_account import Credentials


# Google Sheets API setup:
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


# Menu Navigation functions:
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
            odo_data_input()
            break
        elif mode == "2":
            select_metrics()
            break
        else:
            print("Invalid input. Please try again.")


def select_metrics():
    """
    Function to select metrics type.
    Run a while loop until the user selects a valid option.
    Calls the latest_metrics() function if user selection is 1.
    Calls the select_year function if user selection is 2.
    Calls the total_ownership_metrics() function if user selection is 3.
    Calls the select_mode() function if user selection is 4.
    """

    while True:
        print("Please select which metrics you would like to see:")
        print("1: Latest Fueling Metrics")
        print("2: Total Ownership Metrics")
        print("3: Back to Mode Selection")

        mode = input("Enter the number of your selected metrics: \n")

        if mode == "1":
            latest_metrics()
            break
        elif mode == "2":
            total_ownership_metrics()
            break
        elif mode == "3":
            select_mode()
            break
        else:
            print("Invalid input. Please try again.")


# Main Metrics functions:
def latest_metrics():
    """This function prints metrics from the latest refueling."""
    trip_distance = calculate_latest_trip_distance()
    latest_gas_mileage = calculate_latest_gas_mileage()
    print("\n")
    print("Latest Fueling Metrics:")
    print(f"Latest Trip Distance: {trip_distance}km.")
    print(f"Latest Gas Mileage: {latest_gas_mileage}l/100km.\n")
    navigate_metrics()


def total_ownership_metrics():
    """This function prints the total ownership metrics."""
    total_distance = calculate_total_trip_distance()
    total_fuel_quantity = calculate_total_fuel_quantity()
    total_fuel_cost = calculate_total_fuel_cost()
    average_gas_mileage = calculate_total_average_gas_mileage()
    average_fuel_price = calculate_total_average_fuel_price()

    print("\n")
    print("Total Ownership Metrics:")
    print(f"Total Trip Distance: {total_distance}km.")
    print(f"Total Fuel Quantity: {total_fuel_quantity}l.")
    print(f"Total Fuel Cost: ${total_fuel_cost}EUR.")
    print(f"Average Gas Mileage: {average_gas_mileage}l/100km.")
    print(f"Average Fuel Price: ${average_fuel_price}EUR/l.\n")
    navigate_metrics()


# Latest metrics calculation functions:
def calculate_latest_gas_mileage():
    """
    Function to calculate the latest gas mileage.
    Calls the calculate_latest_trip_distance() function to get the latest trip
    distance nad converts it to a float.
    Calls the validate_data(2) function to get the fuel quantity data.
    Calculates the latest fuel quantity by dividing the latest fuel quantity
    by the latest trip distance and multiplying by 100 resulting in l/100km.
    """
    latest_trip_distance = float(calculate_latest_trip_distance())
    fuel_quantity_data = validate_data(2)  # This is a list of floats
    latest_fuel_quantity = fuel_quantity_data[-1]  # type: ignore
    return round(latest_fuel_quantity / latest_trip_distance * 100, 2)


def calculate_latest_trip_distance():
    """
    Function to calculate the latest trip distance.
    Calls the validate_data(1) function to validate odometer readings data.
    Calculates the latest trip distance by subtracting the last two readings.
    """
    odo_data = validate_data(1)
    latest_trip_distance = odo_data[-1] - odo_data[-2]
    return latest_trip_distance


# Total ownership metrics calculation functions:
def calculate_total_trip_distance():
    """
    Function to calculate the total trip distance.
    Calls the validate_data(1) function to validate odometer readings data.
    Calculates the total trip distance by subtracting the first and last
    readings.
    """
    odo_data = validate_data(1)
    total_trip_distance = odo_data[-1] - odo_data[0]
    return total_trip_distance


def calculate_total_fuel_quantity():
    """
    Function to calculate the total fuel quantity.
    Calls the validate_data(2) function to validate fuel quantity data.
    Calculates the total fuel quantity by summing all the fuel quantity data.
    """
    fuel_quantity_data = validate_data(2)
    total_fuel_quantity = sum(fuel_quantity_data)
    return total_fuel_quantity


def calculate_total_fuel_cost():
    """
    Function to calculate the total fuel cost.
    Calls the validate_data(3) function to validate fuel cost data.
    Calculates the total fuel cost by summing all the fuel cost data.
    """
    fuel_cost_data = validate_data(3)
    total_fuel_cost = sum(fuel_cost_data)
    return round(total_fuel_cost, 2)


def calculate_total_average_gas_mileage():
    """
    Function to calculate the total average gas mileage.
    Calls the calculate_total_trip_distance() function to get the total trip
    distance and converts it to a float.
    Calls the calculate_total_fuel_quantity() function to get the total fuel
    quantity.
    Calculates the total average gas mileage by dividing the total fuel
    quantity by the total trip distance and multiplying by 100 resulting in
    l/100km.
    """
    total_trip_distance = float(calculate_total_trip_distance())
    total_fuel_quantity = calculate_total_fuel_quantity()
    return round(total_fuel_quantity / total_trip_distance * 100, 2)


def calculate_total_average_fuel_price():
    """
    Function to calculate the total average fuel price
    Calls the calculate_total_fuel_cost() function to get the total fuel cost.
    Calls the calculate_total_fuel_quantity() function to get the total fuel
    quantity.
    Calculates the total average fuel price by dividing the total fuel cost by
    the total fuel quantity.
    """
    total_fuel_cost = calculate_total_fuel_cost()
    total_fuel_quantity = calculate_total_fuel_quantity()
    return round(total_fuel_cost / total_fuel_quantity, 2)


# Validate data retrieval from Google Sheets:
def validate_data(col_num):
    """
    Function to validate data retrieval from Google Sheets.
    Retreives data from the Google Sheet based on the column number,
    and calls the appropriate validation function.
    Throws an error message and returns to the mode selection menu if an error.
    """
    try:
        data = WORKSHEET.col_values(col_num)
        # Check if there are no readings or only the header row.
        if not data or len(data) < 2:
            print(
                "Not enough data available."
                "Please input data before calculating metrics."
            )
            select_mode()
        else:
            # Remove first item (header row).
            data = data[1:]
            if col_num == 1:  # Odometer readings column
                return (validate_int_data(data))
            elif col_num == 2:  # Fuel quantity column
                return (validate_float_data(data, col_num))
            elif col_num == 3:  # Fuel cost column
                return (validate_float_data(data, col_num))
            else:
                print(
                    "Invalid column number."
                    "Please contact the developer for assistance."
                    )
                select_mode()
    except Exception as e:
        print(f"An error occurred: {e}")
        select_mode()


def validate_int_data(int_data):
    """
    Function to validate if odometer readings data is integers.
    Throws an error message and returns to the mode selection menu if an error.
    """
    # Converts all items to integers and checks if they are all digits.
    if all(str(item).isdigit() for item in int_data):
        # Converts all items to integers and returns them in a list.
        return list(map(int, int_data))
    else:
        print(
            "Odometer readings data is invalid."
            "Please contact the developer for assistance."
            )
        select_mode()


def validate_float_data(float_data, col_num):
    """
    Function to validate float data.
    Throws an error message and returns to the mode selection menu if an error.
    """
    if all(str(item).replace('.', '', 1).isdigit() for item in float_data):
        return list(map(float, float_data))
    else:
        if col_num == 2:
            type_data = "Fuel quantity"
        elif col_num == 3:
            type_data = "Fuel cost"
        print(
            f"{type_data} data is invalid."
            "Please contact the developer for assistance."
            )
        select_mode()


# Menu Navigation function:
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


# Data input functions:
def odo_data_input():
    """
    Function to input odometer readings data.
    Run a while loop until the user inputs valid data.
    Calls the validate_odo_input() function.
    Calls the fuel_data_input() function if data entry is successful.
    """
    while True:
        print("Please input your odometer readings data:")
        print("Example: 123456")

        odo_data = input("Enter the odometer readings here: \n")

        if validate_odo_input(odo_data):
            print("Odometer readings data input successful.")
            break

    return odo_data


def fuel_data_input():
    """
    Function to input fueling data.
    Run a while loop until the user inputs valid data.
    Calls the validate_fuel_data() function.
    Calls the select_mode() function if data entry is successful.
    """
    while True:
        print("Please input your fueling data:")
        print("Example: 23.45")

        fuel_quantity = input("Enter the fuel quantity here: \n")
        fuel_cost = input("Enter the fuel cost here: \n")

        if validate_fuel_data(fuel_quantity, fuel_cost):
            print("Fueling data input successful.")
            break
    return fuel_quantity, fuel_cost


# Validate input data functions:
def validate_odo_input(odo_data):
    """
    Function to validate odometer readings data input.
    Checks if the data is an integer.
    Checks if the data is greater than the last reading.
    """
    last_odo_data = validate_data(1)[-1]  # This is integer.
    if not odo_data.isdigit():
        print("Odometer readings data must be an integer.")
        return False
    else:
        odo_data_int = int(odo_data)

        if int(odo_data_int) < last_odo_data:
            print("Odometer reading must be greater than the last reading.")
            print(f"Last reading: {last_odo_data}")
            return False
        else:
            return True


def validate_fuel_data(fuel_quantity, fuel_cost):
    """
    Function to validate fueling data input.
    Checks if the data is a float.
    Checks if the data is greater than 0.
    Checks if the data is less than 40 for fuel quantity.
    (40 is the maximum capacity of the fuel tank)
    """
    if not fuel_quantity.replace('.', '', 1).isdigit():
        print("Fuel quantity must be a float.")
        return False
    elif not fuel_cost.replace('.', '', 1).isdigit():
        print("Fuel cost must be a float.")
        return False
    else:
        fuel_quantity_float = float(fuel_quantity)
        fuel_cost_float = float(fuel_cost)

        if fuel_quantity_float <= 0:
            print("Fuel quantity must be greater than 0.")
            return False
        elif fuel_quantity_float >= 40:
            print("Fuel quantity must not exceed 40.")
            return False
        elif fuel_cost_float <= 0:
            print("Fuel cost must be greater than 0.")
            return False
        else:
            return True


def confirm_data_input(odo_data, fuel_quantity, fuel_cost):
    """
    Function to confirm data input.
    Run a while loop until the user confirms the data input.
    Calls the select_mode() function if data entry is successful.
    """

    new_data_input = [odo_data, fuel_quantity, fuel_cost]
    while True:
        print("Please confirm your data inputs:")
        print(f"Odometer: {odo_data}km")
        print(f"Fuel Quantity: {fuel_quantity}l")
        print(f"Fuel Cost: {fuel_cost}EUR\n")
        print("Press number to select action:")
        print("1: Confirm, Save Data")
        print("2: Re-enter data")
        print("3: Cancel Data Input")

        confirm_data = input("Enter the number of your selected action: \n")

        if confirm_data == "1":
            upload_data(new_data_input)
            select_mode()
            break
        elif confirm_data == "2":
            data_input()
            break
        elif confirm_data == "3":
            print("Data input cancelled.")
            select_mode()
            break
        else:
            print("Invalid input. Please try again.")


def upload_data(data):
    """
    Function to upload data to Google Sheets.
    Calls the append_row() function to append the data to the Google Sheet.
    """
    try:
        print("Data input confirmed.")
        print("Uploading data to Google Sheets...")
        WORKSHEET.append_row(data)
        print("Data uploaded successfully.\n")
    except Exception as e:
        print(f"An error occurred: {e.args}")
        select_mode()


def data_input():
    """
    Function to input data.
    Calls the odo_data_input() function to input odometer readings data.
    Calls the fuel_data_input() function to input fueling data.
    Calls the confirm_data_input() function to confirm data input.
    """
    odo_data = odo_data_input()
    fuel_quantity, fuel_cost = fuel_data_input()
    confirm_data_input(odo_data, fuel_quantity, fuel_cost)


# Run the app:
print("Welcome to the Car Fuel Metrics App")
# select_mode()

data_input()
