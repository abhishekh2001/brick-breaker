import random
from board import Board
from paddle import Paddle
from ball import Ball
from brick import Brick
import time

board = Board()
paddle = Paddle()
balls = [Ball(paddle.get_x() + random.randint(0, paddle.get_width()-1), paddle.get_y()-1, 0, 0, speed=0.2, free=True)]
bricks = [Brick(10, 10, -1, ['BBBB'])]
paddle.hold_ball(balls[0])

prev_ball_timestamp = time.time()  # Improve


def move_balls(pbt):
    flag = False
    for ball in balls:
        if ball.is_free and time.time() - pbt >= ball.get_speed():
            flag = True
            ball.move_relative(board.matrix, ball.get_xvel(), ball.get_yvel())
            ret = ball.handle_paddle_collision(paddle)
            if not ret:
                print('fin')
                quit()
    if flag:
        pbt = time.time()
    return pbt
