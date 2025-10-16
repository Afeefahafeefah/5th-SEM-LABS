import numpy as np

# Distance matrix
distance_matrix = np.array([
    [0, 2, 9, 10, 7],   # A
    [1, 0, 6, 4, 3],    # B
    [15, 7, 0, 8, 9],   # C
    [6, 3, 12, 0, 11],  # D
    [10, 4, 8, 5, 0]    # E
])

cities = ['A', 'B', 'C', 'D', 'E']  # Map indices to letters

num_cities = len(distance_matrix)
num_ants = 5
num_iterations = 100
alpha = 1      # Pheromone importance
beta = 5       # Distance priority
evaporation = 0.5
pheromone_constant = 100

# Initialize pheromone levels
pheromone = np.ones((num_cities, num_cities))

# Function to choose the next city
def choose_next_city(current_city, visited):
    probabilities = []
    for city in range(num_cities):
        if city in visited:
            probabilities.append(0)
        else:
            prob = (pheromone[current_city][city] ** alpha) * ((1 / distance_matrix[current_city][city]) ** beta)
            probabilities.append(prob)
    probabilities = np.array(probabilities)
    probabilities /= probabilities.sum()
    next_city = np.random.choice(range(num_cities), p=probabilities)
    return next_city

# Main ACO loop
best_path = None
best_distance = float('inf')

for iteration in range(num_iterations):
    paths = []
    distances = []

    for ant in range(num_ants):
        visited = [np.random.randint(num_cities)]
        while len(visited) < num_cities:
            next_city = choose_next_city(visited[-1], visited)
            visited.append(next_city)
        visited.append(visited[0])  # Return to start
        paths.append(visited)
        
        # Calculate path distance
        distance = sum(distance_matrix[visited[i]][visited[i+1]] for i in range(num_cities))
        distances.append(distance)
        
        if distance < best_distance:
            best_distance = distance
            best_path = visited

    # Update pheromone
    pheromone *= (1 - evaporation)
    for i, path in enumerate(paths):
        for j in range(num_cities):
            pheromone[path[j]][path[j+1]] += pheromone_constant / distances[i]

# Convert indices to letters for output
best_path_letters = ' -> '.join(cities[i] for i in best_path)

print("Best Path:", best_path_letters)
print("Best Distance:", best_distance)
