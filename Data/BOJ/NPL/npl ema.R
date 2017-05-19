library(TTR)
npl = read.csv('japan npl.csv')
names(npl)=c("Year","NPL")
npl$ema = EMA(npl$NPL,n=4)
write.csv(npl,'japan npl ema.csv')


library(stargazer)
x = read.csv("Japan GDP impute.csv")
y = read.csv("Japan gdp q.csv")
df = data.frame(y=y$JPNNGDP/10000,x=x$JPNNGDP/10000)
a = lm(y~x,data=df)

x = read.csv("Japan unemp impute.csv")
y = read.csv("Japan unemp q.csv")
df = data.frame(y=y$LRUN64TTJPQ156S,x=x$LRUN64TTJPM156S)
b = lm(y~x,data=df)
stargazer(a,b)


