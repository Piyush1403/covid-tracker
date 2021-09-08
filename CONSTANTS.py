import os

state_wise_daily_csv_url = 'https://api.covid19india.org/csv/latest/state_wise_daily.csv'
base_path = os.path.abspath(os.getcwd())
unavailable_state_error = "No data available for this state"
unavailable_date_error = "No data available for this date"
