from pulp import *

months = list(range(1, 13))

base_demand = {
    1: 280, 2: 301, 3: 277, 4: 510, 5: 285, 6: 278,
    7: 291, 8: 220, 9: 304, 10: 295, 11: 302, 12: 297}

# parameters
initial_inventory = 150
final_inventory = 150
safety_stock = 100
production_capacity = 320
material_cost = 1000
labor_cost = 10
inventory_cost = 100
subcontracting_cost = 1200
selling_price = 2600
promo_price = 2340  # discounted price in a promotion month


# function to adjust demand based on promotions
def adjust_demand(qh_promo=None, unilock_promo=None):
    qh_demand = base_demand.copy()
    unilock_demand = base_demand.copy()

    for promo_month in [qh_promo, unilock_promo]:
        if promo_month is not None and promo_month <= 10:  # last two months can't have forward buying
            if qh_promo == promo_month and unilock_promo == promo_month:
                # both firms promote -> no total demand increase, only forward buying occurs
                lost_demand_qh_1 = qh_demand[promo_month + 1] * 0.25
                lost_demand_qh_2 = qh_demand[promo_month + 2] * 0.25
                lost_demand_unilock_1 = unilock_demand[promo_month + 1] * 0.25
                lost_demand_unilock_2 = unilock_demand[promo_month + 2] * 0.25

                # apply forward buying reduction
                qh_demand[promo_month + 1] *= 0.75
                qh_demand[promo_month + 2] *= 0.75
                unilock_demand[promo_month + 1] *= 0.75
                unilock_demand[promo_month + 2] *= 0.75

                # transfer lost demand
                unilock_demand[promo_month] += lost_demand_unilock_1 + lost_demand_unilock_2
                qh_demand[promo_month] += lost_demand_qh_1 + lost_demand_qh_2


            elif qh_promo == promo_month:
                # q&h promotes -> its demand increases by 50%
                qh_demand[promo_month] = qh_demand[promo_month] * 1.5


                # forward buying effect
                lost_demand_1 = qh_demand[promo_month + 1] * 0.2
                lost_demand_2 = qh_demand[promo_month + 2] * 0.2
                qh_demand[promo_month + 1] *= 0.8
                qh_demand[promo_month + 2] *= 0.8

                # q&h gains the lost forward buying demand
                qh_demand[promo_month] += lost_demand_1 + lost_demand_2


            elif unilock_promo == promo_month:
                # unilock promotes -> reducing q&h's demand by 50%
                qh_demand[promo_month] = qh_demand[promo_month] * 0.5  # q&h loses customers


    return qh_demand, unilock_demand

def solve_profit_optimization(firm_name, demand, promo_month=None):
    model = LpProblem(f"Profit_Maximization_{firm_name}", LpMaximize)

    # decision variables
    P = {t: LpVariable(f"P_{firm_name}_{t}", lowBound=0) for t in months}
    C = {t: LpVariable(f"C_{firm_name}_{t}", lowBound=0) for t in months}
    S = {t: LpVariable(f"S_{firm_name}_{t}", lowBound=0) for t in months}

    # objective function
    model += lpSum(
        (promo_price if t == promo_month else selling_price) * demand[t] -
        ((material_cost + labor_cost) * P[t] + subcontracting_cost * C[t] + inventory_cost * S[t])
        for t in months)

    # inventory balance constraints
    for t in months:
        if t == 1:
            model += initial_inventory + P[t] + C[t] - demand[t] == S[t]
        else:
            model += S[t - 1] + P[t] + C[t] - demand[t] == S[t]

    # production capacity constraint
    for t in months:
        model += P[t] <= production_capacity

    # safety stock constraint
    for t in months:
            model += S[t] >= safety_stock

    # final stock constraint
    model += S[12] == final_inventory


    model.solve()

    print(f"\n{firm_name} Solution Status: {LpStatus[model.status]}")
    print(f"{firm_name} Total Profit: {value(model.objective)}")

    for t in months:
        print(f"Month {t}: Production={P[t].varValue}, Subcontract={C[t].varValue}, Stock={S[t].varValue}")

    return value(model.objective)
# Both firms promote in August
qh_demand, unilock_demand = adjust_demand(qh_promo=8, unilock_promo=8)
qh_profit = solve_profit_optimization("QH", qh_demand, promo_month=8)
unilock_profit = solve_profit_optimization("Unilock", unilock_demand, promo_month=8)
