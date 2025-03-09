from pulp import *

model = LpProblem(name="my-first-lp-problem",sense=LpMaximize)

x = LpVariable(name="x", lowBound=0)
y = LpVariable(name="y", lowBound=0)

model += (2 * x + y <= 20, "constraint 1")
model += (4 * x - 5 * y >= -10, "constraint 2")
model += (-x + 2 * y >= -2, "constraint 3")
model += (-x + 5 * y == 15, "constraint 4")

model += lpSum([x, 2 * y])

print(model)

model.solve()
print(LpStatus[model.status])


for v in model.variables():
    print(v.name, "=", v.varValue)

for name, c in list(model.constraints.items()):
    print(name, ":", c, "\t", c.pi, "\t\t", c.slack)