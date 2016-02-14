import py32
from desktop import Desktop

w, h = py32.getScreenResolution()

winds = py32.getAllWindows()
print(len(winds), [py32.getText(win) for win in winds])


desk = Desktop(w, h, winds)

# main = Node(hwnd=winds[0], w=w, h=h)
# # main = Node(winds[0], main)
# for wind in winds[1:]:
#     main.addChild(Node(wind, main))

# main.updateAll()
# # print(main.w, main.x, main.h, main.y, main.split)
# # print(main.children[0].x, main.children[0].y)
# # print(main.children[1].x, main.children[1].y)


def updateLocation(node):
    py32.restore(node.hwnd)
    py32.moveWindow(node.hwnd, node.getWindowLoc(10), node.getWindowDims(10))
    for child in node.children:
        updateLocation(child)

updateLocation(desk.roots[0])
