import numpy as np
from scipy.optimize import linprog

c = [-12, -15, -14]  # Negative because linprog minimizes

A_ub = [
    [1, 1, 1],        # Total weight constraint
    [0, -1, 2],       # Ash content constraint
    [-0.01, 0.01, 0]  # Phosphorous content constraint
]

# Right-hand side of constraints
b_ub = [100, 0, 0]

# Bounds for variables (all non-negative)
bounds = [(0, None), (0, None), (0, None)]

# Solve using simplex method
result = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='simplex')

print("Optimization status:", result.message)
print("\nOptimal solution:")
print(f"Coal A: {result.x[0]:.2f} tons")
print(f"Coal B: {result.x[1]:.2f} tons")
print(f"Coal C: {result.x[2]:.2f} tons")
print(f"Total: {sum(result.x):.2f} tons")

print("\nTotal profit: {:.2f} BDT".format(-result.fun))

# Let's verify our constraints are met
print("\nVerification:")
total_ash = (3*result.x[0] + 2*result.x[1] + 5*result.x[2]) / sum(result.x) * 100
total_phosphorous = (0.02*result.x[0] + 0.04*result.x[1] + 0.03*result.x[2]) / sum(result.x) * 100

print(f"Ash percentage: {total_ash/100:.4f}% (limit: 3%)")
print(f"Phosphorous percentage: {total_phosphorous/100:.4f}% (limit: 0.03%)")
