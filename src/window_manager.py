import window_api
from desktop import Desktop
import sys
from data import Dir


class WindowManager:

    def __init__(self, gap=6):
        width, height = window_api.get_screen_resolution()

        self.desktop = Desktop(width, height)
        self.gap = gap

    def change_gaps(self, delta):
        # Can't have negative gap
        self.gap = max(self.gap + delta, 0)
        self.update_windows()

    def change_ratio(self, delta):
        node = self.get_focused_node()

        # A positive delta would make the window smaller
        if node.is_second_child():
            delta = -delta

        if node.parent is not None:
            node.parent.ratio = WindowManager.clip(node.parent.ratio + delta)
            self.update_windows()

    def set_insertion(self):
        node = self.get_focused_node()

        if node is not None:
            self.desktop.insertion = node

    def change_focus(self, depth=0):
        node = self.get_focused_node()
        focus = WindowManager.get_next_node(node, depth)

        if focus is not None:
            window_api.focus_window(focus.window.hwnd)

    def swap_window(self, depth=0):
        node = self.get_focused_node()
        swap = WindowManager.get_next_node(node, depth)

        if node is not None and swap is not None:
            WindowManager.swap_node(swap, node)
            self.update_windows()

    def change_split(self):
        node = self.get_focused_node()

        if node is not None:
            self.swap_split_recurse(node.parent)

        self.update_windows()

    def swap_split_recurse(self, node):
        if node is not None:
            node.split = node.split.swap()
            self.swap_split_recurse(node.first)
            self.swap_split_recurse(node.second)

    def exit(self):
        self.teardown(self.desktop.root)
        sys.exit(0)

    def teardown(self, node):
        if node is None:
            return

        if node.window:
            node.window.teardown_window()

        self.teardown(node.first)
        self.teardown(node.second)

    def find_node(self, hwnd, node):
        if node is None:
            return None
        if node.window and node.window.hwnd == hwnd:
            return node
        return self.find_node(hwnd, node.first) or self.find_node(hwnd, node.second)

    def insert(self, hwnd=None):
        if hwnd is None:
            hwnd = window_api.get_foreground_window()

        # Window already inserted
        if self.find_node(hwnd, self.desktop.root) is not None:
            return

        self.desktop.insert(hwnd)

    def insert_all(self):
        for window in window_api.get_all_windows():
            self.insert(window)

    def remove(self, node=None):
        if node is None:
            node = self.get_focused_node()

        # No need to remove
        if node is None or not node.is_leaf_node():
            return

        if node.parent is None: # Only node
            self.desktop.root = None
            self.desktop.insertion = None
        else:
            old = node.parent
            new = node.get_sibling()
            new.parent = old.parent
            if old.parent is not None:
                if old.is_first_child():
                    old.parent.first = new
                else:
                    old.parent.second = new
            else:
                self.desktop.root = new
            new.rect = old.rect
            if self.desktop.insertion == node:
                self.desktop.insertion = WindowManager.find_first_leaf(new)
        node.window.teardown_window()
        self.update_windows()
        self.bring_to_top()

    def remove_all(self):
        WindowManager.recurse_nodes(self.desktop.root,
                                    self.remove,
                                    type="node")

    def get_focused_node(self):
        hwnd = window_api.get_foreground_window()
        return self.find_node(hwnd, self.desktop.root)

    def bring_to_top(self):
        old_focus = self.get_focused_node()
        WindowManager.recurse_nodes(self.desktop.root,
                                    window_api.focus_window,
                                    type="hwnd")
        if old_focus is not None:
            window_api.focus_window(old_focus.window.hwnd)

    def update_windows(self):
        self.desktop.update_all(self.desktop.root)

    def debug(self):
        print(self.desktop)
        print("Ins:", self.desktop.insertion)

    @staticmethod
    def recurse_nodes(node, func, type="node"):
        if node is not None:
            if type == "node":
                func(node)
            elif type == "window" and node.is_leaf_node():
                func(node.window)
            elif type == "hwnd" and node.is_leaf_node():
                func(node.window.hwnd)
            WindowManager.recurse_nodes(node.first, func, type=type)
            WindowManager.recurse_nodes(node.second, func, type=type)

    @staticmethod
    def clip(n, low=0, high=1):
        if n < low:
            return low
        elif n > high:
            return high
        return n

    @staticmethod
    def swap_node(a, b):
        a.window, b.window = b.window, a.window
 
    @staticmethod
    def get_next_node(node, depth):
        """
        Moves up `depth` parents, then finds first leaf node under that depth.
        depth=0 would be sibling, depth=1 is parent's sibling's first leaf node.
        """
        # If parent is none then it is the only window.
        if node is None or node.parent is None:
            return None

        next_node = WindowManager.traverse_up(node, depth)
        next_node = WindowManager.find_first_leaf(next_node)

        if next_node is not None and next_node.is_leaf_node():
            return next_node

    @staticmethod
    def traverse_up(node, depth):
        if depth <= 0:
            return node.get_sibling()
        if node.parent is None:
            return node
        return WindowManager.traverse_up(node.parent, depth - 1)

    @staticmethod
    def find_first_leaf(node):
        queue = [node]
        while queue:
            current = queue.pop(0)
            if current.is_leaf_node():
                return current
            queue.append(current.first)
            queue.append(current.second)
