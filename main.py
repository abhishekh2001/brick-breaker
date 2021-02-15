from modules import *
import colorama
from glob import board, paddle, prev_ball_timestamp, move_balls, prev_powerup_timestamp, move_powerups, \
    deactivate_powerups
import glob
import user_action
# TODO: limit x_vel to +/- 2
# TODO: how to handle lost life
# TODO: handle when player has killed all the bricks
# TODO: different bricks, different scores
# TODO: yvel should never be zero
# TODO: DEACTIVATE powerups on init
# TODO: begin game with random ball positions

colorama.init()
glob.init()

while True and glob.player.get_lives():
    # Move paddle
    user_action.make_move()

    os.system('cls' if os.name == 'nt' else 'clear')

    # Perform motion and functionalities
    prev_ball_timestamp = move_balls(prev_ball_timestamp)
    prev_powerup_timestamp = move_powerups(prev_powerup_timestamp)
    deactivate_powerups()

    # Render screen elements
    for ball in glob.balls:
        ball.render(board.matrix)
    for brick in glob.bricks:
        brick.render(board.matrix)
    for powerup in glob.powerups:
        powerup.render(board.matrix)
    glob.paddle.render(board.matrix)

    print('Life: ', glob.player.get_lives())
    print('Score: ', glob.player.get_points())
    glob.board.render()

