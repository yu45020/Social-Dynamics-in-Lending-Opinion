from MLE import *
data_path = '../Data/US/'
output = '../Paper/Result/ModelResult/'
############## US Credit Spread ##############
# past quarter only

# M1 xt1~xt
N = number_banks  = 35
file_name = data_path+"DRISCFLM.csv"
dat = pd.read_csv(file_name)
dat.columns = ["DATE","DICSxt0"]
year = dat['DATE']
dat['DICSxt0'] = -dat['DICSxt0']/100
dat['DICSxt1'] = dat['DICSxt0'].shift(-1)

df = dat.dropna()
df.insert(1,'constant',np.ones(df.shape[0]))
y=df['DICSxt1']
x0=df['DICSxt0']
exog=df[['constant','DICSxt0']]
qmle = QMLE(y, x0,exog,N)
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
result_params = result_M1.params
label_names = ['v'] + list(exog)
M1 = result_M1.summary(xname=label_names,title='M1')
#write_latex(M1,output,'M1.tex','QMLE M1')

newnames = ['constant',"DICS"]
exog.columns = newnames
x_t_pred = predict(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)

# M2 xt1~xt(+) + xt(-)
df['DICSxt0+'] = [df if df>0 else 0 for df in df['DICSxt0']]
df['DICSxt0-'] = [df if df<0 else 0 for df in df['DICSxt0']]
exog = pd.concat([df['DICSxt0+'],df['DICSxt0-']],axis=1)
add_con(exog)
qmle.exog  = exog
result_M1 = qmle.fit(method='ncg',avextol=1e-12)
label_names = ['v'] + list(exog)
M2 = result_M1.summary(xname=label_names,title='QMLE M2')
#write_latex(M2,output,'M2.tex','QMLE M2')

result_params = result_M1.params
x_t_pred = predict(x0=x0,exog=exog,params=result_params,Num_bank=N,repeat=20)
y_act = np.insert(np.array(y),0,x0[0])
df = {"DATE":year,"DICS Actual":y_act,"DICS M2 Predicted":x_t_pred}
out=pd.DataFrame(df)
out.to_csv('./img/USDICS M2 plot.csv',index=False)


# M3 add last 2 quarter, followed from M2
df = dat.copy()
df['DICSxt-1'] = df["DICSxt0"].shift(1)
df['DICSxt0+'] = [df if df>0 else 0 for df in df['DICSxt0']]
df['DICSxt0-'] = [df if df<0 else 0 for df in df['DICSxt0']]
df['DICSxt-1+'] = [df if df>0 else 0 for df in df['DICSxt-1']]
df['DICSxt-1-'] = [df if df<0 else 0 for df in df['DICSxt-1']]
df.dropna(inplace=True)

y=df['DICSxt1']
x0=df['DICSxt0']
exog=df[['DICSxt0+', 'DICSxt0-','DICSxt-1+','DICSxt-1-']]
add_con(exog)

qmle = QMLE(y, x0,exog,N)
result_M3 = qmle.fit(method='ncg',avextol=1e-12)
label_names = ['v'] + list(exog)
M3 = result_M3.summary(xname=label_names,title='M3')
#write_latex(M3,output,'M3.tex','QMLE M3')



########## US Data #################
# median & large firm
N = number_banks  = 33
file_name = "US Credit Spread.csv"
y,x0,exog= input_data(file_name)
sample_points = np.arange(start=10,stop=95,step=5)
US_param = param_list(sample_points, y, x0, exog, random=False)
US_param_random =param_list(sample_points, y, x0, exog, random=True)
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

# small firm
N = number_banks  = 33
file_name = "US Credit Spread Small Firm.csv"
y,x0,exog= input_data(file_name)
sample_points = np.array(list(range(1,10)))*10
y, x0, exog = input_data(file_name)
US_param = param_list(sample_points, y, x0, exog, random=False)
US_param_random =param_list(sample_points, y, x0, exog, random=True)
dff = {'points':sample_points,'order':US_param.iloc[:,3],'random': US_param_random.iloc[:,3]}
df = pd.DataFrame(dff)
df = pd.melt(df,id_vars='points',var_name='US.DICSxt0')
ggplot(aes(x='points',y='value',colour='US.DICSxt0'),data=df)+ geom_point()+geom_line()
US_df = US_param.copy()
posi=2
for i in range(1,4):
    US_df.insert(posi,list(US_param_random)[i],US_param_random.iloc[:,i])
    posi +=2

US_df.to_csv('US DICS Small Beta Compare.csv')



# include one more period
## median & large firm
N = number_banks  = 33
file_name = "US Credit Spread test.csv"
y,x0,exog= input_data(file_name)
sample_points = np.array(list(range(1,10)))*10
y, x0, exog = input_data(file_name)
US_param = param_list(sample_points, y, x0, exog, random=False)
US_param_random =param_list(sample_points, y, x0, exog, random=True)
dff = {'points':sample_points,'order':US_param.iloc[:,3],'random': US_param_random.iloc[:,3]}
df = pd.DataFrame(dff)
df = pd.melt(df,id_vars='points',var_name='US.DICSxt0')
ggplot(aes(x='points',y='value',colour='US.DICSxt0'),data=df)+ geom_point()+geom_line()
US_df = US_param.copy()
posi=2
for i in range(1,5):
    US_df.insert(posi,list(US_param_random)[i],US_param_random.iloc[:,i])
    posi +=2

US_df.to_csv('US DICS Beta Compare past two.csv')

## check the 2nd period
dff = {'points':sample_points,'order':US_param.iloc[:,4],'random': US_param_random.iloc[:,4]}
df = pd.DataFrame(dff)
df = pd.melt(df,id_vars='points',var_name='US.DICSxt0')
ggplot(aes(x='points',y='value',colour='US.DICSxt0'),data=df)+ geom_point()+geom_line()


#########   ECB Lending Survey ############
## Average Risk Loans ##
N = number_banks  = 141
file_name = "ecb margin average net.csv"
y,x0,exog= input_data(file_name)
sample_points = np.arange(10, 31, 5)
ECB_param_ave = param_list(sample_points, y, x0, exog, random=False)
ECB_param_random_ave =param_list(sample_points, y, x0, exog, random=True)
dff = {'points': sample_points, 'order': ECB_param_ave.iloc[:, 3], 'random': ECB_param_random_ave.iloc[:, 3]}
df = pd.DataFrame(dff)
df = pd.melt(df, id_vars='points', var_name='ECB.DICSxt0.ave')
ggplot(aes(x='points', y='value', colour='ECB.DICSxt0.ave'), data=df) + geom_point() + geom_line()
ECB_df = ECB_param_ave.copy()
posi=2
for i in range(1,4):
    ECB_df.insert(posi,list(ECB_param_random_ave)[i],ECB_param_random_ave.iloc[:,i])
    posi +=2
ECB_df.to_csv('ECB DICS Ave Beta Compare.csv')

## Riskier Loans ##
N = number_banks  = 70
file_name = "ecb margin riskier net.csv"
y,x0,exog= input_data(file_name)
sample_points = np.arange(10, 36, 5)
ECB_param_risk = param_list(sample_points, y, x0, exog, random=False)
ECB_param_random_risk =param_list(sample_points, y, x0, exog, random=True)
dff = {'points': sample_points[1:], 'order': ECB_param_risk.iloc[1:, 3], 'random': ECB_param_random_risk.iloc[1:, 3]}
df = pd.DataFrame(dff)
df = pd.melt(df, id_vars='points', var_name='ECB.DICSxt0.risk')
ggplot(aes(x='points', y='value', colour='ECB.DICSxt0.risk'), data=df) + geom_point() + geom_line()
ECB_risk_df = ECB_param_risk.copy()
posi=2
for i in range(1,4):
    ECB_risk_df.insert(posi,list(ECB_param_random_risk)[i],ECB_param_random_risk.iloc[:,i])
    posi +=2
ECB_risk_df.to_csv('ECB DICS Risk Beta Compare.csv')


### JOB
## High Rating Loans Credit Spread Past##
N = number_banks  = 50
file_name = "./BOJ/HRCSpPast.csv"
y,x0,exog= input_data(file_name)
sample_points = np.arange(10, 67, 5)
JOB_param_ave = param_list(sample_points, y, x0, exog, random=False)
JOB_param_random_ave =param_list(sample_points, y, x0, exog, random=True)
dff = {'points': sample_points, 'order': JOB_param_ave.iloc[:, 3], 'random': JOB_param_random_ave.iloc[:, 3]}
df = pd.DataFrame(dff)
df = pd.melt(df, id_vars='points', var_name='JOB.DICSxt0.HighRate')
ggplot(aes(x='points', y='value', colour='JOB.DICSxt0.HighRate'), data=df) + geom_point() + geom_line()
JOB_df = JOB_param_ave.copy()
posi=2
for i in range(1,4):
    JOB_df.insert(posi,list(JOB_param_random_ave)[i],JOB_param_random_ave.iloc[:,i])
    posi +=2
JOB_df.to_csv('JOB DICS High Rate Beta Compare.csv')

## High + Median Rating Loans ##
N = number_banks  = 50
file_name = "./BOJ/HMRCSpPast.csv"
y,x0,exog= input_data(file_name)
sample_points = np.arange(10, 67, 5)
JOB_param_ave = param_list(sample_points, y, x0, exog, random=False)
JOB_param_random_ave =param_list(sample_points, y, x0, exog, random=True)
dff = {'points': sample_points, 'order': JOB_param_ave.iloc[:, 3], 'random': JOB_param_random_ave.iloc[:, 3]}
df = pd.DataFrame(dff)
df = pd.melt(df, id_vars='points', var_name='JOB.DICSxt0.HighRate')
ggplot(aes(x='points', y='value', colour='JOB.DICSxt0.HighRate'), data=df) + geom_point() + geom_line()
JOB_df = JOB_param_ave.copy()
posi=2
for i in range(1,4):
    JOB_df.insert(posi,list(JOB_param_random_ave)[i],JOB_param_random_ave.iloc[:,i])
    posi +=2
JOB_df.to_csv('JOB DICS High Rate Beta Compare.csv')

N = number_banks  = 50
file_name = "./BOJ/MRCSpPast.csv"
y,x0,exog= input_data(file_name)
sample_points = np.arange(10, 67, 5)
JOB_param_ave = param_list(sample_points, y, x0, exog, random=False)
JOB_param_random_ave =param_list(sample_points, y, x0, exog, random=True)
dff = {'points': sample_points[1:], 'order': JOB_param_ave.iloc[1:, 3], 'random': JOB_param_random_ave.iloc[1:, 3]}
df = pd.DataFrame(dff)
df = pd.melt(df, id_vars='points', var_name='JOB.DICSxt0.HighRate')
ggplot(aes(x='points', y='value', colour='JOB.DICSxt0.HighRate'), data=df) + geom_point() + geom_line()
JOB_df = JOB_param_ave.copy()
posi=2
for i in range(1,4):
    JOB_df.insert(posi,list(JOB_param_random_ave)[i],JOB_param_random_ave.iloc[:,i])
    posi +=2
JOB_df.to_csv('JOB DICS High Median Rate Beta Compare.csv')


N = number_banks  = 50
file_name = "./BOJ/cshosue_di.csv"

y,x0,exog= input_data(file_name)
qmle = QMLE(y, exog,x0=x0,N=N)
result_M1 = qmle.fit(method='ncg', cost_fn=None)
label_names = ['v'] + list(exog)
result_M1.summary(xname=label_names,title='M1')
result_params = result_M1.params
x_t_pred = predict(x0=x0,exog=exog,params=result_params,repeat=20)

x0_axis,=plt.plot(x0,label='actual')
xt_axis, = plt.plot(x_t_pred,label='predicted')
plt.ylabel('Diffusion Index')
plt.legend(handles=[x0_axis, xt_axis])
plt.title('Japan Credit Standard Large Firms')


## ECB
N = number_banks  = 141
file_name = "ecb margin average net.csv"
y,x0,exog= input_data(file_name)
qmle = QMLE(y, exog,x0=x0,N=N)
result_M1 = qmle.fit(method='ncg', cost_fn=None)
label_names = ['v'] + list(exog)
result_M1.summary(xname=label_names,title='M1')
result_params = result_M1.params
x_t_pred = predict(x0=x0,exog=exog,params=result_params,repeat=20)
x0_axis,=plt.plot(x0,label='actual')
xt_axis, = plt.plot(x_t_pred,label='predicted Order')
plt.ylabel('ECB Diffusion Index')
plt.legend(handles=[x0_axis, xt_axis])
plt.title('ECB Diffusion Index')
