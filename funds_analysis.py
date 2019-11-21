#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 22:43:53 2019

@author: gladro
"""

#from funds import funds as funds
import funds
import funds_search as searchF
import funds_database as dbF
import pandas as pd
import datetime
import numpy as np
from pandas import DataFrame
import os, sys
#from bs4 import BeautifulSoup as bs
from multiprocessing import Pool
from funds_extrance import args

reportDir = './Reports/'
analysisDir = './Analysis/'

periodMarks = ['振荡上浮','快速上浮','快速下跌','振荡下跌','自定义时段']
stragetyMarks = ['定百分比止盈','简单定投','']

FREQUENCY = [7, 14, 31]
PROFIT = np.arange(0.05, 1.0, 0.01)

Feature1 = searchF.processFeatures(args.aim)
Feature2 = searchF.processFeatures(args.negativeaim)

sdate = funds.processDate(args.sdate)
edate = funds.processDate(args.edate)
_code = args.code

predefined_period1_concuup = [datetime.datetime(2012, 1, 1), datetime.datetime(2013, 7, 1)]
predefined_period1_quickrise = [datetime.datetime(2014, 1, 1), datetime.datetime(2015, 12, 1)]
predefined_period1_deepdrop = [datetime.datetime(2015, 8, 1), datetime.datetime(2017, 2, 1)]
predefined_period_concudown = [datetime.datetime(2017, 1, 1), datetime.datetime(2018, 7, 1)]

predefined_period_date = [sdate, edate]
periods = [predefined_period1_concuup, \
           predefined_period1_quickrise, \
           predefined_period1_deepdrop, \
           predefined_period_concudown, \
           predefined_period_date]

period = periods[int(args.testingPeriod)-1] if args.testingPeriod else periods[-1]

funcs = [funds.scheduled_simple_redemption, funds.scheduled_simple_holds]

stragety = funcs[int(args.stragety)-1]

frequency_str = searchF.processFeatures(args.frequency)
frequency = [int(f) for f in frequency_str]
goalProfit_str = searchF.processFeatures(args.goalProfit)
goalProfit = [float(g) for g in goalProfit_str]
output_report = args.output

Feature1 = searchF.processFeatures(args.aim)
Feature2 = searchF.processFeatures(args.negativeaim)
selected, selected_Names = searchF.get_selected_funds(Feature1, Feature2, args.single, _code)

dataValue = dbF.database_start(usingFullDB=False, codeInput=selected, returnResult=True)


def dealwithPath(outFlag, single_code=False, period=None, otherFeature=None, txtPointer=None):
    '''
    Generate name for files
    '''
    peidstr = periodMarks[periods.index(period)] + ' '#' | ' + 
    if period != None:
        peidstr = peidstr + period[0].strftime('From_%Y%m%d') + period[1].strftime('_To_%Y%m%d')
    if otherFeature != None:
        peidstr = peidstr + ' | ' + otherFeature
    if outFlag == True:
        print('Writing reports now...')
        try:
            os.mkdir(reportDir)
        except:
            print('\"{:s}\" exists'.format(reportDir))
        finally:
            fileOrder = str(len(os.listdir(reportDir))+1).zfill(4)
            if single_code:
                fileName = '{:s} | {:s} | {:s}'.format(fileOrder, single_code, peidstr)
            else:
                fileName = '{:s} | In_{:s} | Ex_{:s} | {:s}'.format(fileOrder, args.aim, args.negativeaim, peidstr)            
            txtName = reportDir + fileName + '.txt'
            return txtName 
    if outFlag == False:
        try:
            os.mkdir(analysisDir)
        except:
            print('\"{:s}\" exists'.format(analysisDir))
        finally:
            fileOrder = str(len(os.listdir(analysisDir))+1).zfill(4)
            if single_code:
                fileName = '{:s} | {:s} | {:s}'.format(fileOrder, single_code, peidstr)
            else:
                fileName = '{:s} | In_{:s} | Ex_{:s} | {:s}'.format(fileOrder, args.aim, args.negativeaim, peidstr)            
            anlyName = analysisDir + fileName + '.txt'
            return anlyName
    


def analysisdata(codeNamelist=selected_Names, codelist=selected, datalist=dataValue, func=stragety, peid=period,
                 fre=frequency, gProft=goalProfit, output_report=output_report):
    '''
    Main part to analyze the selected data
    '''    
    
    funcStr = stragetyMarks[funcs.index(func)]    
    
    txtContent = None if output_report == None else \
                    dealwithPath(output_report, single_code=_code, period=peid, otherFeature=funcStr)
    if output_report:
        txtPrint = open(txtContent, 'w')
    else:
        txtPrint = sys.stdout
        if output_report == False: outdbName = txtContent    
    
    database_total = pd.DataFrame(columns=funds.colName) 
    

    for itemID, code in enumerate(codelist):
        name = codeNamelist[itemID]
        data = datalist[itemID]
        
        print('Basic infomation:')        
        if data == []:
            print('{:s}-{:s} is not recorded by the database'.format(name, code), file=txtPrint)
        else:                        
            dbdate = [datetime.datetime.strptime(d[1], '%Y-%m-%d') for d in data]
            dbdate_str = [d[1] for d in data]
            print('Analysing {:s}-{:s}'.format(name, code),file=txtPrint)            
            print('This fund runs from {:s} to {:s}'.format(dbdate_str[-1], dbdate_str[0]))
            print('Aim to run from {:s} to {:s}'.format(period[0].strftime('%Y-%m-%d'), \
                  period[1].strftime('%Y-%m-%d')))
            
            if dbdate[0] <= peid[0]:
                print('The database does not have enough data for the giving period.', file=txtPrint)
            else:
                outDBFlag = True if output_report == False else False
                for f in fre:
                    for g in gProft:
                        if outDBFlag:
                            dbout = func(code, name, data, period, g, f, outDBFlag, txtPrint, args.single)
                            database_total = database_total.append(dbout)                    
                        else:
                            func(code, name, data, period, g, f, outDBFlag, txtPrint)        
        print('\n', file=txtPrint)
        
    
    if output_report == False:
        database_total.to_csv(outdbName, sep='\t')
        return database_total
#                if :
#                    outDB = func(data, code, gPr)
#        return database
#    else:
#        print('This fund runs from {:s} to {:s} [Aim: from {:s} to {:s}]'.format(
#              aimfunddb['Date'].values[-1], aimfunddb['Date'].values[0],
#              sdate.strftime('%Y-%m-%d'),edate.strftime('%Y-%m-%d')))               

#def p
        
    
    
#----------------------------------MAIN PART-----------------------------------    
if args.runWithin:
    analysisdata(fre=frequency, gProft=goalProfit)
    
    
    
#    pool = Pool(3)
#    if output_report == False:
#        database = pd.DataFrame(columns=funds.colName)    
#        for f in FREQUENCY:
#            for aimP in np.arange(0.05, 0.25, 0.01):
#                aa = pool.apply_async(func=analysisdata, \
#                                      args=(fre=f, gProft=aimP, ))
#                database = database.append(aa)
#    else:
#        for f in frequency:
#            for aimP in goalProfit:
#        
#    pool.close()
#    pool.join()       
    
    
    
    
    
    
    
    



'''
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



aimx = ''
aims = [args.aim1, args.aim2, args.aim3, args.aim4, \
        args.negativeaim1 + args.negativeaim2, args.negativeaim3, args.negativeaim4]
for loc, values in enumerate(aims):
    aimx += combine_aims(values, loc)
print(aimx)





#if __name__=="__main__":  


pool = Pool(50)






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
'''
