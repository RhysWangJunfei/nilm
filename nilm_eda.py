import pandas as pd
from pandas import DataFrame as df
import matplotlib.pyplot as plt
from datetime import datetime
import eda_process
import seaborn as sns
import numpy as np

base_dir='D://canada//uwo//project//dataset//'

#DWE_data = pd.read_csv(base_dir+'Electricity_DWE.csv')
#print(DWE_data.head())


#Read cloth dryer data
DWE_data = pd.read_csv(base_dir+'Electricity_DWE.csv')[['unix_ts','P']]

DWE_data['datetime'] = pd.to_datetime(DWE_data['unix_ts'],unit='s')
DWE_data = DWE_data.drop(['unix_ts'],axis=1)
#DWE_data.set_index('Date/Time')
weather = eda_process.get_upsampled_weather()
result = pd.merge(DWE_data, weather, how='inner', left_on='datetime', right_on='Date/Time')
result = result.dropna(axis=0,how='any')
plt.scatter(result['Temp (C)'],result['P'])
plt.show()

DWE_data['P'].plot()
plt.show()

DWE_greater = DWE_data.loc[(DWE_data['P']>0),]
sns.distplot(DWE_greater['P'])
plt.title('DWE power consumption distribution')
plt.show()


'''
result.groupby('Weather')['P'].mean().plot(kind='bar')
plt.tight_layout()
plt.ylabel('power/minute')
plt.title('DWE mean per minute by Weather')
plt.show()
'''
plt.scatter(result['Rel Hum (%)'],result['P'])
plt.show()


DWE_data['month'] = DWE_data['datetime'].dt.month
DWE_data['hour'] = DWE_data['datetime'].dt.hour
DWE_data['weekday'] = DWE_data['datetime'].dt.dayofweek
DWE_data['quarter'] = DWE_data['datetime'].dt.quarter

DWE_data.groupby('month')['P'].mean().plot(kind='bar')
plt.xlabel('Month')
plt.ylabel('power/minute')
plt.title('DWE mean per minute by Month')
plt.show()

DWE_data.groupby('quarter')['P'].mean().plot(kind='pie',labels=['Q1','Q2','Q3','Q4'],autopct='%1.0f%%',\
                                              shadow=True,explode=(0.05, 0.05, 0.05, 0.05))
plt.title('Quarterly Power Consumption Comparison')
centre_circle = plt.Circle((0,0),0.75,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.tight_layout()
plt.show()

DWE_data.groupby('hour')['P'].mean().plot(kind='bar')#DWE_data.groupby('quarter')['P'].mean().plot(kind='pie',labels=['Q1','Q2','Q3','Q4'],autopct='%1.0f%%')
plt.title('DWE mean per minute by Hour')
plt.show()
ax = DWE_data.groupby('weekday')['P'].mean().plot(kind='bar')
ax.set_xticklabels(['Mon','Tue','Wed','Thur','Fri','Sat','Sun'],rotation=0)
plt.title('DWE mean per minute by weekday')
plt.show()
#https://machinelearningmastery.com/basic-feature-engineering-time-series-data-python/
#https://www.analyticsvidhya.com/blog/2016/01/guide-data-exploration/#one
