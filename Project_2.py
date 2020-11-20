from copy import deepcopy
from collections import deque
import time
import numpy as np

class Node:
    def __init__(self, parent, grid):
        self.parent = parent
        self.grid = grid

def print_answer(groundzero_initial, node_initial, groundzero_goal, node_goal):
    initial_to_middle = []
    while node_initial.parent:
        initial_to_middle.insert(0, node_initial.grid)
        node_initial = node_initial.parent
    print("\nStep by step solution:\n")
    print(np.matrix(groundzero_initial.grid), "\n")
    for i in initial_to_middle:
        print(np.matrix(i), "\n")
    print("-----------middle--------------", "\n")
    while node_goal.parent:
        print(np.matrix(node_goal.grid), "\n")
        node_goal = node_goal.parent
    print(np.matrix(groundzero_goal.grid), "\n")

def goaltest(node_initial, node_goal, frontier_initial, frontier_goal, initial, goal):
    if node_initial.grid == node_goal.grid:
        print_answer(initial, node_initial, goal, node_goal)
        return True
    
    for x in frontier_initial:
        if node_goal.grid == x.grid:
            node_initial = x
            print_answer(initial, node_initial, goal, node_goal)
            return True
    
    for x in frontier_goal:
        if node_initial.grid == x.grid:
            node_goal = x
            print_answer(initial, node_initial, goal, node_goal)
            return True
    
    return False

def check_grid(grid, frontier, explored):       # Question: cross 'explored' check or not? (13 0 14 0 case)
    frontier_len = len(frontier)
    if frontier_len == 0:
        if grid not in explored:
            return True
    else:
        if grid not in explored:
            for i in range(frontier_len):
                if frontier[i].grid == grid:
                    return False
        else:
            return False
    return True

def expand(node, frontier, explored):
    first_0 = [None, None]
    second_0 = [None, None]

    found_first_0 = False
    found_all_0 = False
    for i in range(4):
        if not found_all_0:
            for j in range(4):
                if node.grid[i][j] == 0:
                    if not found_first_0:
                        first_0 = [i, j]
                        found_first_0 = True
                    else:
                        second_0 = [i, j]
                        found_all_0 = True
                        break
        else:
            break
    
    move_left(node, first_0, frontier, explored)
    move_left(node, second_0, frontier, explored)
    move_right(node, first_0, frontier, explored)
    move_right(node, second_0, frontier, explored)
    move_up(node, first_0, frontier, explored)
    move_up(node, second_0, frontier, explored)
    move_down(node, first_0, frontier, explored)
    move_down(node, second_0, frontier, explored)

def add_to_frontier(node, child_grid, frontier):
    child = Node(node, child_grid)
    frontier.append(child)

def move_left(node, coordinate, frontier, explored):
    i, j = coordinate[0], coordinate[1]
    if j == 0 or node.grid[i][j-1] == 0:
        pass
    else:
        child_grid = deepcopy(node.grid)
        child_grid[i][j], child_grid[i][j-1] = child_grid[i][j-1], child_grid[i][j]
        if check_grid(child_grid, frontier, explored):
            add_to_frontier(node, child_grid, frontier)

def move_right(node, coordinate, frontier, explored):
    i, j = coordinate[0], coordinate[1]
    if j == 3 or node.grid[i][j+1] == 0:
        pass
    else:
        child_grid = deepcopy(node.grid)
        child_grid[i][j], child_grid[i][j+1] = child_grid[i][j+1], child_grid[i][j]
        if check_grid(child_grid, frontier, explored):
            add_to_frontier(node, child_grid, frontier)

def move_up(node, coordinate, frontier, explored):
    i, j = coordinate[0], coordinate[1]
    if i == 0 or node.grid[i-1][j] == 0:
        pass
    else:
        child_grid = deepcopy(node.grid)
        child_grid[i][j], child_grid[i-1][j] = child_grid[i-1][j], child_grid[i][j]
        if check_grid(child_grid, frontier, explored):
            add_to_frontier(node, child_grid, frontier)

def move_down(node, coordinate, frontier, explored):
    i, j = coordinate[0], coordinate[1]
    if i == 3 or node.grid[i+1][j] == 0:
        pass
    else:
        child_grid = deepcopy(node.grid)
        child_grid[i][j], child_grid[i+1][j] = child_grid[i+1][j], child_grid[i][j]
        if check_grid(child_grid, frontier, explored):
            add_to_frontier(node, child_grid, frontier)

def bidirectional_search(initial, frontier_initial, explored_initial, goal, frontier_goal, explored_goal):
    while frontier_initial and frontier_goal:
        node_initial = deque.popleft(frontier_initial)
        node_goal = deque.popleft(frontier_goal)
        if goaltest(node_initial, node_goal, frontier_initial, frontier_goal, initial, goal):
            break
        else:
            explored_initial.append(node_initial.grid)
            expand(node_initial, frontier_initial, explored_initial)
            explored_goal.append(node_goal.grid)
            expand(node_goal, frontier_goal, explored_goal)

def read_input_file(filename, grid):
    numbers = ""
    numbers_counter = 0

    f = open(filename, "r")
    numbers = f.readline().split(" ")
    f.close()

    for i in range(4):
        for j in range(4):
            grid[i][j] = int(numbers[numbers_counter])
            numbers_counter += 1
    
    return grid

grid = [[None for _ in range(4)] for _ in range(4)]
grid = read_input_file("input.txt", grid)

initial = Node(None, grid)
frontier_initial = deque()
frontier_initial.append(initial)
explored_initial = []

goal_grid = [[1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 0, 0]]
goal = Node(None, goal_grid)
frontier_goal = deque()
frontier_goal.append(goal)
explored_goal = []

start_time = time.time()

bidirectional_search(initial, frontier_initial, explored_initial, goal, frontier_goal, explored_goal)

print("Initial side")
print("frontier: ", len(frontier_initial))
print("explored: ", len(explored_initial), "\n")
print("Goal side")
print("frontier: ", len(frontier_goal))
print("explored: ", len(explored_goal))

print("--- %s seconds ---" % (time.time() - start_time))