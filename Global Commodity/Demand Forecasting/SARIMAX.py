import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse
import argparse
import sys
import time
import warnings
warnings.filterwarnings("ignore")
import logging
logging.disable(logging.CRITICAL)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f', '--trading_file', type=str, required=True, help='Please provide the input raw trading CSV file which is needed to be processed Headers should be as first row of the file, and data should be in th')
  args = parser.parse_args()
  sarimamodel(args.trading_file)

def sarimamodel(f):


  def dataset(f):
    df = pd.read_csv(f)
    del df['Unnamed: 0']
    return df

  # helper function: fit the sarimax model
  def fit_it(model):
    res=model.fit()
    return res
  
  # helper function: plot the predictions
  def plot_fitted(pred, act, flavor):
    plt.figure(figsize=(8,5))
    act.plot(label='actual')
    pred.plot(label='prediction')
    plt.legend()
    plt.show()


  # set up, fit, run, plot, and evaluate the Sarima model

  def run_Sarima(df,start,end):

    
    #setting up the model 
    model=SARIMAX(train['y'],order=(1,1,1),seasonal_order=(1,0,0,12))
    res=fit_it(model)
    predictions1=res.predict(start,end,typ='levels').rename('SARIMA Predictions')


    plot_fitted(predictions1, test['y'], "Sarima")

    return [predictions1]

  def metrics(predictions1, df):
    
    pred_df = pd.DataFrame(predictions1)
    pred_df.to_csv('Cat62data_pred_sarima.csv')
    sum = 0
    for i in range(len(pred_df)):
      sum += ((df['y'].iloc[i] - pred_df.iloc[i])/test['y'].iloc[i])**2
    sum /= len(pred_df)
    mspe = sum*100
    print("MSPE =", mspe, "%")

    

  df= dataset(f)
  # split training vs test dataset
  train = df.iloc[:97]
  test = df.iloc[96:]

  start=len(train)-1
  end=len(train)+len(test)-2
  
  predictions1= run_Sarima(df, start, end)
  metrics(predictions1, test)

if __name__ == "__main__":
    main()
