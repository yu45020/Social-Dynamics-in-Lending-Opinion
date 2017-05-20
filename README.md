# Social Dynamics in Lending Opinion


______________ Codes Folder ______________

1. MLE.py codes the opinion formation model. The class is inherited from Scipy's GenericLikelihoodModel.
2. utility.py contains self-defined functions. Not all of them are used for the paper. 

3. peer only. py contains model 1/2 for US, Euro Area, and Japan.
4. USdata.py, EUdata.py, Japandata.py contain models that include exogenous variables.
5. Feature Selection.py uses random forest and Boruta method to select optimal subsets of variables for US, Euro Area,        and Japan. 
6. USDICS stability check.py examines the coefficient of the diffusion index of credit spread in peer only US model. 

______________ Data Folder ______________

All raw data are public, and many of them can be obtain from central banks' websites. 

df1mea.csv : US dataset
ECB dataset completed.csv : Euro Area dataset 
BOJ complete.csv : Japan dataset
US,Euro Area, Japan: reasons for changing lending policies

US:
  1. clean us data.R cleans all raw data and output df1ema.csv, which is used to analyze US credit dynamics. 
  2. xls files contains description on the data, and csv files don't. 
  3. Lendging Survey folder contains codes for extrating factors/reasons for changing lending policies.

ECB: 
  Contains data for Eura Area. Some of them are cleaned by 'hand'. 
  
BOJ: 
  Contains raw data for Japan and imputed data for bad loan data. A relatively easy way to extra data from BOJ's lending survey may be tabulapdf/tabula from https://github.com/tabulapdf/tabula . Converting the pdfs to xml/html may be inefficient.
  
_______________________________________

If you find any error,  please make a new issue. I will update the code and result (if necessary) as soon as possible. 
