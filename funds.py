#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 13:01:05 2019

@author: gladro
"""

import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import datetime
import os
from scipy import optimize

colName = ['code', 'name', 'sdate', 'edate', 'intervals', 'aim_%', 'invest_times',
           'redemption times', 'profit_then_%', 'profit_then_anual_%', 'profit_total_%', 
           'profit_total_annual_%', 'avdays_before_profit', 'maxdays_before_profit',
           'mindays_before_profit']

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False



def get_value_to_analysis(code, sdate='2016-01-01', edate=datetime.date.today()):
    aimfunddb = get_fund_data(code, sdate, edate)
    sdate = datetime.datetime.strptime(sdate, '%Y-%m-%d').date()
    print(aimfunddb)
    if aimfunddb.shape[0] == 0:
        print('The database is empty')
        return 
    db_edate = datetime.datetime.strptime(aimfunddb['Date'].values[0], '%Y-%m-%d')        
    if db_edate.date() <= sdate:
        print('The database does not have enough data')
        return 
    else:
        print('This fund runs from {:s} to {:s} [Aim: from {:s} to {:s}]'.format(
              aimfunddb['Date'].values[-1], aimfunddb['Date'].values[0],
              sdate.strftime('%Y-%m-%d'),edate.strftime('%Y-%m-%d')))    
        x_line = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in aimfunddb['Date'].values.tolist()]
        y_line = [float(y) for y in aimfunddb['Value'].values.tolist()]
        plt.plot(x_line, y_line)
        plt.show()
        
#        for interv in [7, 14, 31]:
#            for aimProfit in np.arange(0.1, 0.21, 0.01):
#        print('Interval {:2d} days, Aimprofit {:.2f}'.format(interv, aimProfit))
                
#                outDb = funds.strategy_scheduled_simple_callback(aimfunddb, 
#                                                                 code, aimfunddb
#                                                                 [aimfund['code'].values[0], item], 
#                                                                 profit=aimProfit, intervals=interv)
#                try:
#                    database = database.append(outDb, ignore_index=True)
#                except:
#                    print('Continue!')


















def xnpv(rate, cashflows):
    return sum([cf/(1+rate)**((t-cashflows[0][0]).days/365.0) for (t,cf) in cashflows])
 
def xirr(cashflows, guess=0.1):
    try:
        return optimize.newton(lambda r: xnpv(r,cashflows),guess)
    except:
        print('Calc Wrong')


def get_url(url, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text


def get_fund_data(code,sdate='',edate='',per=10,proxies=None):
    print('Getting fund data of {:s}'.format(code))
    try:
        if not os.path.exists('./Funds_data/{:s}.txt'.format(code)):    
            url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
            params = {'type': 'lsjz', 'code': code, 'page':1,'per': per, 'sdate': sdate, 'edate': edate}
            html = get_url(url, params, proxies)
            soup = BeautifulSoup(html, 'html.parser')
            pattern=re.compile(r'pages:(.*),')
            result=re.search(pattern,html).group(1)
            pages=int(result)    
            heads = []
            for head in soup.findAll("th"):
                heads.append(head.contents[0])    
            records = []    
            page=1
            while page<=pages:
                params = {'type': 'lsjz', 'code': code, 'page':page,'per': per, 'sdate': sdate, 'edate': edate}
                html = get_url(url, params, proxies)
                soup = BeautifulSoup(html, 'html.parser')   
                for row in soup.findAll("tbody")[0].findAll("tr"):
                    row_records = []
                    for record in row.findAll('td'):
                        val = record.contents                
                        if val == []:
                            row_records.append(np.nan)
                        else:
                            row_records.append(val[0])            
                    records.append(row_records)        
                page=page+1    
            np_records = np.array(records)
            data= pd.DataFrame()
            for col,col_name in enumerate(heads):
                data[col_name] = np_records[:,col]
            # Un-chinese usage
            data.columns = ['Date', 'Value', 'Cumulative net Value', 'Growth rate', 
                            'Perchase state', 'Redemption state', 'Dividend']
            data.to_csv('./Funds_data/{:s}.txt'.format(code), sep='\t')
        else:
            data = pd.read_csv('./Funds_data/{:s}.txt'.format(code), sep='\t', 
                               index_col=False)    
        return data
    except:
        print('Not enough data')
        return pd.DataFrame(columns=['Date', 'Value', 'Cumulative net Value', 'Growth rate', 'Perchase state', 'Redemption state', 'Dividend'])

def reached_or_not(currentProfit, aimProfit, sdate, edate):    
    years = int((edate - sdate).days / 365) + 1
    Flag = True if currentProfit >= (aimProfit * years + 1) else False
    return Flag

def strategy_scheduled_simple_callback(data, code, profit=0.12, intervals=30, 
                                       money_per_amount=1000, PRINTOUT=True):
    print('Analysing...')    
    days_before_profit = []
    cash_flow = []
    datelist = [datetime.datetime.strptime(i, '%Y-%m-%d') for i in data['Date']]    
    take_times = 0
    money_outside = 0
    invest_times = 0
    funds_hold = 0
    money_total = 0
    money_actual = 0
    edate = datelist[0]
    sdate = datelist[-1]
    last_withdraw_date = sdate
    latest_invest_date = sdate    
    daysdelta = edate - sdate
    invest_time_total = 0
    profit_total_amount = 0
    print('The product has been over %4d days.' % daysdelta.days)
    money_prev_total = 0
    while(latest_invest_date <= edate):
#        data_loc = (data.Date == latest_invest_date.strftime('%Y-%m-%d')).tolist().index(True)
        try:
            netValue = float(data[data.Date == latest_invest_date.strftime('%Y-%m-%d')].Value.values[0])
            amounts = money_per_amount / netValue        
        except:
            latest_invest_date -= datetime.timedelta(days=2)
            netValue = float(data[data.Date == latest_invest_date.strftime('%Y-%m-%d')].Value.values[0])
            amounts = money_per_amount / netValue        
        invest_times += 1
        invest_time_total += 1
        money_total += money_per_amount
        funds_hold += amounts
        days = intervals
        if latest_invest_date + datetime.timedelta(days=intervals) <= edate:
            try:
                while(not (latest_invest_date + datetime.timedelta(days=days)) in datelist):
                    days += 1
                latest_invest_date += datetime.timedelta(days=days)
#                print('Invest {:3d} times at {:s}'.format(invest_times, latest_invest_date.strftime('%Y-%m-%d')))
            except:
                latest_invest_date = edate + datetime.timedelta(days=1)
#                print('Not invested')
        else:
            latest_invest_date = edate + datetime.timedelta(days=1)
#            print('Not invested')            
        if invest_times != 1:
            money_actual = funds_hold * netValue
            currentProfit = money_actual / money_total
            if reached_or_not(currentProfit, profit, last_withdraw_date, latest_invest_date):                
                take_times += 1
                cash_flow.append((last_withdraw_date, -1*money_total))
                duration = (latest_invest_date - last_withdraw_date).days
                print('[Income times: {:>2d}] {:s} {:>4d} days'.format(\
                      take_times, latest_invest_date.strftime('%Y-%m-%d'), duration), end=' ')
                print('In: {:8.2f}\tOut: {:8.2f}'.format(money_total, money_actual))
                days_before_profit.append(duration)
                profit_total_amount += money_actual - money_total
                money_prev_total += money_total
                last_withdraw_date = latest_invest_date                
                money_outside += money_actual
                money_actual = 0
                money_total = 0
                invest_times = 0
                funds_hold = 0
    final_duration = (edate - last_withdraw_date).days
    days_before_profit.append(final_duration)                
    current_total_money = money_outside + money_actual
    if take_times > 1:        
        cash_flow.append((last_withdraw_date, money_outside))
    cash_flow_total = [(sdate, -1 * invest_time_total * money_per_amount), 
                       (edate, current_total_money)]
    try:
        profit_then = (money_outside / money_prev_total - 1) * 100
    except:
        profit_then = None
    
    try:
        profit_then_anual = xirr(cash_flow) * 100
    except:
        profit_then_anual = None
        
    try:
        profit_total = (profit_total_amount / (money_per_amount * invest_time_total)) * 100
    except:
        profit_total = None
    
    try:
        profit_total_anual = xirr(cash_flow_total) * 100
    except:
        profit_total_anual = None
#    profit_then = None if money_prev_total == 0 else (money_outside / money_prev_total - 1) * 100
#    profit_then_anual = None if money_prev_total == 0 else xirr(cash_flow) * 100
#    profit_total = (profit_total_amount / (money_per_amount * invest_time_total)) * 100
#    profit_total_anual = xirr(cash_flow_total) * 100
        
    print('--' * 10)
    print('Total {:d} days. Invest {:d} times, redemption {:d} times, '.format(daysdelta.days, invest_time_total, take_times))    
    try:
        print('Previous profit {:8.2f} % [Profit of all previous redemptions]'.format(profit_then)) 
    except:
        print('No profit so far')
        
    '''
    percentage = current_total_money/(invest_time_total * money_per_amount) - 1
    try:
        print('Total profit {:8.2f} % [Received profit / total money in hand]'.format((profit_total / current_total_money) * 100))
        print('Profit percentage {:8.2f} [Profit percent by counting all the money]%'.format(percentage * 100))
    #    print('Already profit {:8.2f}'.format(profit_total))
        result_str = 'profits' if (money_actual - money_total) > 0 else 'loss'
        print('Current {:8.2f} % {:s} [After remove the received profit]'.format((money_actual - money_total)/money_total*100,result_str), end='\n\n')  
    except:
        print('No currenty money so far')
    '''
    
#colName = ['code', 'name', 'sdate', 'edate', 'intervals', 'aim', 'invest_times',
#           'redemption times', 'profit_then', 'profit_then_anual', 'profit_total', 
#           'profit_total_annual', 'avdays_before_profit', 'maxdays_before_profit',
#           'mindays_before_profit']
#   
    if PRINTOUT:
        output_data = np.array([[code[0], code[1], data['Date'].values[-1], 
                       data['Date'].values[0], intervals, profit * 100, 
                       invest_time_total, take_times, 
                       profit_then, profit_then_anual, profit_total, 
                       profit_total_anual, np.mean(days_before_profit), 
                       np.max(days_before_profit), np.min(days_before_profit)]])
        output = pd.DataFrame(output_data, columns=colName)    
    #    
        return output
    
    
    

if __name__ == "__main__":
    data=get_fund_data('161725',per=49,sdate='2018-01-01',edate='2018-12-31')
    
    data['净值日期']=pd.to_datetime(data['净值日期'],format='%Y/%m/%d')
    data['单位净值']= data['单位净值'].astype(float)
    data['累计净值']=data['累计净值'].astype(float)
    data['日增长率']=data['日增长率'].str.strip('%').astype(float)
    
    data=data.sort_values(by='净值日期',axis=0,ascending=True).reset_index(drop=True)
    print(data)

    
    net_value_date = data['净值日期']
    net_asset_value = data['单位净值']
    accumulative_net_value = data['累计净值']
    daily_growth_rate = data['日增长率']

    fig = plt.figure()
    
    ax1 = fig.add_subplot(111)
    ax1.plot(net_value_date,net_asset_value)
    ax1.plot(net_value_date,accumulative_net_value)
    ax1.set_ylabel('净值')
    ax1.set_xlabel('日期')
    plt.legend(loc='upper left')
    
    ax2 = ax1.twinx()
    ax2.plot(net_value_date,daily_growth_rate,'r')
    ax2.set_ylabel('日增长率(%)')
    plt.legend(loc='upper right')
#    plt.title('??????')
    plt.show()

    bonus = accumulative_net_value-net_asset_value
    plt.figure()
    plt.plot(net_value_date,bonus)
    plt.xlabel('日期')
    plt.ylabel('累计净值-单位净值')
#    plt.title('??????')
    plt.show()
#
#    print('??????:',sum(np.isnan(daily_growth_rate)))
#    print('?????????:',sum(daily_growth_rate>0))
#    print('??????(??0)???:',sum(daily_growth_rate<=0))