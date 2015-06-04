

System Hotkeys
==============

Multiplatform system wide hotkeys for python 3, no python2 support

Atm support x11 and windows. Osx support is coming in a few years i would say!


Installation
------------

the old "pip3 install system_hotkeys" should do the trick


Windows
^^^^^^^
also install pywin32


Linux
^^^^^

| For x11 you will can either use `xcffib <https://github.com/tych0/xcffib>`_  (bsd license), 
| or you may use the python xlib bindings (gpl license)


Usage:
------

``from system_hotkey import SystemHotkeys``
``	hk = SystemHotkeys()``
``	hk.register(('control', 'shift', 'h'), callback=lambda:print("Easy hotkeys 123!!!"))``
``	hk.unregister(('control', 'shift', 'h'))``


To not use the callback sytem you can do something like this

``python
def some_func(self, event, hotkey, args):	
	pass	

hk = SystemHotkeys(consumer=some_func)
``

