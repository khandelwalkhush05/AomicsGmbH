import numpy as np
import pandas as pd
import argparse
from datetime import datetime
import matplotlib.pyplot as plt
from statistics import mean
from collections import defaultdict
from pprint import pprint
import warnings
import math
from matplotlib.backends.backend_pdf import PdfPages

def main():
    parser = argparse.ArgumentParser(description="A program for processing the trade raw files")
    parser.add_argument('-f', '--trading_file', type=str, required=True,
                        help='Please provide the input raw trading CSV file which is needed to be processed'
                             'Headers should be as first row of the file, and data should be in th')
    parser.add_argument('-re', '--reporter', type=str, required=True,
                        help='Please provide the reporter country name')
    parser.add_argument('-pa', '--partner', type=str, required=True,
                        help='Please provide the partner country name')
    parser.add_argument('-flow', '--flow', type=str, required=True,
                        help='Please provide the flow')
    #parser.add_argument('-y', '--year', type=int, nargs='?', default=2019,
                        #help='Please provide the year, default value is 2019')
    #parser.add_argument('-cat', '--category_id', type=int, required=True,
                        #help='Please provide the two-digit category id (for example 61)')
    parser.add_argument('-o', '--output_file', type=str, required=True,
                        help='Please provide the output file name where you want to store the processed file')

    args = parser.parse_args()

    delivarable2(args.reporter, args.partner, args.flow, args.trading_file, args.output_file)
 
    


def delivarable2(re, pa, flow, trading, out, k=20):
    #Import Data
    data = pd.read_csv(trading)
    del data['Unnamed: 0']
    
    
    #dataimport = data[data['FLOW']=="export"]
   
 
    datareq1=data[data['DECLARANT']== re]
    datareq2=datareq1[datareq1['PARTNER']== pa]
    #datareq3=datareq2[datareq2['check']== cat]
    datareq3 = datareq2[datareq2['FLOW']==flow]
    #datareq4=datareq3[(datareq3['PERIOD']/100).astype(int)== 2015]
    #datareq5 = datareq4.sort_values(by = 'VALUE_IN_EUROS', ascending=False)
    datareq6=datareq3.groupby('PRODUCT_ID', as_index=False, sort=False).agg({'VALUE_IN_EUROS':'sum', 'PERIOD':'first'})
    
    df = pd.DataFrame(datareq6['PRODUCT_ID'], columns=['PRODUCT_ID','Year 2015','Year 2016','Year 2017','Year 2018', 'Year 2019'])
    for ind in range(20):
        if(int(datareq6['PERIOD'][ind]/100)==2015):
            df['Year 2015'][ind]=datareq6['VALUE_IN_EUROS'][ind]
        else:
            if(int(datareq6['PERIOD'][ind]/100)==2016):
                df['Year 2016'][ind]=datareq6['VALUE_IN_EUROS'][ind]
            if(int(datareq6['PERIOD'][ind]/100)==2017):
                df['Year 2017'][ind]=datareq6['VALUE_IN_EUROS'][ind]
            if(int(datareq6['PERIOD'][ind]/100)==2018):
                df['Year 2018'][ind]=datareq6['VALUE_IN_EUROS'][ind]
            if(int(datareq6['PERIOD'][ind]/100)==2019):
                df['Year 2019'][ind]=datareq6['VALUE_IN_EUROS'][ind]
            
    df['Year 2015']=df['Year 2015'].fillna(0)
    df['Year 2016']=df['Year 2016'].fillna(0)
    df['Year 2017']=df['Year 2017'].fillna(0)
    df['Year 2018']=df['Year 2018'].fillna(0)
    df['Year 2019']=df['Year 2019'].fillna(0)
    df_final=df.head(20)
    print(df_final)
    fig, ax =plt.subplots(figsize=(21,6))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df_final.values,colLabels=df_final.columns,loc='center')
    pp = PdfPages(out)
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

if __name__ == '__main__':
    main()
