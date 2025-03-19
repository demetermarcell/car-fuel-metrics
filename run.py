import metrics
import data_input


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
            data_input.data_input()
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
            metrics.latest_metrics()
            break
        elif mode == "2":
            select_year()
            break
        elif mode == "3":
            metrics.total_ownership_metrics()
            break
        elif mode == "4":
            select_mode()
            break
        else:
            print("Invalid input. Please try again.")


def select_year():
    """
    Function to select the year for annual metrics.
    Run a while loop until the user selects a valid year.
    Calls the annual_metrics() function with the selected year
    if the selected year is available in the data.
    """
    available_years = metrics.get_years()
    if not available_years or len(available_years) < 1:
        print("No data available.")
        select_metrics()
    else:
        while True:
            print("Available Years:")
            for year in available_years:
                print(year)
            selected_year = input("Enter the year you would like to view: \n")
            if selected_year in available_years:
                metrics.annual_metrics(selected_year)
                break
            else:
                print("Incorrect input value, please enter an available year.")


# Run the app:
print("Welcome to the Car Fuel Metrics App")
select_mode()
