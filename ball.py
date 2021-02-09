from component import Component
import config


class Ball(Component):
    def __init__(self, x, y, xvel, yvel, representation=[['o']], free=0, speed=1):
        """
        Ball component
        :param x: x position
        :param y: y position
        :param xvel: velocity in the x direction
        :param yvel: velocity in the y direction
        :param representation: representation of ball in matrix
        """
        super().__init__(x, y, representation)
        self._xvel = xvel
        self._yvel = yvel
        self._speed = speed
        self.is_free = free

    def set_is_free(self, free):
        self.is_free = free

    def get_is_free(self):
        return self.is_free

    def set_speed(self, speed):
        self._speed = speed

    def get_speed(self):
        return self._speed

    def move_relative(self, board, x_diff=0, y_diff=0):
        """
        Sets new position relative to current position of paddle
        :param board: matrix storing the board
        :param x_diff: delta by which the position of ball changes in the x-axis
        :param y_diff: delta by which the position of ball changes in the y-axis
        """
        self.clear(board)

        new_pos_x = self._x + x_diff
        if new_pos_x >= 0 and new_pos_x + self._width <= config.board_width:
            self.set_x(new_pos_x)

        new_pos_y = self._y + y_diff
        if new_pos_y >= 0 and new_pos_y + self._height <= config.board_height:
            self.set_y(new_pos_y)

    def set_relative_velocity(self, x_vel_diff=0, y_vel_diff=0):
        self._xvel += x_vel_diff
        self._yvel += y_vel_diff