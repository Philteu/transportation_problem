"""
P&T Co. Tranpoartation Problem
"""

from pulp import *
import pandas as pd

#initalize the model 
model = LpProblem('P&T Co. Transportation Problem', LpMinimize)

#Define the decision Variable
cannery =['C1', 'C2','C3']
warehouse  =['W1', 'W2', 'W3', 'W4']
cost= {('C1','W1'):464, ('C1','W2'):513, ('C1','W3'):654, ('C1','W4'):867,
       ('C2','W1'):352, ('C2','W2'):416, ('C2','W3'):690, ('C2','W4'):791,
       ('C3','W1'):995, ('C3','W2'):682, ('C3','W3'):388, ('C3','W4'):685}
supply= {'C1':75, 'C2': 125, 'C3': 100}
demand = {'W1': 80, 'W2': 65, 'W3':70, 'W4':85 }

quantity = LpVariable.dicts("Shipping Quantity", [(c,w) for c in cannery for w in warehouse],
                        lowBound=0, cat='Integer')

#Define Objective Function
model += lpSum([cost[(c,w)] * quantity[(c,w)] for c in cannery for w in warehouse])

#Define Constraints
for w in warehouse: 
    model += lpSum([quantity[('C1', w)]] + [quantity[('C2', w)]] + [quantity[('C3', w)]]) ==demand[w]  
    
for c in cannery: 
    model += lpSum([quantity[(c, 'W1')]] + [quantity[(c, 'W2')]] +  [quantity[(c, 'W3')]] 
                   + [quantity[(c, 'W4')]] )  == supply[c] 

#Solve the model
model.solve()
print ("Status:", LpStatus[model.status])
o = [{'W1':quantity[(c,'W1')].varValue, 'W2':quantity[(c,'W2')].varValue, 'W3':quantity[(c,'W3')].varValue,
      'W4':quantity[(c,'W4')].varValue} for c in cannery]
o= pd.DataFrame(o, index = cannery)
print(o)
print("Total shipping cost expected of meeting demands = ${}".format(value(model.objective)))

#Sensitive Analysis
print(pd.DataFrame([{'name':name, 'shadow price': con.pi, 'slack':con.slack} 
                    for name, con in model.constraints.items()]))
