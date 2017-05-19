import scipy.stats
import scipy
from scipy.misc import derivative
from sklearn import preprocessing
from statsmodels.base.model import GenericLikelihoodModel
import numpy as np
import pandas as pd
from sklearn import preprocessing
import matplotlib.pyplot as plt
from utility import *


def predict(x0,exog,params,Num_bank,repeat=50,scale_df=False,*args,**kwargs):
    """
    This part is adapted from Lacus, Stefano M.
        "Simulation and Inference for Stochastic Differential Equations with R Examples" 
                -- Springer, Page 88-90
    This function updates the diffusion index of credit spread by the actual data and predicts the next quarter value.
    """
    # standardize each feature s.t. they have mean 0 and variance 0
    if scale_df:
        exog_scale = preprocessing.scale(exog)
        exog=pd.DataFrame(exog_scale,columns=list(exog))

    def sde_sim_shoji(x0, Dt, N, params,*args , **kwargs):
        def drift(x, *args):
            v = params[0]
            exog_t = exog.loc[[t]]
            utility = np.dot(exog_t, params[1:])
            return 2 * v * np.cosh(utility) * (np.tanh(utility) - x)

        def sigma(x, *args):
            v = params[0]
            exog_t = exog.loc[[t]]
            utility = np.dot(exog_t, params[1:])
            return np.sqrt(2 * v * np.cosh(utility) * (1 - x * np.tanh(utility)) / N)
        # the model derivative is independent on time
        def d1t(*args, **kwargs):
            return 0
        def d1x(x0):
            return scipy.misc.derivative(drift, x0, n=1, dx=1e-8)
        def d1xx(x0):
            return scipy.misc.derivative(drift, x0, n=2, dx=1e-8)

        d1 = drift
        s1 = sigma
        n = len(x0)+1
        X = np.zeros(n)
        X[0] = x0[0]
        t = 0
        for i in range(1, n):
            x = X[i - 1]
            S = s1(x)
            Lx = d1x(x)
            Mx = (pow(S, 2) * d1xx(x) / 2 + d1t(x))
            Ex = (x + d1(x) * (np.exp(Lx * Dt) - 1) / Lx + Mx * (np.exp(Lx * Dt) - 1 - Lx * Dt) / pow(Lx, 2))
            Vx = (pow(S, 2) * (np.exp(2 * Lx * Dt) - 1) / (2 * Lx))
            x1 = np.random.normal(loc=Ex, scale=np.sqrt(Vx))
            t += 1
            if x1 > 1:
                X[i] = 1
            elif x1 < -1:
                X[i] = -1
            else:
                X[i] = x1

        return X

    result = []
    repeat = int(repeat)
    for trials in range(repeat):
        out = sde_sim_shoji(x0, Dt=0.25, N=Num_bank, params=params)
        result.append(out)

    return np.mean(result,axis=0)

def predict2(x0,exog,params,Num_bank,repeat=50,scale_df=False,*args,**kwargs):
    """
    This part is adapted from Lacus, Stefano M.
        "Simulation and Inference for Stochastic Differential Equations with R Examples" 
                -- Springer, Page 88-90
    This function updates the diffusion index of credit spread by the calculated value,
     so only the initial value from the actual data is used.
    """
    # standardize each feature s.t. they have mean 0 and variance 0
    if scale_df:
        exog_scale = preprocessing.scale(exog)
        exog=pd.DataFrame(exog_scale,columns=list(exog))

    def sde_sim_shoji(x0, Dt, N, params,*args , **kwargs):
        def drift(x, *args):
            v = params[0]
            exog_t = exog.loc[[t]]
            exog_t[["DICS"]] = x.copy()
            utility = np.dot(exog_t, params[1:])
            return 2 * v * np.cosh(utility) * (np.tanh(utility) - x)

        def sigma(x, *args):
            v = params[0]
            exog_t = exog.loc[[t]]
            exog_t[["DICS"]] = x.copy()
            utility = np.dot(exog_t, params[1:])
            return np.sqrt(2 * v * np.cosh(utility) * (1 - x * np.tanh(utility)) / N)
        # the model derivative is independent on time
        def d1t(*args, **kwargs):
            return 0
        def d1x(x0):
            return scipy.misc.derivative(drift, x0, n=1, dx=1e-8)
        def d1xx(x0):
            return scipy.misc.derivative(drift, x0, n=2, dx=1e-8)

        d1 = drift
        s1 = sigma
        n = len(x0)+1
        X = np.zeros(n)
        X[0] = x0[0]
        t = 0
        for i in range(1, n):
            x = X[i - 1]
            S = s1(x)
            Lx = d1x(x)
            Mx = (pow(S, 2) * d1xx(x) / 2 + d1t(x))
            Ex = (x + d1(x) * (np.exp(Lx * Dt) - 1) / Lx + Mx * (np.exp(Lx * Dt) - 1 - Lx * Dt) / pow(Lx, 2))
            Vx = (pow(S, 2) * (np.exp(2 * Lx * Dt) - 1) / (2 * Lx))
            x1 = np.random.normal(loc=Ex, scale=np.sqrt(Vx))
            t += 1
            if x1 > 1:
                X[i] = 1
            elif x1 < -1:
                X[i] = -1
            else:
                X[i] = x1

        return X

    result = []
    repeat = int(repeat)
    for trials in range(repeat):
        out = sde_sim_shoji(x0, Dt=0.25, N=Num_bank, params=params)
        result.append(out)

    return np.mean(result,axis=0)

class QMLE(GenericLikelihoodModel):
    def __init__(self, endog,x0, exog, N,**kwds):
        """
        :param endog: y (x_t+1) diffusion index for next quarter
        :param exog:  first column is constant if added, rest are exogenous variables
        :param lamb: for lasso/lasso regularization
        :param N: the number of banks
        :param kwds:
        """
        self.endog = endog
        self.exog = exog
        self.N = N
        self.x0 = x0
        self.cost_fn=None
        self.lamb=None
        super(QMLE, self).__init__(endog, exog,**kwds)

    def log_mle(self,y, exog_x0,exog_df, v,theta, N, *args, **kwargs):
        """
        :param y: diffusion index for next quarter 
        :param exog_x0: current period of diffusion index 
        :param exog_df: first column is constant, rest are exog
        :param v: turn over rate, to be estimated
        :param theta: inside U, to be estimated
        :param N: number of bank
        :return: negative value of likelihood 
        """
        t = 0.25
        x0=exog_x0
        X= exog_df
        utility = np.dot(X, theta)
        core = 2 * v * np.cosh(utility)
        Ex = core * (np.tanh(utility) - x0)
        #setattr(self,'mean',Ex)
        estimated_ex = x0 + np.multiply(Ex, t)
        Vx = core * (1 - x0 * np.tanh(utility)) / N
        estimated_va = (Vx * t)
        #setattr(self,'var',estimated_va)
        estimated_sd = np.sqrt(estimated_va)
        density = scipy.stats.norm.logpdf(x=y, loc=estimated_ex, scale=estimated_sd)

        if self.cost_fn == 'lasso':
            w = theta.copy()
            penality = (sum(abs(w))) * self.lamb
        elif self.cost_fn == 'ridge':
            w = theta.copy()
            w_sq = np.square(w)
            ww = w_sq.sum() + v**2
            penality = ww * self.lamb
        else:
            penality = 0
        return -density - penality

    def nloglikeobs(self, params,**kwds):
        """
        :param params: to be estimated
        :return: log likelihood value
        """
        v = params[0]
        theta = params[1:]

        if self.buildx0:
            self.x0 = np.dot(self.exog, theta)
            ll = self.log_mle(self.endog, self.x0, self.exog, v, theta, N=self.N)
        else:
            ll = self.log_mle(self.endog, self.x0, self.exog, v, theta, N=self.N)
        return ll
        #################

    def fit(self, method='ncg',start_params=None, maxiter=1000, maxfun=5000, **kwds):
        # we have one additional parameter and we need to add it for summary
        if start_params == None:
            # Reasonable starting values
            n = self.exog.shape[1]+1
            start_params = np.zeros(n)+0.01
        return super(QMLE, self).fit(start_params=start_params,method=method,
                                     maxiter=maxiter, maxfun=maxfun,disp=True,
                                     **kwds)

# for regularization parameter grid search
def optimal_lamb(qmle,y,x0,exog,N,lamb_range):
    if qmle.cost_fn==None:
        return ('choose regulization')

    MSE_list = []

    for lam in lamb_range:
        qmle.lamb = lam
        result = qmle.fit(method='ncg', avextol=1e-8)
        if  np.isnan(result.mle_retvals['fopt']):
            MSE = float('inf')
        else:
            result_params = result.params
            pred = predict(x0=x0, exog=exog, params=result_params, Num_bank=N, repeat=20)
            y_act = np.insert(np.array(y),0,x0[0])
            MSE = np.mean(np.square(pred - y_act))
        MSE_list.append(MSE)
    return(MSE_list)
