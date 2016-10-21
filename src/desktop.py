"""Stores the Desktop class"""
from node import Node
from data import Size, Rect
from window import Window


class Desktop:
    """Desktop holds the root nodes and provides methods to switch between these.

    Attributes:
        roots: Root nodes holding all nodes.
    """

    def __init__(self, width, height):
        """Initializes the Desktop class.

        Args:
            width: width of the desktop.
            height: height of the desktop.
            hwnds: all hwnds detected.
        """
        self.root = None
        self.focus = None
        self.size = Size(width, height)

    def __str__(self):
        """Prints out full tree representation
        """
        # TODO Spacing on print
        current_nodes = [self.root]
        next_nodes = []
        output = ""
        while any(current_nodes):
            for node in current_nodes:
                output += str(node.rect if node else "NA") + " | "
                if node:
                    next_nodes.append(node.first)
                    next_nodes.append(node.second)
            current_nodes = next_nodes
            next_nodes = []
            output += "\n"
        return output

    def insert(self, hwnd):
        leaf_node = Node(Window(hwnd))
        internal_node = Node()
        if self.focus is None:
            self.focus = self.root

        # first window
        if self.root is None:
            assert(self.root == self.focus)
            self.root = leaf_node
            self.root.rect = Rect(0, 0, self.size.w, self.size.h)
        else:
            internal_node.first = leaf_node
            internal_node.second = self.focus
            internal_node.rect = Rect(0, 0, self.size.w, self.size.h)
            if self.focus.parent is None:
                self.root = internal_node
            else:
                internal_node.parent = self.focus.parent
                if self.focus.is_first_child():
                    self.focus.parent.first = internal_node
                else:
                    self.focus.parent.second = internal_node
            leaf_node.parent = internal_node
            self.focus.parent = internal_node

        self.update_all(self.root)

    def update_all(self, current):
        if current is None:
            return

        current.update()
        self.update_all(current.first)
        self.update_all(current.second)
