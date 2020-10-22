from copy import deepcopy
from collections import deque
import os
import time

class Node:
    def __init__(self, parent, grid):
        self.parent = parent
        self.grid = grid
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def goaltest(self, node_initial, node_goal, frontier_initial, frontier_goal, groundzero_initial, groundzero_goal):

        if node_initial.grid == node_goal.grid:
            self.print_answer(node_initial, node_goal, node_initial.grid, node_goal.grid, groundzero_initial, groundzero_goal)
            return True
        
        for x in frontier_initial:
            if node_goal.grid == x.grid:
                self.print_answer(x, node_goal, x.grid, node_goal.grid, groundzero_initial, groundzero_goal)
                return True
        
        for x in frontier_goal:
            if node_initial.grid == x.grid:
                self.print_answer(node_initial, x, node_initial.grid, x.grid, groundzero_initial, groundzero_goal)
                return True
    
        return False

    def expand(self, node, frontier):
        print("> Node expansion started, please wait...", "\n")
        first_0 = [None, None]      # [i, j]
        second_0 = [None, None]     # [i, j]

        found_first = False

        #find all blank spaces
        for i in range(4):
            for j in range(4):
                if node.grid[i][j] == 0:
                    if not found_first:
                        first_0 = [i, j]
                        found_first = True
                    else:
                        second_0 = [i, j]

        # perform all possible move
        self.move_left(node, first_0)
        self.move_left(node, second_0)
        self.move_right(node, first_0)
        self.move_right(node, second_0)
        self.move_up(node, first_0)
        self.move_up(node, second_0)
        self.move_down(node, first_0)
        self.move_down(node, second_0)


        # check frontier
        if not frontier:
            for x in node.children:
                frontier.append(x)
                #print(x.grid)

        else:
            frontier_len = len(frontier)
            for i in range(frontier_len):
                for x in node.children:
                    if frontier[i].grid != x.grid:
                        frontier.append(x)
                        #print(x.grid)
        print("> Node expansion done...", "\n")

    def move_left(self, node, coordinate):
        i, j = coordinate[0], coordinate[1]
        if j == 0 or node.grid[i][j-1] == 0:
            pass
        else:
            child_grid = deepcopy(node.grid)
            child_grid[i][j], child_grid[i][j-1] = child_grid[i][j-1], child_grid[i][j]
            child = Node(node, child_grid)
            node.add_child(child)

    def move_right(self, node, coordinate):
        i, j = coordinate[0], coordinate[1]
        if j == 3 or node.grid[i][j+1] == 0:
            pass
        else:
            child_grid = deepcopy(node.grid)
            child_grid[i][j], child_grid[i][j+1] = child_grid[i][j+1], child_grid[i][j]
            child = Node(node, child_grid)
            node.add_child(child)

    def move_up(self, node, coordinate):
        i, j = coordinate[0], coordinate[1]
        if i == 0 or node.grid[i-1][j] == 0:
            pass
        else:
            child_grid = deepcopy(node.grid)
            child_grid[i][j], child_grid[i-1][j] = child_grid[i-1][j], child_grid[i][j]
            child = Node(node, child_grid)
            node.add_child(child)

    def move_down(self, node, coordinate):
        i, j = coordinate[0], coordinate[1]
        if i == 3 or node.grid[i+1][j] == 0:
            pass
        else:
            child_grid = deepcopy(node.grid)
            child_grid[i][j], child_grid[i+1][j] = child_grid[i+1][j], child_grid[i][j]
            child = Node(node, child_grid)
            node.add_child(child)

    def bidirectional_search(self, initial, frontier_initial, explored_initial, goal, frontier_goal, explored_goal):
        groundzero_initial = frontier_initial[0]
        groundzero_goal = frontier_goal[0]
        while frontier_initial and frontier_goal:
            node_initial = deque.popleft(frontier_initial)
            node_goal = deque.popleft(frontier_goal)
            print("> Goal testing...", "\n")
            if self.goaltest(node_initial, node_goal, frontier_initial, frontier_goal, groundzero_initial, groundzero_goal):
                #os.system('cls')
                break
            if node_initial.grid not in explored_initial:
                print("> Not the answer, adding to the initial's explored...", "\n")
                explored_initial.append(node_initial.grid)
                self.expand(node_initial, frontier_initial)
            if node_goal.grid not in explored_goal:
                print("> Not the answer, adding to the goal's explored...", "\n")
                explored_goal.append(node_goal.grid)
                self.expand(node_goal, frontier_goal)
            print("> initial frontier: ", len(frontier_initial))
            print("> initial explored: ", len(explored_initial))
            print("> goal frontier: ", len(frontier_goal))
            print("> goal explored: ", len(explored_goal), "\n")

    def print_answer(self, node_initial, node_goal, initial_grid, goal_grid, groundzero_initial, groundzero_goal):
        print("Found an answer!", "\n")
        print("Goal state to the middle steps: ")
        while node_goal.parent:
            print(node_goal.grid)
            print("==============================================================")
            node_goal = node_goal.parent
        print(groundzero_goal.grid, "\n")
        print("Initial state to the middle steps: ")
        while node_initial.parent:
            print(node_initial.grid)
            print("==============================================================")
            node_initial = node_initial.parent
        print(groundzero_initial.grid, "\n")


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
def final_report(frontier_initial, frontier_goal, explored_initial, explored_goal):
    print("Initial side:")
    print("frontier: ", len(frontier_initial))
    print("explored: ", len(explored_initial), "\n")
    print("Goal side:")
    print("frontier: ", len(frontier_goal))
    print("explored: ", len(explored_goal))


grid = [[None for _ in range(4)] for _ in range(4)]
grid = read_input_file("input.txt", grid)
initial = Node(None, grid)
frontier_initial = deque()
frontier_initial.append(initial)
explored_initial = []

goal1 = [[0, 0, 1, 2],
         [3, 4, 5, 6],
         [7, 8, 9, 10],
         [11, 12, 13, 14]]
goal2 = [[1, 2, 3, 4],
         [5, 6, 7, 8],
         [9, 10, 11, 12],
         [13, 14, 0, 0]]
frontier_goal = deque()
explored_goal = []

print("Answer 1: ", goal1)
print("Answer 2: ", goal2)

choice = int(input("Which answer would you like to approach? Number: "))
start_time = time.time()

if choice == 1:
    goal = Node(None, goal1)
    frontier_goal.append(goal)
    goal.bidirectional_search(initial, frontier_initial, explored_initial, goal, frontier_goal, explored_goal)
elif choice == 2:
    goal = Node(None, goal2)
    frontier_goal.append(goal)
    goal.bidirectional_search(initial, frontier_initial, explored_initial, goal, frontier_goal, explored_goal)
else:
    print("Wrong input!")

final_report(frontier_initial, frontier_goal, explored_initial, explored_goal)

print("--- %s seconds ---" % (time.time() - start_time))