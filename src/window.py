"""Stores the Window class."""
import window_api


class Window:
    """
    Holds window information as well as functions to manipulate the window.

    Attributes:
        hwnd (int): The window handle.
        original_rect (Rect): The original bounding rectangle of the window.
    """

    def __init__(self, hwnd):
        """
        Initializes attributes and sets up the window.

        Args:
            hwnd (int): The window handler.
        """
        self.hwnd = hwnd
        self.original_rect = window_api.get_window_rect(hwnd)
        self.setup_window()

    def setup_window(self):
        """
        Restores a window and removes its border.
        """
        window_api.remove_titlebar(self.hwnd)
        window_api.focus_window(self.hwnd)

    def move(self, rect, gap, border=True):
        """
        Moves the window the specified location and dimensions.

        Args:
            rect (Rect): The rect to move to.
            gap (int): The gap between windows.

        Kwargs:
            border (bool): If the invisible border needs to be accounted for.
        """
        window_api.move_window(self.hwnd, rect, gap, border)

    def teardown_window(self):
        """
        Resets the window to original qualities.
        """
        window_api.add_titlebar(self.hwnd)
        self.move(self.original_rect, 0, False)

    def get_rect(self):
        """Gets the current bounding rect of the window.

        Returns:
            (Rect): Bounding rect of the window.
        """
        return window_api.get_window_rect(self.hwnd)
