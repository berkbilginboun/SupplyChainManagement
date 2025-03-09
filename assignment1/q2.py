from pulp import *

months = list(range(1,13))

demand = {1: 280,  2: 301,  3: 277,  4: 510,  5: 285,  6: 278, 7: 291,  8: 220,  9: 304, 10: 295, 11: 302, 12: 297}

#paramaters
initial_inventory = 150
final_inventory = 150
safety_stock = 100
production_capacity = 32000
material_cost = 1000
labor_cost = 10
inventory_cost = 100
subcontracting_cost = 1200
selling_price = 2600

model = LpProblem("Profit_maximization", LpMaximize)

#decision var
P = {t : LpVariable(name=f"P_{t}", lowBound= 0) for t in months} #production
C = {t : LpVariable(name=f"C_{t}",lowBound=0)for t in months} #subcontract production
S = {t : LpVariable(name=f"S_{t}",lowBound=0)for t in months} #stock

#objective function
model += lpSum(selling_price*demand[t] -
               ((material_cost + labor_cost) * P[t] + subcontracting_cost * C[t] + inventory_cost * S[t])
               for t in months)

#constraints

#stock constraint
for t in months:
    if t == 1:
        model += initial_inventory + P[t] + C[t] - demand[t] == S[t]
    else:
        model += S[t-1] + P[t] + C[t] - demand[t] == S[t]

#production capacity constraint
for t in months:
    model += P[t] <= production_capacity

#safety stock capacity constraint
for t in months:
        model += S[t] >= safety_stock

#final stock constraint
model += S[12] == final_inventory

model.solve()
print(LpStatus[model.status])

for t in months:
    print(f"Month {t}: Production={P[t].varValue}, Subcontract={C[t].varValue}, Stock={S[t].varValue}")

print("Total cost:", value(model.objective))