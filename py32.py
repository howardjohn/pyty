import win32gui as wg
import win32api as wa


def getScreenResolution():
    return wa.GetSystemMetrics(0), wa.GetSystemMetrics(1)


def blacklist(hwnd):
    '''Returns if a hwnd is one of the windows 10 hidden windows.
       Currently uses window title, but this is not ideal'''
    black = ("Windows Shell Experience Host", "Program Manager")
    # hwndTry = GetAncestor(hwnd, GA_ROOTOWNER);
    # while(hwndTry != hwndWalk) 
    # {
    #     hwndWalk = hwndTry;
    #     hwndTry = GetLastActivePopup(hwndWalk);
    #     if(IsWindowVisible(hwndTry)) 
    #         break;
    # }
    # if(hwndWalk != hwnd)

    hwndWalk = None
    hwndTry = wg.GetWindow(hwnd, 3)
    print(hwnd, hwndTry)
    while hwndTry != hwndWalk:
        hwndWalk = hwndTry
        # hwndTry = 
    print(wg.GetLastActivePopup(hwnd))
    return wg.GetWindowText(hwnd) in black

def getAllWindows():
    def call(hwnd, param):
        if wg.IsWindowVisible(hwnd) and len(wg.GetWindowText(hwnd)) > 0 and \
           not wg.GetParent(hwnd): # and not blacklist(hwnd)
            print(blacklist(hwnd))
            # print(hwnd, wg.GetWindowText(hwnd), "a")
            # print(wg.GetWindowPlacement(hwnd))
            param.append(hwnd)

    winds = []
    wg.EnumWindows(call, winds)
    return winds

def moveWindow(hwnd, loc, size, gap=0):
    wg.MoveWindow(hwnd, loc[0]-8, loc[1], size[0]+16, size[1]+8, True)

if __name__ == "__main__":
    for a in getAllWindows():
        print(wg.GetWindowPlacement(a), wg.GetWindowText(a)[:40])
