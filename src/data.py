"""Stores data structures"""
from enum import Enum
from namedlist import namedlist


class Split(Enum):
    """Enum containing information of how the window is split:
    horizontally or vertically.
    """
    vert = 0
    horz = 1

    def swap(self):
        """Returns the opposite split.
        """
        return Split((self.value + 1) % 2)

Rect = namedlist('Rect', 'x, y, w, h')
Size = namedlist('Size', 'w, h')
