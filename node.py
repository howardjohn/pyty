from enum import Enum


class Split(Enum):
    vert = 0
    horz = 1


class Node:
    # TODO: what about when there are two nodes with no parents?
    # Best solution is likely to have 'Root' class (or desktop? makes sense too)
    def __init__(self, hwnd, parent=None, w=None, h=None):
        self.parent = parent
        if self.parent is not None:
            self.parent.addChild(self)

        self.children = []
        self.hwnd = hwnd

        self.level = self.getLevel()
        self.split = Split((self.level) % 2)
        self.w = w
        self.h = h
        self.x = None
        self.y = None

    def addChild(self, child):
        self.children.append(child)

    def updateCoords(self):
        if self.parent is None:
            self.x = 0
            self.y = 0
        else:
            self.x, self.y = self.getCoords()

        for child in self.children:
            child.updateCoords()

    def getCoords(self):
        # move relative to parent
        if self.parent.split == Split.vert:
            x = self.parent.x + self.parent.w
            y = self.parent.y
        else:
            x = self.parent.x
            y = self.parent.y + self.parent.h

        # move relative to siblings
        if self.split == Split.vert:
            x += sum([c.w for c in self.parent.children[:self.parent.children.index(self)]])
        else:
            y += sum([c.h for c in self.parent.children[:self.parent.children.index(self)]])

        return x, y

    def updateDims(self):
        if self.parent is None:
            self.w, self.h = self.getDims(self.w, self.h, self.split)
        else:
            self.w, self.h = self.getDims(
                self.parent.w, self.parent.h, self.split)

        for child in self.children:
            child.updateDims()

    def getDims(self, w, h, split=Split.horz):
        n = 1
        if self.parent is not None:
            n += len(self.parent.children) - 1
        n *= 2 if self.children else 1
        if split == Split.horz:
            return (w, h // n)
        return (w // n, h)

    def updateAll(self):
        self.updateDims()
        self.updateCoords()

    def getLevel(self):
        level = 0
        node = self
        while node.parent:
            level += 1
            node = node.parent
        return level

    def __str__(self):
        return '*Node* level:{0}, childs:{1}'.format(self.level, len(self.children))
