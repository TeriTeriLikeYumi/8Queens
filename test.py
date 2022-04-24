#Task E
from queue import PriorityQueue
import re #Regulare expression to check whether the input is valid
SIZE = 8
class State:
    def __init__(self,queens:list):
        self.queens = queens
        self.board = [[False]*SIZE for i in range(SIZE)]
        for coordinate in queens:
            x = coordinate[0]
            y = coordinate[1]
            self.board[x][y] = True
            
    #Redefine the comparison function     
    def __lt__(self,other):
        return self.heuristic_value() < other.heuristic_value()
    
    def __hash__(self):
        hash_value = 0
        two = 1
        for i in range(SIZE*SIZE):
            x = i // SIZE
            y = i % SIZE
            if self.board[x][y]:
                hash_value += two
            two *= 2
        return hash_value
    def __str__(self):
        str = ""
        for i in range(SIZE):
            tmp =""
            for j in range(SIZE):
                if self.board[i][j]:
                    tmp += " Q "
                else:
                    tmp += " . "
            tmp += "\n"
            str+=tmp
        return str
    
    def is_valid(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] and not self.is_possible((i, j)):
                    return False
        return True
    def is_goal(self):
        return self.is_valid() and len(self.queens) == SIZE
      
    def is_possible(self,coordinate: tuple):
        row = coordinate[0]
        col = coordinate[1]
        
        #Check row and column
        for i in range(SIZE):
            if (self.board[row][i] and i != col) or (self.board[i][col] and i != row):
                return False
 
        #Check diagonals
        for i in range(-SIZE,SIZE+1):
            if i == 0:
                continue
            x = row + i
            y = col + i
            
            if x>=0 and x<SIZE and y>=0 and y<SIZE:
                if self.board[x][y]:
                    return False
                
            x = row - i
            y = col + i
            
            if x>=0 and x<SIZE and y>=0 and y<SIZE:
                if self.board[x][y]:
                    return False
                
        return True
    
    def place_a_queen(self,coordinate):
        queens = self.queens[:]
        queens.append(coordinate)
        return State(queens)
    
    def get_successors(self):
        successors = []
        for i in range(SIZE):
            if sum(self.board[i]) == 0:
                for j in range(SIZE):
                    if self.is_possible((i,j)):
                        successors.append(self.place_a_queen((i,j)))
        return successors
    def heuristic_value(self):
        h = 0
        for i in range(SIZE):
            for j in range(SIZE):
                if self.is_possible((i,j)) and not self.board[i][j]:
                    h += 1
        return h
    
def A_star(queens):
    start = State(queens)
    if not start.is_valid():
        print("Invalid start state")
        return None
        
    pq = PriorityQueue()
    pq.put(start)
    visited = set()
    visited.add(start)    
    
    while not pq.empty():
        current = pq.get()
        if current.is_goal():
            return current  
          
        successor = current.get_successors()
        for next in current.get_successors():
            if next not in visited:
                visited.add(next)
                pq.put(next)
                    
    return None

queens = []
file = input("PLease input the file name: ")
with open(file) as f:
    queen_count = f.readline()
    inp = f.readline().rstrip()
    lines = inp.split(" ")

for i in range(len(lines)):
    line = lines[i]
    coordinate = re.findall(r'\d+',line)
    assert len(coordinate) == 2
    coordinate = (int(coordinate[0]),int(coordinate[1]))
    queens.append(coordinate)
    
solution = A_star(queens)
if solution is None:
    print("No solution")
else:
    print(solution)
    
f.close()