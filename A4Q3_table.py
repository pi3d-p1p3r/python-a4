import numpy as np

def simplex_solve():
    tableau = np.array([
        [1.0,  1.0,  1.0,  1.0, 0.0, 0.0,  100.0],  # s1 constraint
        [-0.01, 0.01, 0.0,  0.0, 1.0, 0.0,   0.0],  # s2 constraint  
        [0.0,  -1.0,  2.0,  0.0, 0.0, 1.0,   0.0],  # s3 constraint
        [-12.0, -15.0, -14.0, 0.0, 0.0, 0.0,  0.0]   # objective row
    ])
    
    variables = ['s1', 's2', 's3']  # Basic variables
    iteration = 0
    
    while True:
        iteration += 1
        print(f"\n{'='*50}")
        print(f"ITERATION {iteration}")
        print(f"{'='*50}")
        
        # Print current tableau
        print("\nCurrent Tableau:")
        headers = ['x1', 'x2', 'x3', 's1', 's2', 's3', 'RHS']
        print(f"{'Var':<4}", end="")
        for h in headers: print(f"{h:>8}", end="")
        print()
        
        for i in range(3):
            print(f"{variables[i]:<4}", end="")
            for j in range(7): print(f"{tableau[i,j]:>8.2f}", end="")
            print()
        
        print(f"{'Z':<4}", end="")
        for j in range(7): print(f"{tableau[3,j]:>8.2f}", end="")
        print()
        
        # Check optimality
        if np.all(tableau[3, :-1] >= 0):
            print(f"\nOptimal solution reached!")
            break
            
        # Find entering variable (most negative in objective row)
        entering_col = np.argmin(tableau[3, :-1])
        entering_var = headers[entering_col]
        print(f"\nEntering variable: {entering_var}")
        
        # Find leaving variable (minimum ratio test)
        ratios = []
        for i in range(3):
            if tableau[i, entering_col] > 0:
                ratios.append(tableau[i, -1] / tableau[i, entering_col])
            else:
                ratios.append(float('inf'))
        
        leaving_row = np.argmin(ratios)
        leaving_var = variables[leaving_row]
        print(f"Leaving variable: {leaving_var}")
        
        # Pivot operation
        pivot = tableau[leaving_row, entering_col]
        tableau[leaving_row] /= pivot  # Normalize pivot row
        
        # Eliminate other entries in pivot column
        for i in range(4):
            if i != leaving_row:
                tableau[i] -= tableau[i, entering_col] * tableau[leaving_row]
        
        # Update basic variables
        variables[leaving_row] = entering_var
    
    # Extract solution
    solution = np.zeros(3)
    for i, var in enumerate(variables):
        if var in ['x1', 'x2', 'x3']:
            var_index = ['x1', 'x2', 'x3'].index(var)
            solution[var_index] = tableau[i, -1]
    
    profit = -tableau[3, -1]
    
    print(f"\n{'='*50}")
    print("FINAL SOLUTION")
    print(f"{'='*50}")
    print(f"Coal A (x1): {solution[0]:.0f} tons")
    print(f"Coal B (x2): {solution[1]:.0f} tons") 
    print(f"Coal C (x3): {solution[2]:.0f} tons")
    print(f"Maximum Profit: {profit:.0f} BDT")
    
    return solution, profit

solution, profit = simplex_solve()
