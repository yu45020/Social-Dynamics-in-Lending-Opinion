from sklearn.utils import shuffle
from MLE import *
def param_list(sample_points, y, x0, exog, random=False):
    LIST = []
    dataframe = pd.concat([y, x0, exog], axis=1)
    #np.random.seed(1)
    for pts in sample_points:
        if random:
            if pts>dataframe.shape[0]:
                bootst = True
            else:
                bootst=False
            df = shuffle(dataframe)
            df = df.reset_index(drop=True)
            df_sample = df.sample(n=pts,replace=bootst)
            df_sample = df_sample.reset_index(drop=True)
            y_1, x0_1, exog_1 = df_sample.iloc[:, 0], df_sample.iloc[:, 1], df_sample.iloc[:, 2:]
        else:
            y_1, x0_1, exog_1 = y.iloc[:pts, ], x0.iloc[:pts, ], exog.iloc[:pts, ]

        qmle = QMLE(y_1, x0_1, exog_1, N=N)
        result_M1 = qmle.fit(method='ncg',avextol=1e-12, cost_fn=None)
        p = result_M1.params
        LIST.append(np.insert(p, obj=0, values=pts))
    LIST = pd.DataFrame(LIST)
    if random:
        par_names = list(exog)
        LIST.columns = ['Pts', 'v_ran'] + [y+'_ran' for y in par_names]
    else:
        LIST.columns = ['Pts', 'v'] + list(exog)
    return LIST



data_path = '../Data/US/'
output = '../Paper/Result/ModelResult/'
N = number_banks  = 35
file_name = data_path+"DRISCFLM.csv"
dat = pd.read_csv(file_name)
dat.columns = ["DATE","DICSxt0"]
year = dat['DATE']
dat['DICSxt0'] = -dat['DICSxt0']/100
dat['DICSxt1'] = dat['DICSxt0'].shift(-1)

df = dat.dropna().copy()
df['DICSxt0+'] = [df if df>0 else 0 for df in df['DICSxt0']]
df['DICSxt0-'] = [df if df<0 else 0 for df in df['DICSxt0']]
y=df['DICSxt1']
x0=df['DICSxt0']
exog = pd.concat([df['DICSxt0+'],df['DICSxt0-']],axis=1)
add_con(exog)

# forward & backward predictions

qmle = QMLE(y.iloc[:70], x0.iloc[:70],exog.iloc[:70,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x_t_pred = predict(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
y_act = np.insert(np.array(y),0,x0[0])
df = {"DATE":year,"DICS Actual":y_act,"DICS M2 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/USDICS M2 first 70 plot.csv',index=False)

## back
qmle = QMLE(y.iloc[40:], x0.iloc[40:],exog.iloc[40:,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x0_1 =x0.iloc[40:].reset_index(drop=True)
exog_1 = exog.iloc[40:,].reset_index(drop=True)

x_t_pred1 = predict(x0=x0_1,exog=exog_1,params=result_params,Num_bank=N,repeat=20)

x0_back =x0.iloc[40::-1]
x0_back.reset_index(drop=True,inplace=True)

exog_back=exog.iloc[40::-1,]
exog_back.reset_index(drop=True,inplace=True)

x_t_pred0 = predict(x0=x0_back,exog=exog_back,params=result_params,Num_bank=N,repeat=20)

x_t_pred0=pd.DataFrame(x_t_pred0)
x_t_pred0 = x_t_pred0.iloc[::-1]
x_t_pred0=x_t_pred0[1:]

x_t_pred = pd.concat([x_t_pred0,pd.DataFrame(x_t_pred1)],ignore_index=True)

y_act = np.insert(np.array(y),0,x0[0])
df = {"DATE":year,"DICS Actual":pd.DataFrame(y_act),"DICS M2 Predicted":x_t_pred}
out=pd.concat(df,axis=1)
out.to_csv('./img/USDICS M2 last 65 plot.csv',index=False)



# coefficient over time
sample_points = np.arange(start=15,stop=exog.shape[0],step=5)
US_param = param_list(sample_points, y, x0, exog, random=False)

sample_points = np.arange(start=15,stop=200,step=5)
US_param_random =param_list(sample_points, y, x0, exog, random=True)

result_df = pd.DataFrame(US_param['Pts'])
for i in range(1,US_param.shape[1]):
    result_df=pd.concat([result_df, pd.DataFrame(US_param.iloc[:, i])], axis=1)
    result_df=pd.concat([result_df, pd.DataFrame(US_param_random.iloc[:, i])], axis=1)
#result_df.to_csv('./img/US DICS M2 stability check.csv',index=False)


dff = {'points':sample_points,'order':US_param.iloc[:,3],'random': US_param_random.iloc[:,3]}
df = pd.DataFrame(dff)
df = pd.melt(df,id_vars='points',var_name='US.DICSxt0')
ggplot(aes(x='points',y='value',colour='US.DICSxt0'),data=df)+ geom_point()+geom_line()
US_df = US_param.copy()
posi=2
for i in range(1,4):
    US_df.insert(posi,list(US_param_random)[i],US_param_random.iloc[:,i])
    posi +=2

US_df.to_csv('US DICS Beta Compare.csv')
