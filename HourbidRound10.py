from gurobipy import *
import numpy as np
import pandas as pd

Data = pd.read_csv('Veri_1.in',header = None)
Data.columns= ['ID','OrderID','Hour','BitType','Quantity','price','Duration','LinkID']
def HourBid():
    Index = []
    for i in range(len(Data)):
        if Data['BitType'][i]=='S':
            Index.append(i)
    Data_H = Data.iloc[Index]
    Data_H = Data_H.reset_index(drop=True)
    Index_D = []
    Index_S = []
    for i in range(len(Data_H)):
        if Data_H['Quantity'][i]<0:
            Index_D.append(i)
        else:
            Index_S.append(i)
    Index_DR = []
    INT = [999,1999,2999,3999,4999,5999,6999,7999,8999,9999,10999,11999,12999,13999,14999,15999,16999,17999,18999,19999,20999,21999,22999,23999]
    for i in range(24):
        for j in range(1000):
            # print(999*(i+1)-j)
            Index_DR.append(Index_S[INT[i]-j])

    Data_H_D = Data_H.iloc[Index_DR]
    Data_H_D = Data_H_D.reset_index(drop=True)
    Data_H_S = Data_H.iloc[Index_D]
    Data_H_S = Data_H_S.reset_index(drop=True)
    Data_H_SP = Data_H_S
    # for i in range(len(Data_H_SP)):
        
    #     Data_H_SP['Quantity'][i] = Data_H_S['Quantity'][i]
    Data_H_SP['Quantity']=Data_H_SP['Quantity'].abs()


    Data_H_D['Quantity']=Data_H_D['Quantity'].round(-1)
    Data_H_D['price']=Data_H_D['price'].round(-1)

    Data_H_SP['Quantity']=Data_H_SP['Quantity'].round(-1)
    Data_H_SP['price']=Data_H_SP['price'].round(-1)
    
    HS_Round = Data_H_SP[0:1000].drop_duplicates(subset=['price'])
    for i in range(1,24):
        HS_Round=HS_Round.append(Data_H_SP[1000*i:1000*(i+1)].drop_duplicates(subset=['price']))
    HS_Round=HS_Round.reset_index(drop=True)


    HD_Round = Data_H_D[0:1000].drop_duplicates(subset=['price'])
    for i in range(1,24):
        HD_Round=HD_Round.append(Data_H_D[1000*i:1000*(i+1)].drop_duplicates(subset=['price']))
    HD_Round=HD_Round.reset_index(drop=True)






    return(HS_Round,HD_Round,Index_DR)

def Hour_Index(df):
    Index = []
    S = 0
    End = 0
    Hour_list = np.arange(1,25)
    for i in range(24):
        for j in range(len(df)):
            if df['Hour'][j]==Hour_list[i]:
                End = j+1
        Index.append((S,End-1))
        S = End
    return Index
            
HIndex_S=Hour_Index(HourBid()[0])
HIndex_D=Hour_Index(HourBid()[1])

def find_largest(IND):
    Res = IND[0][1]-IND[0][1]
    for i in range(len(IND)):
        if (IND[i][1]-IND[i][0])>=Res:
            Res = (IND[i][1]-IND[i][0])
    return Res

def Pair(postion,Hour,DF,QP):
    
    if QP == 'DQ':
        DF=DF.iloc[HIndex_D[Hour-1][0]:HIndex_D[Hour-1][1]+1]
        return [DF['Quantity'][postion-1+HIndex_D[Hour-1][0]],DF['Quantity'][postion+HIndex_D[Hour-1][0]]]
    if QP == 'SQ':
        DF=DF.iloc[HIndex_S[Hour-1][0]:HIndex_S[Hour-1][1]+1]
        return [DF['Quantity'][postion-1+HIndex_S[Hour-1][0]],DF['Quantity'][postion+HIndex_S[Hour-1][0]]]
    if QP == 'DP':
        DF=DF.iloc[HIndex_D[Hour-1][0]:HIndex_D[Hour-1][1]+1]
        return [DF['price'][postion-1+HIndex_D[Hour-1][0]],DF['price'][postion+HIndex_D[Hour-1][0]]]
    else:
        DF=DF.iloc[HIndex_S[Hour-1][0]:HIndex_S[Hour-1][1]+1]
        return [DF['price'][postion-1+HIndex_S[Hour-1][0]],DF['price'][postion+HIndex_S[Hour-1][0]]]
