import win32gui as wg
import win32api as wa
import win32process as wp
import win32con as wc
import ctypes
import ctypes.wintypes


def getScreenResolution():
    return wa.GetSystemMetrics(0), wa.GetSystemMetrics(1)


def get_app_name(hwnd):
    """Get applicatin filename given hwnd."""
    return wa.GetModuleFileNameW(hwnd)


def isRealWindow(hwnd):
    '''Returns if a hwnd is one of the windows 10 hidden windows.
    http://stackoverflow.com/a/7292674/238472 
    and https://github.com/Answeror/lit/blob/master/windows.py for details.'''

    class TITLEBARINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcTitleBar", ctypes.wintypes.RECT),
            ("rgstate", ctypes.wintypes.DWORD * 6)
        ]

    class WINDOWINFO(ctypes.Structure):
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
    # the following removes some task tray programs and "Program Manager"
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
    if pwi.dwStyle == 2496593920 or getText=='Netflix':
        return False

    if pwi.dwExStyle & wc.WS_EX_NOACTIVATE:
        return False

    if getText(hwnd) == "":
        print("WARNING: NO TEXT WINDOW: %s"%hwnd)
        return False

    return True


def getAllWindows():
    def call(hwnd, param):
        if isRealWindow(hwnd):
            param.append(hwnd)

    winds = []
    wg.EnumWindows(call, winds)
    return winds


def getText(hwnd):
    return ''.join(char for char in wg.GetWindowText(hwnd) if ord(char) <= 126)

def moveWindow(hwnd, loc, size, gap=0):
    wg.MoveWindow(hwnd, loc[0] - 8, loc[1], size[0] + 16, size[1] + 8, True)

def restore(hwnd):
    wg.ShowWindow(hwnd, wc.SW_RESTORE)

if __name__ == "__main__":
    for a in getAllWindows():
        pass
        # print(getText(a))
