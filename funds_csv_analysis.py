#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 11:05:02 2019

@author: lzy
"""

#import funds_analysis as analysisF
import pandas as pd
import numpy as np
from funds_extrance import args
import os, glob
#import time
#from threading import Thread
args.usingOutput = False
args.runWithin = False
args.single = False
args.code = None
from funds_search import processFeatures
from funds import colName


def foo(helptext):
    helptext += ':\n'
    wait_input_str = input(helptext)
    return wait_input_str


def getIDValues(helptext='Choose the id of the file'):
    s_files_str = processFeatures(foo(helptext))
    try:
        return [int(s) for s in s_files_str]
    except:
        return s_files_str

def bestStragety(data, selectedFeature=None):
    pd.set_option('display.max_columns',None)    
    if selectedFeature == None:
        selectedFeature = ['profit_then_%', 'avdays_before_profit', 'max_withdraw']
        data.sort_values(selectedFeature,ascending=[0, 0, 0],inplace=True)        
    else:
        selectedFeature = (colName[s] for s in selectedFeature)
        ascendingx = [np.zeros(len(selectedFeature), dtype=np.byte)]
        data.sort_values(selectedFeature,ascending=ascendingx,inplace=True)        
    print(data.iloc[:20])


try:
    os.mkdir(args.csvfiledir)
except:
    print('File exists')
finally:
    os.chdir(args.csvfiledir)

    
files = sorted(glob.glob('*.txt'))
print('[--ID--] File name')
for fileid, file in enumerate(files):
    print('[{:^6d}] {:s}'.format(fileid, file))

print('Possible sorting features:')
for colID, col in enumerate(colName):    
    print('[{:^6d}] {:s}'.format(colID, col))

selected_files = getIDValues()
for fileid in selected_files:
    try:
        file = files[fileid]
        try:
            defaultMode = getIDValues('Default analysis?[y/n]')[0]
            defaultMode = True if defaultMode is 'y' or defaultMode is 'Y' else False
            data = pd.read_csv(file, sep='\t', dtype={'code':np.str})        
            print('Reading txt: {:s}'.format(file))
            data.drop(columns=['Unnamed: 0'], inplace=True)
            if defaultMode:
                bestStragety(data)
            else:
                selected_features = getIDValues('Choosing Features(In importance order)')
                bestStragety(data, selected_features)            
        finally:
            print('\n\nFinshed\n\n' + '=='*5)
    except Exception as e:
        print(e)
        continue


