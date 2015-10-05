# -*- coding: utf-8 -*-

import ctypes

GENERIC_WRITE 				= 0x40000000L
CREATE_ALWAYS 				= 2
FILE_ATTRIBUTE_NORMAL  	= 0x00000080

hFile = ctypes.windll.kernel32.CreateFileA(
							"tmp.txt",
							GENERIC_WRITE,
							0,
							0,
							CREATE_ALWAYS,
							FILE_ATTRIBUTE_NORMAL,
							0)

dwBytesWritten = ctypes.c_ulong()
ctypes.windll.kernel32.WriteFile(
							hFile, 
							"abcd", 
							4, 
							ctypes.byref(dwBytesWritten), 
							0)

ctypes.windll.kernel32.CloseHandle(hFile)



