#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 13:12:29 2019

@author: gladro
"""

import funds 
import time
import pandas as pd
import datetime
import numpy as np
#from pandas import DataFrame
import urllib, os, glob
#from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import argparse



parser = argparse.ArgumentParser(description='Keywords analysis')
parser.add_argument('--aim1', '-a1', help='keywords1', default='')
parser.add_argument('--aim2', '-a2', help='keywords2', default='指数')
parser.add_argument('--aim3', '-a3', help='keywords3', default='')
parser.add_argument('--aim4', '-a4', help='keywords4', default='')
parser.add_argument('--negativeaim1', '-na1', help='keywords1', default='货币')
parser.add_argument('--negativeaim2', '-na2', help='keywords2', default='债券')
parser.add_argument('--negativeaim3', '-na3', help='keywords3', default='理财')
parser.add_argument('--negativeaim4', '-na4', help='keywords4', default='现金')
parser.add_argument('--amount', '-tn', help='amount', default=None)

args = parser.parse_args()

sdate = datetime.date(2011, 1, 1)
edate = datetime.date(2015, 12, 31)
#
#def exist_or_not(a):
#    a = a if a is not '' else ''
#    return 


def combine_aims(a, pos):
    a_str = ''
    if a is not '' and pos < 4:
        a_str = '_' + a
    if a is not '' and pos >= 4:
        a_str = '_Without' + a
    return a_str

def analysis(data, item, database, databaseoutput=True):
#    Count+=1
    flag_postive = args.aim1 in item and args.aim2 in item \
                and args.aim3 in item and args.aim4 in item
    flag_negative = args.negativeaim1 not in item \
                and args.negativeaim2 not in item \
                and args.negativeaim3 not in item \
                and args.negativeaim4 not in item
    flag = flag_postive and flag_negative
    if flag:
        aimfund = data[data['Name'] == item]
#        print('No.{:3d}'.format(Count))
    #    Count += 1
        print('Name: {:s}  Code: {:s}'.format(item, aimfund['code'].values[0]))
        aimfunddb = funds.get_fund_data(aimfund['code'].values[0],
                                        sdate=sdate.strftime('%Y-%m-%d'), 
                                        edate=edate.strftime('%Y-%m-%d'))
        if aimfunddb.shape[0] == 0:
            print('The database is empty')
            return database
        db_edate = datetime.datetime.strptime(aimfunddb['Date'].values[0], '%Y-%m-%d')        
        if db_edate.date() <= sdate:
            print('The database does not have enough data')
            return database
        else:
            print('This fund runs from {:s} to {:s} [Aim: from {:s} to {:s}]'.format(
                  aimfunddb['Date'].values[-1], aimfunddb['Date'].values[0],
                  sdate.strftime('%Y-%m-%d'),edate.strftime('%Y-%m-%d')))       
            for interv in [7, 14, 31]:
                for aimProfit in np.arange(0.1, 0.21, 0.01):
                    print('Interval {:2d} days, Aimprofit {:.2f}'.format(interv, aimProfit))
                    outDb = funds.strategy_scheduled_simple_callback(aimfunddb, [aimfund['code'].values[0], item], 
                                                     profit=aimProfit, intervals=interv)
                    try:
                        database = database.append(outDb, ignore_index=True)
                    except:
                        print('Continue!')
            
#                if not os.path.exists(path):
#                    os.mkdir(path)
#                try:
#                    database.to_csv(path+item, aimfund['code']+'.csv', sep='\t')
#                except:
#                    print('No output')
    if databaseoutput:
        return database    

os.getcwd()

aimx = ''
aims = [args.aim1, args.aim2, args.aim3, args.aim4, \
        args.negativeaim1 + args.negativeaim2, args.negativeaim3, args.negativeaim4]
for loc, values in enumerate(aims):
    aimx += combine_aims(values, loc)
print(aimx)

dbname = 'funding_search.txt'
if not os.path.exists(dbname):
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    #contents = funds.get_url(url)
    #parser = 'html.parser'
    #soup = bs(contents, parser)    
    while True:
        try:
            r = urllib.request.urlopen(url, timeout=3)
        except Exception as exc:
            print ('error %s, wait 5 seconds...' % exc)
            time.sleep(5)
        else:
            break
    content = r.read()    
    content = content[11:]
    content = content[:-1]
    
    a = []
    a = eval(content)
    b = ['code', 'Short Name', 'Name', 'Type', 'Alix']
    df = pd.DataFrame(a, columns=b, dtype='str')
    df.set_index('code', inplace=True)
    df.to_csv(dbname)

data = pd.read_table(dbname,sep=",", dtype={'code':str})



#if __name__=="__main__":  


pool = Pool(50)
#    
#    for num in range(data.shape[0]): 
#        pool.apply_async(func=funds.get_fund_data, args=(data['code'].values[num],
#                                                         sdate.strftime('%Y-%m-%d'), 
#                                                         edate.strftime('%Y-%m-%d'),))
#    

global toAnalysis 
toAnalysis = pd.DataFrame(columns=funds.colName)

#txt = 


Count = int(args.amount) if args.amount is not None else None

for ids, item in enumerate(data['Name'].tolist()[:Count]):
    print('Processing {:s} '.format(item))
    toAnalysis_add = pool.apply_async(func=analysis, args=(data, item, toAnalysis, )).get()
    toAnalysis = toAnalysis.append(toAnalysis_add, ignore_index=True)
#    analysis(data, item, toAnalysis)
    
#    pool.apply_async(func=analysis, args=(data, item, toAnalysis, ))
               

#os.chdir('./Analysis')
#for analysis_result in sorted(glob.glob('*.csv')):
#    analysis_db = pd.read_csv(analysis_result, sep='\t')
#    try:
#        analysis_db.drop(columns=['Unnnamed: 0'], inplace=True)
#    finally:        
#        toAnalysis = toAnalysis.append(analysis_db, ignore_index=True)
#        print(analysis_result.split('.')[0])
#        os.remove(analysis_result)
#    

    
toAnalysis.to_csv('Result_Scheduled' + aimx + ' .txt', sep='\t')
#        
#
#
#print(1)

pool.close()  
pool.join()