import numpy as np
import pandas as pd

# Define the problem data
cost_matrix = np.array([
    [4, 3, 1, 2, 6],  # A
    [5, 2, 3, 4, 5],  # B
    [3, 5, 6, 3, 2],  # C
    [2, 4, 4, 5, 3]   # D
])

supply = np.array([80, 60, 40, 20])  # A, B, C, D
demand = np.array([60, 60, 30, 40, 10])  # P, Q, R, S, T

# Helper function to create a solution table for display
def create_solution_table(allocation_matrix, cost=None):
    sources = ['A', 'B', 'C', 'D']
    destinations = ['P', 'Q', 'R', 'S', 'T']
    
    df = pd.DataFrame(allocation_matrix, index=sources, columns=destinations)
    
    if cost is not None:
        df['Supply'] = supply
        total_cost = np.sum(allocation_matrix * cost_matrix)
        return df, total_cost
    else:
        df['Supply'] = supply
        return df

# North-West Corner Rule
def north_west_corner(supply, demand):
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    
    m = len(supply)
    n = len(demand)
    
    # Initialize allocation matrix
    allocation = np.zeros((m, n))
    
    i, j = 0, 0
    
    # Continue until we either run out of supply or demand
    while i < m and j < n:
        # Allocate as much as possible
        quantity = min(supply_copy[i], demand_copy[j])
        allocation[i, j] = quantity
        
        # Update remaining supply and demand
        supply_copy[i] -= quantity
        demand_copy[j] -= quantity
        
        # If supply is exhausted, move to next supplier
        if supply_copy[i] == 0:
            i += 1
        
        # If demand is satisfied, move to next customer
        if demand_copy[j] == 0:
            j += 1
    
    return allocation

# Least Cost Method
def least_cost_method(supply, demand, costs):
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    
    m = len(supply)
    n = len(demand)
    
    # Initialize allocation matrix
    allocation = np.zeros((m, n))
    
    # Continue until all supply is allocated or all demand is met
    while np.sum(supply_copy) > 0 and np.sum(demand_copy) > 0:
        # Find the cell with minimum cost (among cells that can still be allocated)
        min_cost = float('inf')
        min_i, min_j = -1, -1
        
        for i in range(m):
            if supply_copy[i] <= 0:
                continue
                
            for j in range(n):
                if demand_copy[j] <= 0:
                    continue
                    
                if costs[i, j] < min_cost:
                    min_cost = costs[i, j]
                    min_i, min_j = i, j
        
        # Allocate as much as possible to the minimum cost cell
        quantity = min(supply_copy[min_i], demand_copy[min_j])
        allocation[min_i, min_j] = quantity
        
        # Update remaining supply and demand
        supply_copy[min_i] -= quantity
        demand_copy[min_j] -= quantity
    
    return allocation

# Solve using North-West Corner Rule
nw_allocation = north_west_corner(supply, demand)
nw_table, nw_cost = create_solution_table(nw_allocation, cost_matrix)

# Solve using Least Cost Method
lc_allocation = least_cost_method(supply, demand, cost_matrix)
lc_table, lc_cost = create_solution_table(lc_allocation, cost_matrix)

# Print results
print("North-West Corner Rule Solution:")
print(nw_table)
print(f"Total Cost: {nw_cost}")

print("\nLeast Cost Method Solution:")
print(lc_table)
print(f"Total Cost: {lc_cost}")

# Detailed allocation tables with costs
def print_detailed_allocation(allocation, method_name):
    sources = ['A', 'B', 'C', 'D']
    destinations = ['P', 'Q', 'R', 'S', 'T']
    
    print(f"\n{method_name} - Detailed Allocation:")
    print("Cell Format: Allocation (Cost) = Total")
    
    for i in range(len(sources)):
        row = []
        for j in range(len(destinations)):
            if allocation[i, j] > 0:
                cell_cost = allocation[i, j] * cost_matrix[i, j]
                row.append(f"{allocation[i, j]:.0f} ({cost_matrix[i, j]}) = {cell_cost:.0f}")
            else:
                row.append("—")
        print(f"{sources[i]}: {row}")

print_detailed_allocation(nw_allocation, "North-West Corner Rule")
print_detailed_allocation(lc_allocation, "Least Cost Method")