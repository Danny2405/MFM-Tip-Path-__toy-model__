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


#######################################################################################
# Part III — Move strategies: Random and deterministic displacement
# Coverage, efficiency, and final results — this section prints the summary table.
#
# Summary:
# - Random_Walk(): random step attempts (seed=124) with counts for valid steps and collisions.
# - determinist_script(): fixed priority order (e.g., DRLU), first valid direction wins.
# - d_manhattan(): Manhattan distance between S and T (expected 18 on this grid).
# - The final print builds a simple text table for comparison.
#######################################################################################

# Random displacement strategy

def Random_Walk():
    i = 0                           # loop counter (attempts)
    x, y = 0, 0                     # initial position of the MFM tip
    list_position = [(x, y)]        # track unique visited cells (includes S at start)
    valid_steps = 0                 # number of accepted moves
    npas_crashes = 0                # number of collisions (refused attempts)
    max_step = 400                  # maximum number of attempts
    random.seed(124)                # reproducible random sequence

    while i < max_step:
        direct = random.choice(['U', 'D', 'L', 'R'])  # pick a random direction
        z = motion_board(x, y, direct)                # single-step attempt
        if z[1] == True:
            (x, y) = z[0]
            valid_steps += 1
            # Avoid duplicates: len(list_position) will be our coverage (including S)
            if (x, y) not in list_position:
                list_position.append((x, y))
            if x == 9 and y == 9:
                return [x == 9 and y == 9, valid_steps, len(list_position),
                        list_position, (x, y), npas_crashes]
        elif z[1] == False:
            (x, y) = z[0]
            npas_crashes += 1
        i += 1

    # End of budget — if target not reached, return current metrics
    if not (x == 9 and y == 9):     # Boolean style
        return [x == 9 and y == 9, valid_steps, len(list_position),
                list_position, (x, y), npas_crashes]


# Distance (Manhattan) — minimal steps ignoring obstacles
def d_manhattan(a, b):
    # Scan the board to locate symbols a and b (S and T in this project)
    for i in range(10):
        for j in range(10):
            if board[i][j] == a:
                x1, y1 = j, i
            if board[i][j] == b:
                x2, y2 = j, i
    return abs(x1 - x2) + abs(y1 - y2)

d_manhattan("S", "T")

# Path efficiency
efficiency_1 = round(d_manhattan("S", "T") / Random_Walk()[1], 3)

Random_Walk_result = ["RandomWalk", "     " + str(Random_Walk()[0]),
                      "    " + str(Random_Walk()[1]) + "   ",
                      "        " + str(Random_Walk()[-1]),
                      "       " + str( efficiency_1), str(Random_Walk()[2])]

# Re-initialize the board before the deterministic strategy — hence Part I’s importance
board = board_obst()

deter_1 = "DRLU"  # First example of deterministic priority order

def determinist_script(deter_input):
    a = 0
    compteur = 20000
    x, y = 0, 0                     # initial position of the MFM tip
    list_position = [(x, y)]        # coverage tracker (includes S)
    valid_steps = 0                 # number of accepted moves
    npas_crashes = 0                # number of collisions (refused attempts)

    while a < compteur:
        j = 0
        while j < len(deter_input):
            z = motion_board(x, y, deter_input[j])  # try directions in fixed order
            if z[1] == True:
                (x, y) = z[0]
                valid_steps += 1
                # Avoid duplicates for coverage
                if (x, y) not in list_position:
                    list_position.append((x, y))
                if x == 9 and y == 9:
                    return [x == 9 and y == 9, valid_steps, len(list_position),
                            list_position, (x, y), npas_crashes]
                break
            elif z[1] == False:
                (x, y) = z[0]
                npas_crashes += 1
            j += 1

        # If none of the directions worked at this decision point → stop as “blocked”
        if j == len(deter_input):
            return [x == 9 and y == 9, valid_steps, len(list_position),
                    list_position, (x, y), npas_crashes]
        a += 1

    # Safety stop (compteur reached)
    return [x == 9 and y == 9, valid_steps, len(list_position),
            list_position, (x, y), npas_crashes]

efficiency_2 = round(d_manhattan("S", "T") / determinist_script(deter_1)[1], 3)
determinist_script_result = ["Prio-DRLU ", "     " + str(determinist_script(deter_1)[0]),
                             "    " + str(determinist_script(deter_1)[1]) + "    ",
                             "         " + str(determinist_script(deter_1)[-1]),
                             "         " + str( efficiency_2), str(determinist_script(deter_1)[2])]

line = [" strategy ", "achieved ", "valid_step", "obstacles ", " efficiency ", "couverture"]
dot = ["-" * 10, "-" * 9, "-" * 10, "-" * 10, "-" * 12, "-" * 10]

result_table = [line, dot, Random_Walk_result, dot, determinist_script_result]

# Baseline vs deterministic strategy — console table
print()
for i in range(5):
    print(" | ".join(result_table[i]))

#######################################################################################
# Part IV — User input & command scripts | ASCII rendering of a trajectory
# Goal: have fun, interact with the user, and produce an ASCII animation/snapshot.
# This is the part I will convert to a short GIF/MP4 demo for LinkedIn.
# Summary:
# - valid_command(): collect and validate a user-entered command string (U/D/L/R)
# - command_script(): execute the command, count steps/collisions, return the path
# - render_frame(): compose a single ASCII frame with priority S/T/# > * > .
# - draw_trace(): replay a previously computed path, static or animated
#######################################################################################

# Re-initialize the board before running interactive commands — Part I guarantees determinism
board = board_obst()


# User input & command scripts

# I create a function that I can easily modify later.
def valid_command():
    word = input("Enter a list of directions, e.g. RRDDLU: ")  # input prompt
    word = word.upper()  # normalize to uppercase
    list_direct = ['U', 'D', 'L', 'R']  # valid direction symbols
    if word == "":  # first validation: empty input
        print("Please enter a non-empty input.")
        return valid_command()
    else:
        if " " in word:   # second validation: remove spaces
            word = word.replace(" ", "")
        if "," in word:   # third validation: remove commas
            word = word.replace(",", "")
    list_word = list(word)
    for i in range(len(list_word)):
        # if any character is not a valid direction, restart the prompt
        if list_word[i] not in list_direct:
            print("Please enter only valid symbols: R, D, L, or U.")
            return valid_command()
    return list_word  # This list is consumed by the next function.

result = valid_command()

# Function to execute the user command and collect metrics/path
def command_script(user_input):
    list_position = []
    x, y = 0, 0  # initial position of the MFM tip
    valid_steps = 0  # count of accepted moves
    npas_crashes = 0  # count of collisions (obstacles or outside of the board)
    for j in user_input:
        z = motion_board(x, y, j)  # avoid recomputing multiple times
        if z[1] == True:
            (x, y) = z[0]
            list_position.append((x, y))
            valid_steps += 1
            if x == 9 and y == 9:
                return [x == 9 and y == 9, valid_steps, list_position, (x, y), npas_crashes]
        elif z[1] == False:
            (x, y) = z[0]
            npas_crashes += 1
    return [x == 9 and y == 9, valid_steps, list_position, (x, y), npas_crashes]

result_2 = command_script(result)
path = result_2[2]

# =========================
# ASCII rendering of a trajectory
# =========================

# --- 1) Compose a single frame with priority: S/T/# > * > . ---
def render_frame(base, visits, pos=None, spaced=True):
    """
    base    : immutable grid (S, T, #, .)
    visits  : set of (x,y) positions already visited → rendered as '*'
    pos     : current (x,y) position to optionally render a cursor 'o'
    spaced  : True → spaces between characters for readability
    """
    lines = []
    for y, row in enumerate(base):
        line = []
        for x, cell in enumerate(row):
            if cell in ('S', 'T', '#'):
                ch = cell                     # base has highest priority
            elif (x, y) in visits:
                ch = '*'                      # only mark free cells as visited
            elif pos is not None and (x, y) == pos:
                ch = 'o'                      # optional cursor to show current tip
            else:
                ch = '.'
            line.append(ch)
        lines.append(' '.join(line) if spaced else ''.join(line))
    print('\n'.join(lines))

# --- 2) Replay the path and place '*' only on free cells '.' ---
def draw_trace(base, path, animate=False, delay=0.1, show_cursor=False):
    """
    base        : immutable grid
    path        : list of (x,y) positions AFTER each validated step
    animate     : True → frame-by-frame animation; False → final static frame
    delay       : pause between frames if animate=True
    show_cursor : True → show 'o' at the current position along with '*'
    """
    visits = set()
    # starting position (useful if you want to display a pre-move cursor)
    current = (0, 0)

    if animate:
        import time

    # Optional initial frame:
    if animate:
        print("\033[2J\033[H", end="")        # clear terminal screen
        render_frame(base, visits, current if show_cursor else None)
        time.sleep(delay)

    # Replay the path: add '*' only on free '.' cells
    for (x, y) in path:
        current = (x, y)
        if base[y][x] == '.':
            visits.add((x, y))

        if animate:
            print("\033[2J\033[H", end="")    # clear terminal screen
            render_frame(base, visits, current if show_cursor else None)
            time.sleep(delay)

    # If not animating, render just the final state (complete trace)
    if not animate:
        render_frame(base, visits, current if show_cursor and path else None)

base = board
# Render the final trace (static) and then an animated version (2s per frame for demo clarity)
draw_trace(base, path, animate=False)            # final static rendering
#draw_trace(base, path, animate=True, delay=2)    # frame-by-frame animation

