System Hotkey
=============

Multi platform system wide hotkeys for python 3, 

Currently no mac or  python2 support :(

Mac support is coming in a few years i would say!


Installation
------------

| the old 
| ``pip3 install system_hotkey``
| should do the trick

Windows
^^^^^^^
install pywin32

Linux
^^^^^
| For x11 you will can either use `xcffib <https://github.com/tych0/xcffib>`_  (bsd license), 
| or you may use the python xlib bindings (gpl license)



Usage
------


.. code-block:: python

	from system_hotkey import SystemHotkey
	hk = SystemHotkeys()
	hk.register(('control', 'shift', 'h'), callback=lambda:print("Easy!"))

**Input Charachters**

You can bind directly to symbols such as !@#$%^&*().
Numpad keys can be bind by prefixing with kp_.

Sysytem hotkeys uses the keysym names from xlib. You can
see system_hotkeys.py for a list of avaliable chars.
If you are unable to bind to a certain key please let us know.

To unregister a hotkey

.. code-block:: python

	hk.unregister(('control', 'shift', 'h'))


If you want you can pass in a custom consumer:

.. code-block:: python

	def some_func(self, event, hotkey, args):	
		pass	

	hk = SystemHotkeys(consumer=some_func)

So you have a master function that receives all hotkey presses and can delegate as desired.

Supported modifers include:

- control
- shift
- super (win key)
- alt
 
Features
--------
- Support for up to 3 modifyers and a key

Limitations
-----------
- I have only mapped most common keys, i have not experimented with unicode/japanese charchters etc. It's only a matter of mapping a name to the keysym on linux and virtual key code on windows.

- Default non-midifyable (no current need to change this) behavior is to ignore the state of the numlock and capslock key. i.e binding to kp_left (key pad left) will also bind to kp_4
