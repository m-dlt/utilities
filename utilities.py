# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 09:36:30 2016

@author: moleary
"""
import os
import time
import urllib
import sqlalchemy as sql
import pandas as pd
from datetime import date,timedelta
from calendar import monthrange
from pandas.tseries.holiday import USFederalHolidayCalendar as fedHoliCal

def search(fname, directory):
    for dirpath, dirnames, filenames in os.walk(directory):
        if fname in filenames:
            return os.path.join(dirpath,fname)

def currTime():
    """generates Current Date/time in clean format"""
    return str(time.strftime("%a %d-%b-%Y, %I:%M:%S%p"))


def sqlConn(serverName,dbName,userName,password):
    params = urllib.parse.quote_plus('''DRIVER={SQL Server};SERVER='''+serverName+''';PORT=1433;
                                        DATABASE='''+dbName+''';UID='''+userName+''';PWD='''+password)
    engine = sql.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    return engine


#Find n-th work Day for specific month
#Default is current month, month needs to be numeric 1-12


def businessDay(month='', day=1):
    if month not in list(range(1,13)):
        return "ERROR: Month value outside of range"
    if month == '':
        begMon = date.today().replace(day=1)
        endMon = date.today().replace(day=monthrange(date.today().year,date.today().month)[1])
        cal = fedHoliCal()
        count = 0
        if day > monthrange(date.today().year,date.today().month)[1]:
            return "ERROR: Day outside of month range"
        else:
            drange = pd.bdate_range(start=begMon,periods=day).to_pydatetime()
            for day in drange:
                if day in cal.holidays(begMon,endMon):
                    count+=1
            return drange[-1]+timedelta(days=count)
    else:
        begMon = date(date.today().year,month,1)
        endMon = begMon.replace(day=monthrange(begMon.year,month)[1])
        cal = fedHoliCal()
        count = 0
        if day > monthrange(begMon.year,month)[1]:
            return "ERROR: Day outside of month range"
        else:
            drange = pd.bdate_range(start=begMon,periods=day).to_pydatetime()
            for day in drange:
                if day in cal.holidays(begMon,endMon):
                    count+=1
            return drange[-1]+timedelta(days=count)
