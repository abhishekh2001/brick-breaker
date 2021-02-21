from modules import *
import colorama
from glob import board, paddle, prev_ball_timestamp, prev_powerup_timestamp, move_powerups, \
    deactivate_powerups
import glob
import user_action
# TODO: how to handle lost life
# TODO: handle when player has killed all the bricks
# TODO: different bricks, different scores
# TODO: yvel should never be zero
# TODO: DEACTIVATE powerups on init
# TODO: begin game with random ball positions

colorama.init()
glob.init()
start_time = time.time()
max_points = 0

while True and glob.player.get_lives():
    # Move paddle
    user_action.make_move()

    os.system('cls' if os.name == 'nt' else 'clear')

    # Perform motion and functionalities
    glob.balls.move_all()
    prev_powerup_timestamp = move_powerups(prev_powerup_timestamp)
    deactivate_powerups()

    # Render screen elements
    glob.balls.render_all(board.matrix)
    for brick in glob.bricks:
        brick.render(board.matrix)
    for powerup in glob.powerups:
        powerup.render(board.matrix)
    glob.paddle.render(board.matrix)

    glob.max_points = max(glob.player.get_points(), glob.max_points)

    print('Life: ', glob.player.get_lives())
    print('Score: ', glob.player.get_points())
    print('Time: ', str(int(time.time() - start_time)), 's')
    glob.board.render()

    if not len(list(filter(lambda b: b.get_brick_type() != -1, glob.bricks))):
        break

print('Max score is ', glob.max_points)
