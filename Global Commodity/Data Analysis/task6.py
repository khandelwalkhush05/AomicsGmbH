#!/usr/bin/env python
# coding: utf-8


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
    parser.add_argument('-ocsv', '--output_file_csv', type=str, required=True,
                        help='Please provide the output file name where you want to store the processed file')
    args = parser.parse_args()

    deliverable(args.reporter, args.partner, args.trading_file, args.output_file_csv)


    
def find_top_k(df, outfile, source = 'GERMANY', typ = 'import',  k = 5):
    filtered = df[df['DECLARANT'] == source]
    filtered = filtered[filtered['FLOW'] == typ]
    filtered = filtered[filtered['Year'] == '2019']
    filtered = filtered.sort_values('VALUE_IN_EUROS', ascending = False)
    filtered = filtered.groupby('PRODUCT_ID', as_index=False, sort=False).agg({'VALUE_IN_EUROS':'sum'})
    fig, ax =plt.subplots(figsize=(15,6))
    filtered = filtered.iloc[:k]
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=filtered.values,colLabels=filtered.columns,loc='center')
    pp = PdfPages(outfile)
    pp.savefig(fig, bbox_inches='tight')
    pp.close()
    return filtered
    
def return_quarter(mth_str):
    if mth_str in ['01','02', '03']:
        return 'Q1'
    elif mth_str in ['04', '05','06']:
        return 'Q2'
    elif mth_str in ['07','08','09']:
        return 'Q3'
    elif mth_str in ['10', '11','12']:
        return 'Q4'
        
    
def deliverable(source, partner, file, output):
    df = pd.read_csv(file)
    df = df.drop('Unnamed: 0', axis = 1)
    df['Period'] = df.apply(lambda x: str(x['PERIOD']), axis = 1)
    df['Year'] = df.apply(lambda x: x['Period'][:4], axis = 1)
    df['Month'] = df.apply(lambda x: x['Period'][4:6], axis = 1)
    df['Quarter'] = df.apply(lambda x: return_quarter(x['Month']), axis = 1)
    find_top_k(df, output)

    
if __name__ == '__main__':
    main()