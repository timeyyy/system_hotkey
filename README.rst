

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

To unregister a hotkey

.. code-block:: python

	hk.unregister(('control', 'shift', 'h'))

There are api plans to allow something like the following:

.. code-block:: python

	def some_func(self, event, hotkey, args):	
		pass	

	hk = SystemHotkeys(consumer=some_func)

So you have a master function that receives all hotkey presses and can delegate as desired.

