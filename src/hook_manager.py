"""Manages hotkeys"""
import sys
import pyhk


class HookManager():
    """Registers hotkeys and calls WindowManager functions when pressed.

    Attributes:
        hot: Stores and starts monitoring hotkeys
        win_manager: The window manager
    """

    def __init__(self, win_manager):
        """Initializes the hook manager given a WindowManager

        Args:
            win_manager (TYPE): Description
        """
        self.win_manager = win_manager
        # create pyhk class instance
        self.hot = pyhk.pyhk()

        # add hotkey
        self.hot.addHotkey(['Win', 'Shift', 'Alt', 'G'],
                           win_manager.decrease_gaps)
        self.hot.addHotkey(['Win', 'Shift', 'G'],
                           win_manager.increase_gaps)
        self.hot.addHotkey(['Win', 'Shift', 'mouse wheel up'],
                           win_manager.increase_gaps)
        self.hot.addHotkey(['Win', 'Shift', 'mouse wheel down'],
                           win_manager.decrease_gaps)

        self.hot.addHotkey(['Win', 'Shift', 'S'], win_manager.swap_split)
        self.hot.addHotkey(['Win', 'Shift', 'E'], sys.exit)

        # start looking for hotkey.
        self.hot.start()
