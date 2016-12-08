"""Manages hotkeys."""
from global_hotkeys import GlobalHotkeys as ghk
from data import Dir
import subprocess
import time


def terminal(wm):
    subprocess.run("C:\\cygwin64\\bin\\mintty.exe")
    time.sleep(.2)
    wm.insert()


class HookManager():
    """
    Defines and registers all hotkeys.

    Attributes:
        win_manager (WindowManager): The window manager.
    """

    def __init__(self, win_manager):
        """
        Initializes the hook manager given a WindowManager

        Args:
            win_manager (WindowManager): Description
        """
        self.win_manager = win_manager

        MOD = ghk.MOD_WIN | ghk.MOD_SHIFT
        ALTMOD = MOD | ghk.MOD_ALT

        # TODO error when using VK_UP/DOWN? why?
        ghk.register(ghk.VK_PRIOR, MOD, win_manager.change_focus, dir=Dir.up)
        ghk.register(ghk.VK_NEXT, MOD, win_manager.change_focus, dir=Dir.down)
        ghk.register(ghk.VK_PRIOR, ALTMOD, win_manager.move_window, dir=Dir.up)
        ghk.register(ghk.VK_NEXT, ALTMOD, win_manager.move_window, dir=Dir.down)

        ghk.register(ghk.VK_G, MOD, win_manager.change_gaps, delta=2)
        ghk.register(ghk.VK_G, ALTMOD, win_manager.change_gaps, delta=-2)

        ghk.register(ghk.VK_R, MOD, win_manager.change_ratio, delta=.1)
        ghk.register(ghk.VK_R, ALTMOD, win_manager.change_ratio, delta=-.1)

        ghk.register(ghk.VK_F, MOD, win_manager.set_insertion)
        ghk.register(ghk.VK_S, MOD, win_manager.change_split)

        ghk.register(ghk.VK_M, ALTMOD, win_manager.bring_to_top)

        ghk.register(ghk.VK_RETURN, ALTMOD, terminal, wm=win_manager)

        ghk.register(ghk.VK_E, MOD, win_manager.exit)

        ghk.register(ghk.VK_OEM_PLUS, MOD, win_manager.insert)
        ghk.register(ghk.VK_OEM_PLUS, ALTMOD, win_manager.insert_all)
        ghk.register(ghk.VK_OEM_MINUS, MOD, win_manager.remove)
        ghk.register(ghk.VK_OEM_MINUS, ALTMOD, win_manager.remove_all)

        ghk.listen()
