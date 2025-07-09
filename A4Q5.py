import numpy as np
import pandas as pd

cost_matrix = np.array([[4, 3, 1, 2, 6], [5, 2, 3, 4, 5], [3, 5, 6, 3, 2], [2, 4, 4, 5, 3]])
supply = np.array([80, 60, 40, 20])
demand = np.array([60, 60, 30, 40, 10])

def north_west_corner(supply, demand):
    s, d = supply.copy(), demand.copy()
    m, n = len(s), len(d)
    alloc = np.zeros((m, n))
    i, j = 0, 0
    while i < m and j < n:
        qty = min(s[i], d[j])
        alloc[i, j] = qty
        s[i] -= qty
        d[j] -= qty
        if s[i] == 0: i += 1
        if d[j] == 0: j += 1
    return alloc

def least_cost_method(supply, demand, costs):
    s, d = supply.copy(), demand.copy()
    c = costs.copy().astype(float) # Use a float copy for infinity
    m, n = len(s), len(d)
    alloc = np.zeros((m, n))
    while np.sum(alloc) < np.sum(supply):
        # Find the cell with the minimum cost in the available grid
        i, j = np.unravel_index(np.argmin(c), c.shape)
        
        # Allocate as much as possible
        qty = min(s[i], d[j])
        alloc[i, j] = qty
        
        # Update remaining supply and demand
        s[i] -= qty
        d[j] -= qty
        
        # Mark exhausted rows/columns as infinitely expensive to ignore them
        if s[i] == 0: c[i, :] = np.inf
        if d[j] == 0: c[:, j] = np.inf
    return alloc

# --- Helper Function for Display ---

def print_solution(method_name, allocation, costs):
    """Calculates cost and prints the resulting allocation table."""
    print(f"\n--- {method_name} ---")
    total_cost = np.sum(allocation * costs)
    df = pd.DataFrame(allocation, index=['A', 'B', 'C', 'D'], columns=['P', 'Q', 'R', 'S', 'T'])
    print(df)
    print(f"Total Cost: ${total_cost:,.2f}")
    
# Solve and display North-West Corner solution
nw_alloc = north_west_corner(supply, demand)
print_solution("North-West Corner Rule", nw_alloc, cost_matrix)

# Solve and display Least Cost Method solution
lc_alloc = least_cost_method(supply, demand, cost_matrix)
print_solution("Least Cost Method", lc_alloc, cost_matrix)
