from node import Node
from data import Split, Location, Size


class Desktop:
    """Desktop holds the root nodes and provides methods to switch between these.

    Attributes:
        roots: Root nodes holding all nodes.
    """

    def __init__(self, w, h, hwnds):
        """Initializes the Desktop class.

        Args:
            w: width of the desktop.
            h: height of the desktop.
            hwnds: all hwnds detected.
        """
        # TODO: roots not root
        self.roots = [Node(hwnd=hwnds[0], parent=self, w=w, h=h)]
        self.roots[0].split = Split.vert
        self.size = Size(w, h)
        for hwnd in hwnds[1:]:
            Node(hwnd, self.roots[0])
        for root in self.roots:
            root.updateAll()
