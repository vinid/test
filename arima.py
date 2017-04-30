import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
from pandas import datetime
import datetime as dt

df = pd.read_csv("data.csv", delimiter=",")
df["Data"] = pd.to_datetime(pd.Series(df["Data"]), format = '%d/%m/%Y').apply(lambda x: x.strftime('%Y-%m-%d'))
mask = (df['Data'] >= '01-01-2016') & (df['Data'] <= '31-01-2016')
data = df[mask]
real_values = data["Reale"].values
predicted_values = data["Previsto"].values

return jsonify(real=real_values, predicted = predicted_values)


# import pandas as pd
# from statsmodels.tsa.arima_model import ARIMA
# from pandas import datetime
# import datetime as dt
#
# df = pd.read_csv("final_day.csv", delimiter=";")
#
# df["Data"] = pd.to_datetime(pd.Series(df["Data"]), format = '%Y%m%d').apply(lambda x: x.strftime('%Y-%m-%d'))
#
#
# #
# # train = df.iloc[183+363:366+365,]
# #
# # test =  df.iloc[368+363:397+365,]
# mask = (df['Data'] >= '2015-07-01') & (df['Data'] <= '2015-12-31')
#
# df_train = df[mask]
# train = df_train.set_index("Data")
# train.index = pd.to_datetime(train.index)
#
# mask_test = (df['Data'] >= '2016-01-01') & (df['Data'] <= '2016-01-31')
#
# df_test = df[mask_test]
# test = df_test.set_index("Data")
# test.index = pd.to_datetime(test.index)
#
#
# #print df.loc['2015-07-01':'2015-12-31']
#
# train = df.set_index("Data")
# train.index = pd.to_datetime(train.index)
#
#
#
# train["LAVORATIVO"] = pd.get_dummies(train["LAVORATIVO"])["NO"]
# train["AUTUNNO"] = pd.get_dummies(train["Stagione"])["AUTUNNO"]
# train["ESTATE"] = pd.get_dummies(train["Stagione"])["ESTATE"]
# train["INVERNO"] = pd.get_dummies(train["Stagione"])["INVERNO"]
#
# #
# #
# #
# # test["LAVORATIVO"] = pd.get_dummies(test["LAVORATIVO"])["NO"]
# # # test["AUTUNNO"] = pd.get_dummies(test["Stagione"])["AUTUNNO"]
# # # test["ESTATE"] = pd.get_dummies(test["Stagione"])["ESTATE"]
# # test["INVERNO"] = pd.get_dummies(test["Stagione"])["INVERNO"]
#
# train = train.drop('Stagione', 1)
# test = test.drop('Stagione', 1)
#
# print train.head()
#
# model = ARIMA(train["CCT NORD"], order=(1,0,2), exog=train[["LAVORATIVO", "AUTUNNO", "ESTATE", "INVERNO"]])
# #model = ARIMA(train, order=(1,0,2), exog=train[["LAVORATIVO", "AUTUNNO", "ESTATE", "INVERNO"]])
# model_fit = model.fit(disp=0)
# print model_fit.predict(start="2016-01-01",exog= train[["LAVORATIVO", "INVERNO"]])
#
#
# from statsmodels.tsa.arima_model import _arima_results_predict
# res = sm.tsa.ARMA(y, (3, 2)).fit(trend="nc")
#
# # get what you need for predicting one-step ahead
# params = res.params
# residuals = res.resid
# p = res.k_ar
# q = res.k_ma
# k_exog = res.k_exog
# k_trend = res.k_trend
# steps = 1
#
# _arma_predict_out_of_sample(params, steps, residuals, p, q, k_trend, k_exog, endog=y, exog=None, start=len(y))