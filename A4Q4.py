import numpy as np

def big_m_method():
    # Coefficients for constraints (A matrix)
    # Columns: x, y, s1, s2, s3, a1, a2, a3
    A = np.array([
        [200, 100, -1, 0, 0, 1, 0, 0],  # Vitamins
        [1, 2, 0, -1, 0, 0, 1, 0],      # Minerals
        [40, 40, 0, 0, -1, 0, 0, 1]     # Calories
    ])
    
    # Right-hand side (b vector)
    b = np.array([4000, 50, 1400])
    
    # Objective function coefficients (c vector)
    # Original: 4x + 3y, artificial variables with Big M
    M = 1e6  # Large positive number
    c = np.array([4, 3, 0, 0, 0, M, M, M])
    
    # Initial basic variables: a1, a2, a3 (indices 5,6,7)
    basic_vars = [5, 6, 7]
    
    # Initial tableau: [A | b]
    tableau = np.hstack((A, b.reshape(-1, 1)))
    
    # Adjust the objective row
    # Z = c - M * sum of artificial rows
    artificial_rows = A[[0,1,2], :]  # Rows corresponding to a1, a2, a3
    obj_row = c - M * np.sum(artificial_rows, axis=0)
    tableau = np.vstack((tableau, np.append(obj_row, 0)))
    
    # Simplex iterations
    while True:
        # Find the entering variable (most negative in obj row)
        obj_row = tableau[-1, :-1]
        if np.all(obj_row >= 0):
            break  # Optimal solution reached
        entering = np.argmin(obj_row)
        
        # Find the leaving variable (min ratio test)
        ratios = tableau[:-1, -1] / tableau[:-1, entering]
        ratios[ratios <= 0] = np.inf
        leaving = np.argmin(ratios)
        
        # Pivot
        pivot_element = tableau[leaving, entering]
        tableau[leaving, :] /= pivot_element
        for i in range(tableau.shape[0]):
            if i != leaving:
                factor = tableau[i, entering]
                tableau[i, :] -= factor * tableau[leaving, :]
        
        # Update basic variables
        basic_vars[leaving] = entering
    
    # Extract solution
    solution = np.zeros(len(c))
    for i, var in enumerate(basic_vars):
        if var < len(c):
            solution[var] = tableau[i, -1]
    
    x, y = solution[0], solution[1]
    total_cost = 4 * x + 3 * y
    
    return x, y, total_cost

# Run the function
x, y, total_cost = big_m_method()
print(f"Optimal number of units of Food A: {x}")
print(f"Optimal number of units of Food B: {y}")
print(f"Total Cost (BDT): {total_cost}")

# Verify constraints
vitamins = 200 * x + 100 * y
minerals = 1 * x + 2 * y
calories = 40 * x + 40 * y
print(f"Vitamins provided: {vitamins}")
print(f"Minerals provided: {minerals}")
print(f"Calories provided: {calories}")