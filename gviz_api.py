from flask import Flask, render_template, url_for
from flask import jsonify, send_from_directory
import pandas as pd
import os
import json
import numpy as np
APP_STATIC = os.path.join(APP_ROOT, 'static')

df = pd.read_csv(os.path.join(APP_STATIC, 'previsioni.csv'), delimiter=";")
df["Data"] = pd.to_datetime(pd.Series(df["Data"]), format = '%d/%m/%Y').apply(lambda x: x.strftime('%Y-%m-%d'))
mask = (df['Data'] >= '2016-02-01') & (df['Data'] <= '2016-02-28')
data = df[mask]
dates_ = data["Data"].values.tolist()
dates = []
for i in dates_:
    dates.append(i)