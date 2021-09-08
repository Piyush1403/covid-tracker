from app import app
from flask import request, render_template
import CONSTANTS
import pandas as pd
import requests
import datetime


@app.route("/covid-tracker", methods=['GET', 'POST'])
def get_covid_data():
    try:
        if request.method == "POST":
            response = requests.request(method='GET', url=CONSTANTS.state_wise_daily_csv_url)
            data = response.content
            date = request.form['date']
            state_abbr = (request.form['state']).upper()
            csv_path = CONSTANTS.base_path + "/state_wise_covid_data.csv"
            csv_file = open(csv_path, 'wb')
            csv_file.write(data)
            csv_file.close()
            data = pd.read_csv(csv_path)
            if state_abbr not in data.columns:
                final_data = CONSTANTS.unavailable_date_error
                return render_template("index.html", output=final_data)
            date_rows = data.loc[data['Date_YMD'] == date]
            if date_rows.empty:
                final_data = CONSTANTS.unavailable_date_error
                return render_template("index.html", output=final_data)
            state_date_data = date_rows[['Status', state_abbr]]
            final_data = dict(state_date_data.values)
            formatted_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")
            final_data['date'], final_data['state_abbr'] = formatted_date, state_abbr
            return render_template("index.html", output=final_data)
        return render_template("index.html", output='')
    except Exception as e:
        print(e)
