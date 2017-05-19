library(readr)
df=read_csv('toclean.csv')
library(TTR)in
names(df)=names(df)

clean = function(df,dfname){
  EMA = EMA(df,4)
  demean = df-EMA
  positive = ifelse(demean>0,demean,0)
  negative = ifelse(demean<0,demean,0)
  out = data.frame(positive,negative)
  names(out) = paste(dfname,names(out))
  return(out)
}

RGDP = clean(df$GDP,'RGDP_lag2')
Unemp = clean(df$Unemployment,'Unemp')
df = cbind(time=df[,1],RGDP,Unemp)
write_csv(df,'ECB dataset completed.csv')

#df = read_csv("ECB dataset completed.csv")
#inflation  = clean(df$Inflation,"inflation")
#SPF_inflation = clean(df$SPF_Inflation,'SPF inflation')



# clean vix japan
library(lubridate)
library(dplyr)
library(zoo)
vjx = read_csv("vxj.csv")
vjx$VXJ = ifelse(vjx$VXJ=='closed',NA,vjx$VXJ)
vjx = vjx[complete.cases(vjx$VXJ),]
vjx$Year =ymd(vjx$Year)
vjx$VXJ =as.numeric(vjx$VXJ)

z = zoo(vjx$VXJ,vjx$Year)
out = aggregate(z,as.yearqtr,mean)
VJX = as.data.frame(out)
write.csv(VJX,'VJX.csv')


## clean npl


