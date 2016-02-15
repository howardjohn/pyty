import pyhk
import sys

class HookManager():
    """Registers hotkeys and calls WindowManager functions when pressed.

    Attributes:
        hot: Stores and starts monitoring hotkeys
        wm: The window manager
    """

    def __init__(self, wm):
        """Initializes the hook manager given a WindowManager

        Args:
            wm (TYPE): Description
        """
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

    def exit():
        sys.exit(1)