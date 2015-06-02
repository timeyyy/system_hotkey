System Hotkeys
==============

'Multiplatform system wide hotkeys'

Atm support x11 and windows. Osx support is coming in a few years i would say!

Installation
____________

For windows you will need to install pywin32

For x11 you will should probably use the xcffib library, you will need the xcb bindings (bsd license) installed to use it (i think???)
Also supported is the python xlib bindings (gpl license)

then do the old pip3 install system_hotkeys

Usage:
______

from system_hotkey import SystemHotkeys

hk = SystemHotkeys()
hk.register(('control', 'shift', 'h'), callback=lambda:print("Easy hotkeys 123!!!"))
hk.unregister(('control', 'shift', 'h'))

To not use the callback sytem you can do something like this

def some_func(self, event, hotkey, args):	
				self.do_something(hotkey)	
			
hk = SystemHotkeys(consumer=some_func)
