from node import Node

class Desktop:

    def __init__(self, w, h, hwnds):
        self.root = Node(hwnd=hwnds[0], w=w, h=h)
        Node(hwnds[1], self.root)
        n = Node(hwnds[2], self.root)
        Node(hwnds[3], n)
        Node(hwnds[4], n)
        self.root.updateAll()


