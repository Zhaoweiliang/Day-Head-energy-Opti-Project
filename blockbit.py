from gurobipy import *
import numpy as np
import pandas as pd
def Blockbit():
    Data = pd.read_csv('/Users/weiliang/Desktop/project/Veri_1.in',header = None)
    Data.columns= ['ID','OrderID','Hour','BitType','Quantity','price','Duration','LinkID']

#extract flexible bits 
    Index = []
    for i in range(len(Data)):
        if Data['BitType'][i]=='B':
            Index.append(i)
    Data_B = Data.iloc[Index]
    Data_B = Data_B.reset_index(drop=True)

    #  spreate the demand and supply
    Index_D = []
    Index_S = []
    for i in range(len(Data_B)):
        if Data_B['Quantity'][i]<0:
            Index_D.append(i)
        else:
            Index_S.append(i)

    Data_B_D = Data_B.iloc[Index_S]
    Data_B_D = Data_B_D.reset_index(drop=True)
    Data_B_S = Data_B.iloc[Index_D]
    Data_B_S = Data_B_S.reset_index(drop=True)

    # convert the supply to postive 
    Data_B_SP = Data_B_S
    Data_B_SP['Quantity']=Data_B_SP['Quantity'].abs()
    return (Data_B_SP,Data_B_D)



