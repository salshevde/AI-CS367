from ksat import create_k_sat
import heapq
import random
# Utility functions

def random_solution(n):
    return [random.choice([True,False]) for i in range(n)]

def evaluate(problem,solution):
    satisifed = 0
    for clause in  problem:
        clause_satisfied = False
        for var in clause:
            if var[0] == "~":
                var_i = int(var[2:])
                var = not solution[var_i]
            else: 
               var_i = int(var[1:])
               var = solution[var_i]


            clause_satisfied = clause_satisfied or var

        if clause_satisfied:
            satisifed+=1

    return satisifed

def get_neighbors(curr_solution,n):
    neighbors = []
    for i in range(n):
        neighbor = list(curr_solution)
        neighbor[i] = not neighbor[i]
        neighbors.append(tuple(neighbor))
    return neighbors

def get_best_neighbor(problem,curr_solution,n,function=get_neighbors):
    max_value = 0
    best = curr_solution
    changed = False
    neighbors = function(curr_solution,n)

    for neighbor in neighbors:
        value = evaluate(problem,neighbor)
        if value>max_value:
            max_value = value
            best = neighbor
            changed = True

    return changed,best,max_value, set(neighbors)

# HILL CLIMBING


def hill_climbing(problem,n,k,m ,max_steps = 1000):
    all_neighbors = set() # for penetrance
    curr_solution = random_solution(n)
    max_value = evaluate(problem,curr_solution)
    
    for _ in range(max_steps):

        changed,curr_solution,max_value,neighbors = get_best_neighbor(problem,curr_solution,n)
        all_neighbors.update(neighbors)
        if not changed:
            break

    penetrance = len(all_neighbors)
    return curr_solution,max_value,penetrance

# BEAM SEARCH

def beam_search(problem,beam_width,n,max_steps=1000):
    all_neighbors = set() # for penetrance

    curr_solutions = [random_solution(n) for _ in range(beam_width)]

    for _ in range(max_steps):
        next_solution = []
        for solution in curr_solutions:
            neighbors = get_neighbors(solution,n)
            all_neighbors.update(neighbors)
            next_solution.extend(neighbors)

        curr_solutions = sorted(next_solution,key=lambda x:evaluate(problem,x))[:beam_width]

    penetrance = len(all_neighbors)
    return curr_solutions[0],evaluate(problem,curr_solutions[0]),penetrance

#  VND

def get_neighbors_2(curr_solution,n):
    neighbors = []
    for i in range(n):
        for j in range(n):
            neighbor = list(curr_solution)
            neighbor[i] = not neighbor[i]
            neighbor[j] = not neighbor[j]
            neighbors.append(tuple(neighbor))
    return neighbors

def get_neighbors_3(curr_solution,n):
    neighbors = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                neighbor = list(curr_solution)
                neighbor[i] = not neighbor[i]
                neighbor[j] = not neighbor[j]
                neighbor[k] = not neighbor[k]
                neighbors.append(tuple(neighbor))
    return neighbors

def variable_neighbourhood_descent(problem,n,max_steps=1000):
    curr_solution = random_solution(n)
    max_value = evaluate(problem,curr_solution)
    neighborhoods = [get_neighbors,get_neighbors_2,get_neighbors_3]
    all_neighbors = set()
    for _ in range(max_steps):
        for neighborhood in neighborhoods:
            changed,curr_solution,max_value,neighbors = get_best_neighbor(problem,curr_solution,n,function=neighborhood)
            all_neighbors.update(neighbors)
        if not changed:
            break 

    penetrance = len(all_neighbors)
    return curr_solution,max_value,penetrance
# Main
def main():

    n_ = [5,6,7]
    m_ = [3,4,5]
    

    for n in n_:
        for m in m_:
            print("_"*100)
            problem = create_k_sat(3,n,m)

            sol,m,p = hill_climbing(problem,n,3,m)
            print(f"Hill Climbing: \n\tSolution Generated:{sol}\n\tClauses Satisfied: {m}\n\tPentrance: {p}")
            
            sol,m,p = beam_search(problem,3,n)
            print(f"Beam Search with beam width 3: \n\tSolution Generated:{sol}\n\tClauses Satisfied: {m}\n\tPentrance: {p}")

            
            sol,m,p = beam_search(problem,4,n)
            print(f"Beam Search with beam width 4: \n\tSolution Generated:{sol}\n\tClauses Satisfied: {m}\n\tPentrance: {p}")
            
            sol,m,p = variable_neighbourhood_descent(problem,n)
            print(f"Variable Neighborhood Descent: \n\tSolution Generated:{sol}\n\tClauses Satisfied: {m}\n\tPentrance: {p}")


if __name__ == "__main__":
    main()