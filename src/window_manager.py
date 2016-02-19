"""Manages and modifies windows."""
import window_api
from desktop import Desktop
from node import Split


class WindowManager:
    """Initializes, keeps track of, and calls functions to modify windows.
    """

    def __init__(self, gap=6):
        """Initializes the WM and makes a desktop.

        Args:
            gap (int, optional): The gap between windows
        """
        width, height = window_api.get_screen_resolution()
        windows = window_api.get_all_windows()

        self.desktop = Desktop(width, height, windows)
        self.gap = gap
        self.update_all_windows()

    def update_all_windows(self):
        """Tells all nodes to updateLocation.
        """
        for root in self.desktop.roots:
            self.update_node_locations(root)

    def update_node_locations(self, node):
        """Tells a node to:
        * Update its location and size
        * Unmaximize it's window
        * Move it to its new location/size
        * Call this function on all of its children
        """
        node.update_all()

        window_api.restore(node.hwnd)
        window_api.move_window(node.hwnd, node.get_window_loc(self.gap),
                               node.get_window_dims(self.gap))
        for child in node.children:
            self.update_node_locations(child)

    def increase_gaps(self):
        """Increase gap size.
        """
        self.gap += 2
        self.update_all_windows()

    def decrease_gaps(self):
        """Decrease gap size.
        """
        self.gap = max(self.gap - 2, 0)
        self.update_all_windows()

    def swap_split(self):
        """Swap split type.
        """
        self.desktop.roots[0].split = Split.horz
        self.update_all_windows()
