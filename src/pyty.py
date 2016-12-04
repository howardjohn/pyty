"""Initializes the pyty"""
from window_manager import WindowManager
from hook_manager import HookManager
import traceback

if __name__ == "__main__":
    WINDOW_MANAGER = WindowManager()
    try:
        HOOK_MANAGER = HookManager(WINDOW_MANAGER)
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        WINDOW_MANAGER.exit()
