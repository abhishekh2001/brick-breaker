import random
from board import Board
from paddle import Paddle
from brick import Brick
import time
from powerup import PowerUp, ExpandPaddle, ShrinkPaddle, PaddleGrab, type_repr_map, \
    FastBall, ThruBall, BallMultiplier
import config
from player import Player
from balls import Balls
from explodingBricks import ExplodingBrick


player = Player()
max_points = 0

board = Board()
paddle = Paddle(8)
balls = Balls()
powerups = []
to_activate_powerups = []
active_powerups = []
bricks = []

prev_ball_timestamp = time.time()
prev_powerup_timestamp = time.time()


def clear_screen():
    if paddle:
        paddle.clear(board.matrix)
    for ball in balls.get_balls():
        ball.clear(board.matrix)
    for powerup in powerups:
        powerup.clear(board.matrix)
    for brick in bricks:
        brick.clear(board.matrix)


def init():
    global paddle
    global bricks
    global powerups
    global active_powerups
    global to_activate_powerups
    global balls
    global prev_ball_timestamp
    global prev_powerup_timestamp
    global active_powerups

    clear_screen()

    balls.remove_all()

    paddle = Paddle(8, width=5)
    balls.add_ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.2,
                   free=True)
    paddle.hold_ball(balls.get_balls()[0])

    powerups = []
    to_activate_powerups = []
    active_powerups = []

    bricks = []
    for y in range(4, 9, 4):
        for j in range(10, 100, 10):
            # bricks.append(Brick(j, y, -1, ['BBBBB']))
            bricks.append(Brick(j, y, random.choice([-1, 1, 2, 3]), ['BBBB']))

    for x in range(40, 55, 4):
        bricks.append(ExplodingBrick(x, 14))
    bricks.append(ExplodingBrick(36, 13))
    bricks.append(ExplodingBrick(56, 13))
    bricks.append(Brick(45, 13, 2, ['BBBB']))

    prev_ball_timestamp = time.time()  # Improve
    prev_powerup_timestamp = time.time()


def start_new_life():
    global balls
    global powerups
    global to_activate_powerups
    global active_powerups
    global paddle
    clear_screen()

    balls.remove_all()

    paddle = Paddle(8, width=5)
    balls.add_ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.2,
                   free=True)
    paddle.hold_ball(balls.get_balls()[0])

    powerups = []
    to_activate_powerups = []
    active_powerups = []


def spawn_powerup(x, y):
    if random.random() <= config.prob_powerup:
        p_type = random.choice([1, 2, 3, 4, 5, 6])
        if p_type == 1:
            powerups.append(ExpandPaddle(x, y))
        elif p_type == 2:
            powerups.append(ShrinkPaddle(x, y))
        elif p_type == 3:
            powerups.append(BallMultiplier(x, y))
        elif p_type == 4:
            powerups.append(FastBall(x, y))
        elif p_type == 5:
            powerups.append(ThruBall(x, y))
        elif p_type == 6:
            powerups.append(PaddleGrab(x, y))


def deactivate_powerups():
    for powerup in list(active_powerups):
        if time.time() - powerup.get_activation_time() >= powerup.get_deactivation_time():
            powerup.deactivate()
            active_powerups.remove(powerup)


def activate_powerups():
    global to_activate_powerups
    global active_powerups

    for powerup in to_activate_powerups:
        to_append = powerup.activate()
        if to_append:
            powerup.set_activation_time()
            active_powerups.append(powerup)

    to_activate_powerups = []


def is_thru_ball():
    return 5 in map(lambda x: x.get_type(), active_powerups)


def handle_impact(brick):
    """
    Behavior of brick on successful impact with ball
    :param brick: brick instance
    """
    if brick.get_brick_type() == 4:
        brick.chain_explosions()
    elif is_thru_ball():  # if thru-ball is active, destroy brick
        brick.destroy(board.matrix)
        spawn_powerup(brick.get_x(), brick.get_y())
        player.increment_points_by(brick.get_score())  # increase points
    elif brick.got_hit(board.matrix):  # Brick has zero health -> is destroyed
        spawn_powerup(brick.get_x(), brick.get_y())
        player.increment_points_by(brick.get_score())  # increase player points


def move_powerups(ppt):
    """
    Responsible for moving all powerups and handling cases when user misses the powerup or catches it.
    :param ppt: previous powerup timestamp
    :return: value of powerup timestamp after current iteration
    """
    global powerups
    flag = False
    for powerup in powerups:
        if time.time() - ppt >= powerup.get_speed():
            flag = True
            if powerup.is_caught_by_paddle(paddle):  # Check if powerup is caught
                to_activate_powerups.append(powerup)  # temporarily store powerups to activate
                powerup.set_status(config.powerup_status['ACTIVE'])  # Update status of caught powerup
            if powerup.go_down(board.matrix):
                powerup.set_status(config.powerup_status['MISSED'])  # User has missed the powerup
    if flag:
        ppt = time.time()

    powerups = list(filter(lambda p: p.get_status() == config.powerup_status['SPAWNED'], powerups))

    activate_powerups()

    return ppt

