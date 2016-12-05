"""Stores data structures."""
from enum import Enum
from namedlist import namedlist


class Split(Enum):
    """
    Enum containing information of how the window is split:
    horizontally or vertically.
    """
    vert = 0
    horz = 1

    def swap(self):
        """Gets the opposite split.

        Returns:
            (Split): the split opposite of the current split.
        """
        return Split((self.value + 1) % 2)


class Dir(Enum):
    """
    Enum containing information of how the direction in 4 ways.
    """
    up = 0
    right = 1
    down = 2
    left = 3


Rect = namedlist('Rect', 'x, y, w, h')
Size = namedlist('Size', 'w, h')
