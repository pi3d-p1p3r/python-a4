import numpy as np
from scipy.optimize import linear_sum_assignment

# Define the profit matrix
profit_matrix = np.array([
    [16, 10, 14, 11],
    [14, 11, 15, 15],
    [15, 15, 13, 12],
    [13, 12, 14, 15]
])

# Since linear_sum_assignment minimizes the sum, we use the negative of the profit matrix
cost_matrix = -profit_matrix

# Solve the assignment problem
row_ind, col_ind = linear_sum_assignment(cost_matrix)

# Calculate the total profit
total_profit = profit_matrix[row_ind, col_ind].sum()

# Define labels for salesmen and cities
salesmen = ['A', 'B', 'C', 'D']
cities = ['1', '2', '3', '4']

# Print the assignments
print("Optimal Assignment:")
for i in range(len(row_ind)):
    salesman = salesmen[row_ind[i]]
    city = cities[col_ind[i]]
    profit = profit_matrix[row_ind[i], col_ind[i]]
    print(f"Salesman {salesman} assigned to city {city}, profit: {profit} BDT")

# Print the total profit
print(f"\nTotal profit: {total_profit} BDT per day")