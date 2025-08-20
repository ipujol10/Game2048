"""Module to have utilities"""

from enum import Enum


class Directions(Enum):
    """Possible movements that the player can do in the game"""

    Up = 0  # pylint: disable=C0103
    Left = 1  # pylint: disable=C0103
    Down = 2  # pylint: disable=C0103
    Right = 3  # pylint: disable=C0103
