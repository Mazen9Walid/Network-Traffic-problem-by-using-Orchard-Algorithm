import networkx as nx
import random
import time

# Load the graph from the dataset (make sure to provide the correct path to your data)
file_path = "data/1221/weights.intra"  # Update this path
G = nx.Graph()

# Load graph from file
with open(file_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) == 3:
            node1, node2, weight = parts
            G.add_edge(node1, node2, weight=float(weight))

# Define source and target nodes
source = 'Brisbane,+Australia1800'
target = 'Darwin,+Australia1837'

# Orchard Algorithm parameters
N_pop = 50  # Number of solutions (seedlings)
GYN = 10  # Growth years number
alpha = 0.7  # Weight for objective function
beta = 0.3  # Weight for growth rate

# Function to calculate growth rate
def calculate_growth_rate(solution, previous_solution):
    growth_rate = sum([solution[i] - previous_solution[i] for i in range(len(solution))])
    return growth_rate

# Function to simulate local search for growth (for Orchard Algorithm)
def local_search(G, path):
    new_path = path[:]
    random.shuffle(new_path)  # Randomly shuffle to simulate local search
    return new_path

# Function for the Orchard Algorithm to find the best path using exploration and exploitation
def orchard_algorithm(G, source, target, N_pop, GYN):
    # Initialize the orchard with random paths as solutions
    orchard = []
    for _ in range(N_pop):
        random_path = list(nx.shortest_path(G, source, target))  # Generate random path (for simplicity)
        orchard.append({'path': random_path, 'cost': nx.path_weight(G, random_path, weight='weight'), 'growth_rate': 0})
    
    best_solution = None
    best_cost = float('inf')
    
    for generation in range(GYN):
        # Growth phase: improving solutions through local search
        for tree in orchard:
            tree['path'] = local_search(G, tree['path'])
            tree['cost'] = nx.path_weight(G, tree['path'], weight='weight')
        
        # Screening phase: Evaluate solutions based on cost and growth rate
        orchard = sorted(orchard, key=lambda x: (x['cost'], -x['growth_rate']))
        
        # Elitism: Keep the best solutions (elite trees)
        best_solution = orchard[0]
        best_cost = best_solution['cost']
        
        # Grafting: Improve medium solutions using strong solutions
        for i in range(1, N_pop):
            if orchard[i]['cost'] > best_solution['cost']:
                orchard[i]['path'] = best_solution['path']
                orchard[i]['cost'] = best_solution['cost']
        
        # Replace weak solutions
        orchard = orchard[:int(N_pop * alpha)]  # Keep only top solutions
        while len(orchard) < N_pop:
            random_path = list(nx.shortest_path(G, source, target))  # Create random new paths
            orchard.append({'path': random_path, 'cost': nx.path_weight(G, random_path, weight='weight'), 'growth_rate': 0})
    
    return best_solution

# Measure execution time
start_time = time.time()
best_path = orchard_algorithm(G, source, target, N_pop, GYN)
execution_time = time.time() - start_time

# Output the results
visited_nodes = len(best_path['path'])
path_cost = best_path['cost']

# Results
print("\n=== Orchard Algorithm Evaluation ===")
print(f"Source: {source}")
print(f"Target: {target}")
print(f"→ Execution Time: {execution_time:.6f} seconds")
print(f"→ Path Cost: {path_cost}")
print(f"→ Visited Nodes: {visited_nodes}")
print(f"→ Path: {' -> '.join(best_path['path'])}")
