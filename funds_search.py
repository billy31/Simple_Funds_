#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 13:12:29 2019

@author: gladro
"""

import time
import pandas as pd
import urllib, os
#import argparse
from funds_extrance import args

code_name_list = args.database

def processFeatures(strlist):
    if 'zfill' in dir(strlist) or 'index' in dir(strlist):
        if '，' in strlist:
            strlist.replace('，', ',')        
        strlist = strlist.replace(' ', '')        
        if ',' in strlist:
            strout = [s for s in strlist.split(',')]
        else:
            strout = [strlist]
        return strout
    else:
        return [strlist]

def get_funds_total(dbname=code_name_list):
    if not os.path.exists(dbname):
        url = args.website
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
    return data


def select_features(aim, negativeaim, target):
    initialFlag = True
    try:
        for item in aim:
            itemFlag = item in target
            initialFlag = initialFlag and itemFlag
        for item in negativeaim:
            itemFlag = item not in target
            initialFlag = initialFlag and itemFlag
    except:
        initialFlag = True
    finally:
        return initialFlag


def get_selected_funds(pos, neg, SINGLE=False, code=None, 
                       totallist=get_funds_total()):
    selectedFunds = []
    selectedFundNames = []
    targetlist = totallist.Name.values.tolist()
    codelist = totallist.code.values.tolist()
    if SINGLE:
        try:
            codeid = codelist.index(code)
            return [[code], [targetlist[codeid]]]
        except:
            for _l, target in enumerate(targetlist):
                flag = select_features(pos, neg, target)
        #        print(target, flag)
                if flag:
                    selectedFunds.append(codelist[_l])
                    selectedFundNames.append(target)
            return [selectedFunds, selectedFundNames]
    else:
        for _l, target in enumerate(targetlist):
            flag = select_features(pos, neg, target)
    #        print(target, flag)
            if flag:
                selectedFunds.append(codelist[_l])
                selectedFundNames.append(target)
        return [selectedFunds, selectedFundNames]


Feature1 = processFeatures(args.aim)
Feature2 = processFeatures(args.negativeaim)

if args.usingOutput:
    selected = get_selected_funds(Feature1, Feature2, 
                                  args.single, args.code)
    try:
        for ids, s in enumerate(selected[0]):
            print(s, selected[1][ids])
            
    except Exception as e:
        print(e)
        
        
    


#def autoTurnFeature()
'''
usage:
selected = get_selected_funds(Feature1, Feature2)
'''
#print(selected)

