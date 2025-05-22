import numpy as np
from pulp import *

np.random.seed(42)
n, m = 20, 6
p = np.random.randint(5, 21, size=(n, m))

model = LpProblem("Flowshop_Assignment", LpMinimize)

x = [[LpVariable(f"x_{j}_{k}", cat=LpBinary) for k in range(n)] for j in range(n)]
I = [[LpVariable(f"I_{i}_{k}", lowBound=0) for k in range(n - 1)] for i in range(m)]
W = [[LpVariable(f"W_{i}_{k}", lowBound=0) for k in range(n)] for i in range(m - 1)]

# Objective as required by assignment slides
model += (
    lpSum(x[j][0] * p[j][i] for j in range(n) for i in range(m - 1)) +
    lpSum(I[m - 1][k] for k in range(n - 1))
)

# Constraints
for j in range(n):
    model += lpSum(x[j][k] for k in range(n)) == 1
for k in range(n):
    model += lpSum(x[j][k] for j in range(n)) == 1
for i in range(m - 1):
    model += W[i][0] == 0
for k in range(n - 1):
    model += I[0][k] == 0
for i in range(m - 1):
    for k in range(n - 1):
        lhs = I[i][k] + lpSum(x[j][k + 1] * p[j][i] for j in range(n)) + W[i][k + 1]
        rhs = W[i][k] + lpSum(x[j][k] * p[j][i + 1] for j in range(n)) + I[i + 1][k]
        model += lhs == rhs

model.solve()

# Job sequence
job_seq = [None] * n
for j in range(n):
    for k in range(n):
        if value(x[j][k]) == 1:
            job_seq[k] = j

# True start/finish time calculation
start = np.zeros((n, m))
finish = np.zeros((n, m))

for k in range(n):
    j = job_seq[k]
    for i in range(m):
        if i == 0 and k == 0:
            start[k][i] = 0
        elif i == 0:
            start[k][i] = finish[k - 1][i]
        elif k == 0:
            start[k][i] = finish[k][i - 1]
        else:
            start[k][i] = max(finish[k - 1][i], finish[k][i - 1])
        finish[k][i] = start[k][i] + p[j][i]

print("Job sequence:", job_seq)
print("True Makespan (Cmax):", finish[-1][-1])
print("Start time of first job on last machine:", start[0][-2])
print("Idle time on last machine (from model):", sum(value(I[m - 1][k]) for k in range(n - 1)))