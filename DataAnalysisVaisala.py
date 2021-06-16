#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  5 12:05:57 2021

@author: zaidanma
"""

import os
import pandas as pd
import numpy as np


files1 = os.listdir('vaisala sensor/')
print(files1)

S = 4 # choose Sensor (S): 1:5 SORPES: 3

temp_str = 'vaisala sensor/'+files1[S]+'/'
files2 = os.listdir(temp_str)



# https://revetice.readthedocs.io/en/latest/python/regular_expression.html
# use extend instead of append
# Here we use to list only scv file
files3=[]
for file in os.listdir(temp_str):
    if file.endswith(".csv"):
        print(file)
        files0=[file] # covert the string to be placed in list
        #files3.append(files0)
        files3.extend(files0)

files2 = files3

# https://www.geeksforgeeks.org/how-to-read-a-csv-file-to-a-dataframe-with-custom-delimiter-in-pandas/
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
#df = pd.read_csv('vaisala sensor/raw data_P1720668/P1720668_20180717-20180815.csv', sep=';')
#print(df)

temp_str = 'vaisala sensor/'+files1[S]+'/'+files2[0]
df = pd.read_csv(temp_str, sep=';')
print(files2[0])
print(df)

## Let loop all over the data per sensor, and we append the dataframe

# First let make an empty dataframe
# https://thispointer.com/pandas-how-to-create-an-empty-dataframe-and-append-rows-columns-to-it-in-python/
# We take the column name from the df above
df1 = pd.DataFrame(df.columns.name)


for x in range(len(files2)):
  print(x)
  temp_str = 'vaisala sensor/'+files1[S]+'/'+files2[x]
  df = pd.read_csv(temp_str, sep=';')
  print(files2[x])
  #print(df)
  df1 = df1.append(df)

# We need to sort out the data based on the date,
# Then, we reset the index
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html  
df2 = df1.sort_values(by='Timestamp')
#df3=df2.reset_index() # Reset the index, but old index is kept as new column
df3=df2.reset_index(drop=True) # old index is dropped
print(df3)

# Find the first and the last measurements

print('first measurement time: '+df3.Timestamp[0])
#
# we cannot use -1 to find the last row in 'Series' type
# instead, we find the last row index

# print('last measurement time: '+df3.Timestamp[97943])
last_row = len(df3)-1
print('last measurement time: '+df3.Timestamp[last_row])


#
# to select column in df without sepcifying the name
# https://pbpython.com/selecting-columns.html
# Carbon monoxide
print(df3.iloc[0,3])

if type(df3.iloc[0,3]) == np.float64:
    print('CO mean concentration: ' + np.str(np.mean(df3.iloc[:,3])))
else:
    print("Data might not exist")



## The below code is to rename the columns 

df4 = df3
# print column df3:
# https://www.geeksforgeeks.org/how-to-get-column-names-in-pandas-dataframe/
list(df3.columns)
print(list(df3.columns))

if S==1:
    print('S=1')
    # rename the columns:
    # https://stackoverflow.com/questions/11346283/renaming-columns-in-pandas
    df4 = df3.set_axis(['Time','P', 'T', 'CO', 'Health',
                    'NO2','O3','PM10','PM25','RI','RH',
                    'SO2','WD','WS','NN'], axis=1, inplace=False)
elif S==2:
    print('S=2')
    df4 = df3.set_axis(['Time','P', 'T', 'CO', 'Health',
                    'NO2','O3','PM10','PM25','RI','RH',
                    'SO2','WD','WS','NN1','CO2','NO','NN2'], axis=1, 
                       inplace=False)
elif S==3:
    print('S=3')
    df4 = df3.set_axis(['Time','P', 'T', 'CO2', 'CO', 'Health',
                    'NO2','NO','O3','PM10','PM25','RI','RH',
                    'WD','WS','NN1','NN2'], axis=1, 
                       inplace=False)
elif S==4:
    print('S=4')
    df4 = df3.set_axis(['Time','P', 'T', 'CO', 'Health',
                    'NO2','O3','PM10','PM25','RH',
                    'SO2','NN1','CO2','NO','NN2'], axis=1, 
                       inplace=False)
elif S==5:
    print('S=5')
    df4 = df3.set_axis(['Time','P', 'T',  'CO', 'Health',
                    'NO2','O3','PM10','PM25','RI','RH','SO2',
                    'WD','WS','NN2'], axis=1, 
                       inplace=False)    



# the below function is to save data
save_data = 0
if save_data == 1:
    print('save data df4')
    file_name = files1[S]
    print(file_name.replace('raw data_', ''))
    file_name=file_name.replace('raw data_', '')
    df4.to_csv(file_name+'.csv')
else:
    print('do not save data df3')
    
    
#%% Let plot some data
# Ask some information, such as:
# 1) The name of Vaisala instruments used and vars measured
# 2) The location of the Vaisala instruments
#    a) Check if there are some instruments are near reference stations, so 
#       we can perform sensors validation
#    b) For the instruments run far away from reference instruments, 
#       we can perform remote sensing validations (or other near by stations) 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.close("all")

# https://queirozf.com/entries/pandas-dataframe-plot-examples-with-matplotlib-pyplot

df4.head()
df4.tail()
print(df4.columns.tolist())


# Replace non-numeric values with nan:
# https://stackoverflow.com/questions/36814100/pandas-to-numeric-for-multiple-columns

# Check the data type in your dataframe:
df4.dtypes

# Data as object indicates that they contain some string mixed with numerical data
# To get all data as object:
# cols = df4.columns[df4.dtypes.eq('object')] # it includes col "Time" too
cols = df4.columns.drop('Time') # This is better

# Replace black value with nan:
# https://www.geeksforgeeks.org/python-pandas-to_numeric-method/
df4[cols] = df4[cols].apply(pd.to_numeric, errors='coerce')


df4.plot(x="Time", y="PM25")
plt.show()

#%% What do we need from SORPES:
    
# Variables
print(df4.columns.tolist())
# Datetime ranges    
print('Starting date: ' + df4['Time'].head(1))
print('Ending date: '   + df4['Time'].tail(1))
    