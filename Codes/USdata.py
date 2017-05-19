from MLE import *
data_path = '../Data/US/'
output = '../Paper/Result/ModelResult/'

# M4/ M5(named as M4 full)
N = number_banks  = 35
file_name = data_path+"df1ema.csv"
dat = pd.read_csv(file_name)
year = dat['DATE']
dat = dat.iloc[:,2:]
y=dat.iloc[1:,0]
y=y.reset_index(drop=True)
x0=dat.iloc[:-1,0]
x0=x0.reset_index(drop=True)
y_act = np.insert(np.array(y),0,x0[0])
exog = dat.iloc[:-1,0:]
exog = exog.reset_index(drop=True)
exog = exog[['DICS', 'NPL_positive', 'NPL_negative',"CPI", 'EBP', 'DILD',
       'VIX',"unemp_positive","SPF CPI","NASDAQ"]]
add_con(exog)



qmle = QMLE(y, x0,exog,N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
label_names = ['v'] + list(exog)
M1 = result_M1.summary(xname=label_names,title='M1')
result_params = result_M1.params

x_t_pred = predict2(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/USDICS M4 plot.csv',index=False)
write_latex(M1,output,'M5.tex','QMLE M4')

#forward
qmle = QMLE(y.iloc[:70], x0.iloc[:70],exog.iloc[:70,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x_t_pred = predict2(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/USDICS M4 first 70 plot.csv',index=False)

# back
## back
qmle = QMLE(y.iloc[40:], x0.iloc[40:],exog.iloc[40:,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x0_1 =x0.iloc[40:].reset_index(drop=True)
exog_1 = exog.iloc[40:,].reset_index(drop=True)

x_t_pred1 = predict2(x0=x0_1,exog=exog_1,params=result_params,Num_bank=N,repeat=20)

x0_back =x0.iloc[40::-1]
x0_back.reset_index(drop=True,inplace=True)

exog_back=exog.iloc[40::-1,]
exog_back.reset_index(drop=True,inplace=True)

x_t_pred0 = predict2(x0=x0_back,exog=exog_back,params=result_params,Num_bank=N,repeat=20)

x_t_pred0=pd.DataFrame(x_t_pred0)
x_t_pred0=x_t_pred0[1:-1]
x_t_pred0 = x_t_pred0[::-1]
x_t_pred = pd.concat([x_t_pred0,pd.DataFrame(x_t_pred1)],ignore_index=True)

df = {"DATE":year,"DICS Actual":pd.Series(y_act),"DICS M4 Predicted":x_t_pred}
out=pd.concat(df,axis=1)
out.to_csv('./img/USDICS M4 last 65 plot.csv',index=False)










###################################################

from MLE import *
data_path = '../Data/US/'
output = '../Paper/Result/ModelResult/'

# M4/ M5(named as M4 full)
N = number_banks  = 35
file_name = data_path+"df1ema.csv"
dat = pd.read_csv(file_name)
year = dat['DATE']
dat = dat.iloc[:,2:]
y=dat.iloc[1:,0]
y=y.reset_index(drop=True)
x0=dat.iloc[:-1,0]
x0=x0.reset_index(drop=True)
y_act = np.insert(np.array(y),0,x0[0])
exog = dat.iloc[:-1,0:]
exog = exog.reset_index(drop=True)
add_con(exog)


#forward
qmle = QMLE(y.iloc[:70], x0.iloc[:70],exog.iloc[:70,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x_t_pred = predict2(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/USDICS M5 first 70 plot.csv',index=False)

# back
## back
qmle = QMLE(y.iloc[19:], x0.iloc[19:],exog.iloc[19:,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x0_1 =x0.iloc[19:].reset_index(drop=True)
exog_1 = exog.iloc[19:,].reset_index(drop=True)

x_t_pred1 = predict(x0=x0_1,exog=exog_1,params=result_params,Num_bank=N,repeat=20)

x0_back =x0.iloc[19::-1]
x0_back.reset_index(drop=True,inplace=True)

exog_back=exog.iloc[19::-1,]
exog_back.reset_index(drop=True,inplace=True)

x_t_pred0 = predict(x0=x0_back,exog=exog_back,params=result_params,Num_bank=N,repeat=20)

x_t_pred0=pd.DataFrame(x_t_pred0)
x_t_pred0=x_t_pred0[1:-1]
x_t_pred0 = x_t_pred0[::-1]
x_t_pred = pd.concat([x_t_pred0,pd.DataFrame(x_t_pred1)],ignore_index=True)

df = {"DATE":year,"DICS Actual":pd.DataFrame(y_act),"DICS M4 Predicted":x_t_pred}
out=pd.concat(df,axis=1)
out.to_csv('./img/USDICS M5 last 65 plot.csv',index=False)

