"""This module abstracts the win32 api logic into easily usable functions
relevent to the program."""
import ctypes
import ctypes.wintypes
import win32gui as wg
import win32api as wa
import win32con as wc


def getScreenResolution():
    """Returns the screen resolution in pixels (width, height)."""
    return wa.GetSystemMetrics(0), wa.GetSystemMetrics(1)


def isRealWindow(hwnd):
    """Returns True if the hwnd is a visible window.
    http://stackoverflow.com/a/7292674/238472
    and https://github.com/Answeror/lit/blob/master/windows.py for details.
    """

    class TITLEBARINFO(ctypes.Structure):
        """ctype Structure for TITLEBARINFO"""
        _fields_ = [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcTitleBar", ctypes.wintypes.RECT),
            ("rgstate", ctypes.wintypes.DWORD * 6)
        ]

    class WINDOWINFO(ctypes.Structure):
        """ctype Structure for WINDOWINFO"""
        _fields_ = [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcWindow", ctypes.wintypes.RECT),
            ("rcClient", ctypes.wintypes.RECT),
            ("dwStyle", ctypes.wintypes.DWORD),
            ("dwExStyle", ctypes.wintypes.DWORD),
            ("dwWindowStatus", ctypes.wintypes.DWORD),
            ("cxWindowBorders", ctypes.wintypes.UINT),
            ("cyWindowBorders", ctypes.wintypes.UINT),
            ("atomWindowType", ctypes.wintypes.ATOM),
            ("wCreatorVersion", ctypes.wintypes.DWORD),
        ]

    if not wg.IsWindowVisible(hwnd) or not wg.IsWindow(hwnd):
        return False

    hwndWalk = wc.NULL
    hwndTry = ctypes.windll.user32.GetAncestor(hwnd, wc.GA_ROOTOWNER)
    while hwndTry != hwndWalk:
        hwndWalk = hwndTry
        hwndTry = ctypes.windll.user32.GetLastActivePopup(hwndWalk)
        if wg.IsWindowVisible(hwndTry):
            break

    if hwndWalk != hwnd:
        return False

    # Removes some task tray programs and "Program Manager"
    ti = TITLEBARINFO()
    ti.cbSize = ctypes.sizeof(ti)
    ctypes.windll.user32.GetTitleBarInfo(hwnd, ctypes.byref(ti))
    if ti.rgstate[0] & wc.STATE_SYSTEM_INVISIBLE:
        return False

    # Tool windows should not be displayed either
    if wg.GetWindowLong(hwnd, wc.GWL_EXSTYLE) & wc.WS_EX_TOOLWINDOW:
        return False

    pwi = WINDOWINFO()
    ctypes.windll.user32.GetWindowInfo(hwnd, ctypes.byref(pwi))

    # Backround AND FOREGROUND metro style apps.
    # Should be fixed for background only
    # TODO I don't hate netflix
    if pwi.dwStyle == 2496593920 or getText == 'Netflix':
        return False

    if pwi.dwExStyle & wc.WS_EX_NOACTIVATE:
        return False

    if getText(hwnd) == "":
        print("WARNING: NO TEXT WINDOW: %s" % hwnd)
        return False

    return True


def getAllWindows():
    """Returns the hwnd of all 'real' windows."""
    def call(hwnd, param):
        """The callback function for EnumWindows.
        Appends all hwnds to param list"""
        if isRealWindow(hwnd):
            param.append(hwnd)

    winds = []
    wg.EnumWindows(call, winds)
    return winds


def getText(hwnd):
    """Returns the titlebar text of a window.
    """
    return ''.join(char for char in wg.GetWindowText(hwnd) if ord(char) <= 126)


def moveWindow(hwnd, loc, size):
    """Moves window.
    The 8 and 16 values are due to windows 10 having an invisible border.

    Args:
        loc: (x,y) of new location
        size: (width, height) of new location
    """
    wg.MoveWindow(hwnd, loc[0] - 8, loc[1], size[0] + 16, size[1] + 8, True)


def restore(hwnd):
    """Restores (unmaximizes) the window.
    """
    wg.ShowWindow(hwnd, wc.SW_RESTORE)
