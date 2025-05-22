import numpy as np
from pulp import *

# -------------------------------
# Parameters
np.random.seed(42)
n_jobs = 20
n_machines = 6
processing_times = np.random.randint(5, 21, size=(n_jobs, n_machines))

# -------------------------------
# Model
model = LpProblem("Permutation_Flowshop_Scheduling", LpMinimize)

# Decision variables
x = LpVariable.dicts("x", ((j, k) for j in range(n_jobs) for k in range(n_jobs)), cat="Binary")
I = LpVariable.dicts("I", ((i, k) for i in range(n_machines) for k in range(n_jobs - 1)), lowBound=0)
W = LpVariable.dicts("W", ((i, k) for i in range(n_machines - 1) for k in range(n_jobs)), lowBound=0)

# Objective function (minimize idle time on last machine + early processing)
model += (
    lpSum(x[j, 0] * processing_times[j][i] for i in range(n_machines - 1) for j in range(n_jobs)) +
    lpSum(I[n_machines - 1, k] for k in range(n_jobs - 1))
)

# Assignment constraints
for k in range(n_jobs):
    model += lpSum(x[j, k] for j in range(n_jobs)) == 1
for j in range(n_jobs):
    model += lpSum(x[j, k] for k in range(n_jobs)) == 1

# Flow constraints
for k in range(n_jobs - 1):
    for i in range(n_machines - 1):
        lhs = I[i, k] + lpSum(x[j, k + 1] * processing_times[j][i] for j in range(n_jobs)) + W[i, k + 1]
        rhs = W[i, k] + lpSum(x[j, k] * processing_times[j][i + 1] for j in range(n_jobs))
        if (i + 1, k) in I:
            rhs += I[i + 1, k]
        model += lhs == rhs

# Boundary conditions
for i in range(n_machines - 1):
    model += W[i, 0] == 0
for k in range(n_jobs - 1):
    model += I[0, k] == 0

# -------------------------------
# Solve
model.solve(PULP_CBC_CMD(msg=True))
print("Model status:", LpStatus[model.status])
if LpStatus[model.status] != "Optimal":
    model.writeLP("infeasible_model.lp")
    exit()

# -------------------------------
# Extract optimal sequence
sequence = [None] * n_jobs
for k in range(n_jobs):
    for j in range(n_jobs):
        if round(value(x[j, k])) == 1:
            sequence[k] = j

print("✅ Optimal Job Sequence:", sequence)

# -------------------------------
# Question Answers

# Q1: Cmax
cmax = sum(processing_times[sequence[k]][-1] for k in range(n_jobs)) + \
       sum(value(I[n_machines - 1, k]) for k in range(n_jobs - 1))
print(f"📦 Cmax (Makespan): {round(cmax, 2)}")

# Q2: When does the first job (sequence[0]) reach the last machine?
first_job = sequence[0]
start_time_on_last_machine = sum(processing_times[first_job][i] for i in range(n_machines - 1))
print(f"🕒 First job (#{first_job}) reaches last machine at: {start_time_on_last_machine}")

# Q3: Total idle time on the last machine
idle_last_machine = sum(value(I[n_machines - 1, k]) for k in range(n_jobs - 1))
print(f"⏱ Total idle time on last machine: {round(idle_last_machine, 2)}")