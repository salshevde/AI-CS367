import random

def create_k_sat(clause_length,n_clauses,n_var):

    variables = [("a"+str(i)) for i in range(n_var)]

    problem = ""
    problem_lst = []

    for i in range(n_clauses):
        # n_var c j: choose j from n_var
        chosen_variables = random.sample(variables,clause_length)
        if i!=0:
            problem += "&" 
        clause = "("
        clause_lst = []

        for j, var in enumerate(chosen_variables):
            if j!=0:
                clause+="|"
                
            if random.randint(0,1): # randomly negate
                var = "~"+var
                
            clause+=var
            clause_lst.append(var)

        clause+=")"

        problem+=clause
        problem_lst.append(clause_lst)
    print(problem)
    return problem_lst
# def main():
#     k = int(input("Enter clause length: "))
#     m = int(input("Enter number of clauses: "))
#     n = int(input("Enter number of variables: "))

#     create_k_sat(k,m,n)
# if __name__ == "__main__":
#     main()
