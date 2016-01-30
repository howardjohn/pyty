import win32gui as wg
import win32api as wa
import py32
from node import Node

w, h = py32.getScreenResolution()

winds = py32.getAllWindows()
# print(len(winds), [py32.getText(win) for win in winds])

main = Node(hwnd=winds[0], w=w, h=h)
# main = Node(winds[0], main)
for wind in winds[1:]:
    Node(wind, main)

node = main
print(node.w, node.h)
print(node.children[0].w, node.children[0].h)