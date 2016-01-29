class Node:

    def __init__(self, parent=None):
        self.parent = parent
        if parent:
            parent.adopt(self)

        self.children = []
        self.siblings = []
        self.siblings = self.getSiblings()
        # print(self.siblings)

    def getSiblings(self):
        if self.parent == None:
            return []
        return [sibling for sibling in self.parent.children if sibling is not self] 

    def adopt(self, child):
        self.children.append(child)

    def __str__(self):
        return "Node: %s, %ss, %sc"%("a parent" if self.parent else "no parent",
                                     len(self.siblings), len(self.children))