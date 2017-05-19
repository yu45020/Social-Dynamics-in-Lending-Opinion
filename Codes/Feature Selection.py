# Use recursive feature selection with cross validation on random forest
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import  RFE
from MLE import *

## boruta

from boruta import BorutaPy
import pandas as pd
import numpy as np

test_result=[]
sample_result=[]
df = pd.read_csv('../Data/US/df1ema.csv')
df = df.iloc[:, 2:]
y = df.iloc[1:, 0].values
exog = df.iloc[:-1, 0:]
#exog.drop('ebp', axis=1, inplace=True)
#exog.drop('VIXCLS_CHG', axis=1, inplace=True)

names = list(exog)
#exog = sklearn.preprocessing.scale(exog,with_mean=True, with_std=False)
#exog = pd.DataFrame(exog)
strong =pd.DataFrame(names)
weak = pd.DataFrame(names)
for t in range(20):
    sample = np.random.randint(0, 100, 30)
    y_test = y[sample]
    y_train = np.delete(y, sample)

    exog_test = exog.iloc[sample, :]
    exog_train = exog.drop(sample)
    exog_train = exog_train.values

    rf = RandomForestRegressor(n_estimators=1000, criterion='mse', bootstrap=True, n_jobs=-1,
                               oob_score=True)
    feature_selection = BorutaPy(rf, n_estimators='auto', random_state=1,two_step=True,perc=90)
    feature_selection.fit(exog_train, y_train)

    df_imp = pd.DataFrame(np.array(feature_selection.support_,dtype=int))
    df_wek = pd.DataFrame(np.array(feature_selection.support_weak_,dtype=int))
    strong = pd.concat([strong, df_imp], axis=1)
    weak = pd.concat([weak,df_wek],axis=1)

    exog_test = exog_test.values
    transform = feature_selection.transform(exog_test)
    rf.fit(transform, y_test)
    test_result.append(rf.oob_score_)

rec_strong = pd.DataFrame(np.sum(strong.iloc[:,1:],axis=1))
rec_weak = pd.DataFrame(np.sum(weak.iloc[:,1:],axis=1))
dd=pd.concat([strong.iloc[:,0],rec_strong,rec_weak],axis=1)
dd.columns=['Var','Strong','Weak']
dd = dd.sort_values( 'Strong',axis=0, ascending=False)
dd.to_csv('US 30 relavant.csv')




############################################################
# ECB

from boruta import BorutaPy
import pandas as pd
import numpy as np

test_result=[]
sample_result=[]
df = pd.read_csv('../Data/ECB/ECB dataset completed.csv')
df = df.iloc[:, 1:]
y = df.iloc[1:, 0].values
exog = df.iloc[:-1, 0:]
exog.reset_index(drop=True,inplace=True)

names = list(df)
exog = pd.DataFrame(exog)
strong =pd.DataFrame(names)
weak = pd.DataFrame(names)
for t in range(20):
    sample = np.random.randint(0, exog.shape[0],10)
    y_test = y[sample]
    y_train = np.delete(y, sample)

    exog_test = exog.iloc[sample, :]
    exog_train = exog.drop(sample)
    exog_train = exog_train.values

    rf = RandomForestRegressor(n_estimators=1000, criterion='mse', bootstrap=True, n_jobs=-1, oob_score=True)
    feature_selection = BorutaPy(rf, n_estimators='auto', two_step=True,perc=90)
    feature_selection.fit(exog_train, y_train)

    df_imp = pd.DataFrame(np.array(feature_selection.support_,dtype=int))
    df_wek = pd.DataFrame(np.array(feature_selection.support_weak_,dtype=int))
    strong = pd.concat([strong, df_imp], axis=1)
    weak = pd.concat([weak,df_wek],axis=1)

    exog_test = exog_test.values
    transform = feature_selection.transform(exog_test)
    rf.fit(transform, y_test)
    test_result.append(rf.oob_score_)

rec_strong = pd.DataFrame(np.sum(strong.iloc[:,1:],axis=1))
rec_weak = pd.DataFrame(np.sum(weak.iloc[:,1:],axis=1))
dd=pd.concat([strong.iloc[:,0],rec_strong,rec_weak],axis=1)
dd.columns=['Var','Important','Weak']
dd[['Var']] = names
dd = dd.sort_values( 'Important',axis=0, ascending=False)
dd.to_csv('JOB variable selection.csv')

## transform
id = np.array(dd.index[dd.iloc[:,1]>10],dtype=int)
exog.iloc[:,id].columns
transformed = exog.iloc[:,id]




##################### JAP


from boruta import BorutaPy
import pandas as pd
import numpy as np

test_result=[]
sample_result=[]
df = pd.read_csv('../Data/BOJ/BOJ complete.csv')
df = df.iloc[:, 1:]
y = df.iloc[1:, 0].values
exog = df.iloc[:-1, 0:]
exog.reset_index(drop=True,inplace=True)

names = list(df)
exog = pd.DataFrame(exog)
strong =pd.DataFrame(names)
weak = pd.DataFrame(names)
for t in range(20):
    sample = np.random.randint(0, exog.shape[0],10)
    y_test = y[sample].copy()
    y_train = np.delete(y, sample)

    exog_test = exog.iloc[sample, :]
    exog_train = exog.drop(sample)
    exog_train = exog_train.values

    rf = RandomForestRegressor(n_estimators=1000, criterion='mse', bootstrap=True, n_jobs=-1, oob_score=True)
    feature_selection = BorutaPy(rf, n_estimators='auto', two_step=True,perc=90)
    feature_selection.fit(exog_train, y_train)

    df_imp = pd.DataFrame(np.array(feature_selection.support_,dtype=int))
    df_wek = pd.DataFrame(np.array(feature_selection.support_weak_,dtype=int))
    strong = pd.concat([strong, df_imp], axis=1)
    weak = pd.concat([weak,df_wek],axis=1)

    exog_test = exog_test.values
    transform = feature_selection.transform(exog_test)
    rf.fit(transform, y_test)
    test_result.append(rf.oob_score_)

rec_strong = pd.DataFrame(np.sum(strong.iloc[:,1:],axis=1))
rec_weak = pd.DataFrame(np.sum(weak.iloc[:,1:],axis=1))
dd=pd.concat([strong.iloc[:,0],rec_strong,rec_weak],axis=1)
dd.columns=['Var','Strong','Weak']
dd[['Var']] = names
dd = dd.sort_values( 'Strong',axis=0, ascending=False)
dd.to_csv('Jap variable selection V2.csv')

## transform
id = np.array(dd.index[dd.iloc[:,1]>10],dtype=int)
exog.iloc[:,id].columns
transformed = exog.iloc[:,id]

