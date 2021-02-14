import random
from board import Board
from paddle import Paddle
from ball import Ball
from brick import Brick
import time
from powerup import PowerUp
import config

debug_statement = 'NONE'

board = Board()
paddle = Paddle(8)
balls = [
    Ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.3, free=True),
    # Ball(1, 1, 1, -1, speed=0.2, free=True)
    # Ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.2, free=True),
]
powerups = []
to_activate_powerups = []
active_powerups = []

bricks = []
for y in range(5, 15, 4):
    for j in range(10, 100, 15):
        # bricks.append(Brick(j, y, 1, ['BBBBB']))
        bricks.append(Brick(j, y, random.choice([-1, 1, 2, 3]), ['BBBB']))
paddle.hold_ball(balls[0])

prev_ball_timestamp = time.time()  # Improve
prev_powerup_timestamp = time.time()


def spawn_powerup(x, y):
    if random.random() <= config.prob_powerup:
        powerup = PowerUp(x, y, ['P'])
        powerups.append(powerup)


def activate_powerups():
    global to_activate_powerups
    global balls
    global active_powerups

    to_append = True
    for powerup in to_activate_powerups:
        if powerup.get_type() == 1:  # expand paddle
            paddle.set_width(paddle.get_width() + 2)
        elif powerup.get_type() == 2:  # shrink paddle
            paddle.clear(board.matrix)
            paddle.set_width(paddle.get_width() - 2)
        elif powerup.get_type() == 3:  # ball multiply
            to_append = False
            if len(balls) < 4:
                to_append = True
                for ball in list(balls):
                    balls.append(
                        Ball(ball.get_x(),
                             ball.get_y(), -ball.get_xvel(), -ball.get_yvel(),
                             free=True, speed=ball.get_speed())
                    )
        elif powerup.get_type() == 4:  # ball speed
            to_append = False
            for ball in balls:
                if 0.1 < ball.get_speed() <= 0.3:
                    to_append = True
                    ball.set_speed(ball.get_speed() - 0.1)
        elif powerup.get_type() == 5:  # thru-ball
            to_append = True
        elif powerup.get_type() == 6:  # Paddle grab
            paddle.set_grab(True)
        if to_append:
            active_powerups.append(powerup)

    to_activate_powerups = []


def is_thru_ball():
    return 5 in map(lambda x: x.get_type(), active_powerups)


def handle_ball_brick_collision(ball):
    global bricks
    for brick in bricks:
        if brick.get_x() - 1 <= ball.get_x() <= brick.get_x() + brick.get_width() and \
                brick.get_y() - 1 <= ball.get_y() <= brick.get_y() + brick.get_height():
            if is_thru_ball():  # if thru-ball is active, destroy brick
                brick.destroy(board.matrix)
                spawn_powerup(brick.get_x(), brick.get_y())
            elif brick.got_hit(board.matrix):  # Brick has zero health -> is destroyed
                spawn_powerup(brick.get_x(), brick.get_y())

            if not is_thru_ball():  # handle collisions only if thru-ball is inactive
                if brick.get_x() <= ball.get_x() <= brick.get_x() + brick.get_width() - 1:
                    ball.set_yvel(-ball.get_yvel())
                elif brick.get_y() <= ball.get_y() <= brick.get_y() + brick.get_height() - 1:
                    ball.set_xvel(-ball.get_xvel())
                else:
                    ball.set_yvel(-ball.get_yvel())
                    # ball.set_xvel(-ball.get_xvel())
            break
    bricks = list(filter(lambda b: b.get_health(), bricks))


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


def move_balls(pbt):
    global bricks
    flag = False
    for ball in list(balls):
        if ball.is_free and time.time() - pbt >= ball.get_speed():
            flag = True
            handle_ball_brick_collision(ball)
            ball.move_relative(board.matrix, ball.get_xvel(), ball.get_yvel())
            ret = ball.handle_paddle_collision(paddle)
            if not ret:
                balls.remove(ball)
        if not len(balls):
            print('fin', debug_statement)
            print(ball.get_xvel(), ball.get_yvel())
            quit()
    if flag:
        pbt = time.time()
    return pbt
