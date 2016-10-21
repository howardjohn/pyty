import ctypes
import ctypes.wintypes
import win32con

# Created by
# http://makble.com/python-win32-programming-example-register-hotkey-and-switching-tab


class GlobalHotkeys():
    """
    Register a key using the register() method, or using the decorator
    Use listen() to start the message pump
    """

    key_mapping = []
    user32 = ctypes.windll.user32

    MOD_ALT = win32con.MOD_ALT
    MOD_CTRL = win32con.MOD_CONTROL
    MOD_CONTROL = win32con.MOD_CONTROL
    MOD_SHIFT = win32con.MOD_SHIFT
    MOD_WIN = win32con.MOD_WIN

    @classmethod
    def register(self, vk, modifier=0, func=None):
        """
        vk is a windows virtual key code
         - can use ord('X') for A-Z, and 0-1 (note uppercase letter only)
         - or win32con.VK_* constants
         - full list: http://msdn.microsoft.com/en-us/library/dd375731.aspx

        modifier is a win32con.MOD_* constant

        func is the function to run.
        """

        # Called as a decorator?
        if func is None:
            def register_decorator(f):
                self.register(vk, modifier, f)
                return f
            return register_decorator
        else:
            self.key_mapping.append((vk, modifier, func))

    @classmethod
    def listen(self):
        """
        Start the message pump
        """

        for index, (vk, modifiers, func) in enumerate(self.key_mapping):
            if not self.user32.RegisterHotKey(None, index, modifiers, vk):
                raise Exception('Unable to register hot key: ' + str(vk) +
                                ' error code is: ' +
                                str(ctypes.windll.kernel32.GetLastError()))

        try:
            msg = ctypes.wintypes.MSG()
            while self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                if msg.message == win32con.WM_HOTKEY:
                    (vk, modifiers, func) = self.key_mapping[msg.wParam]
                    if not func:
                        break
                    func()

                self.user32.TranslateMessage(ctypes.byref(msg))
                self.user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            for index, (vk, modifiers, func) in enumerate(self.key_mapping):
                self.user32.UnregisterHotKey(None, index)

    @classmethod
    def _include_defined_vks(self):
        for item in win32con.__dict__:
            item = str(item)
            if item[:3] == 'VK_':
                setattr(self, item, win32con.__dict__[item])

    @classmethod
    def _include_alpha_numeric_vks(self):
        for key_code in (list(range(ord('A'), ord('Z') + 1)) +
                         list(range(ord('0'), ord('9') + 1))):
            setattr(self, 'VK_' + chr(key_code), key_code)

    @classmethod
    def _include_custom_vks(self):
        setattr(self, 'VK_OEM_PLUS', 0xBB)
        setattr(self, 'VK_OEM_MINUS', 0xBD)

GlobalHotkeys._include_defined_vks()
GlobalHotkeys._include_alpha_numeric_vks()
GlobalHotkeys._include_custom_vks()
