import random
from component import Component
import config


class PowerUp(Component):
    """
    self._type is one of the six power-up types
    The map is as follows:
    1: expand paddle
    2: shrink paddle
    3: ball multiplier
    4: fast ball
    5: thru-ball
    6: paddle grab


    _status determines current status of the powerup
    -1: missed
    0: spawned
    1: active
    2: disabled
    """
    def __init__(self, x, y, representation):
        super().__init__(x, y, representation)
        self._type = random.randint(1, 6)
        self._type = 4                              # TESTING
        self._speed = 0.6
        self._status = 0

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_type(self):
        return self._type

    def get_speed(self):
        return self._speed

    def is_caught_by_paddle(self, paddle):
        """
        Return true if caught by paddle and false otherwise
        :param paddle: The paddle instance
        :return: Boolean, true if caught and false otherwise
        """
        if paddle.get_x() <= self._x <= paddle.get_x() + paddle.get_width() and \
                self._y == paddle.get_y() - 1:
            return True
        return False

    def go_down(self, board):
        """
        Continue motion of powerup
        Returns true if powerup is lost
        :param board: matrix storing the board
        """
        self.clear(board)

        new_pos_y = self._y + 1
        if new_pos_y >= 0 and new_pos_y + self._height <= config.board_height:
            self.set_y(new_pos_y)

        if self._y >= config.paddle_row_restriction:
            return True
        return False
