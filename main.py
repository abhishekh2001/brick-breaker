from modules import *
import colorama
from glob import board, paddle, balls, prev_ball_timestamp, move_balls, prev_powerup_timestamp, move_powerups
import glob
import user_action


colorama.init()

while True:
    # Move paddle
    user_action.make_move()

    os.system('cls' if os.name == 'nt' else 'clear')

    # Perform motion and functionalities
    prev_ball_timestamp = move_balls(prev_ball_timestamp)
    prev_powerup_timestamp = move_powerups(prev_powerup_timestamp)

    # Render screen elements
    for ball in balls:
        ball.render(board.matrix)
    for brick in glob.bricks:
        brick.render(board.matrix)
    for powerup in glob.powerups:
        powerup.render(board.matrix)
    paddle.render(board.matrix)
    board.render()

