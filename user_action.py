from input import input_to, Get
from glob import board, paddle, balls


def make_move():
    c = input_to(Get())

    if c == 'a':
        paddle.move_relative(board.matrix, -1)

    if c == 'd':
        paddle.move_relative(board.matrix, 1)

    if c == 'q':
        print('fin')
        quit()
