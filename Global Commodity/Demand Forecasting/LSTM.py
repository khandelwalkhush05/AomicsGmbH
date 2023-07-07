#import all the necessary modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.models import RNNModel
from darts.utils.statistics import check_seasonality, plot_acf
from darts.utils.timeseries_generation import datetime_attribute_timeseries

import argparse
import sys
import time
import warnings
warnings.filterwarnings("ignore")
import logging
logging.disable(logging.CRITICAL)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--num_epoches", "-e", type=int, default=300)
  parser.add_argument("-lr", type=float, default=1e-3)
  parser.add_argument("--fc_n", "-fcn", type=int, default=24)
  parser.add_argument("--fc_stride", "-fcsrd", type=int, default=10)
  parser.add_argument("--fc_start", "-fcsrt", type=str, default="20181201")
  parser.add_argument("--train_len", "-tl", type=int, default=10)
  parser.add_argument("--hidden_dim", "-hdd", type=int, default=20)
  parser.add_argument("--dropout", "-d", type=int, default=0)
  parser.add_argument("--batch_size", "-b", type=int, default=16)
  parser.add_argument("--max_lag", "-ml", type=int, default=240)
  parser.add_argument('-f', '--trading_file', type=str, required=True,
                      help='Please provide the input raw trading CSV file which is needed to be processed'
                             'Headers should be as first row of the file, and data should be in th')
  args = parser.parse_args()
  lstmmodel(args.num_epoches, args.lr, args.fc_n, args.fc_stride, args.fc_start, args.train_len, args.hidden_dim, args.dropout, args.batch_size, args.max_lag, args.trading_file)


def lstmmodel(e, lr, fcn, fcsrd, fcsrt, tl, hdd, d, b, ml, f):

  def dataset(f):
    df = pd.read_csv(f)
    del df['Unnamed: 0']
    series = TimeSeries.from_dataframe(df, "Month", "y")
    return df, series

  #check the seasonality and periodicity of our dataset and change the arguments accordingly
  def check_seasonal(series, ml):
    is_seasonal, periodicity = check_seasonality(series, max_lag=ml)
    dict_seas ={
        "is seasonal?":is_seasonal, 
        "periodicity (months)":f'{periodicity:.1f}', 
        "periodicity (~years)": f'{periodicity/12:.1f}'}
    _ = [print(k,":",v) for k,v in dict_seas.items()]
    return periodicity

  # normalize the time series
  def normlise(train, val, series):
    trf = Scaler()
    # fit the transformer to the training dataset
    train_trf = trf.fit_transform(train)
    # apply the transformer to the validation set and the complete series 
    val_trf = trf.transform(val)
    series_trf = trf.transform(series)
    return train_trf, val_trf, series_trf, trf

  # create month and year covariate series
  def cov_series(series, fcsrt):
    year_series = datetime_attribute_timeseries(
        pd.date_range(start=series.start_time(), 
            freq=series.freq_str, 
            periods=1000),
        attribute='year', 
        one_hot=False)
    year_series = Scaler().fit_transform(year_series)

    month_series = datetime_attribute_timeseries(
        year_series, 
        attribute='month', 
        one_hot=True)

    covariates = year_series.stack(month_series)
    cov_train, cov_val = covariates.split_after(pd.Timestamp("20181201"))
    return cov_train, cov_val, covariates

  # helper function: fit the LSTM model

  def fit_it(model, train, val, fcsrt):
      t_start =  time.perf_counter()
      print("\nbeginning the training of the {0} :".format("LSTM"))
      cov_train, cov_val, covariates = cov_series(series, fcsrt)
      res = model.fit(train,
              future_covariates=covariates,
              val_series=val,
              val_future_covariates=covariates,
              verbose=True)

      res_time = time.perf_counter() - t_start
      print("training of the {0} LSTM has completed:".format("LSTM"), f'{res_time:.2f} sec')

      return res

  # helper function: plot the predictions

  def plot_fitted(pred, act, flavor):
      plt.figure(figsize=(12,5))
      act.plot(label='actual')
      pred.plot(label='prediction')
      plt.legend();
      plt.show()

  # set up, fit, run, plot, and evaluate the LSTM model

  def run_LSTM(series, train, val, ml, tl, hdd, b, e, d, lr,fcsrt):
      periodicity = check_seasonal(series, ml)
      cov_train, cov_val, covariates=cov_series(series, fcsrt)
      # set the model up
      model_LSTM = RNNModel(
          model="LSTM",
          model_name="LSTM" + str(" LSTM"),
          input_chunk_length=periodicity,
          training_length=tl,
          hidden_dim=hdd,
          batch_size=b,
          n_epochs=e,
          dropout=d,
          optimizer_kwargs={'lr': lr},
          log_tensorboard=True,
          random_state=42,
          force_reset=True)

      # fit the model
      fit_it(model_LSTM, train, val, fcn)

      # compute N predictions
      pred = model_LSTM.predict(n=fcn, future_covariates=covariates) 

      # plot predictions vs actual
      plot_fitted(pred, series, "LSTM")

      return [pred]

  def metrics(pred_trf, df):
    prediction = trf.inverse_transform(pred_trf[0][0])
    pred_df = prediction.pd_dataframe()
    pred_df.to_csv('Cat62data_pred.csv', encoding='utf-8')
    sum = 0
    for i in range(12):
      sum += ((df['y'].iloc[i+96] - pred_df['y'].iloc[i])/df['y'].iloc[i+96])**2
    sum /= 12
    mspe = sum*100
    print("MSPE =", mspe, "%")
  
  df, series = dataset(f)
  # split training vs test dataset
  train, val = series.split_after(pd.Timestamp("20181201"))
  train_trf, val_trf, series_trf, trf = normlise(train, val, series)
  pred_trf = [run_LSTM(series_trf, train_trf, val_trf, ml, tl, hdd, b, e, d, lr, fcsrt)]
  metrics(pred_trf, df)

if __name__ == "__main__":
    main()
