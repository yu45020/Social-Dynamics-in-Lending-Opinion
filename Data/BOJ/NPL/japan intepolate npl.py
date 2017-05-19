import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as sm

npl = pd.read_excel('../Data/BOJ/NPL/japan npl.xlsx',index_col='Year')
"""
npl_ratio = special attention / total credit 
special attention: sum of loans whose interest/principal payments are unpaid by more than 3 months
"Non-Performing Loan Reduction with Regulatory Transition A Japanese Experience, 1998–2013" P19
"""
npl['npl'] = (npl['Special Attention']+npl['Doubtful '])/npl['Total Credit']
series = pd.Series(npl['npl'])
series = series.resample('3MS').asfreq()
a=series.interpolate(method='spline',order=3,s=0)
plt.plot(a)
plt.plot(npl['npl'],color='red')
#a.to_csv('../Data/BOJ/NPL/japan npl.csv')

#bankcrupt
npl['bankcrupt'] = (npl['Bankrupt or De facto Bankrupt (100million yen)'])/npl['Total Credit']
series = pd.Series(npl['bankcrupt'])
series = series.resample('3MS').asfreq()
a=series.interpolate(method='spline',order=3,s=0)
plt.plot(a)
plt.plot(npl['bankcrupt'],color='red')
#a.to_csv('../Data/BOJ/NPL/japan bankcrupt.csv')


##### examples on japan unemployment data
unemp = pd.read_csv('../Data/BOJ/NPL/jp unemp se-an.csv',index_col=0)
unemp.index = pd.to_datetime(unemp.index)
unemp = unemp.resample('QS').asfreq()
unemp_int = unemp.interpolate(method='spline',order=3,s=0)
unemp_int.to_csv('unemp impute.csv')
plt.plot(unemp_int)
unemp_m = pd.read_csv('../Data/BOJ/NPL/jp unemp q.csv',index_col=0)
unemp_m.index = pd.to_datetime(unemp_m.index)
plt.plot(unemp_m,color='black')
df = pd.concat([unemp_m,unemp_int],axis=1)
df.columns = ['y',"x"]
result  = sm.ols(formula="y ~ x", data=df).fit()
result.params
result.summary()
result

##### GDP

unemp = pd.read_csv('../Data/BOJ/NPL/jp gdp se-an.csv',index_col=0)
unemp.index = pd.to_datetime(unemp.index)
unemp = unemp.resample('QS').asfreq()
unemp_int = unemp.interpolate(method='spline',order=3,s=0)
unemp_int.to_csv('GDP impute.csv')
plt.plot(unemp_int)
unemp_m = pd.read_csv('../Data/BOJ/NPL/jp gdp q.csv',index_col=0)
unemp_m.index = pd.to_datetime(unemp_m.index)

plt.plot(unemp_m,color='black')
df = pd.concat([unemp_m,unemp_int],axis=1)
df.columns = ['y',"x"]
result  = sm.ols(formula="y ~ x", data=df).fit()
result.params
result.summary()

