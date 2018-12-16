import curses
from curses import wrapper
import random

board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
winning_board = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
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
def has_won():
    if board == winning_board:
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

# main method
def main(stdscr):

    # set up a board with 400 random moves
    init_board(400)
    mvs = 0
    print_board(stdscr, mvs)

    # loop until someone presses "q"
    while 1:

        # move based on input
        c = stdscr.getch()
        if c == curses.KEY_LEFT:
            if do_left():
                mvs = mvs + 1
        elif c == curses.KEY_RIGHT:
            if do_right():
                mvs = mvs + 1
        elif c == curses.KEY_UP:
            if do_up():
                mvs = mvs + 1
        elif c == curses.KEY_DOWN:
            if do_down():
                mvs = mvs + 1
        elif c == ord('q'):
            break

        # print the new board
        print_board(stdscr, mvs)

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


def print_board(stdscr, mvs):
    # clear screen
    stdscr.clear()

    # headers
    stdscr.addstr(0, 0, "{:~^56}".format("Fifteen Puzzle"), curses.A_BOLD)
    stdscr.addstr(2, 0, "{:^21}".format("Play"))
    stdscr.addstr(2, 35, "{:^21}".format("Target"))

    # print play board
    print_empty_board(stdscr, 3, 0)
    print_board_tiles(stdscr, board, 3, 0)

    # print target board
    print_empty_board(stdscr, 3, 7)
    print_board_tiles(stdscr, winning_board, 3, 7)

    # print the moves
    stdscr.addstr(9, 0, "{} moves".format(str(mvs)))

    # print if we won
    stdscr.addstr(9, 35, "Have we won? {}".format(str(has_won())))

    # refresh the screen
    stdscr.refresh()

# wrap the main method in the curses wrapper
wrapper(main)
