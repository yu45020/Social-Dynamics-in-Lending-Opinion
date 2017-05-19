library(readr)
df=read_csv('ECB dataset.csv')
library(TTR)
names(df)=names(df)

df$RGDPEMA =EMA(df$`RGDP grate lag2`,4)
df$RGDP_positive = 

df$UnempEMA = EMA(df$Unemp,4)
df$SPF_UnempEMA=EMA(df$SPF_Unemp,4)
df$SPF_RGDPEMA = EMA(df$`SPF_RGDP grate`,4)

clean = function(df,dfname){
  EMA = EMA(df,4)
  demean = df-EMA
  positive = ifelse(demean>0,demean,0)
  negative = ifelse(demean<0,demean,0)
  out = data.frame(positive,negative)
  names(out) = paste(dfname,names(out))
  return(out)
}

RGDP = clean(df$`RGDP grate lag2`,'RGDP_lag2')
Unemp = clean(df$Unemp,'Unemp')
SPFRGDP = clean(df$`RGDP grate lag2`,'SPF_RGDP')
SPFUnemp = clean(df$SPF_Unemp,'SPF_Unemp')
df1 = df[,1:6]
df = cbind(df1,RGDP,Unemp,SPFRGDP,SPFUnemp)
write_csv(df,'ECB dataset completed.csv')

#df = read_csv("ECB dataset completed.csv")
#inflation  = clean(df$Inflation,"inflation")
#SPF_inflation = clean(df$SPF_Inflation,'SPF inflation')

#df = cbind(df,inflation,SPF_inflation)
