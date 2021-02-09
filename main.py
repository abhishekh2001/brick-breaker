from modules import *

from glob import board, paddle, balls
import user_action


def is_data():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

#
# paddle = Paddle()
# board = Board()
#
# old_settings = termios.tcgetattr(sys.stdin)
# start = time.time()
# counter = 0
# begin = time.time()
# try:
#     tty.setcbreak(sys.stdin.fileno())
#     while 1:
#         os.system('cls' if os.name == 'nt' else 'clear')
#         if is_data():
#             c = sys.stdin.read(1)
#             print('input', c)
#
#             if c == 'a':
#                 paddle.clear(board.matrix)
#                 paddle.move_relative(-1)
#
#             if c == 'd':
#                 paddle.clear(board.matrix)
#                 paddle.move_relative(1)
#
#             if c == 'q':
#                 break
#         paddle.render(board.matrix)
#         board.render()
# finally:
#     termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


while True:
    user_action.make_move()

    os.system('cls' if os.name == 'nt' else 'clear')
    for ball in balls:
        ball.render(board.matrix)
    paddle.render(board.matrix)
    board.render()
