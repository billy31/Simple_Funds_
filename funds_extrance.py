#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 07:47:13 2019

@author: lzy
"""

#import pandas as pd
import datetime
#import numpy as np
#from pandas import DataFrame
#import os, sys
#from bs4 import BeautifulSoup as bs
#from multiprocessing import Pool
import argparse

parser = argparse.ArgumentParser(description='Introduction:\t'
                                 'Use this file to generate analysis files.\n'
                                 'Default values:\n'
                                 '-a,  default=\"指数\"\n'
                                 '-na, default=\"货币, 债券, 理财, 现金, 分级\"\n'
                                 '-sd/ed, default=[Years-1, Today]\n'
                                 '-tP, Testing periods modes, default=customed\n'
                                 '-s, stregaties to take\n'
                                 '-f, frequency, usually try 14,31\n'
                                 '-g, goal profit, usually try 0.05-0.2\n')

parser.add_argument('--aim', '-a', help='keywords', default='指数')
parser.add_argument('--negativeaim', '-na', help='keywords to filter out', \
                    default='货币, 债券, 理财, 现金, 分级')
parser.add_argument('--sdate', '-sd', help='begin date', \
                    default='2009-01-01')
#                    default=datetime.datetime.today() - datetime.timedelta(days=365*10))
parser.add_argument('--edate', '-ed', help='end date', default=datetime.datetime.today())
parser.add_argument('--testingPeriod', '-tP', help='predefined periods', default=None)
parser.add_argument('--stragety', '-s', help='different ways to invest, see '
                    'details in ...', default=1)
parser.add_argument('--frequency', '-f', help='how often do', default='14,31')
parser.add_argument('--goalProfit', '-g', help='what is the goal profit', default='0.05,0.07,0.1,0.12,0.15,0.17,0.2')
parser.add_argument('--output', '-ot', help='need the output in report? True as'
                    'report, False as databasefile, None as database', default=False)

parser.add_argument('--single', '-sg', help='single fund', default=False)
parser.add_argument('--code', '-fc', help='fund code', default=None)
parser.add_argument('--runWithin', '-rw', help='run within this file', default=True)
parser.add_argument('--usingOutput', '-u', default=False)
parser.add_argument('--csvfiledir', '-cdir', default='./Analysis/')

parser.add_argument('--database', '-db', default='funding_search.txt')
parser.add_argument('--website', '-wb', default='http://fund.eastmoney.com/js/fundcode_search.js')

args = parser.parse_args()
#database = pd.DataFrame(columns=funds.colName)

#Possible values
#'中证500'
#'沪深300'
#龙头
#军工
#医药
#白酒
#消费
#
#纳斯达克
#
#创业板
#中小板


#pool = Pool(3)
#
#for f in analysisF.FREQUENCY:
#    for aimP in np.arange(0.05, 0.25, 0.01):
#        dbanalysis = pool.apply_async(func=analysisF.analysisdata, 
#                                      args=(fre=f, gProft=aimP, )).getValues()
#        database = database.append(dbanalysis)
#        
#pool.close()
#pool.join()        
#
#print(1)
        