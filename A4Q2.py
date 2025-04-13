import numpy as np
from scipy.optimize import linprog

# Define the problem parameters
# Cost per unit for each food type
costs = np.array([45, 40, 85, 65])

# Yields per unit for each nutrient type
# Each row represents a food type (1-4)
# Each column represents protein, fat, carbohydrates
yields = np.array([
    [3, 2, 6],  # Food type 1
    [4, 2, 4],  # Food type 2
    [8, 7, 7],  # Food type 3
    [6, 5, 4],  # Food type 4
])

# Minimum daily requirements
requirements = np.array([800, 200, 700])

# Linear Programming Model Formulation
# Decision variables: x1, x2, x3, x4 (units of each food type)
# Objective: Minimize cost = 45x1 + 40x2 + 85x3 + 65x4
# Constraints:
#   3x1 + 4x2 + 8x3 + 6x4 >= 800 (protein)
#   2x1 + 2x2 + 7x3 + 5x4 >= 200 (fat)
#   6x1 + 4x2 + 7x3 + 4x4 >= 700 (carbohydrates)
#   x1, x2, x3, x4 >= 0 (non-negativity)

# For scipy.linprog, we need to convert ">=" constraints to "<=" by multiplying by -1
A_ub = -yields.T  # Transpose and negate
b_ub = -requirements

# Bounds for variables (all non-negative)
bounds = [(0, None)] * 4

# Solve the linear programming problem
result = linprog(
    c=costs,           # Objective function coefficients
    A_ub=A_ub,         # Inequality constraint coefficients
    b_ub=b_ub,         # Inequality constraint right-hand side
    bounds=bounds,     # Variable bounds
    method='highs'     # Using the highs solver for better precision
)

# Display results
print("Optimization Status:", result.message)
print("\nOptimal Solution:")
print(f"Food type 1: {result.x[0]:.4f} units")
print(f"Food type 2: {result.x[1]:.4f} units")
print(f"Food type 3: {result.x[2]:.4f} units")
print(f"Food type 4: {result.x[3]:.4f} units")
print(f"\nMinimum Cost: {result.fun:.2f} BDT")

# Calculate actual nutrients obtained
nutrients_obtained = yields.T @ result.x
print("\nNutrients Obtained:")
print(f"Proteins:       {nutrients_obtained[0]:.2f} (required: {requirements[0]})")
print(f"Fat:            {nutrients_obtained[1]:.2f} (required: {requirements[1]})")
print(f"Carbohydrates:  {nutrients_obtained[2]:.2f} (required: {requirements[2]})")

# Check if any constraints are binding (at their limit)
tolerance = 1e-6
binding = np.isclose(nutrients_obtained, requirements, atol=tolerance)
print("\nBinding Constraints:")
nutrient_names = ["Protein", "Fat", "Carbohydrates"]
for i, is_binding in enumerate(binding):
    print(f"{nutrient_names[i]}: {'Yes' if is_binding else 'No'}")