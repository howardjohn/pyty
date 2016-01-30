from enum import Enum


class Split(Enum):
    vert = 0
    horz = 1


class Node:

    def __init__(self, hwnd, parent=None, w=None, h=None):
        self.parent = parent
        self.children = []
        self.hwnd = hwnd

        self.level = self.getLevel()
        self.split = Split(self.level % 2)
        self.w = w
        self.h = h

    def addChild(self, child):
        self.children.append(child)

    def updateDims(self):
        if self.parent is None:
            self.w, self.h = self.getDims(self.w, self.h, self.split)
        else:
            self.w, self.h = self.getDims(self.parent.w, self.parent.h, self.split)

        for child in self.children:
            child.updateDims()


    def getDims(self, w, h, split=Split.horz):
        n = 1
        if self.parent is not None:
            n += len(self.parent.children)-1
        n += 1 if self.children else 0
        if split == Split.horz:
            return (w, h // n)
        return (w // n, h)

    def getLevel(self):
        level = 0
        node = self
        while node.parent:
            level += 1
            node = node.parent
        return level

    def __str__(self):
        return '*Node* level:{0}, childs:{1}'.format(self.level, len(self.children))
