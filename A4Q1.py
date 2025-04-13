import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# Define the constraints as functions
def constraint1(x1):
    # x1 + 2*x2 <= 10
    return (10 - x1) / 2

def constraint2(x1):
    # x1 + x2 <= 6
    return 6 - x1

def constraint3(x1):
    # x1 - x2 <= 2
    return x1 - 2

def constraint4(x1):
    # x1 - 2*x2 <= 1
    return (x1 - 1) / 2

def constraint5(x1):
    # x1 >= 0
    return 0

def constraint6(x2):
    # x2 >= 0
    return 0

# Define objective function Z = 2*x1 + x2
def objective_function(x1, x2):
    return 2*x1 + x2

# Set up the plotting area
plt.figure(figsize=(10, 8))
plt.grid(True)
plt.xlim(-1, 10)
plt.ylim(-1, 6)
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Graphical Method for Linear Programming')
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)

# Plot the constraint lines
x1_values = np.linspace(0, 10, 1000)
plt.plot(x1_values, constraint1(x1_values), 'r-', label='x1 + 2*x2 = 10')
plt.plot(x1_values, constraint2(x1_values), 'g-', label='x1 + x2 = 6')
plt.plot(x1_values, constraint3(x1_values), 'b-', label='x1 - x2 = 2')
plt.plot(x1_values, constraint4(x1_values), 'y-', label='x1 - 2*x2 = 1')
plt.axhline(y=0, color='m', linestyle='-', label='x2 = 0')
plt.axvline(x=0, color='c', linestyle='-', label='x1 = 0')

# Calculate the vertices of the feasible region by finding intersections
vertices = []

# Constraint 1 and 2: x1 + 2*x2 = 10 and x1 + x2 = 6
x1 = 2
x2 = 4
vertices.append((x1, x2))

# Constraint 2 and 3: x1 + x2 = 6 and x1 - x2 = 2
x1 = 4
x2 = 2
vertices.append((x1, x2))

# Constraint 3 and 4: x1 - x2 = 2 and x1 - 2*x2 = 1
x1 = 3
x2 = 1
vertices.append((x1, x2))

# Constraint 4 and x2 = 0: x1 - 2*x2 = 1 and x2 = 0
x1 = 1
x2 = 0
vertices.append((x1, x2))

# Constraint x1 = 0 and Constraint 1: x1 = 0 and x1 + 2*x2 = 10
x1 = 0
x2 = 5
vertices.append((x1, x2))

# Verify which vertices satisfy all constraints
feasible_vertices = []
for vertex in vertices:
    x1, x2 = vertex
    if (x1 + 2*x2 <= 10 + 1e-6 and 
        x1 + x2 <= 6 + 1e-6 and 
        x1 - x2 <= 2 + 1e-6 and 
        x1 - 2*x2 <= 1 + 1e-6 and 
        x1 >= 0 - 1e-6 and 
        x2 >= 0 - 1e-6):
        feasible_vertices.append(vertex)

# Shade the feasible region
if feasible_vertices:
    # Sort vertices to form a convex polygon (clockwise or counterclockwise)
    feasible_vertices = np.array(feasible_vertices)
    center = np.mean(feasible_vertices, axis=0)
    angles = np.arctan2(feasible_vertices[:, 1] - center[1], 
                       feasible_vertices[:, 0] - center[0])
    sorted_indices = np.argsort(angles)
    sorted_vertices = feasible_vertices[sorted_indices]
    
    # Create polygon
    polygon = Polygon(sorted_vertices, alpha=0.2, color='gray')
    plt.gca().add_patch(polygon)

# Evaluate objective function at each vertex
objective_values = []
for vertex in feasible_vertices:
    x1, x2 = vertex
    z = objective_function(x1, x2)
    objective_values.append((x1, x2, z))
    plt.annotate(f'({x1:.1f}, {x2:.1f})\nZ={z:.1f}', 
                (x1+0.1, x2+0.1), fontsize=9)

# Find the optimal solution
if objective_values:
    optimal_solution = max(objective_values, key=lambda x: x[2])
    print(f"Vertices of the feasible region: {feasible_vertices}")
    print(f"Objective values at each vertex: {objective_values}")
    print(f"Optimal solution: x1 = {optimal_solution[0]}, x2 = {optimal_solution[1]}")
    print(f"Maximum value of Z = {optimal_solution[2]}")
    
    # Highlight the optimal solution
    plt.plot(optimal_solution[0], optimal_solution[1], 'ro', markersize=10)
    plt.annotate(f'OPTIMAL\n({optimal_solution[0]}, {optimal_solution[1]})\nZ={optimal_solution[2]}',
                (optimal_solution[0]+0.2, optimal_solution[1]+0.2), 
                fontsize=12, color='red')
    
    # Plot some level curves of the objective function
    for z in np.linspace(2, 14, 4):
        x1_vals = np.linspace(0, 8, 100)
        x2_vals = z - 2*x1_vals
        plt.plot(x1_vals, x2_vals, 'k--', alpha=0.5)
        plt.annotate(f'Z={z}', (4, z-8), color='k', alpha=0.7)
    
    # Add arrow showing direction of increasing Z
    plt.arrow(3, 2, 0.5, -0.25, head_width=0.2, head_length=0.2, fc='red', ec='red')
    plt.annotate('Direction of\nincreasing Z', (3.6, 1.8), color='red')

plt.legend(loc='upper right')
plt.tight_layout()
plt.show()

print("\nInterpretation:")
if objective_values:
    print(f"The maximum value of Z = 2x₁ + x₂ = {optimal_solution[2]}")
    print(f"This occurs at the point (x₁, x₂) = ({optimal_solution[0]}, {optimal_solution[1]})")
    print("\nVerification:")
    print(f"x₁ + 2x₂ = {optimal_solution[0] + 2*optimal_solution[1]:.1f} ≤ 10 ✓")
    print(f"x₁ + x₂ = {optimal_solution[0] + optimal_solution[1]:.1f} ≤ 6 ✓")
    print(f"x₁ - x₂ = {optimal_solution[0] - optimal_solution[1]:.1f} ≤ 2 ✓")
    print(f"x₁ - 2x₂ = {optimal_solution[0] - 2*optimal_solution[1]:.1f} ≤ 1 ✓")
    print(f"x₁ = {optimal_solution[0]:.1f} ≥ 0 ✓")
    print(f"x₂ = {optimal_solution[1]:.1f} ≥ 0 ✓")