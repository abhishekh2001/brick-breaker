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
    """
    def __init__(self, x, y, representation):
        super().__init__(x, y, representation)
        self._type = random.randint(1, 6)
        self._speed = 0.6

    def get_type(self):
        return self._type

    def get_speed(self):
        return self._speed

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
