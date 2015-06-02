system hotkeys
==============

'Multiplatform system wide hotkeys'

Atm support x11 and windows.

Installation

For windows you will need to pywin32

For x11 you will need either the xlib library and python bindings or the xcffib library which is a drop in replacement for the xcb pthon bindings. Xcb is bsd where as the python xlib bindings are gpl

Usage:

from system_hotkey import SystemHotkeys

hk = SystemHotkeys()
hk.register(('control', 'shift', 'h'), callback=lambda:print("Easy hotkeys 123!!!"))
hk.unregister(('control', 'shift', 'h'))
