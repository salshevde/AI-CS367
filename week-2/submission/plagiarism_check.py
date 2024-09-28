import heapq


#  Utility Functions
def preprocess(text):
    text = [line.lower().strip()  for line in text]
    for i, ch in enumerate(text):
        if ch in "!#$%&'()*+,-/:;<=>?@[\\]^_{|}~`":
            text[i] = text.replace(ch,"")
    
    
    return [line.split() for line in text if line]


def levenshtein_dist(s1: str, s2: str):
    n, m = len(s1), len(s2)

    if n < m:
        return levenshtein_dist(s2, s1)

    distances = range(len(s2) + 1)

    for i in range(1,n+1):
        new_dist = [i]
        for j in range(1,m+1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            new_dist.append(min(new_dist[j-1]+1,distances[j]+1,distances[j-1]+cost))
        distances = new_dist
    return distances[m]


def heuristic( i1, i2,file1, file2):
    h = 0
    for i in range(i1, len(file1)):
        min_cost = float("inf")
        for j in range(i2, len(file2)):
            min_cost = min(min_cost, levenshtein_dist(file1[i], file2[j]))
        h += min_cost
    return h


# State


class State:
    def __init__(self, i1, i2, cost, file1,file2, g=0) -> None:
        self.i1 = i1
        self.i2 = i2
        self.cost = cost
        self.file1 = file1
        self.file2 = file2
        self.g = g

    def f(self):
        return self.g + heuristic(self.i1,self.i2,self.file1,self.file2)
    
    def __lt__(self, other):
        return self.f() < other.f()

    def __eq__(self, state):
        return [state.i1, state.i2, state.cost] == [self.i1, self.i2, self.cost]

    def __hash__(self) -> int:
        return hash(tuple(self.i1, self.i2, self.cost))


# Search Agent


class Agent:
    def __init__(self) -> None:
        self.memory = 0

    def Astar(self, file1, file2, initialState: State):
        frontier = []
        heapq.heappush(frontier, (initialState.g, initialState))
        explored = set()

        while frontier:
            curr_cost, curr_state = heapq.heappop(frontier)

            if curr_state.i1 == len(file1) and curr_state.i2 == len(file2):
                return curr_state.cost

            if curr_state.i1 < len(file1) and curr_state.i2 < len(file2):
                edit_cost = levenshtein_dist(file1[curr_state.i1], file2[curr_state.i2])
                new_cost = curr_state.cost + edit_cost

                new_state = State(curr_state.i1 + 1, curr_state.i2 + 1, new_cost,file1,file2)
                heapq.heappush(
                    frontier,
                    (
                        new_cost + heuristic(new_state.i1, new_state.i2,file1, file2 ),
                        new_state,
                    ),
                )

            if curr_state.i1 < len(file1):
                new_state = State(curr_state.i1 + 1, curr_state.i2, curr_state.cost + 1,file1,file2)
                heapq.heappush(
                    frontier,
                    (
                        new_state.cost
                        + heuristic(new_state.i1, new_state.i2,file1, file2, ),
                        new_state,
                    ),
                )

            if curr_state.i2 < len(file2):
                new_state = State(curr_state.i1, curr_state.i2 + 1, curr_state.cost + 1,file1,file2)
                heapq.heappush(
                    frontier,
                    (
                        new_state.cost
                        + heuristic(new_state.i1, new_state.i2,file1, file2),
                        new_state,
                    ),
                )

        return None


def detect_plagiarism(file1_path, file2_path,threshold = 3):
    file1 = open(file1_path, "r")
    file2 = open(file2_path, "r")

    text1 = preprocess(file1.readlines())
    text2 = preprocess(file2.readlines())
    
    search_agent = Agent()
    total_cost = search_agent.Astar(text1, text2, State(0, 0, 0,text1,text2))


    plagiarised = []
    weighted_plagiarism_cost = 0
    for i,sentence1 in enumerate(text1):
        for j,sentence2 in enumerate(text2):
            edit_dist = levenshtein_dist(sentence1,sentence2)
            weighted_plagiarism_cost+= (1-edit_dist/max(len(sentence1),len(sentence2)))
            if edit_dist<=threshold:
                plagiarised.append((i,j,' '.join(sentence1),' '.join(sentence2),edit_dist))
                
                print(plagiarised[-1])


    plagiarism_percentage = min(100.0,weighted_plagiarism_cost*100/max(len(text1),len(text2)))
    print("\nPLAGIARISM-PERCENTAGE: ",plagiarism_percentage)

    if plagiarism_percentage>=95:
        print("Identical Documents")
    elif plagiarism_percentage>=60:
        print("Similar Document")
        
    elif plagiarism_percentage>=30:
        print("Partial Overlap")
        
    elif plagiarism_percentage>=10:
        print("Little Overlap")

    else:
        print("No Overlap")
    print("\n\n")
    file1.close()
    file2.close()
    return total_cost,len(text1),len(text2)


# Analysis Functions

def test():

    statements = []
    for i in range(1, 5):
        test_case = f"./week-2/submission/test_cases/test{i}/"
        title_file = open(f"./week-2/submission/test_cases/test{i}/case-title.txt")
        
        title = title_file.read()
        print(title)
        print("_"*100)
        c,l1,l2 = detect_plagiarism(test_case + "file1.txt", test_case + "file2.txt")
        statements.append(f"{title:<35}|{c:<20}|{l1:<20}|{l2:<20}")
        title_file.close()

    print("-"*40+"Test-Cases-Analysis"+"-"*40)
    print(f"{'Test-type':<35}|{'Alignment Cost':<20}|{'Length of Doc1':<20}|{'Length of Doc2':<20}")
    print("_"*100)
    for i in range(4):
        print(statements[i])



#  Main
def main():

    test()


if __name__ == "__main__":
    main()
