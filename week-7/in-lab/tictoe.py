import random

class MENACE:
    def __init__(self):
        self.boxes = {}
        self.create_boxes()

    def create_boxes(self):
        initial_state = "........."
        self.add_box(initial_state)
        states_to_generate = [initial_state]
        visited_states = set([initial_state])

        while states_to_generate:
            current_state = states_to_generate.pop()
            next_states = self.get_next_states(current_state, 'X') + self.get_next_states(current_state, 'O')

            for state, move in next_states:
                if state not in visited_states:
                    self.add_box(state)
                    visited_states.add(state)
                    states_to_generate.append(state)

    def add_box(self, state):
        self.boxes[state] = [3 if c == '.' else 0 for c in state]

    def get_next_states(self, state, player):
        next_states = []
        for i, c in enumerate(state):
            if c == '.':
                next_state = state[:i] + player + state[i+1:]
                next_states.append((next_state, i))
        return next_states

    def choose_move(self, state):
        if state not in self.boxes:
            raise Exception(f"No box found for state {state}")

        beads = self.boxes[state]
        total_beads = sum(beads)
        if total_beads == 0:
            return random.choice([i for i, c in enumerate(state) if c == '.'])

        choices = []
        for move, count in enumerate(beads):
            choices += [move] * count

        return random.choice(choices)

    def update_box(self, state, move, result):
        if result == "win":
            self.boxes[state][move] += 3
        elif result == "draw":
            self.boxes[state][move] += 1
        elif result == "loss":
            self.boxes[state][move] = max(0, self.boxes[state][move] - 1)

    def play_game(self, human_first=True):
        state = "........."
        history = []

        while True:
            self.display_board(state)

            if not human_first:
                move = self.choose_move(state)
                print(f"MENACE plays X at position {move + 1}")
                history.append((state, move))
                state = state[:move] + 'X' + state[move+1:]
                if self.is_winner(state, 'X'):
                    self.display_board(state)
                    print("MENACE wins!")
                    for state, move in history:
                        self.update_box(state, move, "win")
                    return "win"
                human_first = True

            if '.' not in state:
                self.display_board(state)
                print("It's a draw!")
                for state, move in history:
                    self.update_box(state, move, "draw")
                return "draw"

            human_move = self.get_human_move(state)
            state = state[:human_move] + 'O' + state[human_move+1:]

            if self.is_winner(state, 'O'):
                self.display_board(state)
                print("You win!")
                for state, move in history:
                    self.update_box(state, move, "loss")
                return "loss"

            move = self.choose_move(state)
            print(f"MENACE plays X at position {move + 1}")
            history.append((state, move))
            state = state[:move] + 'X' + state[move+1:]

            if self.is_winner(state, 'X'):
                self.display_board(state)
                print("MENACE wins!")
                for state, move in history:
                    self.update_box(state, move, "win")
                return "win"

            if '.' not in state:
                self.display_board(state)
                print("It's a draw!")
                for state, move in history:
                    self.update_box(state, move, "draw")
                return "draw"

    def get_human_move(self, state):
        valid_moves = [i for i, c in enumerate(state) if c == '.']
        move = None
        while move not in valid_moves:
            try:
                move = int(input(f"Enter your move (1-9): ")) - 1
                if move not in valid_moves:
                    print("Invalid move, try again.")
            except ValueError:
                print("Please enter a number between 1 and 9.")
        return move

    def display_board(self, state):
        print("\n")
        for i in range(0, 9, 3):
            row = state[i:i+3]
            print(" " + " | ".join(c if c != '.' else str(i+1) for i, c in enumerate(row, start=i)))
            if i < 6:
                print("---+---+---")
        print("\n")

    def is_winner(self, state, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if all(state[i] == player for i in combo):
                return True
        return False

menace = MENACE()

print("Welcome to Tic-Tac-Toe!")
menace.play_game(human_first=False)
