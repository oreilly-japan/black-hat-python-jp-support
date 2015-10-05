# -*- coding: utf-8 -*-

from ctypes import *
GENERIC_WRITE 				= 0x40000000L
CREATE_ALWAYS 				= 2
FILE_ATTRIBUTE_NORMAL  	= 0x00000080

dll = windll.kernel32
addr = dll.GetProcAddress(dll._handle, "CreateFileA")
addr = addr + 2
type_CreateFileA = WINFUNCTYPE(
							c_ulong, 
							c_char_p, 
							c_ulong, 
							c_ulong, 
							c_ulong, 
							c_ulong, 
							c_ulong, 
							c_ulong) 
sdc_CreateFileA = type_CreateFileA(addr)

hFile = sdc_CreateFileA(
							"tmp.txt",
							GENERIC_WRITE,
							0,
							0,
							CREATE_ALWAYS,
							FILE_ATTRIBUTE_NORMAL,
							0)

dwBytesWritten = c_ulong(0)
windll.kernel32.WriteFile(
							hFile, 
							"abcd", 
							len("abcd"), 
							byref(dwBytesWritten), 
							0)

windll.kernel32.CloseHandle(hFile)



