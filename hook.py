import pythoncom, pyHook

def OnKeyboardEvent(event):
    print('Key:', event.Key)
    print('KeyID:', event.KeyID)
    print('Alt', event.Alt)
    print('Transition', event.Transition)

# return True to pass the event to other handlers
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyAll = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()