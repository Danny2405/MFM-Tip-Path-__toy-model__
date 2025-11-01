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
