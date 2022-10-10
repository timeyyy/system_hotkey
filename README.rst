System Hotkey
=============

Multi platform system wide hotkeys for python 3,

Currently no mac or  python2 support :(


Installation
------------

.. code-block:: bash

  pip install . --user

in the root folder

Windows
^^^^^^^
install pywin32

Linux
^^^^^
For x11 you should use `xcffib <https://github.com/tych0/xcffib>`_  (bsd license),

If for some reason you have to use the python xlib bindings (gpl license), a few fixes need be added first. See `here <https://github.com/timeyyy/system_hotkey/issues/6#issuecomment-265410255>`_


Usage
------

**Input Keysyms**

System hotkeys uses the keysym names from xlib for everything besides modifiers.(although case insensitive)
grep for vk_codes for a list of available chars.
If you are unable to bind to a certain key please let us know.

You can bind directly to symbols such as ["',. etc
Numpad keys can be binded by prefixing with kp\_.

Supported modifiers include:

- control
- shift
- super (windows key)
- alt

InvalidKeyError will be raised if a key was not understood

.. code-block:: python

    from system_hotkey import SystemHotkey
    hk = SystemHotkey()
    hk.register(('control', 'shift', 'h'), callback=lambda x: print("Easy!"))

A SystemRegisterError will be raised if a hotkey is already in use.

To unregister a hotkey

.. code-block:: python

    hk.unregister(('control', 'shift', 'h'))

A KeyError will be raised if the combination is not already grabbed.

A UnregisterError will be raised if unregistering failed for any other reason.

If you want you can pass in a custom consumer:

.. code-block:: python

    def some_func(self, event, hotkey, args):
        pass

    hk = SystemHotkey(consumer=some_func)
    hk.register(hotkey, arg1, arg2, arg3)

So you have a master function that receives all hotkey presses and can delegate as desired.

**Note**
Modifier keys are independent of order i.e control + alt + del  is the same as alt + control + del

Features
--------
- Support for up to 3 modifiers and a key

Limitations
-----------
- I have only mapped most common keys, i have not experimented with Unicode/Japanese characters etc. It's only a matter of mapping a name to the keysym on Linux and virtual key code on windows.

- binding to kp_left (key pad left) will also bind to kp_4, there is a flag (unite_kp) to toggle this behaviour but it is experimental

- Requires an xserver (x11)...
