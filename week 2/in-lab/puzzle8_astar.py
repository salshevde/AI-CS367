import heapq
import random
from time import time
import sys

default = [1, 2, 3, 4, 5, 6, 7, 8, 0]


def heuristic(state, goal_state):
    h = 0
    for i in range(9):
        if state.positions[i]:
            goal_i = goal_state.index(state.positions[i])
            h += abs(i // 3 - goal_i // 3) + abs(i % 3 - goal_i % 3)
    return h


class State:
    def __init__(self, positions, goal_state, parent=None, g=0) -> None:
        self.positions = positions
        self.parent = parent
        self.g = g
        self.h = heuristic(self, goal_state)  # to goal
        self.f = self.g + self.h
        self.goal_state = goal_state

    def getSuccessors(self):
        possible_states = []
        index = self.positions.index(0)
        x, y = index // 3, index % 3
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for move in moves:
            new_x, new_y = move[0] + x, move[1] + y
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                ind = new_x * 3 + new_y
                new_positions = list(self.positions)
                new_positions[ind], new_positions[index] = (
                    new_positions[index],
                    new_positions[ind],
                )
                possible_states.append(
                    State(new_positions, self.goal_state, self, self.g + 1)
                )
        return possible_states

    def isGoal(self):
        return self.positions == self.goal_state

    def __lt__(self, other):
        return self.g < other.g

    def __eq__(self, state):
        return state.positions == self.positions

    def __hash__(self) -> int:
        return hash(tuple(self.positions))


class Agent:
    def __init__(self) -> None:
        self.memory = 0

    def BFS(self, initialState: State):
        frontier = []
        heapq.heappush(frontier, (initialState.g, initialState))
        explored = set()

        while frontier:
            _, curr_state = heapq.heappop(frontier)
            if curr_state in explored:
                continue
            explored.add(curr_state)
            if curr_state.isGoal():
                # print("Number of Valid Nodes Explored: ",len(explored))
                state_size = sys.getsizeof(State([0] * 9, [0] * 9))
                self.memory = len(frontier) * (state_size) + len(explored) * (
                    state_size
                )
                return curr_state

            possibleStates = curr_state.getSuccessors()
            for state in possibleStates:
                state.h = heuristic(state, initialState.goal_state)
                state.f = state.g + state.h
                heapq.heappush(frontier, (state.f, state))
        # print("Number of Valid Nodes Explored: ",len(explored))

        return None

    def solutionBFS(self, initialState: State):

        goal = self.BFS(initialState)
        path = [goal]
        if not goal:
            return None
        parent = goal.parent

        while parent:
            path.append(parent)
            parent = parent.parent
        while path:
            state = path.pop()
            arr = state.positions

            for i in range(9):
                print(arr[i] if arr[i] != 0 else "_", end="  ")
                if (i + 1) % 3 == 0:
                    print()

            print("\n")


def generate_config(initialState: State, d: int):
    state = initialState

    for _ in range(d):
        possible = state.getSuccessors()
        state = random.choice(possible)

    return state.positions


def generate_config_diverse(initialState: State, d: int):
    state = initialState
    last_move = None
    for _ in range(d):
        possible = state.getSuccessors()
        if last_move is not None:
            possible = [state for state in possible if state != last_move]
        state = random.choice(possible)
        last_move = state
        state = random.choice(possible)

    return state.positions


def usage_analysis():
    depths = [i for i in range(501)]
    goal_state = State(default,default)

    print("---------------------------USAGE ANALYSIS--------------------")
    print("depth\t| time\t|memory\t")
    for d in depths:
        time_taken = 0
        memory = 0

        for _ in range(50):
            initial_state = State(generate_config(goal_state, d),default)

            start_time = time()
            search_agent = Agent()
            search_agent.BFS(initial_state)
            end_time = time()

            time_taken += end_time - start_time
            memory += search_agent.memory

        time_taken /= 50
        memory = memory / 50

        print(d, time_taken, memory,sep="\t")


def main():

    ini = generate_config(State(default, default), 10)
    goal = default
    initial_state = State(ini, goal)
    search_agent = Agent()
    search_agent.solutionBFS(initial_state)

    usage_analysis()

if __name__ == "__main__":
    main()
