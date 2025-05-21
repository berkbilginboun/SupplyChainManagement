import numpy as np
from pulp import *

np.random.seed(42)
n, m = 20, 6
p = np.random.randint(5, 21, size=(n, m))

model = LpProblem("flowshop", LpMinimize)

# x = iş j sırada k'daysa 1 olcak
x = [[LpVariable(f"x_{j}_{k}", cat=LpBinary) for k in range(n)] for j in range(n)]

# idle ve bekleme süresi
I = [[LpVariable(f"I_{i}_{k}", lowBound=0) for k in range(n - 1)] for i in range(m)]
W = [[LpVariable(f"W_{i}_{k}", lowBound=0) for k in range(n)] for i in range(m - 1)]

# amaç: ilk iş ve son makinadaki boşluklar
model += (
    lpSum(x[j][0] * p[j][i] for j in range(n) for i in range(m - 1)) +
    lpSum(I[m - 1][k] for k in range(n - 1))
)

# her sıraya 1 iş, her işe 1 sıra
for k in range(n):
    model += lpSum(x[j][k] for j in range(n)) == 1
for j in range(n):
    model += lpSum(x[j][k] for k in range(n)) == 1

# ilklerde bekleme yok
for i in range(m - 1):
    model += W[i][0] == 0
for k in range(n - 1):
    model += I[0][k] == 0

# denklem - zaman akışı
for i in range(m - 1):
    for k in range(n - 1):
        a = I[i][k] + lpSum(x[j][k + 1] * p[j][i] for j in range(n)) + W[i][k + 1]
        b = W[i][k] + lpSum(x[j][k] * p[j][i + 1] for j in range(n)) + I[i + 1][k]
        model += a == b

model.solve()

job_seq = [None] * n
for j in range(n):
    for k in range(n):
        if value(x[j][k]) == 1:
            job_seq[k] = j

print("sirala:", job_seq)
print("cmax:", value(model.objective))
print("idle son makina:", sum(value(I[m - 1][k]) for k in range(n - 1)))

first = job_seq[0]
start_last = sum(p[first][i] for i in range(m - 1))
print("ilk iş ne zmn başlyo son mknd:", start_last)