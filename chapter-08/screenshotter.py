# -*- coding: utf-8 -*-
import win32gui
import win32ui
import win32con
import win32api

# メインのデスクトップ画面のハンドルを取得
hdesktop = win32gui.GetDesktopWindow()

# モニターのサイズをピクセル単位で特定
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# デバイスコンテキストを作成
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# メモリーデバイスコンテキストの作成
mem_dc = img_dc.CreateCompatibleDC()

# ビットマップオブジェクトの作成
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# メモリーデバイスコンテキストにデスクトップ画面をコピー
mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# ビットマップをファイルに保存
screenshot.SaveBitmapFile(mem_dc, 'c:\\WINDOWS\\Temp\\screenshot.bmp')

# オブジェクトを解放
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())