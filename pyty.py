"""Initializes the pyty"""
from window_manager import WindowManager
from hook_manager import HookManager

if __name__ == "__main__":
    WINDOW_MANAGER = WindowManager()
    HOOK_MANAGER = HookManager(WINDOW_MANAGER)
