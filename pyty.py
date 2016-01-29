import win32gui as wg
import win32api as wa
import py32
from node import Node

w, h = py32.getScreenResolution()

winds = py32.getAllWindows()

desktop = Node()
main = Node(desktop)
for wind in winds:
    pass 