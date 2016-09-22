"""Stores data structures"""
from enum import Enum
from namedlist import namedlist


class Split(Enum):
    """Enum containing information of how the window is split:
    horizontally or vertically.
    """
    vert = 0
    horz = 1

Location = namedlist('Location', 'x, y')
Size = namedlist('Size', 'w, h')
