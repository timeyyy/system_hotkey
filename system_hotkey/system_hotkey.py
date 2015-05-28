import os
import _thread as thread 										
import queue
import time 
from collections import defaultdict
from pprint import pprint

from timstools import unique_int

KEYBINDS = defaultdict(list)
CALLBACKS = defaultdict(list)	
	
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
		'Control_L':2,
		'Shift_L':4,
		'Control_R':2,
		'Alt_L': 1,
		'Shift_R':4,
		'Win_L':8,
		'Win_R':8
		}
else:
	import xcffib
	from xcffib import xproto
	from xpybutil import keybind
	
	xcb_modifiers  = {
		'Control_L' : xproto.ModMask.Control,
		'Control_R' : xproto.ModMask.Control,
		'Shift_R' : xproto.ModMask.Shift,	#different or? for l and r on mask names?
		'Shift_L' :  xproto.ModMask.Shift
		}
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
		'Control_L' : X.ControlMask,
		'Shift_L' :  X.ShiftMask,
		'Control_R' : X.ControlMask,	#different or? for l and r on mask names?
		'Shift_R' :  X.ShiftMask
		}
		
def xcb_get_modifiers(state):
    """
    Takes a ``state`` (typically found in key press or button press events)
    and returns a string list representation of the modifiers that were pressed
    when generating the event.

    :param state: Typically from ``some_event.state``.
    :return: List of modifier string representations.
    :rtype: [str]
    """
    ret = []

    if state & xproto.ModMask.Shift:
        ret.append('Shift')
    if state & xproto.ModMask.Lock:
        ret.append('Lock')
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

class SysHotkeyRegisterError(Exception):pass	

class MixIn():
	def parse_event(self, event):
		'''Turns an event back into a hotkeylist'''
		hotkey = []
		if os.name == 'posix':
			if self.library == 'xcb':
				hotkey.append(get_modifiers(event.state)[0])	#TBD
			elif self.library == 'xlib':
				hotkey.append('Control_L')	#TBD
			hotkey.append(self._get_keysym(event.detail))
		else:
			print('event from windows')
			keycode, modifiers = self.hk_ref[event.wParam][0], self.hk_ref[event.wParam][1]
			if modifiers:
				for mod in modifiers:
					hotkey.append(self._get_modifersym(mod))
			hotkey.append(self._get_keysym(keycode))
		print('hotkey ', hotkey)
		return hotkey
		
	def parse_hotkeylist(self, full_hotkey):
		'''Returns keycodes and masks from a list of hotkey masks stuff'''
		masks = []
		keycode = self._get_keycode(full_hotkey[-1])
		if len(full_hotkey) > 1:
			for item in full_hotkey[:-1]:
				masks.append(self.modders[item])
		else:								
			masks = None
		return keycode, masks
	
	def register(self, hotkey, callback=None, event_type='keypress'):
		'''Registers a tuple/list of hotkey/modifers
		event type can be keypress, keyrelease or both which will bind to both
		In reality what happens on xwindows is you filter out the unwanted results
		on my laptoop anyway keyrelease fires even if key is still down
		
		holding keypress down also sends multiple times... '''
		assert event_type in ('keypress', 'keyrelease', 'both')
		if self.v:
			print('registering')
		keycode, masks = self.parse_hotkeylist(hotkey)
		if self._the_grab(keycode, masks):
			print('Register Failed holy shit man')
			return False
		copy = hotkey[:]
		if event_type != 'both':	
			copy.append(event_type)
			KEYBINDS[tuple(copy)].append(callback)
		else:	# Binding to both keypress and keyrelease
			copy1 = hotkey[:]
			copy.append('keypress')
			copy1.append('keyrelease')
			KEYBINDS[tuple(copy)].append(callback)
			KEYBINDS[tuple(copy1)].append(callback)
		if self.v:
			print('keybinds')
			pprint(KEYBINDS)
			print()
		return True
		
	def get_callback(self, hotkey ,event_type):
		copy = hotkey[:]
		copy.append(event_type)
		if self.v:
			print('Keybinds , key here -> ', tuple(copy))
			pprint(KEYBINDS)
		for func in KEYBINDS[tuple(copy)]:
			yield func
			
class SystemHotkeys(MixIn):
	'''
	System Wide Hotkeys

	#https://wiki.python.org/moin/AppsWithPythonScripting
	#~ http://msdn.microsoft.com/en-us/library/ms927178.aspx
	#http://www.kbdedit.com/manual/low_level_vk_list.html
	'''	
	hk_ref = {}	# used for windows
	def __init__(self, consumer='callback', conn=None, library='xlib', v=False):
		# Changes the class methods to point to differenct functions 
		# Depening on the operating system and library used
		# Consumer defaults to callback which associate a unique function to each hotkey
		# Consumer can be set to a function also, which will be sent the event
		# as well as the key and mask already broken out
		# Last option for consumer is False, then you have to listen to the queue yourself
		# data_queue
		self.v = v
		def mark_event_type(event):
			if os.name == 'posix':
				if self.library == 'xlib':
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
			self.register = self._nt_register
			self._the_grab = self._nt_the_grab
			self._get_keycode = self._nt_get_keycode			
			self._get_keysym = self._nt_get_keysym
			self._get_modifersym = self._nt_get_modifiersym
			thread.start_new_thread(self._nt_wait,(),)
			
		elif library == 'xlib':												# Use the python-xlib library bindings, GPL License
			#~ self.the_grab = self._xlib_the_grab
			self.modders = xlib_modifiers
			self.register = self._xlib_register
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
		
		elif library == 'xcb':												# Using xcb and the xcffib python bindings Apache 2 http://stackoverflow.com/questions/40100/apache-license-vs-bsd-vs-mit
			self.modders = xcb_modifiers	#tbd use the xcb modders
			self._the_grab = self._xcb_the_grab
			self._get_keycode = self._xcb_get_keycode
			self._get_keysym = self._xcb_get_keysym
			
			if not conn:
				self.conn = xcffib.connect()
			else:
				self.conn = conn
			self.root = self.conn.get_setup().roots[0].root
			
			thread.start_new_thread(self._xcb_wait,(),)
		
		self.library = library
		
		if consumer == 'callback':
			if self.v:
				print('Callback')
			def thread_me():
				while 1:
					time.sleep(.1)
					try:
						event = self.data_queue.get(block=False)
					except queue.Empty:
						pass	
					else:
						event = mark_event_type(event)
						hotkey = self.parse_event(event)
						for cb in self.get_callback(hotkey, event.event_type):
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
						event = mark_event_type(event)
						hotkey = self.parse_event(event)
						#~ if os.name == 'nt':
							#~ callbacks = None
						#~ else:
						callbacks = [cb for cb in self.get_callback(hotkey, event.event_type)]
						consumer(event, hotkey, callbacks)	#tbd build up hotkey completly
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
				result = remove_or_add()	
				if result:	# TBD mm wtf somehow a None is getting on the queue if the hotkeylist is entry
					#~ print(result,'result')
					if result == (key_code, mask):						# The Keycode pressed was just removed so dont open the workbook
						continue
			if user32.PeekMessageA(byref(msg), 0, 0, 0, PM_REMOVE):		# Checking the windows message Queue
				if msg.message == win32con.WM_HOTKEY:
					#~ keycode, mask = self.hk_ref[msg.wParam][0], self.hk_ref[msg.wParam][1]				
					self.data_queue.put(msg)						# This will open up a workbook page
				else:
					print('some other message')
			time.sleep(.025)
	
	def _nt_register(self, hotkey, callback=None, event_type='keypress'):
		assert event_type in ('keypress', 'keyrelease', 'both')
		if self.v:
			print('registering')
		def register(hotkey):
			keycode, mask = self.parse_hotkeylist(hotkey)
			uniq = unique_int(self.hk_ref.keys())	# A unique integer for the new key
			self.hk_ref[uniq] = ((keycode, mask))
			self._the_grab(keycode, mask, uniq)
		self.hk_action_queue.put(lambda:register(hotkey))
		
		copy = hotkey[:]
		if event_type != 'both':	
			copy.append(event_type)
			KEYBINDS[tuple(copy)].append(callback)
		else:	# Binding to both keypress and keyrelease
			copy1 = hotkey[:]
			copy.append('keypress')
			copy1.append('keyrelease')
			KEYBINDS[tuple(copy)].append(callback)
			KEYBINDS[tuple(copy1)].append(callback)
		if self.v:
			print('keybinds')
			pprint(KEYBINDS)
			print()
		return True

	def _nt_get_keycode(self, key, disp=None):	
		return vk_codes[key]
	
	def _nt_get_keysym(self, keycode):
		for key, value in vk_codes.items():
			if value == keycode:
				return key
	
	def _nt_get_modifiersym(self, modcode):
		for key, value in win_modders.items():
			if value == modcode:
				return key
	
	def _nt_the_grab(self, keycode, masks, id, root=None):
		#~ print(keycode,masks,type(masks))
		try:
			if len(masks)==1:
				print('Keycode Added - grab masks 1')
				if not user32.RegisterHotKey(None, id, masks[0], keycode):
					raise SysHotkeyRegisterError
			elif len(masks)==2:
				print('Keycode Added - grab masks 2')
				if not user32.RegisterHotKey(None, id, masks[0] | masks[1] , keycode):
					raise SysHotkeyRegisterError 
			elif len(masks)==3:
				print('Keycode Added - grab masks 3')
				if not user32.RegisterHotKey(None, id, masks[0] | masks[1] | masks[2], keycode):
					raise SysHotkeyRegisterError
		except TypeError:						#No masks
			print('Keycode Added - no masks')
			if not user32.RegisterHotKey (None, id, 0, keycode):
				raise SysHotkeyRegisterError('Failed to register a hotkey, have you got another prgoram instance in the background runnign?')
		#~ except SysHotkeyRegisterError as e:
			#~ raise print('error was thrownn while adding hk. mostleyly it w')
	
	def _xlib_register(self, *args, **kwargs):
		if MixIn.register(self, *args, **kwargs):
			self.disp.flush()
			return True
		else:
			return False
			
	def _xlib_get_keycode(self, key) :
		keysym = XK.string_to_keysym(key)
		if keysym == 0:
			keysym = XK.string_to_keysym(special_X_keysyms[key])
		keycode = self.disp.keysym_to_keycode(keysym)
		return keycode
	
	def _xlib_get_keysym(self, keycode, i=0):
		return chr(self.disp.keycode_to_keysym(keycode, i))
	
	def _xlib_the_grab(self, keycode, masks):
		root = self.xRoot
		if masks == None:
			#~ print('MASKS NOW []')
			masks =[]	# need it as a [] to check the length
		if len(masks)==1:
			print('Keycode Added - grab masks 1')
			root.grab_key(keycode, masks[0], 1, X.GrabModeAsync, X.GrabModeAsync)
		elif len(masks)==2:
			print('Keycode Added - grab masks 2')
			root.grab_key(keycode, masks[0] | masks[1] , 1, X.GrabModeAsync, X.GrabModeAsync)
		elif len(masks)==3:
			print('Keycode Added - grab masks 3')
			root.grab_key(keycode, masks[0] | masks[1] | masks[2] , 1, X.GrabModeAsync, X.GrabModeAsync)
		elif len(masks)==0:
			print('Keycode Added - no masks')
			root.grab_key(keycode, 0 , 1, X.GrabModeAsync, X.GrabModeAsync)
		
	def _xcb_the_grab(self, keycode, masks):
		#~ masks = 0
		print('masks! ', masks)
		masks = masks[0]
		self.conn.core.GrabKeyChecked(True, self.root, masks, keycode, xproto.GrabMode.Async, xproto.GrabMode.Async).check()
	
	def _xcb_get_keycode(self, key):
		return keybind.lookup_string(key)
	
	def _xcb_get_keysym(self, keycode, i=0):
		return chr(keybind.get_keysym(keycode, i))

if __name__ == '__main__':
	#~ hk = SystemHotkeys(library='xlib')	# 
	#~ hk.register(['Control_L', 'k'], callback=lambda e: print('i am control k'))
	#~ hk.register(['k'], callback=lambda e: print('i am k'))
	#~ hk = SystemHotkeys(library='xlib')	# xcb
	#~ hk.register(['Control_L', 'k'], callback=lambda e: print('i am control k'))
	#~ hk.register(['k'], callback=lambda e: print('i am k'))
	hk = SystemHotkeys()	
	#~ hk.register(['Shift_L','Alt_L', 'k'], callback=lambda e: print('i am control k'))
	hk.register(['k'], callback=lambda e: print('i am k'))
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
