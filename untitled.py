from __future__ import print_function # In python 2.7
import sys
from flask import Flask, render_template, url_for, request
from flask import jsonify, send_from_directory
import sys
import pandas as pd
import os
import json
import numpy as np
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

def dispatch_date(month):
    if month == "Gennaio":
        start_date = "2016-01-01"
        end_date = "2016-01-31"
    if month == "Febbraio":
        start_date = "2016-02-01"
        end_date = "2016-02-28"
    if month == "Marzo":
        start_date = "2016-03-01"
        end_date = "2016-03-31"
    if month == "Aprile":
        start_date = "2016-04-01"
        end_date = "2016-04-30"
    if month == "Maggio":
        start_date = "2016-05-01"
        end_date = "2016-05-31"
    if month == "Giugno":
        start_date = "2016-06-01"
        end_date = "2016-06-30"
    if month == "Luglio":
        start_date = "2016-07-01"
        end_date = "2016-07-31"
    if month == "Agosto":
        start_date = "2016-08-01"
        end_date = "2016-08-31"
    if month == "Settembre":
        start_date = "2016-09-01"
        end_date = "2016-09-30"
    if month == "Ottobre":
        start_date = "2016-10-1"
        end_date = "2016-10-31"
    if month == "Novembre":
        start_date = "2016-11-1"
        end_date = "2016-11-31"
    if month == "Dicembre":
        start_date = "2016-12-1"
        end_date = "2016-12-31"
    return start_date, end_date


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    start_date, end_date = dispatch_date(request.args.get("month"))

    df = pd.read_csv(os.path.join(APP_STATIC, 'previsioni.csv'), delimiter=";")
    df["Data"] = pd.to_datetime(pd.Series(df["Data"]), format = '%d/%m/%Y').apply(lambda x: x.strftime('%Y-%m-%d'))
    mask = (df['Data'] >= start_date) & (df['Data'] <= end_date)
    data = df[mask]
    dates_ = data["Data"].values.tolist()
    dates = []
    for i in dates_:
        dates.append(i)


    real_values = data["Osservati"].values.tolist()
    predicted_values = data["Previsti"].values.tolist()

    mean_real = np.mean(real_values)
    predicted_mean = np.mean(predicted_values)

    zipped = zip(dates, real_values, predicted_values)
    column_names = ['date', 'real', 'predicted']
    return_value = dict()
    return_value["data"] = [dict(zip(column_names, row)) for row in zipped]
    return_value["mean_real"] = mean_real
    return_value["predicted_mean"] = predicted_mean
    return json.dumps(return_value, indent=1)

@app.route('/select-month/')
def show_post():
    return render_template('run_predict.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=1)
