import sys
class State:
    def __init__(self,positions,parent = None,action ="initial-state") -> None:
        self.positions = positions # -1 -> west moving (-), 1-> east moving (+), 0 empty stone
        self.parent = parent
        if action != "initial-state":
            self.bun ,self.bun_ini,self.bun_steps,self.bun_final = action
            self.action = "intermediary-state"
            self.shortest_path = sys.maxsize
        else:
            self.action = action
            self.shortest_path = 0    
        
    def setShortest(self):
        self.shortest_path = min(self.shortest_path,self.parent.shortest_path)

    
    def isGoal(self):
        return self.positions ==[0]*len(self.positions) 
    
    def __eq__(self,state):
        return state.positions == self.positions

    def __hash__(self) -> int:
        return hash(tuple(self.positions))
    def generateStates(self):
        possibleStates = []

        n = len(self.positions)
        
        for i in range(n):
            bun = self.positions[i]
            if bun==0: 
                continue
            
            for j in range(2): # simulate jumps 
                jump = i+(bun)*(j+1)
                if not(0<=jump<n) or self.positions[jump] == 0: 
                    
                    newState = self.positions.copy()
                    newState[i]= 0
                    if 0<=jump<n:
                        newState[jump] = bun
                    possibleStates.append(State(newState,parent =self,action=[bun,i,j+1,jump]))
        return possibleStates

    def printgenerateStatess(self):
        states = self.generateStates()
        for x in states:
            print(x.positions)
        print("")


def BFS(initialState:State):
    frontier = [initialState]
    explored = set()
    
    while frontier:
        curr_state = frontier.pop(0)    
        if curr_state.isGoal():
            print("Number of Valid Nodes Explored: ",len(explored))
            return curr_state
        explored.add(curr_state)
        
        possibleStates = curr_state.generateStates()
        for state in possibleStates:
            if (state not in explored) and (state not in frontier):
                frontier.append(state)
    print("Number of Valid Nodes Explored: ",len(explored))
    return None
def DFS(initialState:State):
    frontier = [initialState]
    explored = set()
    
    while frontier:
        curr_state = frontier.pop()    
        if curr_state.isGoal():
            print("Number of Valid Nodes Explored: ",len(explored))
            return curr_state
        explored.add(curr_state)
        
        possibleStates = curr_state.generateStates()
        for state in possibleStates:
            if (state not in explored) and (state not in frontier):
                frontier.append(state)
    return None

def solutionBFS(initialState:State):
    
    goal = BFS(initialState)
    path = [goal]
    if not goal:
        return None
    parent = goal.parent

    while parent:
        path.append(parent)
        parent = parent.parent
    while path:
        state = path.pop()
        
        print(state.positions,state.action\
            if state.action== "initial-state"\
            else  f"{"East" if state.bun==1 else "West" }\
            -facing rabbit at index {state.bun_ini} jumps\
            {state.bun_steps} rocks to {state.bun_final \
            if (0<=state.bun_final <len(state.positions)) else "destination"} index")

def solutionDFS(initialState:State):
    
    goal = DFS(initialState)
    path = [goal]
    if not goal:
        return None
    parent = goal.parent

    while parent:
        path.append(parent)
        parent = parent.parent
    while path:
        state = path.pop()
        
        print(state.positions,state.action if state.action== "initial-state" else  f"{"East" if state.bun==1 else "West" }-facing rabbit at index {state.bun_ini} jumps{state.bun_steps} rocks to {state.bun_final if (0<=state.bun_final <len(state.positions)) else "destination"} index")
def optimalBFS(initialState:State):
    frontier = [initialState]
    explored = set()

    while frontier:
        curr_state = frontier.pop(0)    
        
        if curr_state.isGoal():
            print("Number of Valid Nodes Explored: ",len(explored))
            return curr_state
        explored.add(curr_state)
        
        possibleStates = curr_state.generateStates()
        for state in possibleStates:
            if (state not in explored) and (state not in frontier):
                frontier.append(state)
                
                if state.shortest_path>curr_state.shortest_path+1:
                    state.parent = curr_state
                    state.shortest_path = curr_state.shortest_path+1
  
    return None
def optimalBFSsolution(initialState:State):
    goal = optimalBFS(initialState)
    path = [goal]
    solution  =0
    if not goal:
        return 'NOTHING'
    parent = goal.parent

    while parent:
        path.append(parent)
        parent = parent.parent
        solution+=1
    while path:
        state = path.pop()
        print(state.positions,state.action if state.action== "initial-state" else  f"{"East" if state.bun==1 else "West" }-facing rabbit at index {state.bun_ini} jumps {state.bun_steps} rocks to {state.bun_final if (0<=state.bun_final <len(state.positions)) else "destination"} index")
    print(solution)
def main():

    ini = eval(input("Initial-State: "))
    initialState = State(ini) #[1,1,1,0,-1,-1,-1]
    
    # initialState.printgenerateStatess()
    print("BFS ")
    optimalBFSsolution(initialState)
    print("\nDFS ")
    solutionDFS(initialState)
    
if __name__ == "__main__":
    main()