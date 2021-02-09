from component import Component
import config


class Paddle(Component):
    def __init__(self, x=config.board_width // 2, width=config.paddle_init_width, ball=None):
        representation = ['X' * width]
        super().__init__(x, config.paddle_row_restriction, representation)
        self._ball = ball

    def get_center_x_coordinate(self):
        return self._x + self._width // 2

    def hold_ball(self, ball):
        if self._ball:
            #  Handle if paddle already holds a ball
            self._ball.set_is_free(True)
        ball.set_is_free(False)
        self._ball = ball

    def release_ball(self):
        """
        Release ball held by paddle
        :return:
        """
        #  TODO: Handle trajectory of ball
        if self._ball:
            self._ball.set_is_free(True)

    def set_width(self, width=3):
        """
        Sets width of paddle
        :param width: width of paddle
        """
        representation = ['X' * width]
        self.set_representation(representation)

    def move_relative(self, board, x_diff=0):
        """
        Sets new position relative to current position of paddle
        :param board: matrix storing the board
        :param x_diff: delta by which the position of paddle changes in the x-axis
        """
        self.clear(board)
        new_pos = self._x + x_diff
        if new_pos >= 0 and new_pos + self._width < config.board_width:
            self.set_x(new_pos)
            if self._ball:
                self._ball.move_relative(board, x_diff)

    def render(self, board):
        for row in range(self._height):
            for col in range(self._width):
                board[self._y + row][self._x + col] = self._representation[row][col]
