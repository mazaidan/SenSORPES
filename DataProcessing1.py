#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 15:55:43 2021

@author: zaidanma
"""
import pandas as pd

def VaisalaPreProcess(Vaisala1,SensorNo):
  cols = Vaisala1.columns.drop('Time') 
  Vaisala1[cols] = Vaisala1[cols].apply(pd.to_numeric, errors='coerce')
  print(Vaisala1.dtypes)
  # To allow resample, convert column date to datetimes:
  # https://stackoverflow.com/questions/57703538/typeerror-only-valid-with-datetimeindex-timedeltaindex-or-periodindex-but-got    
  Vaisala1['Time'] = pd.to_datetime(Vaisala1['Time'])
  # set the datetime as index:
  Vaisala1 = Vaisala1.set_index('Time')
  # Convert the timezone:
  Vaisala1a = Vaisala1.tz_convert('Asia/Shanghai') 
  # resample
  Vaisala1b = Vaisala1a.resample('1H').mean()
  
  cols  = Vaisala1b.columns
  cols1 = cols+'v'+str(SensorNo)
  
  Vaisala1b.columns = cols1 
  
  return Vaisala1b
  