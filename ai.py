import copy
from heapq import heappush, heappop

n = 3
directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

class PriorityQueue:
    def __init__(self):
        self.heap = []
    def push(self, item):
        heappush(self.heap, item)
    def pop(self):
        return heappop(self.heap)
    def is_empty(self):
        return len(self.heap) == 0

class Node:
    def __init__(self, parent, matrix, empty_pos, cost, depth):
        self.parent = parent
        self.matrix = matrix
        self.empty_pos = empty_pos
        self.cost = cost
        self.depth = depth
    def __lt__(self, other):
        return self.cost < other.cost

def calculate_cost(matrix, goal):
    return sum(1 for i in range(n) for j in range(n) if matrix[i][j] and matrix[i][j] != goal[i][j])

def create_node(matrix, empty_pos, new_empty_pos, depth, parent, goal):
    new_matrix = copy.deepcopy(matrix)
    x1, y1 = empty_pos
    x2, y2 = new_empty_pos
    new_matrix[x1][y1], new_matrix[x2][y2] = new_matrix[x2][y2], new_matrix[x1][y1]
    cost = calculate_cost(new_matrix, goal)
    return Node(parent, new_matrix, new_empty_pos, cost, depth)

def display_matrix(matrix):
    for row in matrix:
        print(" ".join(str(cell) for cell in row))
    print()

def print_solution_path(node):
    if node is None:
        return
    print_solution_path(node.parent)
    display_matrix(node.matrix)

def is_within_bounds(x, y):
    return 0 <= x < n and 0 <= y < n

def solve_puzzle(initial, empty_pos, goal):
    queue = PriorityQueue()
    initial_cost = calculate_cost(initial, goal)
    root = Node(None, initial, empty_pos, initial_cost, 0)
    queue.push(root)

    while not queue.is_empty():
        current = queue.pop()
        if current.cost == 0:
            print_solution_path(current)
            return

        for dx, dy in directions:
            new_empty_pos = [current.empty_pos[0] + dx, current.empty_pos[1] + dy]
            if is_within_bounds(new_empty_pos[0], new_empty_pos[1]):
                child = create_node(current.matrix, current.empty_pos, new_empty_pos, current.depth + 1, current, goal)
                queue.push(child)

initial = []
goal = []

print("Enter the initial matrix:")
for _ in range(3):
    row = [int(input()) for _ in range(3)]
    initial.append(row)

print("Enter the goal matrix:")
for _ in range(3):
    row = [int(input()) for _ in range(3)]
    goal.append(row)

empty_tile_pos = None
for i in range(3):
    for j in range(3):
        if initial[i][j] == 0:
            empty_tile_pos = [i, j]
            break
    if empty_tile_pos:
        break

solve_puzzle(initial, empty_tile_pos, goal)
