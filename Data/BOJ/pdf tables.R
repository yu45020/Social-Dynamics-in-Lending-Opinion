
df = read.csv('BOJ Credit Standard.csv',header = FALSE)
cut = seq(2,544,by=2)
df = df[-cut,]

Year = seq(ymd('2000-04-01'),ymd('2017-01-01'),by='quarter')

coltitle = c('Eased Consid', "Eased Some",
             "Unchanged", "Tightened Some","Tightened Consid")


## Credit Standard Results
cslf = seq(1,dim(df)[1],by=4)
credit_standard_large_firm = df[cslf,]
cslf = sapply(credit_standard_large_firm,FUN=function(x)as.numeric(as.character(x)))

csmf = seq(2,dim(df)[1],by=4)
credit_standard_medium_firm = df[csmf,]
csmf = sapply(credit_standard_medium_firm,FUN=function(x)as.numeric(as.character(x))) 

cssf = seq(3,dim(df)[1],by=4)
credit_standard_small_firm = df[cssf,]
cssf = sapply(credit_standard_small_firm,FUN=function(x)as.numeric(as.character(x)))


cshouse = seq(4,dim(df)[1],by=4)
credit_standard_house = df[cshouse,]
cshosue = sapply(credit_standard_house,FUN=function(x)as.numeric(as.character(x)))

## Diffusion Index 
diffusion_index = function(df,weighted=FALSE){
  total = rowSums(df)
  percen = df[,]/total
  if(weighted){
    wi = c(1,0.5,0,0.5,1)
    percen = sapply(1:5,FUN=function(i)wi[i]*percen[,i])
    
  }
  wi_di = (percen[,1]+percen[,2]) - (percen[,4]+percen[,5])
  return(wi_di)
}
cslf_di = diffusion_index(cslf,weighted = FALSE)
csmf_di = diffusion_index(csmf,weighted = FALSE)
cssf_di = diffusion_index(cssf,weighted = FALSE)
cshosue_di = diffusion_index(cshosue,weighted = FALSE)



cslf_di = data.frame(Year,cslf_di)
write.csv(cslf_di,"cslf_di.csv",row.names = FALSE)

csmf_di = data.frame(Year,csmf_di)
write.csv(csmf_di,"csmf_di.csv",row.names = FALSE)

cssf_di = data.frame(Year,cssf_di)
write.csv(cssf_di,"cssf_di.csv",row.names = FALSE)

cshosue_di = data.frame(Year,cshosue_di)
write.csv(cshosue_di,"cshosue_di.csv",row.names = FALSE)

