from modules import *

from glob import board, paddle, balls, move_balls, prev_ball_timestamp
import user_action


while True:
    user_action.make_move()

    os.system('cls' if os.name == 'nt' else 'clear')
    prev_ball_timestamp = move_balls(prev_ball_timestamp)
    for ball in balls:
        ball.render(board.matrix)
    paddle.render(board.matrix)
    board.render()
