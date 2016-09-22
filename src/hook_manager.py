"""Manages hotkeys"""
from global_hotkeys import GlobalHotkeys as ghk


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

        MOD = ghk.MOD_WIN | ghk.MOD_SHIFT
        ALTMOD = MOD | ghk.MOD_ALT

        # Add hotkeys
        ghk.register(ghk.VK_G, MOD, win_manager.increase_gaps)
        ghk.register(ghk.VK_G, ALTMOD, win_manager.decrease_gaps)

        # TODO scroll hotkey?
        # ghk.register(ghk.VK_mouse wheel up, MOD, win_manager.increase_gaps)
        # ghk.register(ghk.VK_mouse wheel down, MOD, win_manager.decrease_gaps)

        ghk.register(ghk.VK_S, MOD, win_manager.swap_split)
        ghk.register(ghk.VK_E, MOD, win_manager.exit)

        # start looking for hotkey.
        ghk.listen()
