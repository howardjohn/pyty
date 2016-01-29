import win32gui as wg
import win32api as wa
import py32

w, h = py32.getScreenResolution()

winds = py32.getAllWindows()

n = 5
for wind in winds:
   if n == 0:
      wg.MoveWindow(wind, 0, 7, 963, 535, True)
      # wg.MoveWindow(wind, -2, 6, 955, 531, True)
      # wg.MoveWindow(wind, -2, 6, 955, 531, True)
   elif n == 1:
      wg.MoveWindow(wind, 0, 543, 963, 535, True)
   elif n == 2:
      wg.MoveWindow(wind, 954, 8, 963, 535, True)
   elif n == 3:
      wg.MoveWindow(wind, 954, 543, 963, 535, True)
   else:
      break
   n+=1
