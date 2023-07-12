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
import random
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
    parser.add_argument('-ocsv', '--output_file_csv', type=str, required=True,
                        help='Please provide the output file name where you want to store the processed file')
    args = parser.parse_args()

    delivarable2(args.reporter, args.partner, args.trading_file, args.output_file_csv)
 
    


def delivarable2(re, pa, trading , oc):
    #Import Data
    data = pd.read_csv(trading)
    del data['Unnamed: 0']
    datareq1=data[data['DECLARANT']== re]
    datareq2=datareq1[datareq1['PARTNER']== pa]
    datareq3 = datareq2.sort_values(by = 'PERIOD', ascending=False)
    ind = np.shape(datareq3)[0]
    q=[0]*ind
    v=[0]*ind
    q=datareq3['QUANTITY_IN_KG']
    v=datareq3['VALUE_IN_EUROS']
    q=pd.array(q)
    v=pd.array(v)
    for i in range(ind):
      ro=random.randint(-7,7)
      q[i]=round((q[i])*0.01*(100+ro))
      v[i]=round((v[i])*0.01*(100+ro)) #randomly adding (-7, 7) % in Quantity and Value columns for data generation
    datareq3['QUANTITY_IN_KG']=q
    datareq3['VALUE_IN_EUROS']=v
    print(datareq3)
    datareq3=datareq3.to_csv(oc)

if __name__ == '__main__':
    main()