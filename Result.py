import pandas as pd
from OPT import *

E.optimize()


Index = [v.VarName for v in V_D.values()]
value = [v.x for v in V_D.values()]
Solution_FD = [[] for i in range(len(Index))]
for i in range(len(Index)):
    Solution_FD[i].append(Index[i])
    Solution_FD[i].append(value[i])

Solution_FD = pd.DataFrame(Solution_FD,columns=['VarName', 'Reject Value'])
Solution_FD.to_csv('Result/FD.csv',index=False,header=False)

Index = [v.VarName for v in V_S.values()]
value = [v.x for v in V_S.values()]
Solution_FS = [[] for i in range(len(Index))]
for i in range(len(Index)):
    Solution_FS[i].append(Index[i])
    Solution_FS[i].append(value[i])

Solution_FS = pd.DataFrame(Solution_FS,columns=['VarName', 'Reject Value'])
Solution_FS.to_csv('Result/FS.csv',index=False,header=False)

Index = [v.VarName for v in xS.values()]
value = [v.x for v in xS.values()]
Solution_HS = [[]for i in range(len(J))]
for j in range(len(J)):
    for i in range(24):
        Solution_HS[j].append(value[len(J)*i+j])

Solution_HS = pd.DataFrame(Solution_HS)
Solution_HS
Solution_HS.to_csv('Result/HS.csv',index=False,header=False)

Index = [v.VarName for v in xD.values()]
value = [v.x for v in xD.values()]
Solution_HD = [[]for i in range(len(J))]
for j in range(len(J)):
    for i in range(24):
        Solution_HD[j].append(value[len(J)*i+j])

Solution_HD = pd.DataFrame(Solution_HD)
Solution_HD.to_csv('Result/HD.csv',index=False,header=False)

Index = [v.VarName for v in yD.values()]
value = [v.x for v in yD.values()]
Solution_YD = [[] for i in range(len(Index))]
for i in range(len(Index)):
    Solution_YD[i].append(Index[i])
    Solution_YD[i].append(value[i])

Solution_YD = pd.DataFrame(Solution_YD,columns=['VarName', 'Reject Value'])
Solution_YD.to_csv('Result/BD.csv',index=False,header=False)

Index = [v.VarName for v in yS.values()]
value = [v.x for v in yS.values()]
Solution_YS = [[] for i in range(len(Index))]
for i in range(len(Index)):
    Solution_YS[i].append(Index[i])
    Solution_YS[i].append(value[i])

Solution_YS = pd.DataFrame(Solution_YS,columns=['VarName', 'Reject Value'])
Solution_YS.to_csv('Result/BS.csv',index=False,header=False)