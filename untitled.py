from flask import Flask, render_template, url_for
from flask import jsonify, send_from_directory
import pandas as pd
import os
import json
import numpy as np
app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict/', methods=['POST', 'GET'])
def predict():
    df = pd.read_csv(os.path.join(APP_STATIC, 'data.csv'), delimiter=",")
    df["Data"] = pd.to_datetime(pd.Series(df["Data"]), format = '%d/%m/%Y').apply(lambda x: x.strftime('%Y-%m-%d'))
    mask = (df['Data'] >= '2016-01-01') & (df['Data'] <= '2016-01-31')
    data = df[mask]
    dates_ = data["Data"].values.tolist()

    dates = []
    for i in dates_:
        dates.append(i)


    real_values = data["Reale"].values.tolist()
    predicted_values = data["Previsto"].values.tolist()

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
    app.run(host='0.0.0.0', port=port)
