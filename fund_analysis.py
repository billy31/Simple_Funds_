#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 22:43:53 2019

@author: gladro
"""

import funds 
import pandas as pd
import datetime
import numpy as np
#from pandas import DataFrame
import urllib, os, glob
#from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
import argparse

predefined_period1_concuup = [datetime.datetime(2012, 1, 1), datetime.datetime(2013, 7, 1)]
predefined_period1_quickrise = [datetime.datetime(2013, 12, 1), datetime.datetime(2015, 6, 1)]
predefined_period1_deepdrop = [datetime.datetime(2015, 8, 1), datetime.datetime(2017, 2, 1)]
predefined_period_concudown = [datetime.datetime(2017, 1, 1), datetime.datetime(2018, 7, 1)]










parser = argparse.ArgumentParser(description='Keywords analysis')
parser.add_argument('--aim1', '-a1', help='keywords1', default='')
parser.add_argument('--aim2', '-a2', help='keywords2', default='')
parser.add_argument('--aim3', '-a3', help='keywords3', default='')
parser.add_argument('--aim4', '-a4', help='keywords4', default='')
parser.add_argument('--amount', '-tn', help='amount', default=None)

args = parser.parse_args()

#aim = args.aim1 + '*' + args.aim2 + '*' + args.aim3 + '*' + args.aim4 + \
#'*' + args.amount.__str__()
aim = '指数'
os.getcwd()
file = sorted(glob.glob('Result_Scheduled.txt'))[0]
#for file in filelist:
db = pd.read_csv(file, sep='\t', dtype={'code':str})
db.drop(columns=['Unnamed: 0'], inplace=True)
locs = [aim in item for item in db.name.values.tolist()]
data_aim = db[locs]
data_aimna = data_aim.dropna(axis=0,how='any')
#data_aim = 
data_aimna.sort_values('profit_then_%', ascending = False, inplace=True)
print(db)


#if not os.path.exists(dbname):
