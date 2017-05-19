# Social Dynamics in Bland Lending Opinions

## This script is used to clean the US data


# Prepare Packages
pkg = c("ggplot2",'mFilter',"reshape","readxl","tframePlus","readr","TTR","lubridate","zoo")
new.pkg = pkg[!(pkg %in% installed.packages()[,"Package"])]
if (length(new.pkg)) {install.packages(new.pkg,dependencies = TRUE)}
sapply(pkg,require, character.only=TRUE)
ema_n = 4


# Helper Functions


## Function for converting quarter to month 

QtoM = function(data,col=4){
  # to clean SPF data
  # First column is year and second is quarter
  n = nrow(data)
  year_qrt = as.yearqtr(paste0(data$YEAR,'Q',data$QUARTER))
  DATE = yq(year_qrt)
  df = sapply(data[,3:ncol(data)],as.numeric)
  fin_df = data.frame(DATE,df)
  return(fin_df)
  return(data)
}



## add dataframe as a list into a list of dataframe (for merging purpose)

list.df=list()
add.list = function(data) {
  list.df <<- append(list.df,list(data))
}



# Prepare Data
##  Diffusion Index on Spread
### The original data is about tightening credit spread, so put a negative sign

DICS = read_csv("DRISCFLM.csv")
DICS$DRISCFLM = -DICS$DRISCFLM/100
names(DICS)[2] = 'DICS'
add.list(DICS)


## Loan demand
DILD = read_csv('DRSDCILM.csv')
DILD$DRSDCILM = DILD$DRSDCILM / 100
names(DILD)[2] = "DILD"
add.list(DILD)

## EBP

EBP = read_csv('Excessive Bond Premium.csv')
EBP$date = as.Date(as.yearmon(EBP$date))

m = ts(EBP$ebp, start = c(1973, 1), frequency = 12)
ebp_quarter = as.quarterly(m, FUN = mean)


ebp = data.frame(DATE = seq(ymd('1973-01-01'), ymd('2017-02-01'), by = 'quarter'))
ebp$EBP = as.numeric(ebp_quarter)
ebp$EBP = c(NA, diff(ebp$EBP))

add.list(ebp)


##  VIX 
### One quarter change, from daily average

vix = read_csv("VIXCLS.csv")
vix$VIXCLS_CHG = vix$VIXCLS_CHG/100
names(vix)[2] = 'VIX'
add.list(vix)


##  NASDAQ
### One quarter percent change, from daily average

NASDAQ = read_csv("NASDAQCOM.csv")
NASDAQ$NASDAQCOM_PCH = NASDAQ$NASDAQCOM_PCH/100
names(NASDAQ)[2] = 'NASDAQ'
add.list(NASDAQ)

#######################

##  Expected Inflation

CPI = read_csv("CPIAUCSL.csv")
CPI$CPIAUCSL_PCH = CPI$CPIAUCSL_PCH/100
names(CPI)[2] ='CPI'

SPF_CPI = read_excel("Mean_CPI_Level.xls") 
SPF_CPI = QtoM(SPF_CPI)
SPF_CPI = subset(SPF_CPI,select=c("DATE","CPI3"))
SPF_CPI$CPI3 = SPF_CPI$CPI3/100
d = diff(SPF_CPI$CPI3)/SPF_CPI$CPI3[-length(SPF_CPI$CPI3)]
SPF_CPI$CPI3 = c(NA,d)
names(SPF_CPI )[2] = 'SPF CPI'
CPI_df = merge(CPI,SPF_CPI,by='DATE')
add.list(CPI_df)


## RGDP percentage change
### # past 2 quarter RGDP available. SPF GDP use col 6: expectation for next year


RGDP = read_csv('GDPC1.csv')
RGDP$GDPC1_PCH =RGDP$GDPC1_PCH/100
nr=nrow(RGDP)
past_2q = data.frame(RGDP$DATE[-c(1,2)],RGDP$GDPC1_PCH[-c(nr,nr-1)])
names(past_2q) = names(RGDP)


SPF_GDP = read_excel("Mean_RGDP_Growth.xls")
SPF_GDP = QtoM(SPF_GDP)
names(SPF_GDP)[3] = 'SPF_GDP'
SPF_GDP$SPF_GDP = SPF_GDP$SPF_GDP/100

GDP = merge(past_2q,SPF_GDP,by='DATE')

# EMA
GDP$RGDP_EMA1Y = EMA(GDP$GDPC1_PCH,n=ema_n)
GDP$RGDP_demean = GDP$GDPC1_PCH - GDP$RGDP_EMA1Y
GDP$GDP_positive = ifelse(GDP$RGDP_demean>0,GDP$RGDP_demean,0)
GDP$GDP_negative = ifelse(GDP$RGDP_demean<0,GDP$RGDP_demean,0)

GDP$RGDP_EMA1Y = EMA(GDP$SPF_GDP, n = ema_n)
GDP$RGDP_demean = GDP$SPF_GDP - GDP$RGDP_EMA1Y
GDP$GDP_positive_future = ifelse(GDP$RGDP_demean>0,GDP$RGDP_demean,0)
GDP$GDP_negative_future = ifelse(GDP$RGDP_demean<0,GDP$RGDP_demean,0)

GDP_final = subset(GDP,select=c(DATE,GDP_positive,GDP_negative,GDP_positive_future,GDP_negative_future))

names(GDP_final)[2:5] = c("RGDP positive","RGDP negative",'SPF RGDP positive','SPF RGDP negative')
add.list(GDP_final)


## Unemployment percentage change
### Use quarterly average

Unemp = read_csv('UNRATE.csv')
names(Unemp)[2]='UNRATE'
Unemp$UNRATE = Unemp$UNRATE / 100

SPF_Unemp = read_excel("Mean_UNEMP_Level.xls")
SPF_Unemp = QtoM(SPF_Unemp)
SPF_Unemp = subset(SPF_Unemp,select = c(DATE,UNEMP3))
d= diff(SPF_Unemp$UNEMP3)/SPF_Unemp$UNEMP3[-length(SPF_Unemp$UNEMP3)]
names(SPF_Unemp)[2] = 'SPF_Unemp'
SPF_Unemp$SPF_Unemp =c(NA,d)



Unemp = merge(Unemp, SPF_Unemp, by = 'DATE')

Unemp$unemp_EMA1Y = EMA(Unemp$UNRATE,n=ema_n)
Unemp$unemp_demean = Unemp$UNRATE - Unemp$unemp_EMA1Y
Unemp$unemp_positive = ifelse(Unemp$unemp_demean>0,Unemp$unemp_demean,0)
Unemp$unemp_negative = ifelse(Unemp$unemp_demean<0,Unemp$unemp_demean,0)

Unemp$unemp_EMA1Y = EMA(Unemp$SPF_Unemp, n = ema_n)
Unemp$unemp_demean = Unemp$SPF_Unemp - Unemp$unemp_EMA1Y
Unemp$unemp_positive_future = ifelse(Unemp$unemp_demean>0,Unemp$unemp_demean,0)
Unemp$unemp_negative_future = ifelse(Unemp$unemp_demean<0,Unemp$unemp_demean,0)

Unemp_final = subset(Unemp, select = c(DATE, unemp_positive, unemp_negative, unemp_positive_future, unemp_negative_future))

names(Unemp_final)[4:5] = c("SPF unemp positive","SPF unemp negative")
add.list(Unemp_final)


##  Corporate Profits After Tax (without IVA and CCAdj)
# lag 2 because of release date
SPF_corp = read_excel('Mean_CPROF_Growth.xls')
SPF_corp = QtoM(SPF_corp)
names(SPF_corp)[3] = "SPF_Corp"
SPF_corp$SPF_Corp = SPF_corp$SPF_Corp/100


corp = read_csv('CP.csv')
corp$CP_PCH = corp$CP_PCH/100
nr=nrow(corp)
past_2q_cp = data.frame(corp$DATE[-c(1,2)],corp$CP_PCH[-c(nr,nr-1)])
names(past_2q_cp) = names(corp)

corp_profit = merge(past_2q_cp,SPF_corp,by='DATE')

corp_profit$corp_EMA_1Year = EMA(corp_profit$CP_PCH,n=ema_n)
corp_profit$corp_demean = corp_profit$CP_PCH - corp_profit$corp_EMA_1Year
corp_profit$corp_positive = ifelse(corp_profit$corp_demean>0,corp_profit$corp_demean,0)
corp_profit$corp_negative = ifelse(corp_profit$corp_demean<0,corp_profit$corp_demean,0)


corp_profit$corp_EMA_1Year = EMA(corp_profit$SPF_Corp, n = ema_n)
corp_profit$corp_demean = corp_profit$SPF_Corp - corp_profit$corp_EMA_1Year
corp_profit$corp_positive_future = ifelse(corp_profit$corp_demean>0,corp_profit$corp_demean,0)
corp_profit$corp_negative_future = ifelse(corp_profit$corp_demean<0,corp_profit$corp_demean,0)



corp_final = subset(corp_profit,select=c(DATE,corp_positive,corp_negative,corp_positive_future,corp_negative_future))


names(corp_final)[4:5]=c("SPF Corp positive",'SPF Corp negative')
add.list(corp_final)



## NPL
NPL = read_csv("NPCMCM.csv")
NPL$NPCMCM = NPL$NPCMCM/100
NPL$ema = EMA(NPL$NPCMCM,n=ema_n)

NPL$demean = NPL$NPCMCM-NPL$ema
NPL$NPL_positive = ifelse(NPL$demean>0,NPL$demean,0)
NPL$NPL_negative = ifelse(NPL$demean<0,NPL$demean,0)
NPL =subset(NPL,select = c(DATE,NPL_positive,NPL_negative))
add.list(NPL)





# Merge Data


df = Reduce(function(...) merge(...,by="DATE",all=TRUE), list.df)

df= df[complete.cases(df),]


# write data

write.csv(df,"df1ema.csv")





















