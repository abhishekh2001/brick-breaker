from board import Board
from paddle import Paddle
from ball import Ball

board = Board()
paddle = Paddle()
balls = [Ball(paddle.get_center_x_coordinate(), paddle.get_y()-1, 1, 1)]
paddle.hold_ball(balls[0])
