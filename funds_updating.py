#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 10:34:00 2019
Updated version of funds.py

@author: lzy
"""

import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime
import os, sys
from scipy import optimize

colName = ['code', 'name', 'sdate', 'edate', 'intervals', 'aim_%', 'invest_times',
           'redemption times', 'profit_then_%', 'profit_then_anual_%', 'profit_total_%', 
           'profit_total_annual_%', 'avdays_before_profit', 'maxdays_before_profit',
           'mindays_before_profit', 'max_withdraw']

_money = 100


class Investment(object):
    
    def __init__(self, code, name, data, ivtime, profit=0.12, intervals=31,
                 PRINTOUT=True, INFILE=sys.stdout):
        self.code = code
        self.name = name
        self.data = data
        self.ivtime = ivtime
        self.profit = profit
        self.intervals = intervals
        self.printout = PRINTOUT
        self.infile = INFILE
        
    def __initialize(self):
        date = [datetime.datetime.strptime(d[1], '%Y-%m-%d') for d in self.data]
        ivtime = processingPeriods(self.ivtime)
        datestr = [d[1] for d in self.data]
        values = [v[2] for v in self.data]
        dividend = [None if v[-1] == 'nan' else v[-1] for v in self.data]
        buystates = ['开放' if v[5]==None else v[5] for v in self.data]
        sellstates = ['开放' if v[6]==None else v[6] for v in self.data]
        buystates = [False if '暂停' in v else True for v in buystates]
        sellstates = [False if '暂停' in v else True for v in sellstates]
        print('Using scheduled plans with simple redemption with \n annual aimprofit at'
              '{:6.2f}% and intervals of roughly {:3d}'.format(profit*100, intervals), file=INFILE)
        sdate, edate =  self.ivtime[0], self.ivtime[1]    
        totalDuration = edate - sdate
        last_redp_date, latest_invest_date = sdate, sdate
        days_before_profit = []
        redp_times = 0
        times = {'_invest_curr':0, '_redp':0, '_invest_tot':0}
        money = {'_in_input':0, '_in_current':0, '_out_input':0, 
                 '_out_redp':0, '_out_divd':0}
        funds_hold = 0
        cash_flow = []
        max_range = 0
        
    
    
        
    
    
    __initialize()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
