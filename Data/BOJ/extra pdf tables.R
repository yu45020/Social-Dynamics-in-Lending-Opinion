# Extra Tables from Pdfs 
library(readr)
library(plyr)
library(stringr)
library(zoo)
library(lubridate)
get_files = function(end_name,folder=BOJ_folder){
  file.names = list.files(path=folder,pattern = paste0(end_name,'.csv'),
                    all.files = TRUE,full.names = TRUE,
                    recursive = TRUE,include.dirs = TRUE)
  lapply(file.names,FUN=function(x) read.csv(x,header=FALSE))    
} 

clean_loan_csv = function(df){
  re = data.frame(llply(df, function(x) {
    x =str_replace_all(x, pattern="[^0-9\\.\\,-]", replacement="")
    x =str_replace(x, pattern="\\,", replacement=".")
    return(as.numeric(x))
  }))
  return(re)
}

diffusion_index = function(df){
  if(dim(df)[2]==5){
    di = (rowSums(df[,c(1,2)]) - rowSums(df[,c(4,5)]))/rowSums(df)
  }else{
    di = (df[,1] - df[,3])/rowSums(df)
  }
  return(di)
}

Year = seq(ymd('2000-04-01'),ymd('2017-01-01'),by='quarter')
## BOJ
BOJ_folder = './BOJ Credit Spread'

### Loan Demand Past
BOJ_files_paste = get_files('-0')
loan_demand_paste = lapply(BOJ_files_paste,FUN=function(x)clean_loan_csv(x))

loan_demand_paste = lapply(loan_demand_paste,FUN=function(x)x[c(1,3,5),1:5])

loan_demand_past_di = lapply(loan_demand_paste,FUN=function(x)diffusion_index(x))


df = Reduce(cbind,loan_demand_past_di)

rownames(df) = c("HRLDPast","MRLDPast","LRLDPast")

for(i in 1:dim(df)[1]){
  out = data.frame(Year,df[i,])
  names(out)[2] = rownames(df)[i]
  out_name = paste0(BOJ_folder,"/",names(out)[2],'.csv')
  write_csv(out,out_name)
}

### Loan Demand Future
BOJ_files_future = get_files('-1')
loan_demand_future = lapply(BOJ_files_future,FUN=function(x)clean_loan_csv(x))

loan_demand_future = lapply(loan_demand_future,FUN=function(x) x[1,c(1,2,3,4,5)])

loan_demand_future_di = lapply(loan_demand_future,FUN=function(x)diffusion_index(x))

df = Reduce(cbind,loan_demand_future_di)
df= as.numeric(df)
out = data.frame(Year,df)
names(out)[2] = 'Firm_LoanDemand_Future'
out_name = paste0(BOJ_folder,"/",names(out)[2],'.csv')
write_csv(out,out_name)


### Loan Sapply Past credit spread
BOJ_files_Past = get_files('-2')
loan_sapply_Past = lapply(BOJ_files_Past,FUN=function(x)clean_loan_csv(x))

loan_sapply_Past = lapply(loan_sapply_Past,FUN=function(x) x[c(1,3,5),c(1,2,3)])

loan_sapply_Past_di = lapply(loan_sapply_Past,FUN=function(x)diffusion_index(x))

df = -Reduce(cbind,loan_sapply_Past_di)
rownames(df) = c("HRCSpPast","MRCSpPast","LRCSpPast")

for(i in 1:dim(df)[1]){
  out = data.frame(Year,df[i,])
  names(out)[2] = rownames(df)[i]
  out_name = paste0(BOJ_folder,"/",names(out)[2],'.csv')
  write_csv(out,out_name)
}


### Loan Sapply Future
BOJ_files_future = get_files('-3')
loan_sapply_future = lapply(BOJ_files_future,FUN=function(x)clean_loan_csv(x))

loan_sapply_future = lapply(loan_sapply_future,FUN=function(x) x[c(1,3,5),c(1,2,3)])

loan_sapply_future_di = lapply(loan_sapply_future,FUN=function(x)diffusion_index(x))

df =-Reduce(cbind,loan_sapply_future_di)
rownames(df) = c("HRCSpfuture","MRCSpfuture","LRCSpfuture")

for(i in 1:dim(df)[1]){
  out = data.frame(Year,df[i,])
  names(out)[2] = rownames(df)[i]
  out_name = paste0(BOJ_folder,"/",names(out)[2],'.csv')
  write_csv(out,out_name)
}









### Loan Sapply Past credit spread High + Median
BOJ_files_Past = get_files('-2')
loan_sapply_Past = lapply(BOJ_files_Past,FUN=function(x)clean_loan_csv(x))

loan_sapply_Past = lapply(loan_sapply_Past,FUN=function(x) x[c(1,3,5),c(1,2,3)])

diffusion_index2 = function(df){
  df = df[-3,]
  df = df[1,] + df[2,]
  di = -(df[,1] - df[,3])/rowSums(df)
  return(di)
}


loan_sapply_Past_di = lapply(loan_sapply_Past,FUN=function(x)diffusion_index2(x))

df = Reduce(cbind,loan_sapply_Past_di)

df= as.numeric(df)
out = data.frame(Year,df)
names(out)[2] = 'HMRCSpPast'
out_name = paste0(BOJ_folder,"/",names(out)[2],'.csv')
write_csv(out,out_name)




### Loan Sapply Future credit spread High + Median
BOJ_files_future = get_files('-3')
loan_sapply_future= lapply(BOJ_files_future,FUN=function(x)clean_loan_csv(x))

loan_sapply_future = lapply(loan_sapply_future,FUN=function(x) x[c(1,3,5),c(1,2,3)])

diffusion_index2 = function(df){
  df = df[-3,]
  df = df[1,] + df[2,]
  di = -(df[,1] - df[,3])/rowSums(df)
  return(di)
}


loan_sapply_future_di = lapply(loan_sapply_future,FUN=function(x)diffusion_index2(x))

df = Reduce(cbind,loan_sapply_future_di)

df= as.numeric(df)
out = data.frame(Year,df)
names(out)[2] = 'HMRCSpFuture'
out_name = paste0(BOJ_folder,"/",names(out)[2],'.csv')
write_csv(out,out_name)

