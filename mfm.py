import random
import time

"""
Context: I built this project after obtaining my PCEP certification and during my
PCAP Python Essentials 2 | PCAP-31-03 training. Please don’t be too harsh if the
form or style isn’t fully “professional” — my goal was to practice with a small,
scientifically flavored project.
"""

############################################
############################################
############################################
#    Project: MFM Tip Path (toy model)     #
############################################
############################################
############################################

#######################################################################################
# Part I — From the initial "." vacuum board (10×10) to inserting "#" obstacles

"""
Output of this cell:
- A 10×10 board named `board`
- Start and target markers: S at (0,0) and T at (9,9)
- Empty cells represented by "."
- Obstacles: 15 "#" placed deterministically with seed=123

Tip: call `show_board(board)` to print the grid.
"""
#######################################################################################

# Representation of the initial vacuum board (10×10 elements)

board_initial = [["." for i in range(10)] for j in range(10)]  # Compact list-comprehension.

# Place the start and target markers at the first and last cells of the board.
board_initial[0][0], board_initial[9][9] = "S", "T"

# show_board(board): helper to print the board nicely at each step (print(' '.join(...))).
def show_board(board_initial):  # Print each row on one line, with spaces between cells.
    for i in range(10):
        print(" ".join(board_initial[i]))

# Place 15 obstacles (“#”) randomly (without touching S or T).
def valid_board(board_initial):  # Collect valid positions (exclude S and T).
    valid_list = []
    for i in range(10):
        for j in range(10):
            if board_initial[i][j] == "S" or board_initial[i][j] == "T":
                continue  # Skip S and T.
            else:
                valid_list.append((i, j))
    return valid_list

def board_obst():
    random.seed(123)  # Ensure reproducible obstacle placement (deterministic sample).
    choice_random = random.sample(valid_board(board_initial), 15)  # Chosen coordinates.
    for i in choice_random:
        (y, x) = i
        board_initial[y][x] = "#"  # Each obstacle takes the value "#".
    return board_initial

board = board_obst()

"""
This part is essential: before any tip motion, I first build the `board` from the
same seed(123). That guarantees the exact same obstacle map every time.
"""
show_board(board)

#######################################################################################
# Part II — Core logic: collisions? inside/outside? is the next cell free to move?
#
# Summary:
# This is the heart of the project. Every step, check, and strategy relies on these
# three functions:
#   - inside_board(x, y): grid boundary test
#   - free_board(x, y):   movement permission (inside + not an obstacle)
#   - motion_board(...):  one-step move attempt (U/D/L/R) with success/failure
#######################################################################################

"""
Overview:
This section defines the minimal API for motion and collisions.

- inside_board(x, y): returns True if (x, y) is within the 10×10 grid, else False.
- free_board(x, y):   returns True if (x, y) is inside the grid AND not a '#'.
- motion_board(x, y, direction): tries to move one cell in U/D/L/R and returns:
      [(new_x, new_y), True]   if the move is valid (free cell),
      [(x, y), False]          if blocked (collision or out of bounds).

All higher-level behaviors (random walk, priorities, replay, coverage, etc.)
depend on these foundations.
"""

#Inside or outside the MFM board? True/False — boundary limit
def inside_board(x, y):  # Grid membership test (0 ≤ x,y < 10)
    if 0 <= x < 10 and 0 <= y < 10:  # both x and y within bounds
        return True
    elif x < 0 or y < 0:             # clearly outside on the negative side
        return False
    elif x >= 10 or y >= 10 : 
        return False

#Free cell: inside AND not an obstacle '#'
def free_board(x, y):  # A cell is free if inside the grid and not '#'
    if inside_board(x, y) == True and board[y][x] != "#":  # careful: board indexed as board[y][x]
        return True
    else:
        return False

#Elementary displacement (one step)
def motion_board(x, y, direction):
    # Use a temporary (a, b) to represent the candidate next position
    if direction == "U":
        a, b = x, y - 1
    elif direction == "D":
        a, b = x, y + 1
    elif direction == "L":
        a, b = x - 1, y
    elif direction == "R":
        a, b = x + 1, y

    next_position = free_board(a, b)  # is the candidate cell free?
    if next_position == True:
        return [(a, b), True]         # valid move: advance
    else:
        return [(x, y), False]        # blocked: stay put (collision)



