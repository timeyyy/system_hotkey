import os
import time

import system_hotkey
hk = system_hotkey.SystemHotkey()

CALLBACK_RESULT = []

def append_callback(key):
	print('APPENDING ',key)
	CALLBACK_RESULT.append(key)
	
if os.name == 'nt':
	from win32api import keybd_event
	def send_event(key):	# note if we change the time on checking our queue this sleep time will have to be changed
		time.sleep(0.03)					
		keybd_event(int(hk.get_keycode(key)) , 0, 1, 0)
		time.sleep(0.03)


keys_to_test = [('k',),
				('control','k'),
				('control','shift','k'),
				('control','shift','alt','k'),
				('control','shift','alt','win', 'k')]

def test_register_args():
	'''If in callback mode the register function requires a callback for all hotkeys regiersted,
	an error needs to be raised'''
	_hk = system_hotkey.SystemHotkey()
	try:
		_hk.register((keys_to_test[0]),)
	except TypeError:
		pass
	else:
		assert("hk register with no callback worked when it shouldn't have")
		
def test_register_1():
	'''
	Registers a hotkey without any modifiers, tests that the callback
	was run
	'''
	hk.register(keys_to_test[0], callback=lambda e: append_callback(keys_to_test[0]))	# THIS IS THREADED SO TBD DOCUMENT just need to wait a bit before sending the first key or after pressing a key getting the result
	send_event(keys_to_test[0][0])
	assert CALLBACK_RESULT[0] == keys_to_test[0]


def register_2():
	'''testing with one modifier'''
	hk.register(keys_to_test[1], lambda msg: CALLBACK_RESULT[0].append(keys_to_test[0]))
	send_event(keys_to_test[1])

#~ test_register_1()
#~ register_2()

