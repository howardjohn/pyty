"""Stores the Window class"""
import window_api


class Window:
    """Holds window information as well as functions to manipulate the window.

    Attributes:
        hwnd: the window handle.
        original_rect: the original bounding rectangle of the window.
    """

    def __init__(self, hwnd):
        """Initializes attributes and sets up the window.
        """
        self.hwnd = hwnd
        self.original_rect = window_api.get_window_rect(hwnd)

        self.setup_window()

    def setup_window(self):
        """Restores a window and removes its border.
        """
        window_api.restore(self.hwnd)
        window_api.remove_titlebar(self.hwnd)

    def move(self, location, dimensions):
        """Moves the window the specified location and dimensions.
        """
        window_api.move_window(self.hwnd, location, dimensions)

    def teardown_window(self):
        # TODO reset to original size and locs
        window_api.add_titlebar(self.hwnd)
