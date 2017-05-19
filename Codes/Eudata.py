from MLE import *
data_path = '../Data/ECB/'
output = '../Paper/Result/ModelResult/ECB/'

# EU
#M1
N = number_banks  = 70
file_name = data_path+"ECB DI Margin Average.csv"
dat = pd.read_csv(file_name)
year = dat['Year']
dat = dat.iloc[:,2:]
dat.columns=["ECB DICS"]
y=dat.iloc[1:,0]
y=y.reset_index(drop=True)
x0=dat.iloc[:-1,0]
x0=x0.reset_index(drop=True)
exog = pd.DataFrame(x0)
exog = exog.reset_index(drop=True)
add_con(exog)

qmle = QMLE(y, x0,exog,N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
label_names = ['v'] + list(exog)
M1 = result_M1.summary(xname=label_names,title='M1')
result_params = result_M1.params

x_t_pred = predict(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
y_act = np.insert(np.array(y),0,x0[0])
df = {"DATE":year,"DICS Actual":y_act,"DICS M1 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/ECBDICS M1 plot.csv',index=False)
write_latex(M1,output,'M1.tex','QMLE M1')



exog['ECB DICSx0+'] = [df if df>0 else 0 for df in exog['ECB DICS']]
exog['ECB DICSx0-'] = [df if df<0 else 0 for df in exog['ECB DICS']]
del exog['ECB DICS']
qmle = QMLE(y, x0,exog,N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
label_names = ['v'] + list(exog)
M1 = result_M1.summary(xname=label_names,title='M2')
result_params = result_M1.params

x_t_pred = predict(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
df = {"DATE":year,"DICS Actual":y_act,"DICS M2 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/ECBDICS M2 plot.csv',index=False)
write_latex(M1,output,'M2.tex','QMLE M2')


############### not run
# M4
N = number_banks  = 70
file_name = data_path+"df1ema.csv"
dat = pd.read_csv(file_name)
year = dat['DATE']
dat = dat.iloc[:,2:]
y=dat.iloc[1:,0]
y=y.reset_index(drop=True)
x0=dat.iloc[:-1,0]
x0=x0.reset_index(drop=True)
exog = dat.iloc[:-1,0:]
exog = exog.reset_index(drop=True)
exog = exog[['DICS','DILD','VIXCLS_CHG','unemp_negative','NPL_positive','NPL_negative','ebp']]
add_con(exog)



qmle = QMLE(y, x0,exog,N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
label_names = ['v'] + list(exog)
M1 = result_M1.summary(xname=label_names,title='M1')
result_params = result_M1.params

x_t_pred = predict(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
y_act = np.insert(np.array(y),0,x0[0])
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/USDICS M4 plot.csv',index=False)
#write_latex(M1,output,'M4.tex','QMLE M4')

#forward
qmle = QMLE(y.iloc[:70], x0.iloc[:70],exog.iloc[:70,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x_t_pred = predict(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
y_act = np.insert(np.array(y),0,x0[0])
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Full Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/USDICS M4 full first 70 plot.csv',index=False)

# back
## back
qmle = QMLE(y.iloc[40:], x0.iloc[40:],exog.iloc[40:,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x0_1 =x0.iloc[40:].reset_index(drop=True)
exog_1 = exog.iloc[40:,].reset_index(drop=True)

x_t_pred1 = predict(x0=x0_1,exog=exog_1,params=result_params,Num_bank=N,repeat=20)

x0_back =x0.iloc[39::-1]
x0_back.reset_index(drop=True,inplace=True)

exog_back=exog.iloc[39::-1,]
exog_back.reset_index(drop=True,inplace=True)

x_t_pred0 = predict(x0=x0_back,exog=exog_back,params=result_params,Num_bank=N,repeat=20)

x_t_pred0=pd.DataFrame(x_t_pred0)
x_t_pred0 = x_t_pred0.iloc[::-1]
x_t_pred0=x_t_pred0[1:]

x_t_pred = pd.concat([x_t_pred0,pd.DataFrame(x_t_pred1)],ignore_index=True)

y_act = np.insert(np.array(y),0,x0[0])
df = {"DATE":year,"DICS Actual":pd.DataFrame(y_act),"DICS M4 full Predicted":x_t_pred}
out=pd.concat(df,axis=1)
out.to_csv('./img/USDICS M4 full last 65 plot.csv',index=False)


################ Start
## M3

N = number_banks  = 70
file_name = data_path+"ECB dataset completed.csv"
dat = pd.read_csv(file_name)
year = dat['Year']
dat = dat.iloc[:,1:]
y=dat.iloc[1:,0]
y=y.reset_index(drop=True)
x0=dat.iloc[:-1,0]
y_act = np.insert(np.array(y),0,x0[0])
x0=x0.reset_index(drop=True)
exog=dat.iloc[:,0:]
exog = dat[['DICS',"DILD","STOXX","Inflation",'Unemp positive',"Unemp negative",
            'SPF_Unemp positive','SPF_Unemp negative','SPF_Infla']]
exog = exog.iloc[:-1,:]
exog = exog.reset_index(drop=True)
add_con(exog)

qmle = QMLE(y, x0,exog.iloc,N)
result_M1 = qmle.fit(method='ncg',avextol=1e-4)
label_names = ['v'] + list(exog)
M1 = result_M1.summary(xname=label_names,title='M1')
result_params = result_M1.params

x_t_pred = predict2(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
df = {"DATE":year,"DICS Actual":y_act,"DICS M1 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/ECBDICS M4 plot.csv',index=False)
write_latex(M1,output,'M4.tex','QMLE M3')



#forward
qmle = QMLE(y.iloc[:40], x0.iloc[:40],exog.iloc[:40,],N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
x_t_pred = predict2(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
df = {"DATE":year,"DICS Actual":y_act,"DICS M4 Full Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/EUDICS M4 first 70 plot.csv',index=False)
