import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def fit_sarima_model(series):
    model = SARIMAX(series, order=(1,1,1), seasonal_order=(1,1,1,7), enforce_stationarity=False, enforce_invertibility=False)
    model_fit = model.fit(disp=False)
    return model_fit

def forecast_traffic(series, steps=30):
    model_fit = fit_sarima_model(series)
    pred = model_fit.get_forecast(steps=steps)
    future_dates = pd.date_range(start=series.index[-1]+pd.Timedelta(days=1), periods=steps)
    forecast = pred.predicted_mean
    conf_int = pred.conf_int()
    return future_dates, forecast, conf_int

def calculate_metrics(actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    r2 = r2_score(actual, predicted)
    return dict(mae=mae, mse=mse, rmse=rmse, mape=mape, r2=r2)

def analyze_patterns(dates, traffic):
    df = pd.DataFrame({'date': dates, 'traffic': traffic})
    df['dow'] = df['date'].dt.dayofweek
    avg_last30 = df.tail(30)['traffic'].mean()
    growth = (avg_last30 - df.head(30)['traffic'].mean()) / df.head(30)['traffic'].mean() * 100
    peak_day = df.groupby('dow')['traffic'].mean().idxmax()

    return [
        {"title": "Average Last 30 Days", "value": f"{avg_last30:.2f}"},
        {"title": "Growth Over Period", "value": f"{growth:.2f}%"},
        {"title": "Peak Day of Week", "value": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][peak_day]},
    ]
