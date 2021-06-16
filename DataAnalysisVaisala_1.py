#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 11:45:20 2021

@author: zaidanma
"""

import pandas as pd
import matplotlib.pyplot as plt


# We read data from Vaisala sensors installed in SORPES:

#df1 = pd.read_csv('clean_vaisala_data2/P1720668.csv') # Ngaco (in Tower)
df2 = pd.read_csv('clean_vaisala_data2/P1720669.csv')  # SORPES
#df1 = pd.read_csv('clean_vaisala_data2/P1910347.csv') #
#df1 = pd.read_csv('clean_vaisala_data2/P1910345.csv') #
df1 = pd.read_csv('clean_vaisala_data2/P2150596.csv')  #

#%% Check data types for each dataframe

print(df1.dtypes)
print(df2.dtypes) 

# The second dataframe has some object which means, it has some missing data
cols = df2.columns.drop('Time') # This is better

# Replace blank value with nan and now everything becomes float number
# https://www.geeksforgeeks.org/python-pandas-to_numeric-method/
df2[cols] = df2[cols].apply(pd.to_numeric, errors='coerce')
print(df2.dtypes) 

# Do the same for df1
cols = df1.columns.drop('Time') 
df1[cols] = df1[cols].apply(pd.to_numeric, errors='coerce')

#%% Sync data

# To allow resample, Convert column date to datetimes:
# https://stackoverflow.com/questions/57703538/typeerror-only-valid-with-datetimeindex-timedeltaindex-or-periodindex-but-got    
df1['Time'] = pd.to_datetime(df1['Time'])
df2['Time'] = pd.to_datetime(df2['Time'])


col = 'T'
X1 = df1.loc[:, ['Time', col]]
Y1 = df2.loc[:, ['Time', col]]


X1a = X1.set_index('Time').resample('5T').mean()
Y1a = Y1.set_index('Time').resample('5T').mean()

# https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
Z1a = pd.merge(X1a, Y1a, on="Time")


#Z1a.plot()


# Scatter plot
plt.scatter(Z1a[col+'_x'], Z1a[col+'_y'], label=col)
plt.legend(loc='best', fontsize=16)
plt.xlabel(col)
plt.ylabel(col)
plt.title('Consistency Sensors validation for var '+col)
plt.show()
