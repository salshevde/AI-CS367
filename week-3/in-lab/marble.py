import heapq
import numpy as np

class MarbleSolitaire:
    def __init__(self, board=None):
        self.initial_board = board if board is not None else self.create_initial_board()
        self.goal_state = self.create_goal_state()

    def create_initial_board(self):
        board = np.zeros((7, 7), dtype=int)
        board[1:6, 1:6] = 1  
        board[3, 3] = 0       
        return board

    def create_goal_state(self):
        goal = np.zeros((7, 7), dtype=int)
        goal[3, 3] = 1
        return goal

    def is_goal_state(self, board):
        return np.array_equal(board, self.goal_state)

    def get_possible_moves(self, board):
        moves = []
        for i in range(7):
            for j in range(7):
                if board[i, j] == 1:
                    for di, dj in [(0, 2), (2, 0), (0, -2), (-2, 0), (2, 2), (2, -2), (-2, 2), (-2, -2)]:
                        if self.is_valid_move(board, i, j, di, dj):
                            moves.append((i, j, di, dj))
        return moves

    def is_valid_move(self, board, i, j, di, dj):
        ni, nj = i + di, j + dj
        mi, mj = i + di // 2, j + dj // 2
        return (0 <= ni < 7 and 0 <= nj < 7 and 
                board[ni, nj] == 0 and 
                board[mi, mj] == 1)

    def make_move(self, board, i, j, di, dj):
        ni, nj = i + di, j + dj
        mi, mj = i + di // 2, j + dj // 2
        new_board = board.copy()
        new_board[i, j] = 0
        new_board[mi, mj] = 0
        new_board[ni, nj] = 1
        return new_board

    def heuristic_remaining_marbles(self, board):
        return np.sum(board)

    def heuristic_distance_to_center(self, board):
        distances = 0
        for i in range(7):
            for j in range(7):
                if board[i, j] == 1:
                    distances += abs(i - 3) + abs(j - 3)
        return distances

    def best_first_search(self, heuristic):
        open_set = []
        heapq.heappush(open_set, (heuristic(self.initial_board), self.initial_board.tobytes(), []))   
        visited = set()

        while open_set:
            _, current_board_bytes, path = heapq.heappop(open_set)
            current_board = np.frombuffer(current_board_bytes, dtype=int).reshape(7, 7)

            if self.is_goal_state(current_board):
                return path

            visited.add(current_board.tobytes())

            for move in self.get_possible_moves(current_board):
                new_board = self.make_move(current_board, *move)
                new_move = (current_board, move, new_board)
                if new_board.tobytes() not in visited:
                    heapq.heappush(open_set, (heuristic(new_board), new_board.tobytes(), path + [new_move]))

        return None

    def a_star_search(self, heuristic):
        open_set = []
        heapq.heappush(open_set, (heuristic(self.initial_board), 0, self.initial_board.tobytes(), []))   
        visited = set()

        while open_set:
            _, cost, current_board_bytes, path = heapq.heappop(open_set)
            current_board = np.frombuffer(current_board_bytes, dtype=int).reshape(7, 7)

            if self.is_goal_state(current_board):
                return path

            visited.add(current_board.tobytes())

            for move in self.get_possible_moves(current_board):
                new_board = self.make_move(current_board, *move)
                new_cost = cost + 1
                new_move = (current_board, move, new_board)

                if new_board.tobytes() not in visited:
                    total_cost = new_cost + heuristic(new_board)
                    heapq.heappush(open_set, (total_cost, new_cost, new_board.tobytes(), path + [new_move]))

        return None

    def display_board(self, board):
        for row in board:
            print(" ".join([str(x) for x in row]))
        print()

 
game = MarbleSolitaire()

print("Running Best First Search (Remaining Marbles Heuristic):")
best_first_path = game.best_first_search(game.heuristic_remaining_marbles)
if best_first_path:
    print("Goal Reached: True")
    print("Moves to Solution:")
    for step in best_first_path:
        game.display_board(step[2])   
else:
    print("No solution found.")

print("\nRunning A* Search (Distance to Center Heuristic):")
a_star_path = game.a_star_search(game.heuristic_distance_to_center)
if a_star_path:
    print("Goal Reached: True")
    print("Moves to Solution:")
    for step in a_star_path:
        game.display_board(step[2])   
else:
    print("No solution found.")
