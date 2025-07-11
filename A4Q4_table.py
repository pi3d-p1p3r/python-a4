import numpy as np

def big_m_method():
    # Columns: x, y, s1, s2, s3, a1, a2, a3
    A = np.array([
        [200, 100, -1, 0, 0,    1, 0, 0],      # Vitamins
        [1, 2,      0, -1, 0,   0, 1, 0],      # Minerals
        [40, 40,    0, 0, -1,   0, 0, 1]       # Calories
    ])
    
    b = np.array([4000, 50, 1400])
    M = 1e6  # Large positive number
    c = np.array([4, 3, 0, 0, 0, M, M, M])
    basic_vars = [5, 6, 7]          # Initial basic variables: a1, a2, a3 (indices 5,6,7)
    
    # Initial tableau: [A | b]
    tableau = np.hstack((A, b.reshape(-1, 1)))
    
    artificial_rows = A[[0,1,2], :]  # Rows corresponding to a1, a2, a3
    obj_row = c - M * np.sum(artificial_rows, axis=0)         # Z = c - M * sum of artificial rows
    tableau = np.vstack((tableau, np.append(obj_row, 0)))

    var_names = ['x', 'y', 's1', 's2', 's3', 'a1', 'a2', 'a3']      # Variable names for printing

    iteration = 0
    print("=" * 100)
    print("BIG-M METHOD SIMPLEX ITERATIONS")
    print("=" * 100)

    # Simplex iterations
    while True:
        iteration += 1
        
        # Print current basic variables
        basic_vars_names = [var_names[i] for i in basic_vars]
        print(f"Iteration -->{iteration:4}  |  Basic Variables -->{str(basic_vars_names):>18}")
        
        # Print tableau header
        print(f"\nTableau {iteration}:")
        print(f"{'':>12} " + " ".join(f"{name:>10}" for name in var_names) + f"{'RHS':>12}")
        print("-" * 120)
        
        # Print constraint rows
        constraint_names = ['Vitamins', 'Minerals', 'Calories', 'Objective']
        for i, row in enumerate(tableau):
            row_name = constraint_names[i] if i < len(constraint_names) else f"Row {i}"
            print(f"{row_name:>12} " + " ".join(f"{v:>10.1f}" for v in row))
        print()

        # Find the entering variable (most negative in obj row)
        obj_row = tableau[-1, :-1]
        if np.all(obj_row >= 0):
            print("OPTIMAL SOLUTION REACHED - All coefficients in objective row are non-negative")
            break  # Optimal solution reached
        entering = np.argmin(obj_row)

        # Find the leaving variable (min ratio test)
        ratios = tableau[:-1, -1] / tableau[:-1, entering]
        ratios[ratios <= 0] = np.inf
        leaving = np.argmin(ratios)

        # Print entering and leaving variables
        print(f"→ Entering variable: {var_names[entering]} (most negative coefficient)")
        print(f"→ Leaving variable: {var_names[basic_vars[leaving]]} (minimum ratio test)")
        print(f"→ Pivot element: {tableau[leaving, entering]:.3f}")
        print()

        pivot_element = tableau[leaving, entering]      # Pivot
        tableau[leaving, :] /= pivot_element
        for i in range(tableau.shape[0]):
            if i != leaving:
                factor = tableau[i, entering]
                tableau[i, :] -= factor * tableau[leaving, :]

        # Update basic variables
        basic_vars[leaving] = entering
        
        print("After pivoting:")
        print("-" * 60)

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

print("\n" + "=" * 50)
print("FINAL SOLUTION")
print("=" * 50)
print(f"Optimal number of units of Food A: {x}")
print(f"Optimal number of units of Food B: {y}")
print(f"Total Cost (BDT): {total_cost}")

print("\n" + "=" * 50)
print("CONSTRAINT VERIFICATION")
print("=" * 50)
# Verify constraints
vitamins = 200 * x + 100 * y
minerals = 1 * x + 2 * y
calories = 40 * x + 40 * y
print(f"Vitamins provided: {vitamins} (Required: ≥ 4000)")
print(f"Minerals provided: {minerals} (Required: ≥ 50)")
print(f"Calories provided: {calories} (Required: ≥ 1400)")
