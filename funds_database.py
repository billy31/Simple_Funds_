#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 21:34:10 2019

1. Data cleaning
2. Data downloading/initialization
3. Data update

@author: gladro
"""

import sqlite3 as sql
import os, glob
import datetime
import numpy as np
import pandas as pd
import funds
from multiprocessing import Pool


def get_FileCreateTime(filePath):
      t = os.path.getctime(filePath)
      return t

def initDatabase(connection, txtdir='./Funds_data'):
    tableNames = []
    os.chdir(txtdir)
    filelist = sorted(glob.glob('*.txt'))
    csvdb = pd.read_csv(filelist[0], sep='\t')
    csvdb.drop(inplace=True, columns=['Unnamed: 0'])
    for item in filelist:        
        tabledb = pd.read_csv(item, sep='\t')
        tabledb.drop(inplace=True, columns=['Unnamed: 0'])
        tableName = item.split('.')[0]
        tableNames.append(tableName)
        try: # Create table 
            tabledb.to_sql(tableName, con=connection)
            print('Writing table \"{:s}\"'.format(tableName))
        except Exception as e:
            print('table creation errors in: \"{:s}\"'.format(str(e)))  
        else:
            continue
    return tableNames

def updateDatabase(dbtoday, connection, code, coltext):
    cursor = connection.cursor()
    today = datetime.datetime.today()
    if (today - dbtoday).days >= 7:
        print('Needs update, ', end=' ')
        dbtoday += datetime.timedelta(days=1)
        newdata = funds.get_fund_data(code, sdate=dbtoday, edate=today, online=True)
        try:
            for records in range(newdata.shape[0]):
                sqlcom = 'INSERT INTO \"{:s}\" ({:s}) '.format(code, coltext) + \
                'VALUES (?,?,?,?,?,?,?);'
                data = newdata.loc[records].values.tolist()
                sqlcom = sqlcom[:-1] + ';'
                cursor.execute(sqlcom, data)               
        except Exception as e:
            print(e)
    print(1)
    cursor.close()
    connection.commit() 
            
def autoName(Names):
    colstrL = (name[0] for name in Names)
    colstr = ''
    for c in colstrL:
        if c != 'index' and c != 'Dividend':
            colstr += ('\"' + c + '\", ')
        if c == 'Dividend':
            colstr += ('\"' + c + '\"')
    return colstr
#    Names = Names if '__iter__' in dir(Names) else list(Names)
#    for dataName in Names:
#        try:
#            dataName = dataName.replace(' ', '')
#            dataName = dataName.replace('%', '')
#        except:
#            continue
#    return Names
#    if 'Value' in dataName or 'value' in dataName or \
#        'rate' in dataName or 'Rate' in dataName or \
#        'profit' in dataName or 'Profit' in dataName or \
#        'aim' in dataName:
#        return dataName + ' Float '    
#    else:    
#        return dataName + ' Text '

#
#def create_table_name(tableName, colName):
#    outStr = 'create table ' + tableName + ' '    
#    if '__iter__' in dir(colName):
#        for colCount, name in enumerate(colName):
#            outStr +=  (autoTypeChooser(name) + 'Primary ') \
#                        if colCount == 0 else \
#                        autoTypeChooser(name)
#    return outStr

#def writingPD2SQL(database, Name, connection):
#    database.to_sql(name=Name, con=connection)
    
    
try: # Create database
    conn = sql.connect("/home/lzy/funds/Funds Info.db")
#    conn.execute("PRAGMA busy_timeout = 30000") 
except Exception as e:
    print('sql connection errors in: \"{:s}\"'.format(str(e)))
else:
    flag = True
    try: # Generate table name list        
        cur = conn.cursor()
        tableNames = cur.execute('select name from sqlite_master where type=\"table\"').fetchall() 
    except Exception as e:
        print('reading sqldb errors in: \"{:s}\"'.format(str(e)))
        print('initializing...')
        tableNames = initDatabase(conn)
        flag = False
    finally: # Checking timeliness
        tableNames = [t[0] for t in tableNames] if flag else tableNames
        cur.execute('select * from \"{:s}\" limit 10'.format(tableNames[0]))
        coltext = autoName(cur.description)
        for table in tableNames: # Read every table
            top10 = cur.execute('select date from \"{:s}\" order by date desc limit 10'.format(table)).fetchall()
#            conn.close()
            latestDate = datetime.datetime.strptime(top10[0][0], '%Y-%m-%d')
#            conn.close()    
#            conn1 = sql.connect('Funds Info.db')
#            curupdate = conn1.cursor()
            updateDatabase(latestDate, conn, table, coltext)
#            conn.commit()
            break
        
        conn.close()