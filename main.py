from modules import *
import colorama
from glob import board, paddle, balls, prev_ball_timestamp, move_balls
import glob
import user_action


colorama.init()

while True:
    user_action.make_move()

    os.system('cls' if os.name == 'nt' else 'clear')
    prev_ball_timestamp = move_balls(prev_ball_timestamp)
    for ball in balls:
        ball.render(board.matrix)
    for brick in glob.bricks:
        brick.render(board.matrix)
    paddle.render(board.matrix)
    board.render()

