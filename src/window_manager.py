"""Manages and modifies windows."""
import window_api
from desktop import Desktop
import sys


def constrain(n, low=0, high=1):
    if n < low:
        return low
    elif n > high:
        return high
    return n


class WindowManager:
    """Initializes, keeps track of, and calls functions to modify windows.
    """

    def __init__(self, gap=6):
        """Initializes the WM and makes a desktop.

        Args:
            gap (int, optional): The gap between windows

        Attributes:
            desktop (Desktop): Stores the desktop object.
        """
        width, height = window_api.get_screen_resolution()

        self.desktop = Desktop(width, height)
        self.gap = gap

    def change_gaps(self, delta):
        """Changes gap size by delta.
        """
        self.gap = max(self.gap + delta, 0)
        self.desktop.update_all(self.desktop.root)

    def change_ratio(self, delta):
        """Change ratio of parent window to expand focused window.
        """
        hwnd = window_api.get_foreground_window()
        node = self.find_node(hwnd, self.desktop.root)
        if node.is_second_child():
            delta = -delta

        if node.parent is not None:
            node.parent.ratio = constrain(node.parent.ratio + delta, 0, 1)
            self.desktop.update_all(self.desktop.root)

    def swap_split(self):
        """Swap split type on focused window.
        """
        hwnd = window_api.get_foreground_window()
        node = self.find_node(hwnd, self.desktop.root)

        if node is not None:
            self.swap_split_recurse(node.parent)

        self.desktop.update_all(self.desktop.root)

    def swap_split_recurse(self, node):
        if node is not None:
            node.split = node.split.swap()
            self.swap_split_recurse(node.first)
            self.swap_split_recurse(node.second)

    def exit(self):
        """Tears down all windows and exits.
        """
        self.teardown(self.desktop.root)

        sys.exit(0)

    def teardown(self, node):
        """Tells a node to teardown its window and tells its children to.
        """
        if node is None:
            return

        if node.window:
            node.window.teardown_window()

        self.teardown(node.first)
        self.teardown(node.second)

    def find_node(self, hwnd, node):
        """Searches through all nodes for the given hwnd.
        If not found, returns None.
        """
        if node is None:
            return None
        if node.window and node.window.hwnd == hwnd:
            return node
        return self.find_node(hwnd, node.first) or self.find_node(hwnd, node.second)

    def insert(self, hwnd=None):
        """Tells desktop to insert given window, or focused window if none.
        """
        if hwnd is None:
            hwnd = window_api.get_foreground_window()

        # Window already inserted
        if self.find_node(hwnd, self.desktop.root) is not None:
            return

        self.desktop.insert(hwnd)

    def insert_all(self):
        """Tells desktop to insert all windows.
        """
        for window in window_api.get_all_windows():
            self.insert(window)

    def remove(self):
        """Tells desktop to remove focused window.
        """
        # TODO implement desktop.remove

    def remove_all(self):
        """Tells desktop to remove all windows.
        """
        # TODO implement desktop.remove_all
