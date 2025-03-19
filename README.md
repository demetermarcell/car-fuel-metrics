# Car Fuel Metrics

## Project Description:

The **Car Fuel Metrics** app is designed to help the developer to track and analyze their fuel usage by uploading fueling data and calculating key performance metrics. 
The app provides  the user with valuable insights into their car's fuel consumption patterns, helping them monitor fuel efficiency and make informed decisions about their driving habits. By storing the data and calculating key metrics, the app makes it easy for the car owner to track fuel costs and performance over time, encouraging better fuel management and cost savings.

You can find the link to the deployed application here: [LINK](https://ci-p3-car-fuel-metrics-3173a2b36120.herokuapp.com/)

![Responsive Preview](https://ui.dev/amiresponsive?url=https%3A%2F%2Fci-p3-car-fuel-metrics-3173a2b36120.herokuapp.com%2F)

## Features:

1. **Simple Navigation**:
    The app includes an intuitive navigation system through the terminal that allows users to easily switch between functions.

2. **Uploading Fueling Data**: 
   The app allows users to input crucial fueling information, including the **odometer reading**, **fuel quantity (in litres)**, and **fuel cost (in EUR)**. This data is collected during each fueling session, allowing users to maintain an accurate record of their car's fuel consumption and cost over time. The app ensures that all data is properly validated before uploading to ensure consistency and accuracy.

3. **Calculating Fuel Metrics**: 
   Once fueling data is uploaded, the app calculates various metrics to provide insights into the car's usage and performance:
   
   - **Latest Refueling Metrics**: The app can calculate and display:
     - **Trip Distance**: The distance driven since the last refueling, calculated by subtracting the previous odometer reading from the latest one.
     - **Gas Mileage**: The fuel efficiency of the car for the most recent refuel, computed by dividing the fuel quantity by the trip distance, then multiplying by 100 to express it in litres per 100 kilometers.
   
   - **Total Ownership Metrics**: The app also calculates metrics based on all uploaded fueling data to provide a comprehensive view of the car’s overall fuel consumption and costs:
     - **Total Distance**: The total distance driven since the first recorded odometer reading.
     - **Total Fuel Used**: The sum of all fuel quantities used across all refueling sessions.
     - **Total Fuel Cost**: The total amount spent on fuel, calculated by summing the fuel cost for each refueling.
     - **Average Gas Mileage**: The average fuel efficiency over the entire driving period, calculated by dividing the total fuel used by the total distance driven, then multiplying by 100.
     - **Average Fuel Price**: The average price of fuel per liter over all refueling sessions, calculated by dividing the total fuel cost by the total fuel used.

4. **Data validation and error handling**: The app validates navigation inputs, fueling data, and data retrieved from Google Sheets. It ensures correct data types, checks for missing or invalid entries, and provides clear error messages to guide users in correcting any issues.

## Data Model
The Car Fuel Metrics app uses a structured data model to track fueling and performance metrics. The primary data consists of three key elements: odometer readings, fuel quantity (litres), and fuel cost (EUR). These values are inputted by the user and stored in a Google Sheet, with each row representing a fueling event. The app validates this data, ensuring accurate entries by checking data types and consistency between odometer readings. Once validated, the app calculates key metrics, including trip distance, gas mileage, total fuel usage, total fuel cost, average gas mileage, and average fuel price. The data model allows for easy retrieval and aggregation of historical fueling data to generate both the latest refueling and total ownership metrics. This organized structure helps users track fuel efficiency and costs over time.

The app utilizes the gspread and google.oauth2.service_account libraries to facilitate API communication between the app and Google Drive/Sheets. It uses a ServiceAccount token, which is generated via Google Cloud, to authenticate the app. The client email has been shared with the Google Sheets worksheet as an editor, granting the app the necessary permissions to access and modify the data in the sheet. This setup enables seamless data retrieval and storage for tracking fueling metrics.

## Testing
- navigation functions have been tested
- calculate metrics functions have beent tested
- data input functions have been tested with incorrect data
- data validation functions on data retreival have been tested with incorrect data
### Solved Bugs
- "validate_odo_input" function did not handle happy path after it was refactored.
- No other bugs were identified after the first deployment.
### Remaining Bugs
- No known bugs related to app and its code.
### Validator Testing
- Tested on [PEP8 Validator](https://pep8ci.herokuapp.com/), no errors found.
## Deployment
- The repository is stored on my personal GitHub account as a public repository.
- The app was deployed to Heroku as per steps below:
    - Login to personal Heroku account.
    - Select New -> Create new app from top right segment of the screen.
    - Set unique name to the app and select location, then hit Create app.
    - After creating app, navigate to Settings from the top navigation.
    - Select Reveal Config Vars and add the following key-value combinations:
        - CRED - value of your service account details from the JSON file generated with Google Cloud.
        - PORT - 8000
    - Add Python and NodeJS buildpacks.
    - Navigate to the Deploy section from the top navigation.
    - Select GitHub as your Deployment Method.
    - Set the name of your repository and hit Search
    - Connect your repository to the Heroku app.
    - On the "Manual deploy" section of the screen, select the correct branch and hit "Deploy Branch"
## Resources:
- [Google Sheet](https://docs.google.com/spreadsheets/d/1v1qFVkJCMoAIYatECJoE_8HGtfYtN3YyKWrUvYZbNAs/edit?usp=sharing)
- A real-life dataset is used from my car's own metrics

## Credits:
 - Code Institute Love Sandwiches project for the Google Sheet API setup and use.
 - Code Institute lessons for the Heroku deployment process.
 - ChatGPT and Copilot for code optimization, debugging suggestions and grammar checking.
