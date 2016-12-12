"""Stores the Desktop class"""
from node import Node
from data import Size, Rect
from window import Window


class Desktop:
    """
    Desktop holds the root nodes and provides methods to switch between these.

    Attributes:
        roots (Node): Root nodes holding all nodes.
        insertion (Node): Insertion point for new nodes.
        size (Size(w, h)): The desktop's size.
    """

    def __init__(self, width, height):
        """
        Initializes the Desktop class.

        Args:
            width (int): The width of the desktop.
            height (int): The height of the desktop.
        """
        self.root = None
        self.insertion = None
        self.size = Size(width, height)

    def __str__(self):
        """
        Prints out full tree representation.

        Returns:
            (string): String representation of tree
        """
        current_nodes = [self.root]
        next_nodes = []
        output = ""
        pad = "\t\t"
        first = True
        while any(current_nodes):
            output += pad
            for node in current_nodes:
                if not first:
                    output += " | "
                first = False
                output += str(node if node else "[   NA  ]")
                if node:
                    next_nodes.append(node.first)
                    next_nodes.append(node.second)
            current_nodes = next_nodes
            next_nodes = []
            output += "\n"
            pad = pad[:-1]
            first = True
        return output

    def insert(self, hwnd):
        """
        Inserts given window into the tree.

        Args:
            hwnd (int): The window handler to insert.
        """
        leaf_node = Node(Window(hwnd))
        internal_node = Node()
        if self.insertion is None:
            self.insertion = self.root

        # first window
        if self.root is None:
            self.root = leaf_node
            self.root.rect = Rect(0, 0, self.size.w, self.size.h)
            self.insertion = self.root
        else:
            internal_node.first = leaf_node
            internal_node.second = self.insertion
            internal_node.rect = Rect(0, 0, self.size.w, self.size.h)
            if self.insertion.parent is None:
                self.root = internal_node
            else:
                internal_node.parent = self.insertion.parent
                if self.insertion.is_first_child():
                    self.insertion.parent.first = internal_node
                else:
                    self.insertion.parent.second = internal_node
            leaf_node.parent = internal_node
            self.insertion.parent = internal_node

        self.update_all(self.root)

    def update_all(self, node):
        """
        Tells window to update itself, and tells children to do so aswell.

        Args:
            node (Node): Currently updating node.
        """
        if node is None:
            return

        node.update()
        self.update_all(node.first)
        self.update_all(node.second)
