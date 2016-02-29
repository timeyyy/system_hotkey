'''
Mainly for testing
'''

from system_hotkey.system_hotkey import SystemHotkey

hk = SystemHotkey(use_xlib=False)
hk.register(('control', 'a',), callback=lambda e:print('hi'))

while 1:
    pass
