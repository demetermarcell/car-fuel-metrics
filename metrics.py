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


# Main Metrics functions:
def latest_metrics():
    """This function prints metrics from the latest refueling."""
    print("Latest Fueling Metrics:")
    trip_distance = calculate_latest_trip_distance()
    latest_gas_mileage = calculate_latest_gas_mileage()
    print(f"Latest Trip Distance: {trip_distance}km.")
    print(f"Latest Gas Mileage: {latest_gas_mileage}l/100km.\n")
    navigate_metrics()


def annual_metrics(selected_year):
    """This function prints the annual metrics for the selected year."""
    print(f"Metrics for {selected_year}")
    navigate_metrics()


def total_ownership_metrics():
    """This function prints the total ownership metrics."""
    print("Total Ownership Metrics")
    total_distance = calculate_total_trip_distance()
    total_fuel_quantity = calculate_total_fuel_quantity()
    total_fuel_cost = calculate_total_fuel_cost()
    average_gas_mileage = calculate_total_average_gas_mileage()
    average_fuel_price = calculate_total_average_fuel_price()
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
    Calls the validate_data(3) function to get the fuel quantity data.
    Calculates the latest fuel quantity by dividing the latest fuel quantity
    by the latest trip distance and multiplying by 100 resulting in l/100km.
    """
    latest_trip_distance = float(calculate_latest_trip_distance())
    fuel_quantity_data = validate_data(3)  # This is a list of floats
    latest_fuel_quantity = fuel_quantity_data[-1]  # type: ignore
    return round(latest_fuel_quantity / latest_trip_distance * 100, 2)  # type: ignore


def calculate_latest_trip_distance():
    """
    Function to calculate the latest trip distance.
    Calls the validate_data(2) function to validate odometer readings data.
    Calculates the latest trip distance by subtracting the last two readings.
    """
    odo_data = validate_data(2)
    latest_trip_distance = odo_data[-1] - odo_data[-2]  # type: ignore
    return latest_trip_distance


# Total ownership metrics calculation functions:
def calculate_total_trip_distance():
    """
    Function to calculate the total trip distance.
    Calls the validate_data(2) function to validate odometer readings data.
    Calculates the total trip distance by subtracting the first and last
    readings.
    """
    odo_data = validate_data(2)
    total_trip_distance = odo_data[-1] - odo_data[0]  # type: ignore
    return total_trip_distance


def calculate_total_fuel_quantity():
    """
    Function to calculate the total fuel quantity.
    Calls the validate_data(3) function to validate fuel quantity data.
    Calculates the total fuel quantity by summing all the fuel quantity data.
    """
    fuel_quantity_data = validate_data(3)
    total_fuel_quantity = sum(fuel_quantity_data)  # type: ignore
    return total_fuel_quantity


def calculate_total_fuel_cost():
    """
    Function to calculate the total fuel cost.
    Calls the validate_data(4) function to validate fuel cost data.
    Calculates the total fuel cost by summing all the fuel cost data.
    """
    fuel_cost_data = validate_data(4)
    total_fuel_cost = sum(fuel_cost_data)  # type: ignore
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


# Annual metrics calculation functions:
def get_years():
    """
    Function to get all the years from the Google Sheet.
    Calls the validate_data(1) function to validate the data.
    """
    date_data = validate_data(1)
    years = [date_data.split('.')[0] for date_data in date_data]  # type: ignore
    unique_years = sorted(list(set(years)))
    return unique_years


# Validate data retrieval from Google Sheets:
def validate_data(col_num):
    """
    Function to validate data retrieval from Google Sheets.
    Retreives data from the Google Sheet based on the column number,
    and calls the appropriate validation function.
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
        return list(map(int, int_data))   # type: ignore
    else:
        print("Odometer readings data is invalid.")
        return None


def validate_float_data(float_data, col_num):
    """
    Function to validate float data.
    """
    if all(str(item).replace('.', '', 1).isdigit() for item in float_data):
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
        return date_data
    else:
        print("Date data is invalid.")
        return None


# Menu Navigation function:
def navigate_metrics():
    """
    Function to navigate back to the metrics or to mode selection menu.
    Run a while loop until the user selects a valid option.
    Calls the select_mode() function if user selection is 1.
    Calls the select_metrics() function if user selection is 2.
    """
    # Local import to avoid circular dependency.
    from run import select_mode, select_metrics
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
