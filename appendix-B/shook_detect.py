# -*- coding: utf-8 -*-

from ctypes import *
dll = windll.kernel32

addr = dll.GetProcAddress(dll._handle, "CreateFileA")
byte = (c_char).from_address(addr)
if byte.value[0] == '\xCC':
	print "Sandbox Detected !!"
else:
	print "We are OK"

