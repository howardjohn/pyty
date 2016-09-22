"""Stores the Node class"""
from data import Split, Location, Size


class Node:
    """Stores all information on a window.

    Attributes:
        children (list): holds all childen Nodes.
        window: the window held by this Node.
        parent (Node): parent Node.
        split (Split): Direction node is split relative to its siblings.
        loc (namedlist): Location of upper left of window.
        size (namedlist): (width,height) of window.
    """

    def __init__(self, window, parent=None, width=None, height=None):
        """Initializes the node. Tells the parent this is a child.
        Calculates the type of split.
        """
        self.parent = parent

        if isinstance(self.parent, Node):
            self.parent.add_child(self)

        self.children = []
        self.window = window

        # Initially nodes should alternate split at each level
        self.split = Split((self.get_level()) % 2)

        self.loc = Location(None, None)
        self.size = Size(width, height)

    def add_child(self, child):
        """Appends child to children list.
        """
        self.children.append(child)

    def update_coords(self):
        """Updates coordinates by calling the getCoords function.
        Then calls this function on all children.
        """
        if not isinstance(self.parent, Node):
            self.loc.x = 0
            self.loc.y = 0
        else:
            self.loc.x, self.loc.y = self.get_coords()

        for child in self.children:
            child.update_coords()

    def get_coords(self):
        """Returns the x, y coordinates by checking parent coordinates,
        and relative position of siblings based on type of split.
        """
        # move relative to parent
        if self.parent.split == Split.vert:
            x = self.parent.loc.x + self.parent.size.w
            y = self.parent.loc.y
        else:
            x = self.parent.loc.x
            y = self.parent.loc.y + self.parent.size.h

        # move relative to siblings
        if self.split == Split.vert:
            x += sum([child.size.w for child in
                      self.parent.children[:self.parent.children.index(self)]])
        else:
            y += sum([child.size.h for child in
                      self.parent.children[:self.parent.children.index(self)]])

        return x, y

    def update_dims(self):
        """Updates dimensions by calling the getDims function.
        Then calls this function on all children.
        """
        self.size.w, self.size.h = self.get_dims(
            self.parent.size.w, self.parent.size.h, self.split)

        for child in self.children:
            child.update_dims()

    def get_dims(self, width, height, split):
        """Returns (width, height) value based on number of siblings and children.
        """
        divisor = 1

        # share space with siblings
        if isinstance(self.parent, Node):
            divisor += len(self.parent.children) - 1

        # share space with children
        divisor *= 2 if self.children else 1

        if split == Split.horz:
            return (width, height // divisor)
        return (width // divisor, height)

    def update_all(self):
        """Calls all update functions.
        """
        self.update_dims()
        self.update_coords()

    def get_level(self):
        """Returns the depth of the node (how many parents above it).
        """
        level = 1
        node = self
        while isinstance(node, Node):
            level += 1
            node = node.parent
        return level

    def get_window_dims(self, gap=0):
        """Returns the window dimensions, taking gap into account.
        """
        root_parent = self
        while isinstance(root_parent, Node):
            root_parent = root_parent.parent

        width = self.size.w - gap
        width -= gap // 2 * (self.loc.x == 0)
        width -= gap // 2 * (self.loc.x + self.size.w == root_parent.size.w)

        height = self.size.h - gap
        height -= gap // 2 * (self.loc.y == 0)
        height -= gap // 2 * (self.loc.y + self.size.h == root_parent.size.h)

        return (width, height)

    def get_window_loc(self, gap=0):
        """Returns the window location, taking gap into account.
        """
        root_parent = self
        while isinstance(root_parent, Node):
            root_parent = root_parent.parent

        x = self.loc.x + gap
        y = self.loc.y + gap

        if self.loc.x != 0:
            x -= gap // 2
        if self.loc.y != 0:
            y -= gap // 2
        return (x, y)

    def __str__(self):
        """Returns a string representation of the Node.
        """
        return '*Node* level:{0}, childs:{1}'.format(self.get_level(),
                                                     len(self.children))
