import pyhk
import sys


class HookManager():

    def __init__(self, wm):
        self.wm = wm
        # create pyhk class instance
        self.hot = pyhk.pyhk()

        # add hotkey
        self.hot.addHotkey(['Win', 'Shift', 'Alt', 'G'], wm.decGaps)
        self.hot.addHotkey(['Win', 'Shift', 'G'], wm.incGaps)
        self.hot.addHotkey(['Win', 'Shift', 'mouse wheel up'], wm.incGaps)
        self.hot.addHotkey(['Win', 'Shift', 'mouse wheel down'], wm.decGaps)

        self.hot.addHotkey(['Win', 'Shift', 'S'], wm.swapSplit)
        self.hot.addHotkey(['Win', 'Shift', 'E'], self.exit)

        # start looking for hotkey.
        self.hot.start()

    def incGaps(self):
        print("Increase Gap")
        self.wm.gap += 2

    def decGaps(self):
        print("Decrease Gap")
        self.wm.gap -= 2

    def exit(self):
        sys.exit(0)
