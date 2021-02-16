import random
from board import Board
from paddle import Paddle
from ball import Ball
from brick import Brick
import time
from powerup import PowerUp, ExpandPaddle, ShrinkPaddle, PaddleGrab, type_repr_map
import config
from player import Player

player = Player()

debug_statement = 'NONE'

board = Board()
paddle = Paddle(8)
balls = [
    Ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.3, free=True)
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


def clear_screen():
    if paddle:
        paddle.clear(board.matrix)
    for ball in balls:
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

    paddle = Paddle(8, width=5)
    balls = [
        Ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.2,
             free=True),
    ]
    paddle.hold_ball(balls[0])

    powerups = []
    to_activate_powerups = []
    active_powerups = []

    bricks = []
    for y in range(5, 15, 4):
        for j in range(10, 100, 15):
            # bricks.append(Brick(j, y, 1, ['BBBBB']))
            bricks.append(Brick(j, y, random.choice([-1, 1, 2, 3]), ['BBBB']))

    prev_ball_timestamp = time.time()  # Improve
    prev_powerup_timestamp = time.time()


def spawn_powerup(x, y):
    if random.random() <= config.prob_powerup:
        p_type = random.choice([1, 2, 3, 4, 5, 6])
        if p_type == 1:
            powerups.append(ExpandPaddle(x, y))
        elif p_type == 2:
            powerups.append(ShrinkPaddle(x, y))
        elif p_type == 6:
            powerups.append(PaddleGrab(x, y))
        else:
            powerups.append(PowerUp(x, y, type_repr_map[p_type], p_type))


def deactivate_powerups():
    for powerup in list(active_powerups):
        if time.time() - powerup.get_activation_time() >= powerup.get_deactivation_time():
            if powerup.get_type() == 1:
                paddle.clear(board.matrix)
                powerup.deactivate(paddle)
            elif powerup.get_type() == 2:
                powerup.deactivate(paddle)
            elif powerup.get_type() == 3:  # no need to make the balls go poof
                pass
            elif powerup.get_type() == 4:  # slow down sped up balls
                for ball in balls:
                    ball.set_speed(ball.get_speed() + config.ball_speed_interval)
            elif powerup.get_type() == 5:  # thru-ball
                pass
            elif powerup.get_type() == 6:  # paddle grab
                powerup.deactivate(paddle)
            active_powerups.remove(powerup)


def activate_powerups():
    global to_activate_powerups
    global balls
    global active_powerups

    to_append = True
    for powerup in to_activate_powerups:
        if powerup.get_type() == 1:  # expand paddle
            if paddle.get_width() < 7:
                powerup.activate(paddle)
            else:
                to_append = False
        elif powerup.get_type() == 2:  # shrink paddle
            if paddle.get_width() > 3:
                paddle.clear(board.matrix)
                powerup.activate(paddle)
            else:
                to_append = False
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
                    ball.set_speed(ball.get_speed() - config.ball_speed_interval)
        elif powerup.get_type() == 5:  # thru-ball
            to_append = True
        elif powerup.get_type() == 6:  # Paddle grab
            powerup.activate(paddle)
        if to_append:
            powerup.set_activation_time()
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
                player.increment_points()  # increase points
            elif brick.got_hit(board.matrix):  # Brick has zero health -> is destroyed
                spawn_powerup(brick.get_x(), brick.get_y())
                player.increment_points()  # increase player points

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
            player.lose_life()
            init()
    if flag:
        pbt = time.time()
    return pbt
