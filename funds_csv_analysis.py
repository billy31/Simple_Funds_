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
from funds_extrance import dirs
import os, glob
#import time
#from threading import Thread
args.usingOutput = False
args.runWithin = False
args.single = False
args.code = None
from funds_search import processFeatures
from funds import colName
from collections import Iterable

initalPath = os.getcwd()    

#-------------------------------- Draw In Shell -----------------------------

def __drawFigInShell(data, wid=61, height=32):
    in_invest = data._in_invest.values.tolist()
    in_total = data._in_total.values.tolist()
    out_invest = data._out_invest.values.tolist()
    out_total = data._out_total.values.tolist()    
    length = len(in_invest)
    currentProfit = in_total / in_invest
    maxProfit, minProfit = max(currentProfit), min(currentProfit)
    # y-axis
#    for h in range(height):
#        if h==0:
#            
    
    
    




#-------------------------------- Utilities -----------------------------------

def standardOutput(aim):
    for fileid, file in enumerate(aim): print('[{:^6d}] {:s}'.format(fileid, file))

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

#---------------------------- CSV Analysis --------------------------------

def bestStragety(data, selectedFeature=None):
    pd.set_option('display.max_columns',None)    
    if selectedFeature == None:
        selectedFeature = ['profit_then_%', 'avdays_before_profit', 'max_withdraw']
        data.sort_values(selectedFeature,ascending=[0, 0, 0],inplace=True)        
    else:
        selectedFeature = [colName[s] for s in selectedFeature]
        ascendingx = [np.zeros(len(selectedFeature), dtype=np.byte)]
        try:
            data.sort_values(selectedFeature,ascending=ascendingx,inplace=True)
        except:
            data.sort_values(selectedFeature[0],ascending=[0],inplace=True)
    print('Single combination choice:')
    print(data.iloc[:20])
    print('==='*10)
    
    print('By fund choice:')
    byFundChoice = data[selectedFeature[0]].groupby(data['name']).mean()   
    print(byFundChoice.nlargest(20))
    print('==='*10)
    
    
    
def relationshipAnalysis(datas, mods=True, selectedFeature=None):
    if mods:
        df = datas[['intervals','aim_%','profit_then_%']]
        print(df.corr())
    else:
        selectedFeature = [colName[s] for s in selectedFeature]
        df = datas[selectedFeature]
        print(df.corr())
    
    
    
def _defaultModeAnalysis(file):
    '''
    Default mode analysis
    '''    
    defaultMode = getIDValues('Default analysis?[y/n]')[0]
    defaultMode = True if defaultMode is 'y' or defaultMode is 'Y' else False
    data = pd.read_csv(file, sep='\t', dtype={'code':np.str})        
    print('Reading txt: {:s}'.format(file))
    data.drop(columns=['Unnamed: 0'], inplace=True)
    data.dropna(axis=0, how='any', inplace=True)
    if defaultMode: 
        bestStragety(data)
        relationshipAnalysis(data)
    else:
        selected_features = getIDValues('Choosing Features(In importance order)')
        bestStragety(data, selected_features)            
        relationshipAnalysis(data, False, selected_features)
        
        
        
def _graphModeAnalysis(file):
    '''
    Graphis analysis 
    '''
    print('==========='*3)
    print('\n')    
    flag = True
    code = file.split(' | ')[1]
    single = False if 'In' in code else True
    if single:
        print('Analysis single fund with multiple circumstances')
        os.chdir(initalPath + dirs['GRAPH'].replace('.', ''))
        graphfilesName = sorted(glob.glob('{:s}*.txt'.format(code)))                
        while flag:                    
            if isinstance(graphfilesName, Iterable):
                graphfiles = [g[:-4] for g in graphfilesName]
                standardOutput(graphfiles)
                graphfile = graphfilesName[getIDValues()[0]]
                gdata = pd.read_csv(graphfile, sep='\t')
                gdata.drop(columns=['Unnamed: 0'], inplace=True)
                gdata.dropna(axis=0, how='any', inplace=True)
                __drawFigInShell(gdata)
                repeat = getIDValues('\nAnalysis more?[y/n]')[0]
                flag = True if repeat is 'y' or repeat is 'Y' else False
                    
            else:
                print('No input data for graph!')
        
    
    
    

    
    
    
#-------------------------------  MAIN PART  -----------------------------------

#REPEATFLAT = True

try:
    os.mkdir(dirs['CSV'])
except:
    print('File exists')
finally:
    os.chdir(dirs['CSV'])

    
files = sorted(glob.glob('*.txt'))
print('[--ID--] File name')
standardOutput(files)

print('Possible sorting features:')
standardOutput(colName)

selected_files = getIDValues()
for fileid in selected_files:
    try:
        file = files[fileid]
        try:
            _defaultModeAnalysis(file)
            _graphModeAnalysis(file)
        finally:
            print('\n\nFinshed\n\n' + '=='*5)
    except Exception as e:
        print(e)
        continue


