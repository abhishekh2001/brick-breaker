import random
from board import Board
from paddle import Paddle
from ball import Ball
from brick import Brick
import time

board = Board()
paddle = Paddle(8)
balls = [
    Ball(paddle.get_x() + random.randint(0, paddle.get_width() - 1), paddle.get_y() - 1, 0, 0, speed=0.2, free=True),
    Ball(10, 5, 0, -1, speed=0.2, free=True)
]
bricks = [Brick(10, 10, 3, ['BBBB'])]
paddle.hold_ball(balls[0])

prev_ball_timestamp = time.time()  # Improve


def handle_ball_brick_collision(ball):
    global bricks
    for brick in bricks:
        if brick.get_x() - 1 <= ball.get_x() <= brick.get_x() + brick.get_width() + 1 and \
                brick.get_y() - 1 <= ball.get_y() <= brick.get_y() + brick.get_height() + 1:
            brick.got_hit(board.matrix)

            if brick.get_x() - 1 <= ball.get_x() <= brick.get_x() + brick.get_width() + 1:
                ball.set_xvel()
    bricks = list(filter(lambda b: b.get_health(), bricks))


def move_balls(pbt):
    global bricks
    flag = False
    for ball in balls:
        if ball.is_free and time.time() - pbt >= ball.get_speed():
            flag = True
            ball.move_relative(board.matrix, ball.get_xvel(), ball.get_yvel())
            ret = ball.handle_paddle_collision(paddle)
            handle_ball_brick_collision(ball)
            if not ret:  # Modify so that game is lost only if *all* balls are missed
                print('fin')
                quit()
    if flag:
        pbt = time.time()
    return pbt
