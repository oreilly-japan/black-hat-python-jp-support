# -*- coding: utf-8 -*-
import win32con
import win32api
import win32security

import wmi
import sys
import os

LOG_FILE = "process_monitor_log.csv"

def get_process_privileges(pid):
    try:
        # 対象のプロセスへのハンドルを取得
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION, False, pid)

        # メインのプロセストークンを開く
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)

        # 有効化されている権限のリストを取得
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)

        # 権限をチェックして、有効化されているものだけを出力するループ
        priv_list = []
        for priv_id, priv_flags in privs:
            # 権限が有効化されているかチェック
            if priv_flags == 3:
                priv_list.append(win32security.LookupPrivilegeName(None, priv_id))

    except:
        priv_list.append("N/A")

    return "|".join(priv_list)

def log_to_file(message):
    fd = open(LOG_FILE, "ab")
    fd.write("%s\r\n" % message)
    fd.close()

    return

# ログファイルのヘッダーの作成
if not os.path.isfile(LOG_FILE):
    log_to_file("Time,User,Executable,CommandLine,PID,ParentPID,Privileges")

# WMIインタフェースのインスタンス化
c = wmi.WMI()

# プロセス監視の開始
process_watcher = c.Win32_Process.watch_for("creation")


while True:
    try:
        new_process = process_watcher()

        proc_owner  = new_process.GetOwner()
        proc_owner  = "%s\\%s" % (proc_owner[0],proc_owner[2])
        create_date = new_process.CreationDate
        executable  = new_process.ExecutablePath
        cmdline     = new_process.CommandLine
        pid         = new_process.ProcessId
        parent_pid  = new_process.ParentProcessId

        privileges  = get_process_privileges(pid)

        process_log_message = "%s,%s,%s,%s,%s,%s,%s" % (create_date, proc_owner, executable, cmdline, pid, parent_pid,privileges)

        print "%s\r\n" % process_log_message

        log_to_file(process_log_message)

    except:
        pass
