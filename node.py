from enum import Enum


class Split(Enum):
    vert = 0
    horz = 1


class Node:

    def __init__(self, hwnd, parent=None, w=None, h=None):
        self.parent = parent
        if parent:
            parent.adopt(self)

        if not w:
            w = parent.w
        if not h:
            h = parent.h

        self.parentW = w
        self.parentH = h

        self.children = []
        self.siblings = self.getSiblings()
        self.hwnd = hwnd
        self.level = self.getLevel()
        self.split = Split.horz if self.level % 2 == 1 else Split.vert
        self.w, self.h = self.getDims(split=self.split)

    def getDims(self, w=None, h=None, split=Split.horz):
        if w is None:
            w = self.parentW
        if h is None:
            h = self.parentH

        n = 1
        n += len(self.siblings)
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

    def getSiblings(self):
        if self.parent is None:
            return []
        sibs = [sibling for sibling in self.parent.children if sibling is not self]
        for sib in sibs:
            if self not in sib.siblings:
                sib.siblings.append(self)
        return sibs

    def adopt(self, child):
        self.children.append(child)
        self.w, self.h = self.getDims(self.parentW, self.parentH, self.split)

    def __str__(self):
        return "Node: %s, %ss, %sc" % ("a parent" if self.parent else "no parent",
                                       len(self.siblings), len(self.children))
