#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 09:52:22 2021

@author: zaidanma
"""

#%% Load necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#%% We read data from SORPES:
    
xls = pd.ExcelFile('SORPES data/gas_aerosol_SORPES_2019.xlsx')
SheetNames = xls.sheet_names  # see all sheet names
#xls.parse(SheetNames)  # read a specific sheet to DataFrame
gas_VOCs_aerosol = pd.read_excel(xls, SheetNames[0])
PNSD             = pd.read_excel(xls, SheetNames[1])    
SA_HOM           = pd.read_excel(xls, SheetNames[2])
    

# Other reading methods: 
#df_SORPES = pd.read_csv('SORPES data/gas_aerosol_SORPES_2019.xlsx')
#df_SORPES = pd.read_excel('SORPES data/gas_aerosol_SORPES_2019.xlsx')

#%% To check the available variables on each sheet

print('gas VOCs aerosol variables include:')
for col in gas_VOCs_aerosol:
    print(col)

print('Particle Number Size Distribution (PNSD) include:')    
for col in PNSD:
    print(col)

print('SA HOM include:')    
for col in SA_HOM:
    print(col)      
    
#%% Download Vaisala (installed in SORPES)
Vaisala1 = pd.read_csv('clean_vaisala_data2/P1720668.csv') # Ngaco (in Tower)
Vaisala2 = pd.read_csv('clean_vaisala_data2/P1720669.csv')  # SORPES 


#print(Vaisala1.dtypes)
#print(Vaisala2.dtypes) 
# Give detailed information of Vaisala data
Vaisala1.info()
Vaisala2.info()


# From the above informaiton, many data contain 'object", we need
# to change them all to float64, except for col "Time", 
# So, we collect all columns names, except "Time"
cols = Vaisala2.columns.drop('Time') # This is better

# Next, we use the "cols" names, to make them 'float'
# Replace blank value with nan and now everything becomes float number
# https://www.geeksforgeeks.org/python-pandas-to_numeric-method/
Vaisala2[cols] = Vaisala2[cols].apply(pd.to_numeric, errors='coerce')
print(Vaisala2.dtypes) 

# Do the same for df1
cols = Vaisala1.columns.drop('Time') 
Vaisala1[cols] = Vaisala1[cols].apply(pd.to_numeric, errors='coerce')
print(Vaisala1.dtypes) 




# We select only relevant SORPES data 
SORPES1 = gas_VOCs_aerosol.iloc[:,0:9]

SORPES1.info()
Vaisala2.info()
Summary_SORPES1 = SORPES1.describe()
Summary_Vaisala2 = Vaisala2.describe()


#%% Sync data: SORPES-Vaisala dataframe merging:
    
# https://www.earthdatascience.org/courses/use-data-open-source-python/use-time-series-data-in-python/date-time-types-in-pandas-python/resample-time-series-data-pandas-python/ 
# https://stackoverflow.com/questions/27080542/merging-combining-two-dataframes-with-different-frequency-time-series-indexes-in



# Convert timezone
# https://stackoverflow.com/questions/25653529/converting-timezones-from-pandas-timestamps

# Resample
# https://stackoverflow.com/questions/57703538/typeerror-only-valid-with-datetimeindex-timedeltaindex-or-periodindex-but-got


# To allow resample, convert column date to datetimes:
# https://stackoverflow.com/questions/57703538/typeerror-only-valid-with-datetimeindex-timedeltaindex-or-periodindex-but-got    
Vaisala2['Time'] = pd.to_datetime(Vaisala2['Time'])
# set the datetime as index:
Vaisala2 = Vaisala2.set_index('Time')
# Convert the timezone:
Vaisala2a = Vaisala2.tz_convert('Asia/Shanghai') 
# resample
Vaisala2b = Vaisala2a.resample('1H').mean()


# To allow resample, convert column date to datetimes:
SORPES1['Dt'] = pd.to_datetime(SORPES1['Dt'])
# set the datetime as index:
SORPES1 = SORPES1.set_index('Dt') 
# Insert the timezone
SORPES1a = SORPES1.tz_localize('Asia/Shanghai')
# resample the timezone
SORPES1b = SORPES1a.resample('1H').mean()

sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = SORPES1b['PM2.5（μg/m3）'].plot(linewidth=0.5);
Vaisala2b['PM25'].plot(linewidth=0.5);
ax.set_title('To observe PM$_{2.5}$ before merging the data of Vaisala-SORPES')
ax.set_ylabel('PM$_{2.5}$ [$\mu g/m^3$]')
plt.style.use('seaborn')
#plt.style.use('tex')


# We concatanete the data:
DATA2 = pd.concat([Vaisala2b, SORPES1b], join='inner', axis=1)

# See the columns, if they are merged:
for col in DATA2:
    print(col) 
    
cols_list = list(DATA2.columns)


# Summary and see if both data have similar or very different statistics:
SUMMARY = DATA2.describe()
print(SUMMARY['PM25'])
print(SUMMARY['PM2.5（μg/m3）'])


#%% Data Visualization (time-series)

# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = SORPES1a['PM2.5（μg/m3）'].plot(linewidth=0.5);
Vaisala2a['PM25'].plot(linewidth=0.5);
Vaisala2b['PM25'].plot(linewidth=0.5);
ax.set_title('Before and after resample, SORPES and Vaisala are very different')
ax.set_ylabel('PM$_{2.5}$ [$\mu g/m^3$]')
plt.style.use('seaborn')


# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA2['PM2.5（μg/m3）'].plot(linewidth=0.5);
DATA2['PM25'].plot(linewidth=0.5);
ax.set_title('After resample, the data remains very different')
ax.set_ylabel('PM$_{2.5}$ [$\mu g/m^3$]')
plt.style.use('seaborn')


sns.set(rc={'figure.figsize':(11, 4)})
ax = DATA2['O3 ppb'].plot(linewidth=0.5);
DATA2['O3'].plot(linewidth=0.5);
ax.set_title('Trace gases, such as O$_3$ is also different')
ax.set_ylabel('O$_3$ [ppb]')
plt.style.use('seaborn')


#%% SCATTER PLOTS


# PM2.5 Scatter plot
plt.scatter(DATA2['PM2.5（μg/m3）'],DATA2['PM25'],label='PM2.5')
plt.legend(loc='best', fontsize=16)
plt.xlabel('PM2.5 (SORPES)')
plt.ylabel('PM2.5 (Vaisala)')
plt.title('PM2.5: SORPES vs Vaisala')
plt.show()


# NO2 Scatter plot
ax=plt.scatter(DATA2['NO2 ppb'],DATA2['NO2'],label='NO2')
plt.legend(loc='best', fontsize=16)
plt.xlabel('NO2 (SORPES)')
plt.ylabel('NO2 (Vaisala)')
plt.show()

# CO Scatter plot
plt.scatter(DATA2['CO ppm'],DATA2['CO'],label='CO')
plt.legend(loc='best', fontsize=16)
plt.xlabel('CO (SORPES)')
plt.ylabel('CO (Vaisala)')
plt.title('CO: SORPES vs Vaisala')
plt.show()
