from MLE import *
data_path = '../Data/BOJ/'
output = '../Paper/Result/ModelResult/JP/'


#peer only

N = number_banks  = 25
file_name = data_path+"BOJ data.csv"
dat = pd.read_csv(file_name)
year = dat['Year']
dat = dat.iloc[:,1]
y=dat.iloc[1:]
y=y.reset_index(drop=True)
x0=dat.iloc[:-1]
x0=x0.reset_index(drop=True)
y_act = np.insert(np.array(y),0,x0[0])
exog = pd.DataFrame(dat.iloc[:-1])
exog = exog.reset_index(drop=True)
add_con(exog)

qmle = QMLE(y, x0,exog,N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
label_names = ['v'] + list(exog)
M1 = result_M1.summary(xname=label_names,title='M1')
result_params = result_M1.params

x_t_pred = predict(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/BOJ M1 plot.csv',index=False)
write_latex(M1,output,'BOJ M1.tex','QMLE BOJ M1')




# M2/ M3(named as M4 full)
N = number_banks  = 26
file_name = data_path+"BOJ complete.csv"
dat = pd.read_csv(file_name)
year = dat['Year']
dat = dat.iloc[:,1:]
y=dat.iloc[1:,0]
y=y.reset_index(drop=True)
x0=dat.iloc[:-1,0]
x0=x0.reset_index(drop=True)
y_act = np.insert(np.array(y),0,x0[0])
exog = dat.iloc[:-1,0:]
exog = exog.reset_index(drop=True)
exog = exog[['DICS', 'VJX',"Business Forecast ", 'NPL negative',"NPL positive","Bankrupt positive","Bankrupt negative",
             "DIHRLD",
             "Nikkei"]]
#"NPL positive", Nikkei
add_con(exog)

exog = exog[['DICS', 'VJX',"Business Forecast ", 'Nikkei',"RGDP_lag2 negative",
             "DIHRLD"]]


qmle = QMLE(y, x0,exog,N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12,maxiter=1000)
label_names = ['v'] + list(exog)
M1 = result_M1.summary(xname=label_names,title='M1')
result_params = result_M1.params

x_t_pred = predict2(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=40)
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/BOJ M2 no badloans plot.csv',index=False)
write_latex(M1,output,'BOJM4.tex','QMLE BOJ M4')

#forward
qmle = QMLE(y.iloc[:40], x0.iloc[:40],exog.iloc[:40,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12,maxiter=1000)
result_params = result_M1.params
x_t_pred = predict2(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=40)
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/BOJ M2 first 70 plot.csv',index=False)

# back
## back
qmle = QMLE(y.iloc[10:], x0.iloc[10:],exog.iloc[10:,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-8,maxiter=1000)
result_params = result_M1.params
x0_1 =x0.iloc[10:].reset_index(drop=True)
exog_1 = exog.iloc[10:,].reset_index(drop=True)

x_t_pred1 = predict2(x0=x0_1,exog=exog_1,params=result_params,Num_bank=N,repeat=20)

x0_back =x0.iloc[10::-1]
x0_back.reset_index(drop=True,inplace=True)

exog_back=exog.iloc[10::-1,]
exog_back.reset_index(drop=True,inplace=True)

x_t_pred0 = predict2(x0=x0_back,exog=exog_back,params=result_params,Num_bank=N,repeat=20)

x_t_pred0=pd.DataFrame(x_t_pred0)
x_t_pred0=x_t_pred0[1:-1]
x_t_pred0 = x_t_pred0[::-1]
x_t_pred = pd.concat([x_t_pred0,pd.DataFrame(x_t_pred1)],ignore_index=True)

df = {"DATE":year,"DICS Actual":pd.Series(y_act),"DICS M4 Predicted":x_t_pred}
out=pd.concat(df,axis=1)
out.to_csv('./img/BOJ M last 65 plot.csv',index=False)









