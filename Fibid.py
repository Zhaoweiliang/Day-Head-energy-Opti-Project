from gurobipy import *
import numpy as np
import pandas as pd
def Fibid():
    Data = pd.read_csv('/Users/weiliang/Desktop/project/Veri_1.in',header = None)
    Data.columns= ['ID','OrderID','Hour','BitType','Quantity','price','Duration','LinkID']

#extract flexible bits 
    Index = []
    for i in range(len(Data)):
        if Data['BitType'][i]=='F':
            Index.append(i)
    Data_F = Data.iloc[Index]
    Data_F = Data_F.reset_index(drop=True)

    #  spreate the demand and supply
    Index_D = []
    Index_S = []
    for i in range(len(Data_F)):
        if Data_F['Quantity'][i]<0:
            Index_D.append(i)
        else:
            Index_S.append(i)

    Data_F_D = Data_F.iloc[Index_S]
    Data_F_D = Data_F_D.reset_index(drop=True)
    Data_F_S = Data_F.iloc[Index_D]
    Data_F_S = Data_F_S.reset_index(drop=True)

    # convert the supply to postive 
    Data_F_SP = Data_F_S
    Data_F_SP['Quantity']=Data_F_SP['Quantity'].abs()
    return (Data_F_SP,Data_F_D)



