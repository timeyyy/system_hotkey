import os

if os.name == 'nt':
	import ctypes
	from ctypes import wintypes
	import win32con
	byref = ctypes.byref
	user32 = ctypes.windll.user32

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
	from Xlib import X
	from Xlib import XK 
	from Xlib.display import Display
	special_X_keysyms = {			# these couldn't be gotten from the xlib keycode function
		' ' : "space",
		'\t' : "Tab",
		'\n' : "Return",  # for some reason this needs to be cr, not lf
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
	posix_modders = {
		'Control_L' : X.ControlMask,
		'Shift_L' :  X.ShiftMask,
		'Control_R' : X.ControlMask,	#different or? for l and r on mask names?
		'Shift_R' :  X.ShiftMask
		}
	
class SystemHotkeys():
	'''
	System Wide Hotkeys

	#https://wiki.python.org/moin/AppsWithPythonScripting
	#~ http://msdn.microsoft.com/en-us/library/ms927178.aspx
	#http://www.kbdedit.com/manual/low_level_vk_list.html
	'''
	class SysHotkeySetupError(Exception):pass
	
	hk_ref = {}	#used for windows
	
	def __init__(self, xlib=True):
		# Changes the class methods to point to differenct functions 
		# Depening on the operating system and library used
		if os.name == 'nt':
			self.the_grab = self._win_the_grab
			self.modders = win_modders
			self.get_keycode = self._win_get_keycode
		elif xlib:								# Use the python-xlib library bindings, GPL License
			self.xlib = True
			self.the_grab = self._xlib_the_grab
			self.modders = posix_modders
			self.get_keycode = self._xlib_get_keycode

	def bind_key(self):
		if os.name == 'nt':
			pass
			#~ self.hk.
		else:
			pass
			
	def free_key(self, *args):
		user32.UnregisterHotKey (None, id)
	
	def _win_get_keycode(full_hotkey, disp=None):	
		return vk_codes[full_hotkey[-1]]
	
	def _xlib_get_keycode(ch, disp) :
		keysym = XK.string_to_keysym(ch)
		if keysym == 0:
			# Unfortunately, although this works to get the correct keysym
			# i.e. keysym for '#' is returned as "numbersign"
			# the subsequent display.keysym_to_keycode("numbersign") is 0.
			keysym = XK.string_to_keysym(special_X_keysyms[ch])
		print('the display', disp)
		keycode = disp.keysym_to_keycode(keysym)
		return keycode

	def the_grab_settings(self, full_hotkey, disp=None):
		if self.xlib and not disp:
			disp = Display()	
		masks=[]
		keycode = self.get_keycode(full_hotkey, disp) 
		for item in full_hotkey:
			masks.append(self.modders.get(item, None))
		masks = [item for item in masks if item]	#we have all masks now
		if not masks:								# empty list
			masks = None							#return as None so doesnt get saved as [] in database
		return keycode, masks
		
	def _win_the_grab(self, keycode,masks, i, root=None):	#TBD WHAT IS THIS I DOING!
		#~ print(keycode,masks,type(masks))
		try:
			if len(masks)==1:
				print('Keycode Added - grab masks 1')
				if not user32.RegisterHotKey(None, i, masks[0], keycode):
					raise SysHotkeySetupError
			elif len(masks)==2:
				print('Keycode Added - grab masks 2')
				if not user32.RegisterHotKey(None, i, masks[0] | masks[1] , keycode):
					raise SysHotkeySetupError 
			elif len(masks)==3:
				print('Keycode Added - grab masks 3')
				if not user32.RegisterHotKey(None, i, masks[0] | masks[1] | masks[2], keycode):
					raise SysHotkeySetupError
		except TypeError:						#No masks
			print('Keycode Added - no masks')
			if not user32.RegisterHotKey (None, i, 0, keycode):
				raise SysHotkeySetupError
		except SysHotkeySetupError:
			print('error was thrownn while adding hk.')
	
	def _xlib_the_grab(self, keycode, masks, root):
		if masks == None:
			#~ print('MASKS NOW []')
			masks =[]	# need it as a [] to check the length
		if len(masks)==1:
			print('Keycode Added - grab masks 1')
			root.grab_key(keycode, masks[0], 1,X.GrabModeAsync, X.GrabModeAsync)
		elif len(masks)==2:
			print('Keycode Added - grab masks 2')
			root.grab_key(keycode, masks[0] | masks[1] , 1,X.GrabModeAsync, X.GrabModeAsync)
		elif len(masks)==3:
			print('Keycode Added - grab masks 3')
			root.grab_key(keycode, masks[0] | masks[1] | masks[2] , 1,X.GrabModeAsync, X.GrabModeAsync)
		elif len(masks)==0:
			print('Keycode Added - no masks')
			root.grab_key(keycode, 0 , 1,X.GrabModeAsync, X.GrabModeAsync)
