import random
from board import Board
from paddle import Paddle
from ball import Ball
import time

board = Board()
paddle = Paddle()
balls = [Ball(paddle.get_x() + random.randint(0, paddle.get_width()-1), paddle.get_y()-1, 1, -1, speed=0.2)]
paddle.hold_ball(balls[0])

prev_ball_timestamp = time.time()  # Improve


def move_balls(pbt):
    for ball in balls:
        if ball.is_free and time.time() - pbt >= ball.get_speed():
            ball.move_relative(board.matrix, 0, -1)
            pbt = time.time()
    return pbt
