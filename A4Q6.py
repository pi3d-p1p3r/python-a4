from pulp import *

# Define supply, demand, and costs
supply = {'F1': 200, 'F2': 160, 'F3': 90}
demand = {'W1': 180, 'W2': 120, 'W3': 150}
costs = {
    'F1': {'W1': 16, 'W2': 20, 'W3': 12},
    'F2': {'W1': 14, 'W2': 8, 'W3': 18},
    'F3': {'W1': 26, 'W2': 24, 'W3': 16}
}

# Create the linear programming problem
prob = LpProblem("Transportation_Problem", LpMinimize)

# Define decision variables
vars = LpVariable.dicts("Route", (supply.keys(), demand.keys()), 0, None, LpContinuous)

# Set the objective function (minimize total cost)
prob += lpSum([vars[f][w] * costs[f][w] for f in supply for w in demand]), "Total Cost"

# Add supply constraints
for f in supply:
    prob += lpSum([vars[f][w] for w in demand]) == supply[f], f"Supply_{f}"

# Add demand constraints
for w in demand:
    prob += lpSum([vars[f][w] for f in supply]) == demand[w], f"Demand_{w}"

# Solve the problem
prob.solve()

# Print the results
print("Status:", LpStatus[prob.status])
print("\nOptimal Shipping Plan:")
for v in prob.variables():
    if v.varValue > 0:
        print(f"{v.name.replace('_', ' to ')}: {v.varValue} units")
print(f"\nTotal Shipping Cost: {value(prob.objective)} BDT")