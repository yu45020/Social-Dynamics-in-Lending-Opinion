from MLE import*
# Collections of functions used during the research.
# Not all of them are used in the paper
def sign_apart(df):
    df= np.array(df)
    df_p,df_n = np.zeros(df.shape[0]),np.zeros(df.shape[0])
    positive = df>0
    negative = df<0
    df_p[positive] = df[positive]
    df_n[negative] = df[negative]
    df_apart = pd.DataFrame([df_p,df_n])
    return df_p,df_n
def write_latex(model,path,name,title,tables=False):
    with open(path+name,'w') as f:
        tit = r'\captionof{table}{'+title+"}"+'\label{'+title+'}'
        f.write(tit)
        if tables:
            for tab in model.tables:
                t = tab.as_latex_tabular()
                f.write(t)
        else:
            f.write(model.as_latex())
def add_con(df):
    df.insert(0,'constant',np.ones(df.shape[0]))

def sample_datainput():
    # df=np.genfromtxt('dff.csv',delimiter=',')
    df = pd.read_csv('dff.csv')
    y = df.iloc[:, 0]
    x0 = y[0:-1]
    df_xt1 = pd.read_csv('dffxt1.csv')
    y = df_xt1.iloc[:, 0]

    exog = pd.DataFrame(x0.copy())
    exog.columns = ['x0']
    exog.insert(0, 'constant', np.ones(exog.shape[0]))
    # exog=np.array(exog, dtype=float)
    N = 33
    lamb = 0.5
    qmle = QMLE(y, exog)
    result = qmle.fit(method='bfgs')
    label_names = ['v'] + list(exog)
    result.summary(xname=label_names)
    result.bootstrap(disp=0, store=0)
    result.mle_settings
    result.mle_retvals
    result.params

    ## Another test
    df = pd.read_csv('df backup.csv')
    x0 = df['DICS']
    df_xt1 = pd.read_csv('dffxt1.csv')
    y = df_xt1.iloc[:, 0]

    exog = df.iloc[:, 1:]
    exog['chargeoff.OneYear'] = exog['chargeoff.OneYear'] / 100
    # col_names = list(exog)
    # exog=preprocessing.normalize(exog, norm='l2')
    # exog = pd.DataFrame(exog)
    # exog.columns = col_names
    exog.insert(0, 'constant', np.ones(exog.shape[0]))
    # exog=np.array(exog, dtype=float)
    N = 33
    lamb = 1
    alpha, beta = 4, 8

    backup = exog.copy()
    back = backup[:70]
    y = y[:70]
    x0 = x0[:70]
    qmle = QMLE(y, exog)  # cost_fn =
    boundaries = [(0, 100), (-1e5, 1e5), (-1e5, 0), (-1e5, 1e5), (-1e5, 1e5), (-1e5, 1e5)]
    result = qmle.fit(method='bfgs', cost_fn=None)  # 'lbfgs','bfgs' ",maxls=100,bounds=boundaries,optimizer='bfgs'
    label_names = ['v'] + list(exog)
    result.summary(xname=label_names)

    # result.bootstrap(disp=0, store=0)
    result.params
    qmle = QMLE(y, exog, method='bfgs', optimizer='bfgs')
    boundaries = [(0, 100), (-1e5, 1e5), (-1e5, 0), (-1e5, -1), (-1e5, 1e5), (-1e5, 1e5)]
    result = qmle.fit(method='bfgs', maxls=100, bounds=boundaries, optimizer='bfgs', start_params=result.params,
                      gtol=1e-6)  # 'lbfgs','bfgs'
    label_names = ['v'] + list(exog)
    result.summary(xname=label_names)

def plot(qmle,y,x0,exog,N,title,vertical=False,rep=20):
    result_params = qmle.params
    x_t_pred = predict(x0=x0, exog=exog, params=result_params, Num_bank=N, repeat=rep)
    y_act = np.insert(np.array(y), 0, x0[0])
    x0_axis, = plt.plot(y_act, label='Actual DICS')
    xt_axis, = plt.plot(x_t_pred, label='Predicted DICS')
    plt.ylabel('Diffusion Index')
    plt.legend(handles=[x0_axis, xt_axis])
    if vertical is not False:
        plt.axvline(vertical, color='r')
    plt.title(title)
    plt.show()