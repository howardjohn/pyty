"""The node class stores all the information about the window it holds.
"""
from enum import Enum


class Split(Enum):
    """Enum containing information of how the window is split:
    horizontally or vertically.
    """
    vert = 0
    horz = 1


class Node:
    """Stores all information on a window.

    Attributes:
        children (list): holds all childen Nodes.
        hwnd: the window held by this Node.
        parent (Node): parent Node.
        split (Split): Direction node is split relative to its siblings.
        h (int): height
        w (int): width
        x (int): x coordinate
        y (int): y coordinate
    """

    def __init__(self, hwnd, parent=None, w=None, h=None):
        """Initializes the node. Tells the parent this is a child.
        Calculates the type of split.
        """
        self.parent = parent

        if type(self.parent) is Node:
            self.parent.addChild(self)
        self.children = []
        self.hwnd = hwnd

        self.split = Split((self.getLevel()) % 2)
        self.w = w
        self.h = h
        self.x = None
        self.y = None

    def addChild(self, child):
        """Appends child to children list.
        """
        self.children.append(child)

    def updateCoords(self):
        """Updates coordinates by calling the getCoords function.
        Then calls this function on all children.
        """
        if type(self.parent) is not Node:
            self.x = 0
            self.y = 0
        else:
            self.x, self.y = self.getCoords()

        for child in self.children:
            child.updateCoords()

    def getCoords(self):
        """Returns the x, y coordinates by checking parent coordinates,
        and relative position of siblings based on type of split.
        """
        # move relative to parent
        if self.parent.split == Split.vert:
            x = self.parent.x + self.parent.w
            y = self.parent.y
        else:
            x = self.parent.x
            y = self.parent.y + self.parent.h

        # move relative to siblings
        if self.split == Split.vert:
            x += sum([c.w for c in
                      self.parent.children[:self.parent.children.index(self)]])
        else:
            y += sum([c.h for c in
                      self.parent.children[:self.parent.children.index(self)]])

        return x, y

    def updateDims(self):
        """Updates dimensions by calling the getDims function.
        Then calls this function on all children.
        """
        if self.parent is None:
            self.w, self.h = self.getDims(self.w, self.h, self.split)
        else:
            self.w, self.h = self.getDims(
                self.parent.w, self.parent.h, self.split)

        for child in self.children:
            child.updateDims()

    def getDims(self, w, h, split):
        """Returns (w, h) value based on number of siblings and children.
        """
        n = 1
        if type(self.parent) is Node:
            n += len(self.parent.children) - 1
        n *= 2 if self.children else 1
        if split == Split.horz:
            return (w, h // n)
        return (w // n, h)

    def updateAll(self):
        """Calls both update functions.
        """
        self.updateDims()
        self.updateCoords()

    def getLevel(self):
        """Returns the depth of the node (how many parents above it).
        """
        level = 1
        node = self
        while type(node) is Node:
            level += 1
            node = node.parent
        return level

    def getWindowDims(self, gap=0):
        """Returns the window dimensions, taking gap into account.
        """
        rootParent = self
        while type(rootParent) is Node:
            rootParent = rootParent.parent

        width = self.w - gap
        width -= gap // 2 * (self.x == 0)
        width -= gap // 2 * (self.x + self.w == rootParent.w)

        height = self.h - gap
        height -= gap // 2 * (self.y == 0)
        height -= gap // 2 * (self.y + self.h == rootParent.h)

        return (width, height)

    def getWindowLoc(self, gap=0):
        """Returns the window location, taking gap into account.
        """
        rootParent = self
        while type(rootParent) is Node:
            rootParent = rootParent.parent

        x = self.x + gap
        y = self.y + gap

        if self.x != 0:
            x -= gap // 2
        if self.y != 0:
            y -= gap // 2
        return (x, y)

    def __str__(self):
        """Returns a string representation of the Node.
        """
        return '*Node* level:{0}, childs:{1}'.format(self.getLevel(),
                                                     len(self.children))
