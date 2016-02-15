"""Stores the Desktop class"""
from node import Node
from data import Split, Size


class Desktop:
    """Desktop holds the root nodes and provides methods to switch between these.

    Attributes:
        roots: Root nodes holding all nodes.
    """

    def __init__(self, width, height, hwnds):
        """Initializes the Desktop class.

        Args:
            width: width of the desktop.
            height: height of the desktop.
            hwnds: all hwnds detected.
        """
        self.roots = [Node(hwnd=hwnds[0], parent=self, width=width, height=height)]
        self.roots[0].split = Split.vert
        self.size = Size(width, height)
        for hwnd in hwnds[1:]:
            Node(hwnd, self.roots[0])
        for root in self.roots:
            root.update_all()
