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
        p = 8
        k = 6
    if month == "Febbraio":
        start_date = "2016-02-01"
        end_date = "2016-02-28"
        p = 7
        k = 8
    if month == "Marzo":
        start_date = "2016-03-01"
        end_date = "2016-03-31"
        p = 7
        k = 8
    if month == "Aprile":
        start_date = "2016-04-01"
        end_date = "2016-04-30"
        p = 7
        k = 8
    if month == "Maggio":
        start_date = "2016-05-01"
        end_date = "2016-05-31"
        p = 12
        k = 8
    if month == "Giugno":
        start_date = "2016-06-01"
        end_date = "2016-06-30"
        p = 4
        k = 4
    if month == "Luglio":
        start_date = "2016-07-01"
        end_date = "2016-07-31"
        p = 13
        k = 10
    if month == "Agosto":
        start_date = "2016-08-01"
        end_date = "2016-08-31"
        p = 16
        k = 12
    if month == "Settembre":
        start_date = "2016-09-01"
        end_date = "2016-09-30"
        p = 16
        k = 12
    if month == "Ottobre":
        start_date = "2016-10-01"
        end_date = "2016-10-31"
        p = 20
        k = 14
    if month == "Novembre":
        start_date = "2016-11-01"
        end_date = "2016-11-31"
        p = 15
        k = 10
    if month == "Dicembre":
        start_date = "2016-12-01"
        end_date = "2016-12-31"
        p = 13
        k = 10
    if month == "Gennaio17":
        start_date = "2017-01-01"
        end_date = "2017-01-31"
        p = 13
        k = 9
    if month == "Febbraio17":
        start_date = "2017-02-01"
        end_date = "2017-02-28"
        p = 8
        k = 7
    if month == "Marzo17":
        start_date = "2017-03-01"
        end_date = "2017-03-31"
        p = 8
        k = 7
    if month == "Aprile17":
        start_date = "2017-04-01"
        end_date = "2017-04-30"
        p = 8
        k = 8
    return start_date, end_date, p, k


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    start_date, end_date, p, k = dispatch_date(request.args.get("month"))

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

    real_values = [round(elem, 3) for elem in real_values]
    predicted_values = [round(elem, 3) for elem in predicted_values]

    mean_real = np.mean(real_values)
    predicted_mean = np.mean(predicted_values)

    zipped = zip(dates, real_values, predicted_values)
    column_names = ['date', 'real', 'predicted']
    return_value = dict()
    return_value["data"] = [dict(zip(column_names, row)) for row in zipped]
    return_value["mean_real"] = round(mean_real, 3)
    return_value["p_value"] = p
    return_value["k_value"] = k
    return_value["predicted_mean"] = round(predicted_mean,3)
    return json.dumps(return_value, indent=1)

@app.route('/delta', methods=['POST', 'GET'])
def delta():

    df = pd.read_csv(os.path.join(APP_STATIC, 'deltas.csv'), delimiter=",")

    dates = df["Date"].values.tolist()
    deltas = df["Scarto"].values.tolist()

    deltas = [round(elem, 3) for elem in deltas]

    zipped = zip(dates, deltas)
    column_names = ['date', 'deltas']
    return_value = dict()
    return_value["data"] = [dict(zip(column_names, row)) for row in zipped]
    return json.dumps(return_value, indent=1)

@app.route('/barchart', methods=['POST', 'GET'])
def barchart():

    df = pd.read_csv(os.path.join(APP_STATIC, 'deltas.csv'), delimiter=",")

    dates = df["Date"].values.tolist()
    observed = df["Observed"].values.tolist()
    predicted = df["Predicted"].values.tolist()

    observed = [round(elem, 3) for elem in observed]
    predicted = [round(elem, 3) for elem in predicted]

    zipped = zip(dates, observed, predicted)
    column_names = ['date', 'observed', 'predicted']
    return_value = dict()
    return_value["data"] = [dict(zip(column_names, row)) for row in zipped]
    return json.dumps(return_value, indent=1)

@app.route('/select-month/')
def show_post():
    return render_template('run_predict.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
