#https://wiki.python.org/moin/AppsWithPythonScripting
#~ http://msdn.microsoft.com/en-us/library/ms927178.aspx
#http://www.kbdedit.com/manual/low_level_vk_list.html
#http://stackoverflow.com/questions/14076207/simulating-a-key-press-event-in-python-2-7	#TBD WINDOWS KEY UP /DOWN ?
import os
import _thread as thread 										
import queue
import time 
from pprint import pprint

from timstools import unique_int
	
KEYBINDS = {}
CALLBACKS = {}	
	
if os.name == 'nt':
	import ctypes
	from ctypes import wintypes
	import win32con
	byref = ctypes.byref
	user32 = ctypes.windll.user32
	PM_REMOVE = 0x0001

	vk_codes= {	
		'F1':win32con.VK_F1,
		'F2':win32con.VK_F2,
		'F3':win32con.VK_F3,
		'F4':win32con.VK_F4,
		'F5':win32con.VK_F5,
		'F6':win32con.VK_F6,
		'F7':win32con.VK_F7,
		'F8':win32con.VK_F8,
		'F9':win32con.VK_F9,
		'F10':win32con.VK_F10,
		'F11':win32con.VK_F11,
		'F12':win32con.VK_F12,
		'a':0x41,
		'b':0x42,
		'c':0x43,
		'd':0x44,
		'e':0x45,
		'f':0x46,
		'g':0x47,
		'h':0x48,
		'i':0x49,
		'j':0x4A,
		'k':0x4B,
		'l':0x4C,
		'm':0x4D,
		'n':0x4E,
		'o':0x5F,
		'p':0x50,
		'q':0x51,
		'r':0x52,
		's':0x53,
		't':0x54,
		'u':0x55,
		'v':0x56,
		'w':0x57,
		'x':0x58,
		'y':0x59,
		'z':0x5A,
		'0':0x30,
		'1':0x31,
		'2':0x32,
		'3':0x33,
		'4':0x34,
		'5':0x35,
		'6':0x36,
		'7':0x37,
		'8':0x38,
		'9':0x39
		}	
	win_modders = {
		'control':2,
		'shift':4,
		'alt': 1,
		'win':8,
		}
		
else:
	try:
		from . import xpybutil_keybind as keybind
	except SystemError:
		import xpybutil_keybind as keybind
	
	try:
		import xcffib			# the xproto con will not work unlesss you inport this first
		from xcffib import xproto
		from xpybutil import keybind
		
		xcb_modifiers  = {
			'control' : xproto.ModMask.Control,
			'shift' : xproto.ModMask.Shift,
			'alt' : xproto.ModMask._1,
			'win' : xproto.ModMask._4	
			}
		xcb_trivial_mods = (	# TBD woring for caps loc and scroll loc but not numloc
			0,
			xproto.ModMask.Lock,
			xproto.ModMask._2,
			xproto.ModMask.Lock | xproto.ModMask._2)
	except ImportError:
		pass
	try:
		from Xlib import X
		from Xlib import XK 
		from Xlib.display import Display
		special_X_keysyms = {			# these couldn't be gotten from the xlib keycode function
			' ' : "space",
			'\t' : "Tab",
			'\n' : "Return",  			# for some reason this needs to be cr, not lf
			'\r' : "Return",
			'\e' : "Escape",
			'!' : "exclam",
			'#' : "numbersign",
			'%' : "percent",
			'$' : "dollar",
			'&' : "ampersand",
			'"' : "quotedbl",
			'\'' : "apostrophe",
			'(' : "parenleft",
			')' : "parenright",
			'*' : "asterisk",
			'=' : "equal",
			'+' : "plus",
			',' : "comma",
			'-' : "minus",
			'.' : "period",
			'/' : "slash",
			':' : "colon",
			';' : "semicolon",
			'<' : "less",
			'>' : "greater",
			'?' : "question",
			'@' : "at",
			'[' : "bracketleft",
			']' : "bracketright",
			'\\' : "backslash",
			'^' : "asciicircum",
			'_' : "underscore",
			'`' : "grave",
			'{' : "braceleft",
			'|' : "bar",
			'}' : "braceright",
			'~' : "asciitilde"
			}
		
		xlib_modifiers = {
			'control' : X.ControlMask,
			'shift' :  X.ShiftMask,
			'alt' : X.Mod1Mask,
			'win' : X.Mod4Mask
			}
		
		xlib_trivial_mods = (	# not working at all !
			0,
			X.LockMask,
			X.Mod2Mask,
			X.LockMask | X.Mod2Mask)
	except ImportError:
		pass
		
class RegisterError(Exception):pass	
class UnregisterError(Exception):pass	

class MixIn():
	def register(self, hotkey, callback=None):
		'''
		Add a system wide hotkey,
		
		hotkey needs to be a tuple/list
		
		If the Systemhotkey class consumer attribute value is set to callback,
		callback will need to be a callable object that will be run
		
		Otherwise callback  is optionall and will be used as parameters
		to the consumer function
		
		Modifiers include
		control
		shift
		win
		alt
		'''
		assert type(hotkey) in (tuple, list)
		if self.consumer == 'callback' and not callback:
			raise TypeError('Function register requires callback argument in non sonsumer mode')
		hotkey = self.order_hotkey(hotkey)
		keycode, masks = self.parse_hotkeylist(hotkey)
		
		if os.name == 'nt':
			def nt_register():
				uniq = unique_int(self.hk_ref.keys())
				self.hk_ref[uniq] = ((keycode, masks))
				self._the_grab(keycode, masks, uniq)
			self.hk_action_queue.put(lambda:nt_register())
		else:
			self._the_grab(keycode, masks)
						
		KEYBINDS[tuple(hotkey)] = callback
	
		if self.verbose:
			print('Printing all keybinds')
			pprint(KEYBINDS)
			print()
		if os.name == 'posix' and self.use_xlib:
			self.disp.flush()
		
		#~ This code works but im not sure abot pywin  support for differentiation between keypress/keyrelease so..
		#~ on my laptoop on linux anyway keyrelease fires even if key is still down...

		#~ assert event_type in ('keypress', 'keyrelease', 'both')
		#~ 
		#~ copy = list(hotkey)
		#~ if event_type != 'both':	
			#~ copy.append(event_type)
			#~ KEYBINDS[tuple(copy)].append(callback)
		#~ else:	# Binding to both keypress and keyrelease
			#~ copy.append('keypress')
			#~ KEYBINDS[tuple(copy)].append(callback)
			#~ copy[-1] = 'keyrelease'
			#~ KEYBINDS[tuple(copy)].append(callback)
		
	def unregister(self, hotkey):
		'''
		Remove the System wide hotkey,
		the order of the modifier keys is irrelevant
		'''
		keycode, masks = self.parse_hotkeylist(hotkey)
		if os.name == 'nt':
			def nt_unregister(hk_to_remove):
				for key, value in self.hk_ref.items():
					if value == hk_to_remove:	
						del self.hk_ref[key]								
						user32.UnregisterHotKey(None, key)
						#~ logging.debug('Checking Error from unregister hotkey %s' % (win32api.GetLastError()))
						return hk_to_remove		
			self.hk_action_queue.put(lambda: nt_unregister((keycode,masks)))
		elif os.name == 'posix':
			if self.use_xlib:
				for mod in self.trivial_mods:
					self.xRoot.ungrab_key(keycode, masks | mod)
			else:
				try:
					for mod in self.trivial_mods:
						self.conn.core.UngrabKeyChecked(keycode, self.root, masks | mod).check()
				except xproto.BadAccess:
					raise SysHotkeyUnregisterError("Failed unregs")
	
	def order_hotkey(self, hotkey):
		# Order doesn't matter for modifiers, so we force an order here
		# control - shift - alt - win, and when we read back the modifers we spit them
		# out in the same value so our dictionary keys always match
		if len(hotkey) > 2:
			new_hotkey = []
			for mod in hotkey[:-1]:
				if 'control' == mod:
					new_hotkey.append(mod)
			for mod in hotkey[:-1]:
				if 'shift' == mod:
					new_hotkey.append(mod)
			for mod in hotkey[:-1]:
				if 'alt' == mod:
					new_hotkey.append(mod)
			for mod in hotkey[:-1]:
				if 'win' == mod:
					new_hotkey.append(mod)
			new_hotkey.append(hotkey[-1])
			hotkey = new_hotkey
		return hotkey
		
	def parse_hotkeylist(self, full_hotkey):
		# Returns keycodes and masks from a list of hotkey masks
		masks = []
		keycode = self.get_keycode(full_hotkey[-1])
		if len(full_hotkey) > 1:
			for item in full_hotkey[:-1]:
				try:
					masks.append(self.modders[item])
				except KeyError:
					raise RegisterError('Modifier: %s not supported' % item)	#TBD rmeove how the keyerror gets displayed as well
			masks = self.or_modifiers_together(masks)
		else:								
			masks = 0
		return keycode, masks	
		
	def or_modifiers_together(self, modifiers):
		# Binary or the modifiers together
		result = 0
		for part in modifiers:
			result |= part
		return result
		
	def get_callback(self, hotkey):
		if self.verbose:
			print('Keybinds , key here -> ', tuple(hotkey))
			pprint(KEYBINDS)
		yield KEYBINDS[tuple(hotkey)]
	
	#~ this was for the event_type callback
	#~ def get_callback(self, hotkey ,event_type):
		#~ copy = list(hotkey)
		#~ copy.append(event_type)
		#~ if self.verbose:
			#~ print('Keybinds , key here -> ', tuple(copy))
			#~ pprint(KEYBINDS)
		#~ for func in KEYBINDS[tuple(copy)]:
			#~ yield func	
	
	def parse_event(self, event):
		#Turns an event back into a hotkeylist
		hotkey = []
		if os.name == 'posix':
			hotkey += self.get_modifiersym(event.state)	
			hotkey.append(self._get_keysym(event.detail))
		else:
			keycode, modifiers = self.hk_ref[event.wParam][0], self.hk_ref[event.wParam][1]
			hotkey += self.get_modifiersym(modifiers)
			hotkey.append(self._get_keysym(keycode))
		if self.verbose:
			print('hotkey ', hotkey)
		return hotkey
	
	def get_modifiersym(self, state):
		ret = []
		if state & self.modders['control']:
			ret.append('control')
		if state & self.modders['shift']:
			ret.append('shift')
		if state & self.modders['alt']:
			ret.append('alt')
		if state & self.modders['win']:
			ret.append('win')
		return ret
	
class SystemHotkey(MixIn):
	'''
	Cross platform System Wide Hotkeys
	'''	
	hk_ref = {}	# used for windows
	def __init__(self, consumer='callback', conn=None, use_xlib=True, verbose=False):
		'''
		consumer defaults to 'callback',...All calls to register will require a callback function
		Other wise you can pass a fuction into consumer that can hanldle the event.
		I wouldn't use this it's still being developed!
		
		set use_xlib to true to use the xlib python bindings (GPL) instead of the xcb ones (BSD) 
		
		I have never programed in xwindows so im not sure if there are restrictions on the connection to the
		display window, You can pass an exisiting display or connection using the conn keyword
		'''
		# Changes the class methods to point to differenct functions 
		# Depening on the operating system and library used
		# Consumer defaults to callback which associate a unique function to each hotkey
		# Consumer can be set to a function also, which will be sent the event
		# as well as the key and mask already broken out
		# Last option for consumer is False, then you have to listen to the queue yourself
		# data_queue
		# Also modifer oder doesn't matter, e.g contrl shift is the same as shift control
		# actually a consequence of the keybaord and operating systems not this library
		self.verbose = verbose
		self.use_xlib = use_xlib
		self.consumer = consumer
		def mark_event_type(event):
			if os.name == 'posix':
				if self.use_xlib:
					if event.type == X.KeyPress:
						event.event_type = 'keypress'
					elif event.type == X.KeyRelease:
						event.event_type = 'keyrelease'
				else:
					if isinstance(event, xproto.KeyPressEvent):
						event.event_type = 'keypress'
					if isinstance(event, xproto.KeyReleaseEvent):
						event.event_type = 'keyrelease'
			else:	#windows, 
				event.event_type = 'keypress'
			return event
			
		self.data_queue = queue.Queue()
		if os.name == 'nt':
			self.hk_action_queue = queue.Queue()
			self.modders = win_modders
			self._the_grab = self._nt_the_grab
			self.get_keycode = self._nt_get_keycode			
			self._get_keysym = self._nt_get_keysym
			
			thread.start_new_thread(self._nt_wait,(),)
			
		elif use_xlib:												# Use the python-xlib library bindings, GPL License
			self.modders = xlib_modifiers
			self.trivial_mods = xlib_trivial_mods
			self._the_grab = self._xlib_the_grab
			self.get_keycode = self._xlib_get_keycode
			self._get_keysym = self._xlib_get_keysym
			if not conn:
				self.disp = Display()
			else:
				self.disp = conn
			self.xRoot = self.disp.screen().root
			self.xRoot.change_attributes(event_mask=X.KeyPressMask)
			
			thread.start_new_thread(self._xlib_wait,(),)
		
		else:												# Using xcb and the xcffib python bindings Apache 2 http://stackoverflow.com/questions/40100/apache-license-vs-bsd-vs-mit
			self.modders = xcb_modifiers	#tbd use the xcb modders
			self.trivial_mods = xcb_trivial_mods
			self._the_grab = self._xcb_the_grab
			self.get_keycode = self._xcb_get_keycode
			self._get_keysym = self._xcb_get_keysym
			if not conn:
				self.conn = xcffib.connect()
			else:
				self.conn = conn
			self.root = self.conn.get_setup().roots[0].root
			
			thread.start_new_thread(self._xcb_wait,(),)
		
		if consumer == 'callback':
			if self.verbose:
				print('In Callback')
			def thread_me():
				while 1:
					time.sleep(.01)
					try:
						event = self.data_queue.get(block=False)
					except queue.Empty:
						pass	
					else:
						event = mark_event_type(event) 
						hotkey = self.parse_event(event)
						#~ for cb in self.get_callback(hotkey, event.event_type):	#when i was using the keypress / keyrelease shit
						for cb in self.get_callback(hotkey):
							if event.event_type == 'keypress':
								if self.verbose:
									print('calling ', repr(cb))
								cb(event)
			thread.start_new_thread(thread_me,(),)
			
		elif callable(consumer):
			# event gets an event_type attribute so the user has a portiabble way
			# actually on windows as far as i know you dont have the option of binding on keypress or release so... 
			# anyway ahve to check it but for now u dont!
			def thread_me():
				while 1:
					time.sleep(.01)
					try:
						event = self.data_queue.get(block=False)
					except queue.Empty:
						pass	
					else:
						hotkey = self.parse_event(mark_event_type(event))
						if event.event_type == 'keypress':
							callbacks = [cb for cb in self.get_callback(hotkey)]
							#~ callbacks = [cb for cb in self.get_callback(hotkey, event.event_type)]
							consumer(event, hotkey, callbacks)	# tbd build up hotkey completly
			thread.start_new_thread(thread_me,(),)
		else:
			print('You need to handle grabbing events yourself!')
			
	def _xlib_wait(self):
		# Pushes Event onto queue
		while 1:
			event = self.xRoot.display.next_event()		
			self.data_queue.put(event)
	
	def _xcb_wait(self):
		# Pushes Event onto queue
		while 1:
			event = self.conn.wait_for_event()
			self.data_queue.put(event)
	
	def _nt_wait(self):
		# Pushes Event onto queue
		# I don't understand the windows msg system
		# I can only get hotkeys to work if they are registeed in the 
		# Thread that is listening for them.
		# So any changes to the hotkeys have to be signaled to be done
		# By the thread. (including unregistering)
		# A new queue is checked and runs functions, either adding
		# or removing new hotkeys, then the windows msg queue is checked
		msg = ctypes.wintypes.MSG ()
		while 1:
			try:											
				remove_or_add = self.hk_action_queue.get(block=False)
			except queue.Empty:
				pass	
			else:
				remove_or_add()	
			if user32.PeekMessageA(byref(msg), 0, 0, 0, PM_REMOVE):		# Checking the windows message Queue
				if msg.message == win32con.WM_HOTKEY:			
					self.data_queue.put(msg)						# This will open up a workbook page
				else:
					print('some other message')
			time.sleep(.01)

	def _nt_get_keycode(self, key, disp=None):	
		return vk_codes[key]
	
	def _nt_get_keysym(self, keycode):
		for key, value in vk_codes.items():
			if value == keycode:
				return key
	
	def _nt_the_grab(self, keycode, masks, id, root=None):
		if not user32.RegisterHotKey(None, id, masks, keycode):
			raise RegisterError('The bind is probably already in use elsewhere on the system')	#TBD RAISE RROR ON LINUX SYSTEMS
			
	def _xlib_get_keycode(self, key) :
		keysym = XK.string_to_keysym(key)
		if keysym == 0:
			keysym = XK.string_to_keysym(special_X_keysyms[key])
		keycode = self.disp.keysym_to_keycode(keysym)
		return keycode
	
	def _xlib_get_keysym(self, keycode, i=0):
		return chr(self.disp.keycode_to_keysym(keycode, i))
		
	def _xlib_the_grab(self, keycode, masks):
		#TBD error handlig  http://tronche.com/gui/x/xlib/event-handling/protocol-errors/default-handlers.html
		#~ try:
		self.xRoot.grab_key(keycode, masks, 1, X.GrabModeAsync, X.GrabModeAsync)
		#~ except Xlib.error.BadAccess:
			#~ raise RegisterError('The bind is probably already in use elsewhere on the system')

	def _xcb_the_grab(self, keycode, masks):
		try:
			for triv_mod in self.trivial_mods:
				self.conn.core.GrabKeyChecked(True, self.root, triv_mod | masks, keycode, xproto.GrabMode.Async, xproto.GrabMode.Async).check()
		except xproto.AccessError:
			raise UnregisterError('The bind is probably already in use elsewhere on the system')
			 
	def _xcb_get_keycode(self, key):
		return keybind.lookup_string(key)
	
	def _xcb_get_keysym(self, keycode, i=0):
		return chr(keybind.get_keysym(keycode, i))

if __name__ == '__main__':
	hk = SystemHotkey(use_xlib=False, verbose=1)	# xcb
	hk.register(('k',), callback=lambda e: print('i am k'))
	
	hk.register(['control', 'k'], callback=lambda e: print('i am control k'))
	hk.register(('control','shift', 'k'), callback=lambda e: print('i am control shift k'))
	hk.register(('control','win', 'k'), callback=lambda e: print('i am control win k'))
	hk.register(['control','alt', 'k'], callback=lambda e: print('i am control alt k'))
	hk.register(['control','shift','win','alt', 'k'], callback=lambda e: print('i am control alt shift win k'))

	#~ hk.unregister(['k'])
	#~ hk.unregister(('control','shift', 'k'))

	#~ hk.register(['k'], callback=lambda e: print('i am k2'))
	#~ hk.register(('control','shift', 'k'), callback=lambda e: print('i am con shift k2'))
	while 1:
		pass
