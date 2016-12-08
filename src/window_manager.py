"""Manages and modifies windows."""
import window_api
from desktop import Desktop
import sys
from data import Dir


class WindowManager:
    """
    Calls functions to modify windows and stores desktop.

    Attributes:
        desktop (Desktop): The desktop object.
        gap (int): The gap between windows.
    """

    def __init__(self, gap=6):
        """
        Initializes the WM and makes a desktop.

        Kwargs:
            gap (int): The gap between windows.
        """
        width, height = window_api.get_screen_resolution()

        self.desktop = Desktop(width, height)
        self.gap = gap

    def change_gaps(self, delta):
        """
        Changes gap size by delta.

        Args:
            delta (int): Amount of pixels to change gap by.
        """
        self.gap = max(self.gap + delta, 0)
        self.desktop.update_all(self.desktop.root)

    def change_ratio(self, delta):
        """
        Changes ratio amount of focused window by delta.

        Args:
            delta (int): Amount of pixels to change ratio by.
        """
        node = self.get_focused_node()

        # A positive delta would make the window smaller
        if node.is_second_child():
            delta = -delta

        if node.parent is not None:
            node.parent.ratio = WindowManager.constrain(node.parent.ratio + delta, 0, 1)
            self.desktop.update_all(self.desktop.root)

    def change_focus(self, dir):
        """
        Moves window focus based on relation in tree.

        Args:
            dir (Dir): Determines change direction.
                - Up focuses parent, down focuses child (if any) or sibling
        """
        node = self.get_focused_node()

        # parent can never be None because then there would be one window only
        if node is None or node.parent is None:
            return

        focus = None
        if dir == Dir.up:
            if node.parent.parent is not None:
                focus = node.parent.parent.first
        elif dir == Dir.down:
            if node.is_first_child():
                focus = node.parent.second
            else:
                focus = node.parent.first
            while focus.window is None:
                focus = focus.first
        if focus is not None and focus.window is not None:
            window_api.focus_window(focus.window.hwnd)

    def set_insertion(self):
        """
        Sets the insertion point to the currently focused window.
        """
        node = self.get_focused_node()

        if node is not None:
            self.desktop.insertion = node

    def move_window(self, dir):
        """
        Swaps currently focused window with another window based on relation in tree.

        Args:
            dir (Dir): Determines change direction.
                - Up swaps parent, down swaps child (if any) or sibling
        """
        node = self.get_focused_node()

        # parent can never be None because then there would be one window only
        if node is None or node.parent is None:
            return

        swap = None
        if dir == Dir.up:
            if node.parent.parent is not None:
                swap = node.parent.parent.first
        elif dir == Dir.down:
            if node.is_first_child():
                swap = node.parent.second
            else:
                swap = node.parent.first
            while swap.window is None:
                swap = swap.first
        if swap is not None and swap.window is not None:
            WindowManager.swap_node(swap, node)
            self.desktop.update_all(self.desktop.root)

    def change_split(self):
        """
        Swap split type on focused window.
        """
        node = self.get_focused_node()

        if node is not None:
            self.swap_split_recurse(node.parent)

        self.desktop.update_all(self.desktop.root)

    def swap_split_recurse(self, node):
        """
        Helper function for swap_split.

        Args:
            node (Node): The current node to swap split.
        """
        if node is not None:
            node.split = node.split.swap()
            self.swap_split_recurse(node.first)
            self.swap_split_recurse(node.second)

    def exit(self):
        """
        Tears down all windows and exits.
        """
        self.teardown(self.desktop.root)

        sys.exit(0)

    def teardown(self, node):
        """
        Tells a node to teardown its window and tells its children to.

        Args:
            node (Node): The current node to teardown.
        """
        if node is None:
            return

        if node.window:
            node.window.teardown_window()

        self.teardown(node.first)
        self.teardown(node.second)

    def find_node(self, hwnd, node):
        """
        Searches through all nodes for the given hwnd.

        Args:
            hwnd (int): The window handler to find.
            node (Node): The current node to search.
        Returns:
            (Node): The Node with given hwnd or None if not in tree.
        """
        if node is None:
            return None
        if node.window and node.window.hwnd == hwnd:
            return node
        return self.find_node(hwnd, node.first) or self.find_node(hwnd, node.second)

    def insert(self, hwnd=None):
        """
        Tells desktop to insert given window, or focused window if none.

        Kwargs:
            hwnd (int): The window handler to insert.
        """
        if hwnd is None:
            hwnd = window_api.get_foreground_window()

        # Window already inserted
        if self.find_node(hwnd, self.desktop.root) is not None:
            return

        self.desktop.insert(hwnd)

    def insert_all(self):
        """
        Tells desktop to insert all windows.
        """
        for window in window_api.get_all_windows():
            self.insert(window)

    def remove(self):
        """Tells desktop to remove focused window.
        """
        # TODO implement desktop.remove

    def remove_all(self):
        """
        Tells desktop to remove all windows.
        """
        # TODO implement desktop.remove_all

    def get_focused_node(self):
        """
        Get the node that is currently focused.

        Returns:
            (Node): Currently focused window's node.
        """
        hwnd = window_api.get_foreground_window()
        return self.find_node(hwnd, self.desktop.root)

    @staticmethod
    def constrain(n, low=0, high=1):
        """
        Helper function to ensure value is between low and high.
        If not, limit to low/high.
        """
        if n < low:
            return low
        elif n > high:
            return high
        return n

    @staticmethod
    def swap_node(a, b):
        """
        Swaps the location of node A and node B in the tree.

        Args:
            a (Node): Node to swap location with B
            b (Node): Node to swap location with A
        """
        temp_parent = a.parent
        temp_first = a.first
        temp_second = a.second
        temp_is_first = a.is_first_child()

        a.parent = b.parent
        a.first = b.first
        a.second = b.second
        if b.is_first_child():
            b.parent.first = a
        else:
            b.parent.second = a

        b.parent = temp_parent
        b.first = temp_first
        b.second = temp_second
        if temp_is_first:
            temp_parent.first = b
        else:
            temp_parent.second = b
