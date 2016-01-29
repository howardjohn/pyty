import win32gui as wg
import win32api as wa

def getScreenResolution():
   return wa.GetSystemMetrics(0), wa.GetSystemMetrics(1)

def blacklist(hwnd):
   return wg.GetWindowPlacement(hwnd)[2] == (-1, -1)
   # return wg.GetWindowText(hwnd) in ("Windows Shell Experience Host", "Program Manager")

def getAllWindows():
   def call(hwnd, param):
       if wg.IsWindowVisible(hwnd) and len(wg.GetWindowText(hwnd)) > 0 and \
          not wg.GetParent(hwnd) and not blacklist(hwnd):
           print(hwnd, wg.GetWindowText(hwnd))
           param.append(hwnd)

   winds = []
   wg.EnumWindows(call, winds)
   return winds

if __name__ == "__main__":
   print(wg.GetWindowPlacement(131130)[2])
   print(wg.GetWindowPlacement(197700)[2])
   print(wg.GetDC(131130))