#https://wiki.python.org/moin/AppsWithPythonScripting
#~ http://msdn.microsoft.com/en-us/library/ms927178.aspx
#http://www.kbdedit.com/manual/low_level_vk_list.html
import os
import _thread as thread 										
import queue
import time 
from collections import defaultdict
from pprint import pprint

from timstools import unique_int

KEYBINDS = defaultdict(list)
CALLBACKS = {}	
	
if os.name == 'nt':
	import ctypes
	from ctypes import wintypes
	import win32con
	byref = ctypes.byref
	user32 = ctypes.windll.user32
	PM_REMOVE = 0x0001

	vk_codes= {					# Windows Key Codes
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
	import xcffib
	from xcffib import xproto
	from xpybutil import keybind
	
	xcb_modifiers  = {
		'control' : xproto.ModMask.Control,
		'shift' : xproto.ModMask.Shift,	
		}
	xcb_trivial_mods = (	# woring for caps loc and scroll loc but not numloc
		0,
		xproto.ModMask.Lock,
		xproto.ModMask._2,
		xproto.ModMask.Lock | xproto.ModMask._2)
		
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
		}
		
	xlib_trivial_mods = (	# not working at all !
		0,
		X.LockMask,
		X.Mod2Mask,
		X.LockMask | X.Mod2Mask)

class SysHotkeyRegisterError(Exception):pass	

class MixIn():
	def register(self, hotkey, callback=None):
		'''Add a system wide hotkey,
		If the Systemhotkey class consumer attribute value is set to callback,
		a corresponding function will be called when the hotkey combination is pressed
		
		Otherwise...
		
		e.g register()
		'''
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
	
		if self.v:
			print('Printing all keybinds')
			pprint(KEYBINDS)
			print()
		if os.name == 'posix' and self.use_xlib:
			self.disp.flush()
		'''
		This code works but im pre sure windows doesn't support differentaion between keypress/keyrelease so delete this
		on my laptoop anyway keyrelease fires even if key is still down

		assert event_type in ('keypress', 'keyrelease', 'both')
		
		copy = list(hotkey)
		if event_type != 'both':	
			copy.append(event_type)
			KEYBINDS[tuple(copy)].append(callback)
		else:	# Binding to both keypress and keyrelease
			copy.append('keypress')
			KEYBINDS[tuple(copy)].append(callback)
			copy[-1] = 'keyrelease'
			KEYBINDS[tuple(copy)].append(callback)
		'''
		
	def unregister(self, hotkey):
		'''
		Remove the System wide hotkey
		'''
		if os.name == 'nt':
			def nt_unregister(hk_to_remove):
				for key, value in self.hk_ref.items():
					if value == hk_to_remove:	
						del self.hk_ref[key]								
						user32.UnregisterHotKey(None, key)
						#~ logging.debug('Checking Error from unregister hotkey %s' % (win32api.GetLastError()))
						return hk_to_remove		
			keycode, masks = self.parse_hotkeylist(hotkey)
			self.hk_action_queue.put(lambda: nt_unregister((keycode,masks)))
		elif os.name == 'posix':
			print('TBD unregisterhotkey')
	
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
		keycode = self._get_keycode(full_hotkey[-1])
		if len(full_hotkey) > 1:
			for item in full_hotkey[:-1]:
				try:
					masks.append(self.modders[item])
				except KeyError:
					raise SysHotkeyRegisterError('Modifier: %s not supported' % item)	#TBD rmeove how the keyerror gets displayed as well
			masks = self.or_modifiers_together(masks)
		else:								
			masks = 0
		return keycode, masks	
		
	def or_modifiers_together(self, modifiers):
		'''Binary or the modifiers together'''
		result = 0
		for part in modifiers:
			result |= part
		return result
		
	def get_callback(self, hotkey):
		if self.v:
			print('Keybinds , key here -> ', tuple(hotkey))
			pprint(KEYBINDS)
		yield KEYBINDS[tuple(hotkey)]
	'''
	this was for the event_type callback
	def get_callback(self, hotkey ,event_type):
		copy = list(hotkey)
		copy.append(event_type)
		if self.v:
			print('Keybinds , key here -> ', tuple(copy))
			pprint(KEYBINDS)
		for func in KEYBINDS[tuple(copy)]:
			yield func	
	'''
	
	def parse_event(self, event):
		#Turns an event back into a hotkeylist
		hotkey = []
		if os.name == 'posix':
			if self.use_xlib == 'xcb':
				hotkey += self.get_modifiersym(event.state)	#TBD
			elif self.use_xlib == 'xlib':
				hotkey += self.get_modifiersym(event.state)	#TBD
			hotkey.append(self._get_keysym(event.detail))
		else:
			keycode, modifiers = self.hk_ref[event.wParam][0], self.hk_ref[event.wParam][1]
			if self.v:
				print('win modifiers ', modifiers)
			hotkey += self.get_modifiersym(modifiers)
			hotkey.append(self._get_keysym(keycode))
		if self.v:
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
		return ret
	
class SystemHotkeys(MixIn):
	'''
	Cross platform System Wide Hotkeys
	'''	
	hk_ref = {}	# used for windows
	def __init__(self, consumer='callback', conn=None, use_xlib=True, v=False):
		'''
		consumer defaults to 'callback',...
		
		set use_xlib to true to use the xlib python bindings (GPL) instead of the xcb ones (BSD) 
		
		I have never programed in xwindows so im not sure if there are restrictions on the connection to the
		display window, You can pass an exisiting display or connection to the conn keyword
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
		self.v = v
		self.use_xlib = use_xlib
		def mark_event_type(event):
			if os.name == 'posix':
				if self.use_xlib == 'xlib':
					if event.type == X.KeyPress:
						event.event_type = 'keypress'
						hotkey = self._get_keysym(event.detail)
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
			self._get_keycode = self._nt_get_keycode			
			self._get_keysym = self._nt_get_keysym
			
			thread.start_new_thread(self._nt_wait,(),)
			
		elif use_xlib:												# Use the python-xlib library bindings, GPL License
			#~ self.the_grab = self._xlib_the_grab
			self.modders = xlib_modifiers
			self.trivial_mods = xlib_trivial_mods
			self._the_grab = self._xlib_the_grab
			self._get_keycode = self._xlib_get_keycode
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
			self._get_keycode = self._xcb_get_keycode
			self._get_keysym = self._xcb_get_keysym
			if not conn:
				self.conn = xcffib.connect()
			else:
				self.conn = conn
			self.root = self.conn.get_setup().roots[0].root
			
			thread.start_new_thread(self._xcb_wait,(),)
		
		if consumer == 'callback':
			if self.v:
				print('In Callback')
			def thread_me():
				while 1:
					time.sleep(.1)
					try:
						event = self.data_queue.get(block=False)
					except queue.Empty:
						pass	
					else:
						hotkey = self.parse_event(mark_event_type(event))
						#~ for cb in self.get_callback(hotkey, event.event_type):	#when i was using the keypress / keyrelease shit
						for cb in self.get_callback(hotkey):
							if event.event_type == 'keypress':
								if self.v:
									print('calling ', repr(cb))
								cb(event)
			thread.start_new_thread(thread_me,(),)
			
		elif callable(consumer):
			# event gets an event_type attribute so the user has a portiabble way
			# actually on windows as far as i know you dont have the option of binding on keypress or release so... 
			# anyway ahve to check it but for now u dont!
			def thread_me():
				while 1:
					time.sleep(.1)
					try:
						event = self.data_queue.get(block=False)
					except queue.Empty:
						pass	
					else:
						hotkey = self.parse_event(mark_event_type(event))
						callbacks = [cb for cb in self.get_callback(hotkey)]
						#~ callbacks = [cb for cb in self.get_callback(hotkey, event.event_type)]
						consumer(event, hotkey, callbacks)	# tbd build up hotkey completly
			thread.start_new_thread(thread_me,(),)
		else:
			print('You need to handle grabbing events yourself!')
		
	def bind_key(self):
		if os.name == 'nt':
			pass
			#~ self.hk.
		else:
			pass
			
	def free_key(self, *args):
		user32.UnregisterHotKey (None, id)
	
	def _xlib_wait(self):
		# Pushes Event onto queue
		while 1:
			event = self.xRoot.display.next_event()		#make error handlig  http://tronche.com/gui/x/xlib/event-handling/protocol-errors/default-handlers.html
			self.data_queue.put(event)
	
	def _xcb_wait(self):
		# Pushes Event onto queue
		while 1:
			event = self.conn.wait_for_event()
			#~ print('Putting on event data queue')
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
			time.sleep(.025)

	def _nt_get_keycode(self, key, disp=None):	
		return vk_codes[key]
	
	def _nt_get_keysym(self, keycode):
		for key, value in vk_codes.items():
			if value == keycode:
				return key
	
	def _nt_the_grab(self, keycode, masks, id, root=None):
		#~ print(keycode,masks,type(masks))
		if not user32.RegisterHotKey(None, id, masks, keycode):
			raise SysHotkeyRegisterError('The bind is probably already in use elsewhere on the system')	#TBD RAISE RROR ON LINUX SYSTEMS
			
	def _xlib_get_keycode(self, key) :
		keysym = XK.string_to_keysym(key)
		if keysym == 0:
			keysym = XK.string_to_keysym(special_X_keysyms[key])
		keycode = self.disp.keysym_to_keycode(keysym)
		return keycode
	
	def _xlib_get_keysym(self, keycode, i=0):
		return chr(self.disp.keycode_to_keysym(keycode, i))
		
	def _xlib_the_grab(self, keycode, masks):
		self.xRoot.grab_key(keycode, masks, 1, X.GrabModeAsync, X.GrabModeAsync)
		
	def _xcb_the_grab(self, keycode, masks):
		for triv_mod in self.trivial_mods:
			self.conn.core.GrabKeyChecked(True, self.root, triv_mod | masks, keycode, xproto.GrabMode.Async, xproto.GrabMode.Async).check()
	def _xcb_get_keycode(self, key):
		return keybind.lookup_string(key)
	
	def _xcb_get_keysym(self, keycode, i=0):
		return chr(keybind.get_keysym(keycode, i))
	
	def _xcb_get_modifiersym(self, state):	# THIS IS JUST FOR REFERNECE 
		"""
		Takes a ``state`` (typically found in key press or button press events)
		and returns a string list representation of the modifiers that were pressed
		when generating the event.

		:param state: Typically from ``some_event.state``.
		:return: List of modifier string representations.
		:rtype: [str]
		"""
		ret = []
		print('state passed in ', state)
		
		if state & xproto.ModMask.Shift:
			print('state and shift ',state & xproto.ModMask.Shift)
			ret.append('Shift_L')
		#~ if state & xproto.ModMask.Lock:
			#~ ret.append('Lock')
		if state & xproto.ModMask.Control:
			ret.append('Control_L')
		if state & xproto.ModMask._1:
			ret.append('Mod1')
		if state & xproto.ModMask._2:
			ret.append('Mod2')
		if state & xproto.ModMask._3:
			ret.append('Mod3')
		if state & xproto.ModMask._4:
			ret.append('Mod4')
		if state & xproto.ModMask._5:
			ret.append('Mod5')
		if state & xproto.KeyButMask.Button1:
			ret.append('Button1')
		if state & xproto.KeyButMask.Button2:
			ret.append('Button2')
		if state & xproto.KeyButMask.Button3:
			ret.append('Button3')
		if state & xproto.KeyButMask.Button4:
			ret.append('Button4')
		if state & xproto.KeyButMask.Button5:
			ret.append('Button5')
		return ret
if __name__ == '__main__':
	hk = SystemHotkeys(use_xlib=False, v=1)	# xcb
	hk.register(['control', 'k'], callback=lambda e: print('i am control k'))
	#~ hk.register(['Shift_L','Control_L', 'k'], callback=lambda e: print('i am control SHIFTt k'))
	#~ hk.register(['Shift_L', 'k'], callback=lambda e: print('i am shift k'))
	#~ hk.register(['g'], callback=lambda e: print('i am k'))
	#~ hk = SystemHotkeys(library='xlib')	# xcb
	#~ hk.register(['Control_L', 'k'], callback=lambda e: print('i am control k'))
	#~ hk.register(['Control_L','Shift_L', 'k'], callback=lambda e: print('i am control SHIFTt k'))
	#~ hk.register(['k'], callback=lambda e: print('i am k'))
	#~ hk = SystemHotkeys(v=0)	
	hk.register(('control','shift', 'k'), callback=lambda e: print('i am control shift k'))
	hk.register(('control','alt', 'k'), callback=lambda e: print('i am control alt k'))
	#~ hk.register(['Shift_L','Control_L', 'k'], callback=lambda e: print('i am control shift k'))
	#~ hk.register(['Control_L', 'k'], callback=lambda e: print('i am control k'))
	#~ hk.register(['k'], callback=lambda e: print('i am k'))
	#~ hk.unregister(('control','shift', 'k'))
	#~ hk.unregister(['k'])
	#~ hk.register(['k'], callback=lambda e: print('i am k'))
	while 1:
		pass
		#~ a = input()
		#~ b = hk._get_keycode(a)
		#~ c = hk._get_keysym(b)
		#~ print('keycode is ', b)
		#~ print('our sym ', c)
		#~ 
		#~ print('getting sym from keycodee')
		#~ 
		#~ for i in range(0,3):
			#~ print('i ', hk._get_keysym(b, i))
			
	'''
	ability to add more binds to a callback - CBF DONT NEED
	unbinding
	use masks in the key ? faster comparison etc, but user will have to call function to get human readable!
	add the windows key modifier
	'''
