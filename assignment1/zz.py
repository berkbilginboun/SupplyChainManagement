# Question 7: Both firms promote in April
qh_demand, unilock_demand = adjust_demand(qh_promo=4, unilock_promo=4)
qh_profit = solve_profit_optimization("QH", qh_demand, promo_month=4)
unilock_profit = solve_profit_optimization("Unilock", unilock_demand, promo_month=4)

# Question 8: Both firms promote in August
qh_demand, unilock_demand = adjust_demand(qh_promo=8, unilock_promo=8)
qh_profit = solve_profit_optimization("QH", qh_demand, promo_month=8)
unilock_profit = solve_profit_optimization("Unilock", unilock_demand, promo_month=8)

# Question 9: Q&H promotes in April, Unilock promotes in August
qh_demand, unilock_demand = adjust_demand(qh_promo=4, unilock_promo=8)
qh_profit = solve_profit_optimization("QH", qh_demand, promo_month=4)
unilock_profit = solve_profit_optimization("Unilock", unilock_demand, promo_month=8)

# Question 10: Q&H promotes in August, Unilock promotes in April
qh_demand, unilock_demand = adjust_demand(qh_promo=8, unilock_promo=4)
qh_profit = solve_profit_optimization("QH", qh_demand, promo_month=8)
unilock_profit = solve_profit_optimization("Unilock", unilock_demand, promo_month=4)