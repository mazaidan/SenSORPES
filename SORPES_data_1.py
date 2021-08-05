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

gas_VOCs_aerosol = pd.read_excel(xls, SheetNames[0])
PNSD             = pd.read_excel(xls, SheetNames[1])    
SA_HOM           = pd.read_excel(xls, SheetNames[2])
    

# Other reading methods: 
#df_SORPES = pd.read_csv('SORPES data/gas_aerosol_SORPES_2019.xlsx')
#df_SORPES = pd.read_excel('SORPES data/gas_aerosol_SORPES_2019.xlsx')

#%% Print the available variables on each sheet

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


# Provide detailed information of Vaisala data
Vaisala1.info()
Vaisala2.info()


# From the above informaiton, many data vars contain 'object", 
# we need to change them all to float64, except for col "Time", 
# So, we collect all columns names, except "Time"
cols = Vaisala2.columns.drop('Time') 

# Next, we use the "cols" names, to make them 'float'
# Replace blank value with nan and now everything becomes float number
# https://www.geeksforgeeks.org/python-pandas-to_numeric-method/
Vaisala2[cols] = Vaisala2[cols].apply(pd.to_numeric, errors='coerce')
print(Vaisala2.dtypes) 

# Do the same for Vaisala1 data
cols = Vaisala1.columns.drop('Time') 
Vaisala1[cols] = Vaisala1[cols].apply(pd.to_numeric, errors='coerce')
print(Vaisala1.dtypes) 


# We select only relevant SORPES data 
SORPES1 = gas_VOCs_aerosol.iloc[:,0:9]

SORPES1.info()
Vaisala1.info()
Vaisala2.info()
Summary_SORPES1 = SORPES1.describe()
Summary_Vaisala1 = Vaisala1.describe()
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
Vaisala1['Time'] = pd.to_datetime(Vaisala1['Time'])
# set the datetime as index:
Vaisala1 = Vaisala1.set_index('Time')
# Convert the timezone:
Vaisala1a = Vaisala1.tz_convert('Asia/Shanghai') 
# resample
Vaisala1b = Vaisala1a.resample('1H').mean()


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
ax = SORPES1['PM2.5（μg/m3）'].plot(linewidth=0.5);
Vaisala2['PM25'].plot(linewidth=0.5);
ax.set_title('To observe PM$_{2.5}$ before modifying time-zone')
ax.set_ylabel('PM$_{2.5}$ [$\mu g/m^3$]')
plt.ylim(0, None)
plt.legend(labels=["SORPES1 (before resample-time change)","Vaisala1 (before resample-time change)"])
plt.style.use('seaborn')

sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = SORPES1b['PM2.5（μg/m3）'].plot(linewidth=0.5);
Vaisala2b['PM25'].plot(linewidth=0.5);
ax.set_title('To observe PM$_{2.5}$ before merging the data of Vaisala-SORPES')
ax.set_ylabel('PM$_{2.5}$ [$\mu g/m^3$]')
plt.ylim(0, None)
plt.legend(labels=["SORPES1b (after resample)","Vaisala2b (after resample)"])
plt.style.use('seaborn')

# To check if there is an effect before and after resample
# ANSWER: NOT MUCH EFFECT, the procedure is correct
sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = SORPES1a['PM2.5（μg/m3）'].plot(linewidth=0.5);
Vaisala2a['PM25'].plot(linewidth=0.5);
Vaisala2b['PM25'].plot(linewidth=0.5);
ax.set_title('Before and after resample, SORPES and Vaisala are very different')
ax.set_ylabel('PM$_{2.5}$ [$\mu g/m^3$]')
plt.ylim(0, None)
plt.legend(labels=["SORPES","Vaisala2a (before resample)","Vaisala2b (after resample)"])
plt.style.use('seaborn')

#%% Now, we will combine all data, SORPES1b, Vaisala1b and Vaisala1a
# We need to relabel the names of columns first

print(Vaisala1b.columns)
Vaisala1b.rename(columns={'P': 'Pv1', 'T': 'Tv1', 'CO': 'COv1', 'Health': 'Healthv1'
             , 'NO2': 'NO2v1', 'O3': 'O3v1', 'PM10': 'PM10v1'
             , 'PM25': 'PM25v1', 'RH': 'RHv1', 'SO2': 'SO2v1'
             , 'NN1': 'NN1v1', 'CO2': 'CO2v1', 'NO': 'NOv1'
             , 'NN2': 'NN2v1'},inplace=True)

print(Vaisala2b.columns)
Vaisala2b.rename(columns={'P': 'Pv2', 'T': 'Tv2', 'CO': 'COv2', 'Health': 'Healthv2'
             , 'NO2': 'NO2v2', 'O3': 'O3v2', 'PM10': 'PM10v2'
             , 'PM25': 'PM25v2', 'RH': 'RHv2', 'SO2': 'SO2v2'
             , 'NN1': 'NN1v2', 'CO2': 'CO2v2', 'NO': 'NOv2'
             , 'NN2': 'NN2v2'},inplace=True)

print(SORPES1b.columns)
SORPES1b.rename(columns={'O3 ppb': 'O3s', 'SO2 ppb': 'SO2s', 'CO ppm': 'COs', 'NO ppb': 'NOs'
             , 'NO2 ppb': 'NO2s', 'NOx ppb': 'NOxs', 'NOy ppb': 'NOys'
             , 'PM25': 'PM25v2', 'RH': 'RHv2', 'SO2': 'SO2v2'
             , 'PM2.5（μg/m3）': 'PM25s'},inplace=True)


from DataProcessing1 import VaisalaPreProcess

Vaisala3 = pd.read_csv('clean_vaisala_data2/P1910347.csv') #
Vaisala4 = pd.read_csv('clean_vaisala_data2/P1910345.csv') #
Vaisala5 = pd.read_csv('clean_vaisala_data2/P2150596.csv')  #
Vaisala3b=VaisalaPreProcess(Vaisala3,3)
Vaisala4b=VaisalaPreProcess(Vaisala4,4)
Vaisala5b=VaisalaPreProcess(Vaisala5,5)

# We concatanete the data:
#DATA2 = pd.concat([SORPES1b,Vaisala1b,Vaisala2b], join='inner', axis=1)
DATA2 = pd.concat([SORPES1b,Vaisala1b,Vaisala2b,Vaisala3b,Vaisala4b,Vaisala5b], join='inner', axis=1)


# See the columns, if they are merged:
for col in DATA2:
    print(col) 
    
cols_list = list(DATA2.columns)


# Summary and see if both data have similar or very different statistics:
SUMMARY = DATA2.describe()
print(SUMMARY['PM25s'])
print(SUMMARY['PM25v1'])
print(SUMMARY['PM25v2'])

#%% We know that PM2.5 sensors do not drift, 
# but they are simply do now work
# To check if trace gases encounter drift (a complete failure)

sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA2['COs'].plot(linewidth=0.5);
DATA2['COv1'].plot(linewidth=0.5);
DATA2['COv2'].plot(linewidth=0.5);
ax.set_title('CO sensors degradation')
ax.set_ylabel('CO [ppb]')
plt.ylim(0, None)
plt.legend(labels=["SORPES","Vaisala1","Vaisala2"])
plt.style.use('seaborn')

sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA2['COs'].plot(linewidth=0.5);
#DATA2['COv1'].plot(linewidth=0.5);
DATA2['COv2'].plot(linewidth=0.5);
ax.set_title('CO sensors degradation')
ax.set_ylabel('CO [ppb]')
plt.ylim(0, None)
#plt.legend(labels=["SORPES","Vaisala1","Vaisala2"])
plt.legend(labels=["SORPES","Vaisala2"])
plt.style.use('seaborn')

AE_CO = abs(DATA2['COs'] - DATA2['COv2'])
sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = AE_CO.plot(linewidth=0.5);
ax.set_title("Absolute Error between SORPES and Vaisala2")
ax.set_ylabel('Absolute Error CO [ppb]')
plt.ylim(0, None)
#plt.legend(labels=["Absolute Error between SORPES and Vaisala2"])
plt.style.use('seaborn') 


sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA2['PM25s'].plot(linewidth=0.5);
DATA2['PM25v1'].plot(linewidth=0.5);
DATA2['PM25v2'].plot(linewidth=0.5);
ax.set_title('PM$_{2.5}$ sensors faulty')
ax.set_ylabel('PM$_{2.5}$ [$\mu$g/m$^3$]')
plt.ylim(0, None)
plt.legend(labels=["SORPES","Vaisala1","Vaisala2"])
plt.style.use('seaborn')


sns.set(rc={'figure.figsize':(7, 7)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
plt.scatter(DATA2['PM25s'], DATA2['PM25v2'],  alpha=0.5)
plt.xlim([0, 300])
plt.ylim([0, 300])
plt.title('PM$_{2.5}$ sensor faulty')
plt.xlabel('PM$_{2.5}$ [$\mu$g/m$^3$] (SORPES)')
plt.ylabel('PM$_{2.5}$ [$\mu$g/m$^3$] (Vaisala2)')
plt.show()


sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA2['O3s'].plot(linewidth=0.5);
DATA2['O3v1'].plot(linewidth=0.5);
DATA2['O3v2'].plot(linewidth=0.5);
ax.set_title('O$_3$ sensors faulty')
ax.set_ylabel('O$_{3}$ [ppb]')
plt.ylim(0, None)
plt.legend(labels=["SORPES","Vaisala1","Vaisala2"])
plt.style.use('seaborn')

sns.set(rc={'figure.figsize':(7, 7)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
plt.scatter(DATA2['O3s'], DATA2['O3v2'],  alpha=0.5)
plt.xlim([0, 125])
plt.ylim([0, 125])
plt.title('O$_{3}$ faulty')
plt.xlabel('PM$_{2.5}$ [ppb] (SORPES)')
plt.ylabel('PM$_{2.5}$ [ppb] (Vaisala2)')
plt.show()

sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA2['NOs'].plot(linewidth=0.5);
DATA2['NOv1'].plot(linewidth=0.5);
DATA2['NOv2'].plot(linewidth=0.5);
ax.set_title('NO sensors drifting')
ax.set_ylabel('NO [ppb]')
plt.ylim(0, None)
plt.legend(labels=["SORPES","Vaisala1","Vaisala2"])
plt.style.use('seaborn')

sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA2['NO2s'].plot(linewidth=0.5);
DATA2['NO2v1'].plot(linewidth=0.5);
DATA2['NO2v2'].plot(linewidth=0.5);
ax.set_title('NO$_2$ sensors faulty')
ax.set_ylabel('NO$_{2}$ [ppb]')
plt.ylim(0, None)
plt.legend(labels=["SORPES","Vaisala1","Vaisala2"])
plt.style.use('seaborn')

sns.set(rc={'figure.figsize':(7, 7)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
plt.scatter(DATA2['NO2s'], DATA2['NO2v2'],  alpha=0.5)
plt.xlim([0, 50])
plt.ylim([0, 50])
plt.title('NO$_{2}$ faulty')
plt.xlabel('NO$_{2}$ [ppb] (SORPES)')
plt.ylabel('NO$_{2}$ [ppb] (Vaisala2)')
plt.show()

sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA2['SO2s'].plot(linewidth=0.5);
DATA2['SO2v1'].plot(linewidth=0.5);
#DATA2['SO2v2'].plot(linewidth=0.5);
ax.set_title('SO$_2$ sensors drifting')
ax.set_ylabel('SO$_{2}$ [ppb]')
plt.ylim(0, None)
plt.legend(labels=["SORPES","Vaisala1","Vaisala2"])
plt.style.use('seaborn')



#%%
mask0a = (SORPES1a.index > '2019-4-1') & (SORPES1a.index <= '2019-7-1')
mask1a = (Vaisala1a.index > '2019-4-1') & (Vaisala1a.index <= '2019-7-1')
mask2a = (Vaisala2a.index > '2019-4-1') & (Vaisala2a.index <= '2019-7-1')


# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = SORPES1a['NO2 ppb'][mask0a].plot(linewidth=0.5)
Vaisala1a['NO2'][mask1a].plot(linewidth=0.5);
Vaisala2a['NO'][mask2a].plot(linewidth=0.5);
ax.set_title('Only between 1 Apr until 1 Jun 2019')
ax.set_ylabel('NO$_{2}$ [ppb]')
plt.legend(labels=["SORPES","Vaisala1","Vaisala2"])
plt.style.use('seaborn')



#%% Consistency Test: Meteorological variables
# We need to:
    # Clean the code and make more functions for cleaning
    # Scatter plot covers entire Vaisala sensors



# Scatter plots

f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True)
ax1.scatter(DATA2['Tv1'], DATA2['Tv2'])
ax1.set_title('Temperature')
ax1.set_xlim(-10, 50)
ax1.set_ylim(-10, 50)
ax1.set_xlabel('Vaisala 1: Temp [C] ')
ax1.set_ylabel('Vaisala 2: Temp [C] ')
ax2.scatter(DATA2['RHv1'], DATA2['RHv2'])
ax2.set_title('Relative Humidity')
ax2.set_xlim(50, 100)
ax2.set_ylim(50, 100)
ax2.set_xlabel('Vaisala 1: RH [%] ')
ax2.set_ylabel('Vaisala 2: RH [%] ')
ax3.scatter(DATA2['Pv1'], DATA2['Pv2'])
ax3.set_title('Pressure')
ax3.set_xlim(950, 1050)
ax3.set_ylim(950, 1050)
ax3.set_xlabel('Vaisala 1: P [mbar] ')
ax3.set_ylabel('Vaisala 2: P [mbar] ')

#%% Consistency Test: Time-Series plots

#figure, axes = plt.subplots(1, 2)
#df1.plot(ax=axes[0])
#df2.plot(ax=axes[1])

f, (ax1, ax2, ax3) = plt.subplots(3, 1, sharey=True)
#sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.0, rc={'text.usetex' : False})

ax1 = plt.subplot(311)
#DATA2['Ts'].plot(ax=ax1,linewidth=0.5);
DATA2['Tv1'].plot(ax=ax1,linewidth=0.5);
DATA2['Tv2'].plot(ax=ax1,linewidth=0.5);
DATA2['Tv3'].plot(ax=ax1,linewidth=0.5);
DATA2['Tv4'].plot(ax=ax1,linewidth=0.5);
DATA2['Tv5'].plot(ax=ax1,linewidth=0.5);
#ax1.set_title('Time-series data: Temperature')
ax1.set_ylabel('Temp [$^{\circ}$C]')
ax1.legend(labels=["Vaisala1","Vaisala2","Vaisala3","Vaisala4","Vaisala5"])
ax1.set_ylim([-10, 50])
#plt.style.use('seaborn')

ax2 = plt.subplot(312)
#sns.set(font_scale=1.0, rc={'text.usetex' : False})
#DATA2['RHs'].plot(ax=ax1,linewidth=0.5);
DATA2['RHv1'].plot(ax=ax2,linewidth=0.5);
DATA2['RHv2'].plot(ax=ax2,linewidth=0.5);
DATA2['RHv3'].plot(ax=ax2,linewidth=0.5);
DATA2['RHv4'].plot(ax=ax2,linewidth=0.5);
DATA2['RHv5'].plot(ax=ax2,linewidth=0.5);
#ax2.set_title('Time-series data: Relative Humidity')
ax2.set_ylabel('RH [%]')
ax2.legend(labels=["Vaisala1","Vaisala2","Vaisala3","Vaisala4","Vaisala5"])
ax2.set_ylim([10, 100])
#plt.style.use('seaborn')

ax3 = plt.subplot(313)
#sns.set(font_scale=1.0, rc={'text.usetex' : False})
#DATA2['RHs'].plot(ax=ax1,linewidth=0.5);
DATA2['Pv1'].plot(ax=ax3,linewidth=0.5);
DATA2['Pv2'].plot(ax=ax3,linewidth=0.5);
DATA2['Pv3'].plot(ax=ax3,linewidth=0.5);
DATA2['Pv4'].plot(ax=ax3,linewidth=0.5);
DATA2['Pv5'].plot(ax=ax3,linewidth=0.5);
#ax3.set_title('Time-series data: Pressure')
ax3.set_ylabel('P [mbar]')
ax3.legend(labels=["Vaisala1","Vaisala2","Vaisala3","Vaisala4","Vaisala5"])
ax3.set_ylim([950, 1050])
plt.style.use('seaborn')





#%%

# PM2.5 Scatter plot
plt.scatter(DATA2['PM2.5（μg/m3）'],DATA2['PM25'],label='PM2.5')
plt.legend(loc='best', fontsize=16)
plt.xlabel('PM2.5 (SORPES)')
plt.ylabel('PM2.5 (Vaisala)')
plt.title('PM2.5: SORPES vs Vaisala')
plt.show()





# Create four polar axes and access them through the returned array
fig, axs = plt.subplots(2, 2, subplot_kw=dict(projection="polar"))
axs[0, 0].plot(x, y)
axs[1, 1].scatter(x, y)



#%% Data Visualization (time-series)


#%%

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

#%% To plot only good Vaisala data

idx = DATA2['PM25']>20
DATA3=DATA2[idx]

# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = DATA3['PM2.5（μg/m3）'].plot(linewidth=0.5);
DATA3['PM25'].plot(linewidth=0.5);
ax.set_title('SORPES vs Vaisala: PM$_{2.5}$ below 10 $\mu g/m^3$')
ax.set_ylabel('PM$_{2.5}$ [$\mu g/m^3$]')
plt.style.use('seaborn')

# PM2.5 Scatter plot
plt.scatter(DATA3['PM2.5（μg/m3）'],DATA3['PM25'],label='PM2.5')
plt.legend(loc='best', fontsize=16)
plt.xlabel('PM2.5 (SORPES)')
plt.ylabel('PM2.5 (Vaisala)')
plt.title('SORPES vs Vaisala: PM$_{2.5}$ below 10 $\mu g/m^3$')
plt.show()


#%% PM2.5 Scatter plot

mask1a = (Vaisala1a.index > '2019-4-1') & (Vaisala1a.index <= '2019-7-1')
mask2a = (Vaisala2a.index > '2019-4-1') & (Vaisala2a.index <= '2019-7-1')


# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})
sns.set(font_scale=1.5, rc={'text.usetex' : False})
ax = Vaisala1a['PM25'][mask1a].plot(linewidth=0.5);
Vaisala2a['PM25'][mask2a].plot(linewidth=0.5);
ax.set_title('Only between 1 Apr until 1 Jun 2019')
ax.set_ylabel('PM$_{2.5}$ [$\mu g/m^3$]')
plt.style.use('seaborn')

