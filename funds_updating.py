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
        
    def _initialize():
        return 0
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
