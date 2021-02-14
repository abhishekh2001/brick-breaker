from modules import *
import colorama
from glob import board, paddle, prev_ball_timestamp, move_balls, prev_powerup_timestamp, move_powerups
import glob
import user_action
# TODO: limit x_vel to +/- 2

colorama.init()

while True:
    # Move paddle
    user_action.make_move()

    os.system('cls' if os.name == 'nt' else 'clear')

    # Perform motion and functionalities
    prev_ball_timestamp = move_balls(prev_ball_timestamp)
    prev_powerup_timestamp = move_powerups(prev_powerup_timestamp)

    # Render screen elements
    for ball in glob.balls:
        ball.render(board.matrix)
    for brick in glob.bricks:
        brick.render(board.matrix)
    for powerup in glob.powerups:
        powerup.render(board.matrix)
    paddle.render(board.matrix)

    board.matrix[0][0] = str(glob.balls[0].get_speed())
    board.matrix[0][10] = str(glob.balls[0].get_x())
    board.matrix[0][15] = str(glob.balls[0].get_y())
    board.matrix[0][20] = str(glob.balls[0].get_xvel())
    board.matrix[0][25] = str(glob.balls[0].get_yvel())
    board.render()

