"""Stores the Node class."""
from data import Split, Rect


class Node:
    """
    Stores all information on a window.

    Attributes:
        parent (Node): The parent Node.
        window (Window): The window held by this Node.
        first (Node): The first child.
        second (Node): The second child.
        split (Split): Direction node is split for children.
        rect (Rect): x, y, w, h coordinates of window
        ratio (int): ratio of split for children.
    """

    def __init__(self, window=None, parent=None):
        """
        Initializes the node.

        Args:
            parent (Node): The parent Node.
            window (Window): The window held by this Node.
        """
        self.parent = parent
        self.window = window

        self.first = None
        self.second = None

        self.rect = None
        self.split = None

        self.ratio = .5

    def update(self):
        """
        Updates a window by setting new split and rect.
        Only if the rect has changed will the the window move.
        """
        if self.window is not None:
            old_rect = self.window.get_rect()
        else:
            old_rect = self.rect

        self.set_split()
        self.set_rect()
        if self.rect != old_rect and self.window is not None:
            gap = 6  # TODO: gap should be taken from window_manager
            self.window.move(self.rect, gap)

    def set_split(self):
        """
        Sets the node's split if is not set to be opposite of parents.
        """
        if self.split is None:
            self.split = self.parent.split.swap() if self.parent is not None else Split.vert

    def set_rect(self):
        """
        Updates the node's rect based on parent.
        """
        if self.parent is None:
            return self.rect

        self.rect = Rect(self.parent.rect.x,
                         self.parent.rect.y,
                         self.parent.rect.w,
                         self.parent.rect.h)

        ratio = self.parent.ratio if self.is_first_child() else 1 - self.parent.ratio

        if self.parent.split == Split.horz:
            if not self.is_first_child():
                self.rect.y += self.parent.rect.h * (1 - ratio)
            self.rect.h *= ratio
        elif self.parent.split == Split.vert:
            if not self.is_first_child():
                self.rect.x += self.parent.rect.w * (1 - ratio)
            self.rect.w *= ratio

    def __str__(self):
        """
        Gets the string representation of the Node.

        Returns:
            (string): Representation of the Node.
        """
        if self.window:
            return '[*{0}*]'.format(self.window.hwnd)
        else:
            return '[Internal]'

    def is_first_child(self):
        return self.parent is not None and self.parent.first == self

    def is_second_child(self):
        return self.parent is not None and self.parent.second == self

    def is_leaf_node(self):
        if self.first is None:
            assert(self.second is None)
            assert(self.window is not None)
        return self.window is not None

    def get_sibling(self):
        if self.parent is None: 
            return self
        if self.is_first_child():
            return self.parent.second
        else:
            return self.parent.first
