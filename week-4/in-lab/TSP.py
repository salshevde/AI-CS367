import random
import math

locs = {
    'J': (26.9124, 75.7873),
    'U': (24.5854, 73.7125),
    'Jo': (26.2393, 73.3083),
    'A': (27.5540, 76.6342),
    'P': (26.4890, 74.5512),
    'Aj': (26.4499, 74.6399),
    'R': (26.0142, 76.4081),
    'M': (24.5921, 72.6792),
    'B': (28.0216, 73.3119),
    'C': (24.8796, 74.6319),
    'K': (25.2138, 75.8648),
    'SM': (26.0205, 76.3564),
    'Bh': (27.2191, 77.4896),
    'Jm': (26.9125, 70.9220),
}

def dist(a, b):
    return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def tour_cost(t):
    return sum(dist(locs[a], locs[b]) for a, b in zip(t, t[1:] + [t[0]]))

def sim_anneal(locs, init_temp, cool_rate, iters):
    tour = list(locs.keys())
    random.shuffle(tour)
    best_tour = tour[:]
    best_cost = tour_cost(tour)
    temp = init_temp

    while temp > 1:
        for _ in range(iters):
            idx1, idx2 = random.sample(range(len(tour)), 2)
            neighbor = tour[:idx1] + tour[idx2:idx1:-1] + tour[idx2+1:]
            neighbor_cost = tour_cost(neighbor)

            if neighbor_cost < best_cost or random.uniform(0, 1) < math.exp((best_cost - neighbor_cost) / temp):
                best_tour = neighbor
                best_cost = neighbor_cost

        temp *= cool_rate

    return best_tour, best_cost

init_temp = 1000
cool_rate = 0.995
num_iters = 100

best_tour, best_cost = sim_anneal(locs, init_temp, cool_rate, num_iters)

print("Best Tour:", " -> ".join(best_tour))
print("Total Travel Cost:", best_cost)