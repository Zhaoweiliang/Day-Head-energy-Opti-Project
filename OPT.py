from gurobipy import *
import numpy as np
import pandas as pd
from Hourbid import *
from Fibid import *
from blockbid import *

# Import the bids data
BS_bids = Blockbid()[0]
BD_bids = Blockbid()[1]
HS_bids = HourBid()[0]
HD_bids = HourBid()[1]
FS_bids = Fibid()[0]
FD_bids = Fibid()[1]

# length of the bids
L_D = len(BD_bids)
L_S = len(Blockbid()[0])

NoneChild_D=[]
Child_D = []
Parent_D=[]
NoneChild_S=[]
Child_S=[]
Parent_S=[]
for i in range(L_D):
    if BD_bids.isnull()['LinkID'][i] == True:
        NoneChild_D.append(i)
    else:
        Parent_D.append(np.where(BD_bids['ID']==BD_bids['LinkID'][i])[0][0])
        Child_D.append(i)
for i in range(L_S):
    if BS_bids.isnull()['LinkID'][i] == True:
        NoneChild_S.append(i)
    else:
        Parent_S.append(np.where(BS_bids['ID']==BS_bids['LinkID'][i])[0][0])
        Child_S.append(i)
        

L_FD = len(Fibid()[1])
L_FS = len(Fibid()[0])
J = np.arange(1,find_largest(HIndex_D)+1)
K = np.arange(1,find_largest(HIndex_S)+1)

# 24 Hours 
H = np.arange(1,25)


#Delta variables
Delta_S = np.zeros([L_S,24])
Delta_D = np.zeros([L_D,24])
# For Demand
for i in range (L_D):
    if BD_bids['Hour'][i]+BD_bids['Duration'][i]<=25:
        Delta_D[i,BD_bids['Hour'][i]-1:(BD_bids['Hour'][i]+BD_bids['Duration'][i])-1] = 1
#For Demand
for i in range (L_S):
    if BS_bids['Hour'][i]+BS_bids['Duration'][i]<=25:
        Delta_S[i,BS_bids['Hour'][i]-1:(BS_bids['Hour'][i]+BS_bids['Duration'][i])-1] = 1
        
#Find the Max and min value for each hour        
def find_F(Del,leng,bids):
    Res = [[] for i in range(24)]
    Res_max = [[] for i in range(24)]
    Res_min = [[] for i in range(24)]
    for i in range (24):
        for j in range(leng):
            if Del[j,i] == 1:
                Res[i].append(bids['price'][j])
    for i in range(24):
        Res_max[i] = np.max(Res[i])
        Res_min[i] = np.min(Res[i])
    return(Res_max,Res_min)
# Max and min for flexible bids
FD_min = np.min(FD_bids['price'])
FD_max = np.max(FD_bids['price'])
FS_min = np.min(FS_bids['price'])
FS_max = np.max(FS_bids['price'])

# Find the max and min for block bid and stored in the form like : [Hour,Block,Flex]
DMax_Res = [[] for i in range(24)]
Dm_Res = [[] for i in range(24)]
SMax_Res = [[] for i in range(24)]
Sm_Res = [[] for i in range(24)]

for i in range(24):
    DMax_Res[i].append(HD_bids['price'][HIndex_D[i][0]])
    DMax_Res[i].append(find_F(Delta_D,L_D,BD_bids)[0][i])
    DMax_Res[i].append(FD_max)
    
for i in range(24):
    SMax_Res[i].append(HS_bids['price'][HIndex_S[i][1]])
    SMax_Res[i].append(find_F(Delta_S,L_S,BS_bids)[0][i])
    SMax_Res[i].append(FS_max)
    
for i in range(24):
    Dm_Res[i].append(HD_bids['price'][HIndex_D[i][1]])
    Dm_Res[i].append(find_F(Delta_D,L_D,BD_bids)[1][i])
    Dm_Res[i].append(FD_min)
    
for i in range(24):
    Sm_Res[i].append(HS_bids['price'][HIndex_S[i][0]])
    Sm_Res[i].append(find_F(Delta_S,L_S,BS_bids)[1][i])
    Sm_Res[i].append(FS_min)
    
# Create the Model    
E = Model("Energy")
E.params.NonConvex =2
E.update()

# Add variables
# solution variables X for demand and supply in Hourly Bids
xD = E.addVars(H,J,ub=1,lb=0,  vtype=GRB.CONTINUOUS, name='xD')
xS = E.addVars(H,J,ub=1,lb=0,  vtype=GRB.CONTINUOUS, name='xS')

# Auxiliary variables for demand and supply
w_D = E.addVars(H,J,ub=1,lb=0,  vtype=GRB.BINARY,name ='W_D')
w_S = E.addVars(H,J,ub=1,lb=0,  vtype=GRB.BINARY,name ='W_S')

#solution variables Y for demand and supply in Block Bids
yD = E.addVars(L_D,ub=1,lb=0,  vtype=GRB.BINARY,name ='yD')
yS = E.addVars(L_S,ub=1,lb=0,  vtype=GRB.BINARY,name ='yS')

# Market clearing price at time H for demand and supply
F_z = E.addVars(H,lb = 0,vtype=GRB.CONTINUOUS, name='F_ZS')

# solution variables V for demand and supply in Hourly Bids
V_S = E.addVars(H,L_FS,lb=0,vtype=GRB.BINARY,name = 'V_S')
V_D = E.addVars(H,L_FD,lb=0,vtype=GRB.BINARY,name = 'V_D')

# Add Objective Function
# Hour Demand Part 
# Hour Supply Part
# Block Part
# Flexbile Part
# First segment for Hour Demand
E.setObjective(sum(0.5*(2*Pair(j,h,HD_bids,'DP')[0]+xD[h,j]*(Pair(j,h,HD_bids,'DP')[1]-Pair(j,h,HD_bids,'DP')[0]))*xD[h,j]*(Pair(j,h,HD_bids,'DQ')[1]-Pair(j,h,HD_bids,'DQ')[0])for j in J for h in H)
                -sum(0.5*(2*Pair(j,h,HS_bids,'SP')[0]+xS[h,j]*(Pair(j,h,HS_bids,'SP')[1]-Pair(j,h,HS_bids,'SP')[0]))*xS[h,j]*(Pair(j,h,HS_bids,'SQ')[1]-Pair(j,h,HS_bids,'SQ')[0])for j in J for h in H)
                +sum(BD_bids['Duration'][i]*BD_bids['Quantity'][i]*BD_bids['price'][i]*yD[i] for i in range(L_D)) - sum(BS_bids['Duration'][i]*BS_bids['Quantity'][i]*BS_bids['price'][i]*yS[i] for i in range(L_S))
                +sum(FD_bids['Quantity'][i]*FD_bids['price'][i] for i in range(L_FD))*sum(V_D[h,i]for i in range(L_FD) for h in H)-sum(FS_bids['Quantity'][i]*FS_bids['price'][i] for i in range(L_FS))*sum(V_S[h,i]for i in range(L_FS) for h in H)
                +sum(Pair(1,h,HD_bids,'DQ')[0]-Pair(1,h,HD_bids,'DP')[0] for h in H)
                
,GRB.MAXIMIZE)

gamma = 1000000

        # (2)
E.addConstrs(-sum((Pair(j,h,HD_bids,'DQ')[1]-Pair(j,h,HD_bids,'DQ')[0]) * xD[h,j] for j in J ) +sum((Pair(j,h,HS_bids,'SQ')[1]-Pair(j,h,HS_bids,'SQ')[0])*xS[h,j] for j in J) -Pair(1,h,HD_bids,'DQ')[0] +Pair(1,h,HS_bids,'SQ')[0] 
                    +sum(Delta_S[i,h-1]*BS_bids['Quantity'][i]*yS[i] for i in range(L_S))  -sum(Delta_D[i,h-1]*BD_bids['Quantity'][i]*yD[i] for i in range(L_D))
                    +sum(FS_bids['Quantity'][i]*V_S[h,i]for i in range(L_FS))-sum(FD_bids['Quantity'][i]*V_D[h,i]for i in range(L_FD))
                    
                    ==0 for h in H) 
 


E.addConstrs(F_z[h] == Sm_Res[h-1][0]+sum((Pair(j,h,HS_bids,'SP')[1]-Pair(j,h,HS_bids,'SP')[0]) * xS[h,j] for j in J)for h in H)        
E.addConstrs(F_z[h] == DMax_Res[h-1][0]+sum((Pair(j,h,HD_bids,'DP')[1]-Pair(j,h,HD_bids,'DP')[0]) * xD[h,j] for j in J) for h in H)
# (8)

E.addConstrs(-BS_bids['Duration'][j]* BS_bids['price'][j]+ sum(Delta_S[j,h-1]*F_z[h] for h in H ) <= yS[j]*gamma for j in NoneChild_S)
# (9)

E.addConstrs(BD_bids['Duration'][j]*BD_bids['price'][j]- sum(Delta_S[j,h-1]*F_z[h] for h in H) <= yD[j]*gamma for j in NoneChild_D)
        
    # E.addConstr(if Blockbid['LinkID'][j] == 'NaN': Blockbid['Duration'][j]*Blockbid['price'][j]+ sum(Delta_S[j,h]*F_z[h] for j in J) <= yd[j]*gamma)
        
# (3)(4)
# Demand
E.addConstrs(w_D[h,1]<=xD[h,1] for h in H)
E.addConstrs(xD[h,1] <=1 for h in H)
E.addConstrs(w_D[h,j]<=xD[h,j] for j in range(2,find_largest(HIndex_D)) for h in H)
E.addConstrs(xD[h,j]<=w_D[h,j-1] for j in range(2,find_largest(HIndex_D)) for h in H)
E.addConstrs(0<= xD[h,999] for h in H)
E.addConstrs(xD[h,999] <= w_D[h,998] for h in H)

# Supply
E.addConstrs(w_S[h,1]<=xS[h,1] for h in H)
E.addConstrs(xS[h,1] <=1 for h in H)
E.addConstrs(w_S[h,j]<=xS[h,j] for j in range(2,find_largest(HIndex_S)) for h in H)
E.addConstrs(xS[h,j]<=w_S[h,j-1] for j in range(2,find_largest(HIndex_S)) for h in H)
E.addConstrs(0<= xS[h,999] for h in H)
E.addConstrs(xS[h,999] <= w_S[h,998] for h in H)


E.addConstrs(sum(V_S[h,i] for h in H )<= 1 for i in range(L_FS) )
E.addConstrs(sum(V_D[h,i] for h in H )<= 1 for i in range(L_FD) )

E.addConstrs(F_z[h]-FS_bids['price'][i] <= gamma*sum(V_S[k,i] for k in H) for i in range(L_FS) for h in H)
E.addConstrs(FD_bids['price'][i]-F_z[h]<=gamma*sum(V_D[k,i] for k in H) for i in range(L_FD) for h in H)

E.addConstrs(yD[Child_D[i]]<=yD[Parent_D[i]] for i in range(len(Child_D)))
E.addConstrs(yS[Child_S[i]]<=yS[Parent_S[i]] for i in range(len(Child_S)))




E.optimize()