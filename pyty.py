import win32gui as wg
import win32api as wa
import py32

w, h = py32.getScreenResolution()

winds = py32.getAllWindows()
print(len(winds))
1/0
n = 0
for wind in winds:
    if n == 0:
        py32.moveWindow(wind, (0,0), (1920//2, 1080//2), True)
    elif n == 1:
        py32.moveWindow(wind, (1920//2,0), (1920//2, 1080//2), True)
    elif n == 2:
        py32.moveWindow(wind, (0, 1080//2), (1920//2, 1080//2), True)
    elif n == 3:
        py32.moveWindow(wind, (1920//2, 1080//2), (1920//2, 1080//2), True)
    else:
        break
    n += 1
