import numpy as np
from pulp import *

np.random.seed(42)
n, m = 20, 6
p = np.random.randint(5, 21, size=(n, m))

model = LpProblem("flowshop", LpMinimize)

# Decision variables
x = [[LpVariable(f"x_{j}_{k}", cat=LpBinary) for k in range(n)] for j in range(n)]
I = [[LpVariable(f"I_{i}_{k}", lowBound=0) for k in range(n - 1)] for i in range(m)]
W = [[LpVariable(f"W_{i}_{k}", lowBound=0) for k in range(n)] for i in range(m - 1)]

# Objective function
model += (
    lpSum(x[j][0] * p[j][i] for j in range(n) for i in range(m - 1)) +
    lpSum(I[m - 1][k] for k in range(n - 1))
)

# Assignment constraints
for k in range(n):
    model += lpSum(x[j][k] for j in range(n)) == 1
for j in range(n):
    model += lpSum(x[j][k] for k in range(n)) == 1

# Initial conditions
for i in range(m - 1):
    model += W[i][0] == 0
for k in range(n - 1):
    model += I[0][k] == 0

# Flow constraints
for i in range(m - 1):
    for k in range(n - 1):
        left = I[i][k] + lpSum(x[j][k + 1] * p[j][i] for j in range(n)) + W[i][k + 1]
        right = W[i][k] + lpSum(x[j][k] * p[j][i + 1] for j in range(n)) + I[i + 1][k]
        model += left == right

model.solve()

job_seq = [None] * n
for j in range(n):
    for k in range(n):
        if value(x[j][k]) == 1:
            job_seq[k] = j

print("Job sequence:", job_seq)
print("Cmax:", value(model.objective))
print("Idle time on last machine:", sum(value(I[m - 1][k]) for k in range(n - 1)))

first = job_seq[0]
start_last = sum(p[first][i] for i in range(m - 1))
print("Start time of first job on last machine:", start_last)