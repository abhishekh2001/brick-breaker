from component import Component
from colorama import Fore, Back, Style


class Brick(Component):
    def __init__(self, x, y, brick_type, representation=[['X']]):
        """
        Implements a single Brick component
        :param x: x position
        :param y: y position
        :param brick_type: type of brick, -1, 1, 2, 3
        :param representation: representation in matrix/board
        """
        super().__init__(x, y, representation)
        self._brick_type = brick_type
        self._health = brick_type
        if brick_type == -1:
            self._health = 9999

    def set_brick_type(self, brick_type):
        self._brick_type = brick_type
        if brick_type == -1:
            self._health = brick_type

    def get_brick_type(self):
        return self._brick_type

    def get_health(self):
        return self._health

    def got_hit(self, board):
        """
        Performs operations for when the brick gets hit by the ball
        and returns whether the brick is destroyed
        :rtype: bool
        """
        if self._brick_type == 1:
            self.destroy(board)
            return True
        elif self._brick_type != -1 and self._brick_type != 0:
            self._health -= 1
            self._brick_type -= 1
        return False

    def destroy(self, board):
        self._health = 0
        self._brick_type = 0
        self.clear(board)

    def _get_color(self):
        if self._brick_type == -1:
            return Back.RED
        elif self._brick_type == 1:
            return Back.GREEN
        elif self._brick_type == 2:
            return Back.BLUE
        elif self._brick_type == 3:
            return Back.MAGENTA
        else:
            return Back.LIGHTCYAN_EX

    def render(self, board):
        for row in range(self._height):
            for col in range(self._width):
                board[self._y + row][self._x + col] = self._get_color() + self._representation[row][col] \
                                                      + Style.RESET_ALL
