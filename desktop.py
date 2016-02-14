from node import Node

class Desktop:

    def __init__(self, w, h, hwnds):
        # TODO: roots not root
        self.root = Node(hwnd=hwnds[0], w=w, h=h)
        for hwnd in hwnds[1:]:
            Node(hwnd, self.root)
        self.root.updateAll()


