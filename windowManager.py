import windowApi
from desktop import Desktop


class WindowManager:

    def __init__(self, gap=6):
        w, h = windowApi.getScreenResolution()
        windows = windowApi.getAllWindows()

        self.desktop = Desktop(w, h, windows)
        self.gap = gap
        self.updateAllWindows()

    def updateAllWindows(self):
        for root in self.desktop.roots:
            self.updateNodeLocations(root)

    def updateNodeLocations(self, node):
        windowApi.restore(node.hwnd)
        windowApi.moveWindow(node.hwnd, node.getWindowLoc(self.gap), node.getWindowDims(self.gap))
        for child in node.children:
            self.updateNodeLocations(child)

    def incGaps(self):
        self.gap += 2
        self.updateAllWindows()

    def decGaps(self):
        self.gap = max(self.gap - 2, 0)

        self.updateAllWindows()