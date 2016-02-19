"""This module abstracts the win32 api logic into easily usable functions
relevent to the program."""
import ctypes
import ctypes.wintypes
import win32gui as wg
import win32api as wa
import win32con as wc


def get_screen_resolution():
    """Returns the screen resolution in pixels (width, height)."""
    return wa.GetSystemMetrics(0), wa.GetSystemMetrics(1)


def is_real_window(hwnd):
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

    hwnd_walk = wc.NULL
    hwnd_try = ctypes.windll.user32.GetAncestor(hwnd, wc.GA_ROOTOWNER)
    while hwnd_try != hwnd_walk:
        hwnd_walk = hwnd_try
        hwnd_try = ctypes.windll.user32.GetLastActivePopup(hwnd_walk)
        if wg.IsWindowVisible(hwnd_try):
            break

    if hwnd_walk != hwnd:
        return False

    # Removes some task tray programs and "Program Manager"
    title_info = TITLEBARINFO()
    title_info.cbSize = ctypes.sizeof(title_info)
    ctypes.windll.user32.GetTitleBarInfo(hwnd, ctypes.byref(title_info))
    if title_info.rgstate[0] & wc.STATE_SYSTEM_INVISIBLE:
        return False

    # Tool windows should not be displayed either
    if wg.GetWindowLong(hwnd, wc.GWL_EXSTYLE) & wc.WS_EX_TOOLWINDOW:
        return False

    pwi = WINDOWINFO()
    ctypes.windll.user32.GetWindowInfo(hwnd, ctypes.byref(pwi))

    # Backround AND FOREGROUND metro style apps.
    # Should be fixed for background only
    if pwi.dwStyle == 2496593920 or get_text(hwnd) == 'Netflix':
        return False

    if pwi.dwExStyle & wc.WS_EX_NOACTIVATE:
        return False

    if get_text(hwnd) == "":
        print("WARNING: NO TEXT WINDOW: %s" % hwnd)
        return False

    return True


def get_all_windows():
    """Returns the hwnd of all 'real' windows."""
    def call(hwnd, param):
        """The callback function for EnumWindows.
        Appends all hwnds to param list"""
        if is_real_window(hwnd):
            param.append(hwnd)

    winds = []
    wg.EnumWindows(call, winds)
    return winds


def get_text(hwnd):
    """Returns the titlebar text of a window.
    """
    return ''.join(char for char in wg.GetWindowText(hwnd) if ord(char) <= 126)


def move_window(hwnd, loc, size):
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


def get_foreground_window():
    """Returns the currently focused window's hwnd.
    """
    return wg.GetForegroundWindow()


def add_titlebar(hwnd):
    """Sets the window style to include a titlebar if it doesn't have one.
    """
    style = wg.GetWindowLong(hwnd, wc.GWL_STYLE)
    style -= wc.WS_CAPTION
    wg.SetWindowLong(hwnd, wc.GWL_STYLE, style)


def remove_titlebar(hwnd):
    """Sets window style to caption (no titlebar).
    """
    style = wg.GetWindowLong(hwnd, wc.GWL_STYLE)
    style += wc.WS_CAPTION
    wg.SetWindowLong(hwnd, wc.GWL_STYLE, style)

def get_window_rect(hwnd):
    """Returns the windows dimensions in the form (x, y, w, h).
    """
    return wg.GetWindowRect(hwnd)