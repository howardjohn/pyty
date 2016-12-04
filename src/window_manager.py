"""Manages and modifies windows."""
import window_api
from desktop import Desktop
import sys


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

        # TODO add multi-desktop support
        # TODO consider desktop manipulating windows.
        self.desktop = Desktop(width, height)
        self.gap = gap


    def increase_gaps(self):
        """Increase gap size.
        """
        self.gap += 2
        self.desktop.update_all(self.desktop.root)

    def decrease_gaps(self):
        """Decrease gap size.
        """
        self.gap = max(self.gap - 2, 0)
        self.desktop.update_all(self.desktop.root)

    def swap_split(self):
        """Swap split type on focused window.
        """
        hwnd = window_api.get_foreground_window()
        node = self.findNode(hwnd, self.desktop.root)

        if node:
            if node.parent:
                node.parent.split = node.parent.split.swap()
            else:
                node.split = node.split.swap()
        self.desktop.update_all(self.desktop.root)

    def exit(self):
        """Tears down all windows and exits.
        """
        # TODO: save original state and restore after
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

    def findNode(self, hwnd, node):
        """Searches through all nodes for the given hwnd.
        If not found, returns null.
        """
        if node is None:
            return None
        if node.window and node.window.hwnd == hwnd:
            return node
        return self.findNode(hwnd, node.first) or self.findNode(hwnd, node.second)

    def insert(self):
        """Tells desktop to insert focused window.
        """
        focused = window_api.get_foreground_window()
        self.desktop.insert(focused)

    def insert_all(self):
        """Tells desktop to insert all windows.
        """
        for window in window_api.get_all_windows():
            self.desktop.insert(window)

    def remove(self):
        """Tells desktop to remove focused window.
        """
        focused = window_api.get_foreground_window()
        # TODO implement desktop.remove

    def remove_all(self):
        """Tells desktop to remove all windows.
        """
        # TODO implement desktop.remove_all
