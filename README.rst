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

**Input Keysyms**

System hotkeys uses the keysym names from xlib for everything besides modifiers.(although case insensitive)
grep for vk_codes for a list of avaliable chars.
If you are unable to bind to a certain key please let us know.

You can bind directly to symbols such as ["',. etc
Numpad keys can be binded by prefixing with kp_.

Supported modifers include:

- control
- shift
- super (win key)
- alt

A InvalidKeyError will be raised if a key was not understood

.. code-block:: python

	from system_hotkey import SystemHotkey
	hk = SystemHotkeys()
    hk.register(('control', 'shift', 'h'), callback=lambda:print("Easy!"))

A SystemRegisterError will be raised if a hotkey is already in use.

To unregister a hotkey

.. code-block:: python

	hk.unregister(('control', 'shift', 'h'))

A keyerror will be raised if the combination is not already grabbed.

A UnregisterError will be raised if unregistering failed for any other reason.

If you want you can pass in a custom consumer:

.. code-block:: python

	def some_func(self, event, hotkey, args):	
		pass	

	hk = SystemHotkeys(consumer=some_func)
    hk.register(hotkey, arg1, arg2, arg3)

So you have a master function that receives all hotkey presses and can delegate as desired.

**Note**
Modifyer keys are independant of order i.e control + alt + del  is the same as alt + control + del
 
Features
--------
- Support for up to 3 modifyers and a key

Limitations
-----------
- I have only mapped most common keys, i have not experimented with unicode/japanese charchters etc. It's only a matter of mapping a name to the keysym on linux and virtual key code on windows.

- binding to kp_left (key pad left) will also bind to kp_4, there is a flag (unite_kp) to toggle this behavior but it is experminetal
