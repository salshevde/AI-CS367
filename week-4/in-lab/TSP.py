import math
import random

def haversine_distance(coord1, coord2):
    """Calculates the Haversine distance between two coordinates."""
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def total_distance(tour, cities):
    """Calculates the total Haversine distance of the given tour."""
    return sum(haversine_distance(cities[tour[i]], cities[tour[i-1]]) for i in range(len(tour)))

def calculate_cost(distance, cost_per_km):
    """Calculates the total cost based on distance and cost per kilometer."""
    return distance * cost_per_km

def simulated_annealing(cities, temp, cooling_rate, iterations, cost_per_km):
    """Performs simulated annealing to find an approximate solution to the TSP."""
    n = len(cities)
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_distance = total_distance(current_tour, cities)
    best_tour = current_tour[:]
    best_distance = current_distance

    while temp > 1:
        for _ in range(iterations):
            # Create a new tour by swapping two cities
            new_tour = current_tour[:]
            i, j = random.sample(range(n), 2)
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

            new_distance = total_distance(new_tour, cities)

            # Determine whether to accept the new tour
            if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temp):
                current_tour = new_tour
                current_distance = new_distance

                # Update the best tour if the new one is better
                if current_distance < best_distance:
                    best_tour = current_tour[:]
                    best_distance = current_distance

        # Decrease the temperature
        temp *= cooling_rate

    return best_tour, best_distance

# Example usage:
cities = {
    "Jaipur": (26.9124, 75.7873),
    "Udaipur": (24.5854, 73.7125),
    "Jodhpur": (26.2389, 73.0243),
    "Alwar": (27.5530, 76.6346),
    "Pushkar": (26.4886, 74.5509),
    "Ajmer": (26.449896, 74.639915),
    "Ranthambore": (25.9776, 76.5533),
    "Mount Abu": (24.5926, 72.7156),
    "Bikaner": (28.0229, 73.3119),
    "Chittorgarh": (24.8829, 74.6230),
    "Kota": (25.2138, 75.8648),
    "Sawai Madhopur": (26.0124, 76.3560),
    "Bharatpur": (27.2152, 77.5030),
    "Jaisalmer": (26.9157, 70.9083),
    "Neemrana": (27.9797, 76.3962),
    "Dholpur": (26.6966, 77.8908),
    "Kumbhalgarh": (25.1528, 73.5870),
    "Sirohi": (24.8827, 72.8609),
    "Shekhawati": (27.6195, 75.1504),
    "Barmer": (25.7521, 71.3967),
}

initial_temp = 1000
cooling_rate = 0.995
iterations = 100
cost_per_km = 150.0  

best_tour, best_distance = simulated_annealing(list(cities.values()), initial_temp, cooling_rate, iterations, cost_per_km)

# Calculate the total cost of the best tour
total_cost = calculate_cost(best_distance, cost_per_km)

# Print the best tour with city names and total cost
print("Best tour:", [list(cities.keys())[i] for i in best_tour])
print("Total distance (in km):", best_distance)
print("Total cost (in Rupees):", total_cost)
