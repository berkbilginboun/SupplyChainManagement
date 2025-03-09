from pulp import *

months = list(range(1,13))

demand = {1: 280,  2: 301,  3: 277,  4: 510,  5: 285,  6: 278, 7: 291,  8: 220,  9: 304, 10: 295, 11: 302, 12: 297}

promo_month = 8 #augusut
demand_promo = demand.copy()

if promo_month <= 10: # it cant be in last 2 months because of 3 months effects
    demand_promo[promo_month] = 1.5 * demand[promo_month] + 0.2 * (demand[promo_month + 1] + demand[promo_month + 2])
    demand_promo[promo_month + 1] = 0.8 * demand[promo_month + 1]
    demand_promo[promo_month + 2] = 0.8 * demand[promo_month + 2]

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
promo_price = 2340

model = LpProblem("Profit_maximization", LpMaximize)

#decision var
P = {t : LpVariable(name=f"P_{t}", lowBound= 0) for t in months} #production
C = {t : LpVariable(name=f"C_{t}",lowBound=0)for t in months} #subcontract production
S = {t : LpVariable(name=f"S_{t}",lowBound=0)for t in months} #stock

model += lpSum(
    (promo_price if t == promo_month else selling_price) * demand_promo[t] -
    ((material_cost + labor_cost) * P[t] + subcontracting_cost * C[t] + inventory_cost)
    for t in months
)

#constraints

#stock constraint
for t in months:
    if t == 1:
        model += initial_inventory + P[t] + C[t] - demand_promo[t] == S[t]
    else:
        model += S[t-1] + P[t] + C[t] - demand_promo[t] == S[t]

#production constraint
for t in months:
    model += P[t] <= production_capacity

#safety constraint
for t in months:
        model += S[t] >= safety_stock

#final stock constraint
model += S[12] == final_inventory

model.solve()
print(LpStatus[model.status])

for t in months:
    print(f"Month {t}: Production={P[t].varValue}, Subcontract={C[t].varValue}, Stock={S[t].varValue}")

print("Total cost:", value(model.objective))