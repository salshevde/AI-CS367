import sys
from collections import deque

class State:
    def __init__(self,m,c,b,parent = None,action ="initial-state") -> None:
        self.positions = [m,c,b ]   
        '''
        (m,c,b) = (0..3, 0..3,0/1) 
        boat : left = 0
        '''
        self.parent = parent
        self.action = action
        if action != "initial-state":
            # self.bun ,self.bun_ini,self.bun_steps,self.bun_final = action
            
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
    
    def isValid(self)->bool:
        m,c,b = self.positions
        if m>3 or c>3 or m<0 or c<0:
            return False
        if m>0 and m<c:
            return False
        
        if 3-m>0 and 3-m <3-c:
            return False
        return True


    def generateStates(self):
        possibleStates = []
        m,c,b = self.positions
        # combinations of people: mm,mc,cc,m,c
        moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]

        mul = 1 if b==0 else -1 
        for move in moves:
            new_state = State(m+mul*(move[0]), c+mul*(move[1]), 0 if b==1 else 1,self,action=[move,b])
            if new_state.isValid():
                possibleStates.append(new_state)

        return possibleStates

    def printgenerateStatess(self):
        states = self.generateStates()
        for x in states:
            print(x.positions)
        print("")

def BFS(initialState:State):
    frontier = deque([initialState])
    explored = set()
    
    while frontier:
        curr_state = frontier.popleft()
        if curr_state in explored:
            continue
        explored.add(curr_state)
        if curr_state.isGoal():
            print("Number of Valid Nodes Explored: ",len(explored))
            return curr_state
        
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
        m,c,b = state.positions
        boat = (" "*5)+"B"+(" "*5)
        print(f'{m*' M '+(3-m)*'   '}{c*' C '+(3-c)*'   '}|{boat.rstrip() if b==0 else boat.lstrip()}|{(3-m)*' M '+m*"   "}{(3-c)*' C '+c*"   "}',end = ": ")

        if state.action == 'initial-state':
            print(state.action)
        else:
            move,boat_move = state.action
            direction = "RIGHT TO LEFT"if boat_move == 0 else "LEFT TO RIGHT"
            statement = f"{move[0]} missionaries" if move[0] else "" + ("and" if move[0] else "")+ f"{move[1]} cannibals" if move[1] else ""
            print(statement+" move "+direction)
        print()

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
        m,c,b = state.positions
        boat = (" "*5)+"B"+(" "*5)
        print(f'{m*' M '+(3-m)*'   '}{c*' C '+(3-c)*'   '}|{boat.rstrip() if b==0 else boat.lstrip()}|{(3-m)*' M '+m*"   "}{(3-c)*' C '+c*"   "}',end = ": ")

        if state.action == 'initial-state':
            print(state.action)
        else:
            move,boat_move = state.action
            direction = "RIGHT TO LEFT"if boat_move == 0 else "LEFT TO RIGHT"
            statement = f"{move[0]} missionaries" if move[0] else "" + ("and" if move[0] else "")+ f"{move[1]} cannibals" if move[1] else ""
            print(statement+" move "+direction)
        print()
def main():

    ini = eval(input("Initial-State: "))
    initialState = State(ini[0],ini[1],ini[2]) # [3,3,1]
    
    # initialState.printgenerateStatess()
    print("BFS ")
    solutionBFS(initialState)
    print("\nDFS ")
    solutionDFS(initialState)
    
if __name__ == "__main__":
    main()
