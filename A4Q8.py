import numpy as np
from scipy.optimize import linprog

# Payoff matrix where rows are Player B's strategies and columns are Player A's strategies
# Entries are payoffs to Player B (row player)
payoff_matrix = np.array([
    [-1, -2, 8],
    [7, 5, -1],
    [6, 0, 12]
])

# For Player B (row player): Maximize v subject to sum p_i * a_{i,j} >= v for each j, sum p_i = 1
# Using linprog, minimize -v, so let x = [p1, p2, p3, v], objective c = [0, 0, 0, -1]
c_B = [0, 0, 0, -1]
# Constraints: a_{i,j} p1 + a_{i,j} p2 + a_{i,j} p3 - v >= 0 => -a_{i,j} p1 - a_{i,j} p2 - a_{i,j} p3 + v <= 0
A_ub_B = np.hstack((-payoff_matrix, np.ones((3, 1))))
b_ub_B = np.zeros(3)
# Equality constraint: p1 + p2 + p3 = 1
A_eq_B = np.array([[1, 1, 1, 0]])
b_eq_B = np.array([1])
# Bounds: p_i >= 0, v free
bounds_B = [(0, None), (0, None), (0, None), (None, None)]

# Solve for Player B
res_B = linprog(c_B, A_ub=A_ub_B, b_ub=b_ub_B, A_eq=A_eq_B, b_eq=b_eq_B, bounds=bounds_B)
p1, p2, p3, v = res_B.x
player_B_strategy = [p1, p2, p3]
game_value = v

# For Player A (column player): Minimize w subject to sum q_j * a_{i,j} <= w for each i, sum q_j = 1
# Let x = [q1, q2, q3, w], minimize w, so c = [0, 0, 0, 1]
c_A = [0, 0, 0, 1]
# Constraints: a_{i,j} q1 + a_{i,j} q2 + a_{i,j} q3 - w <= 0
A_ub_A = np.hstack((payoff_matrix.T, -np.ones((3, 1))))
b_ub_A = np.zeros(3)
# Equality constraint: q1 + q2 + q3 = 1
A_eq_A = np.array([[1, 1, 1, 0]])
b_eq_A = np.array([1])
# Bounds: q_j >= 0, w free
bounds_A = [(0, None), (0, None), (0, None), (None, None)]

# Solve for Player A
res_A = linprog(c_A, A_ub=A_ub_A, b_ub=b_ub_A, A_eq=A_eq_A, b_eq=b_eq_A, bounds=bounds_A)
q1, q2, q3, w = res_A.x
player_A_strategy = [q1, q2, q3]

# Output results
print("Player B's optimal strategy (probabilities for strategies I, II, III):", 
      [float(f"{p:.4f}") for p in player_B_strategy])
print("Player A's optimal strategy (probabilities for strategies I, II, III):", 
      [float(f"{q:.4f}") for q in player_A_strategy])
print("Value of the game (expected payoff to Player B):", float(f"{game_value:.4f}"))

# Verify the solution (should match game_value)
# Expected payoff for Player B's strategies against Player A's mixed strategy
for i, strategy in enumerate(['I', 'II', 'III']):
    payoff = sum(payoff_matrix[i, j] * player_A_strategy[j] for j in range(3))
    print(f"Expected payoff for Player B's strategy {strategy}: {payoff:.4f}")