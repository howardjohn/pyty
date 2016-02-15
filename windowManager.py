import windowApi
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
        w, h = windowApi.getScreenResolution()
        windows = windowApi.getAllWindows()

        self.desktop = Desktop(w, h, windows)
        self.gap = gap
        self.updateAllWindows()

    def updateAllWindows(self):
        """Tells all nodes to updateLocation.
        """
        for root in self.desktop.roots:
            self.updateNodeLocations(root)

    def updateNodeLocations(self, node):
        """Tells a node to:
        * Update its location and size
        * Unmaximize it's window
        * Move it to its new location/size
        * Call this function on all of its children
        """
        node.updateAll()

        windowApi.restore(node.hwnd)
        windowApi.moveWindow(node.hwnd, node.getWindowLoc(self.gap),
                             node.getWindowDims(self.gap))
        for child in node.children:
            self.updateNodeLocations(child)

    def incGaps(self):
        """Increase gap size.
        """
        self.gap += 2
        self.updateAllWindows()

    def decGaps(self):
        """Decrease gap size.
        """
        self.gap = max(self.gap - 2, 0)
        self.updateAllWindows()

    def swapSplit(self):
        """Swap split type.
        """
        self.desktop.roots[0].split = Split.horz
        self.updateAllWindows()
