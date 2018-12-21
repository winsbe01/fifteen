import curses
from curses import wrapper
import random

winning_boards = {
    "classic": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
    "odds/evens": [1,3,5,7,9,11,13,15,2,4,6,8,10,12,14,16],
    "odds/evens (alt)": [1,3,5,7,2,4,6,8,9,11,13,15,10,12,14,16],
    "spiral": [7,8,9,10,6,1,2,11,5,4,3,12,16,15,14,13]
}

board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
moves = ['u', 'd', 'l', 'r']

def init_board(rand_moves):
    # make a number of random moves
    for i in range(0,rand_moves):
        r = random.choice(moves)
        if r is 'u':
            do_up()
        elif r is 'd':
            do_down()
        elif r is 'l':
            do_left()
        elif r is 'r':
            do_right()

# True if we've won, False if not
def has_won(wb):
    if board == wb:
        return True
    return False

# returns the index of the blank tile
def blank():
    return board.index(16)

# Move validity
def can_down():
    return blank() // 4 != 0
def can_up():
    return blank() // 4 != 3
def can_right():
    return blank() % 4 != 0
def can_left():
    return blank() % 4 != 3

# perform a move
def move(offset):
    oc = blank()
    ov = board[oc]
    tc = blank() + offset
    tv = board[tc]
    board[oc] = tv
    board[tc] = ov
def do_right():
    if can_right():
        move(-1)
        return True
    return False
def do_left():
    if can_left():
        move(1)
        return True
    return False
def do_down():
    if can_down():
        move(-4)
        return True
    return False
def do_up():
    if can_up():
        move(4)
        return True
    return False

def choose_board(stdscr):

    # headers
    stdscr.addstr(0, 0, "{:~^56}".format("Fifteen Puzzle"), curses.A_BOLD)
    stdscr.addstr(2, 0, "{:^21}".format("Choose a board"))

    # print the first winning board
    idx = 0
    board_names = list(winning_boards.keys())
    print_board_left(stdscr,winning_boards[board_names[idx]],"{:^21}".format(board_names[idx]))
    stdscr.refresh()

    while 1:
        c = stdscr.getch()
        if c == curses.KEY_LEFT:
            if idx > 0:
                idx -= 1
                print_board_left(stdscr,winning_boards[board_names[idx]], "{:^21}".format(board_names[idx]))
                stdscr.refresh()
        elif c == curses.KEY_RIGHT:
            if idx < len(board_names) - 1:
                idx += 1
                print_board_left(stdscr,winning_boards[board_names[idx]], "{:^21}".format(board_names[idx]))
                stdscr.refresh()
        elif c == ord('p'):
            return winning_boards[board_names[idx]]
        elif c == ord('q'):
            return None

    stdscr.getkey()

# main method
def main(stdscr):

    # choose a board
    bc = choose_board(stdscr)
    if bc is None:
        exit()

    # set up a board with 400 random moves
    init_board(400)
    mvs = 0
    print_board(stdscr, mvs, bc)

    # loop until someone presses "q"
    while 1:

        # move based on input
        c = stdscr.getch()
        if c == curses.KEY_LEFT or c == ord('h'):
            if do_left():
                mvs = mvs + 1
        elif c == curses.KEY_RIGHT or c == ord('l'):
            if do_right():
                mvs = mvs + 1
        elif c == curses.KEY_UP or c == ord('k'):
            if do_up():
                mvs = mvs + 1
        elif c == curses.KEY_DOWN or c == ord('j'):
            if do_down():
                mvs = mvs + 1
        elif c == ord('q'):
            break

        # print the new board
        print_board(stdscr, mvs, bc)

# print an empty board
def print_empty_board(stdscr, y, x):
    # print the first line of dashes
    stdscr.addstr(y,x*5,"{:-^21}".format(""), curses.A_BOLD)

    # empty squares
    for i in range(1,5):
        for j in range(0,5):
            stdscr.addstr((i+y), (j+x)*5, "|", curses.A_BOLD)

    # print the last line of dashes
    stdscr.addstr((5+y), x*5,"{:-^21}".format(""), curses.A_BOLD)

# print the tiles of a board
def print_board_tiles(stdscr, b, y, x):

    # create the color pairs
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)

    # put in numbers
    ocnt = y+1
    icnt = (x*5)+1
    for i,v in enumerate(b):
        # odds get one color, evens the other
        if v % 2 == 1:
            stdscr.addstr(ocnt,icnt,"{:^4}".format(v), curses.color_pair(1))
        elif v == 16:
            # blank tile gets no coloring
            stdscr.addstr(ocnt,icnt,"{:^4}".format(""))
        else:
            stdscr.addstr(ocnt,icnt,"{:^4}".format(v), curses.color_pair(2))

        # update counts
        if (i+1) % 4 == 0:
            ocnt = ocnt + 1
            icnt = (x*5) + 1
        else:
            icnt = icnt + 5

# print a board on the left hand side of the screen
def print_board_left(stdscr, b, cap):
    print_empty_board(stdscr, 3, 0)
    print_board_tiles(stdscr, b, 3, 0)
    stdscr.addstr(9, 0, cap)

# print a board on the left hand side of the screen
def print_board_right(stdscr, b, cap):
    print_empty_board(stdscr, 3, 7)
    print_board_tiles(stdscr, b, 3, 7)
    stdscr.addstr(9, 35, cap)

# print the full boards
def print_board(stdscr, mvs, wb):
    # clear screen
    stdscr.clear()

    # headers
    stdscr.addstr(0, 0, "{:~^56}".format("Fifteen Puzzle"), curses.A_BOLD)
    stdscr.addstr(2, 0, "{:^21}".format("Play"))
    stdscr.addstr(2, 35, "{:^21}".format("Target"))

    # print play board
    print_board_left(stdscr, board, "{} moves".format(str(mvs)))

    # print target board
    print_board_right(stdscr, wb, "Have we won? {}".format(str(has_won(wb))))

    # refresh the screen
    stdscr.refresh()

# wrap the main method in the curses wrapper
wrapper(main)
