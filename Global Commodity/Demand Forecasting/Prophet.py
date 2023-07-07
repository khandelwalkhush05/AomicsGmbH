# mkdir timeseries
# pip install pandas matplotlib numpy cython
# pip install pystan
# pip install prophet

# %matplotlib inline
import pandas as pd
from prophet import Prophet

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--trading_file', type=str, required=True,
                        help='Please provide the input raw trading CSV file which is needed to be processed'
                             'Headers should be as first row of the file, and data should be in th')
  parser.add_argument("--traintl", "-ttl", type=str, default="2018-12-01")
  parser.add_argument("--testst", "-tst", type=str, default="2019-01-01")
  args = parser.parse_args()
  prophet(args.trading_file, args.traintl, args.testst)

def prophet(trading, ttl,tst):
    #Import Data
    target_df = pd.read_csv(trading)
    del target_df['Unnamed: 0']

    target_df['Month'] = pd.DatetimeIndex(target_df['Month'])

    target_df['ds']=target_df["Month"]

    target_df = target_df.set_index('Month')

    train_data = target_df[:ttl]

    test_data = target_df[tst:]

    # ax = target_df['y'].plot(figsize=(12, 8))
    # ax.set_ylabel('Monthly Quantity in kg for PID')
    # ax.set_xlabel('Date')
    # plt.show()

    my_model = Prophet(interval_width=0.98, daily_seasonality=False, weekly_seasonality=False, yearly_seasonality=True,)
    my_model.fit(train_data)

    future_dates = my_model.make_future_dataframe(periods=12, freq='MS')

    forecast = my_model.predict(future_dates)

    # my_model.plot(forecast, uncertainty=True)

    pd.options.mode.chained_assignment = None  # default='warn' supress warning
    yhat = forecast[-24:]["yhat"]
    test_data["yhat"] = yhat[0:12].to_numpy()
    test_data['yhat_lower'] = forecast[-12:][['yhat_lower']].to_numpy()
    test_data['yhat_upper'] = forecast[-12:][['yhat_upper']].to_numpy()
    test_data["yhat"].to_csv('Cat62_pred.csv')
    import numpy as np
    sum = 0
    for i in range(len(test_data)):
      sum += (1-test_data["yhat"].iloc[i]/test_data["y"].iloc[i])**2
    sum

    sum /= len(test_data)
    sum*100
    
    ax = test_data['y'].plot(label='observed', color='green')
    ax = test_data['yhat'].plot(label='predicted', color='orange')
    ax.fill_between(test_data.index,
                    test_data['yhat_lower'],
                    test_data['yhat_upper'], color='k', alpha=.2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Quantity in kg')
    plt.legend()

    plt.show()
    

if __name__ == "__main__":
    main()