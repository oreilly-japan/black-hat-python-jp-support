#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print "[!!] Failed to listen on %s:%d" % (local_host, local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit(0)

    print "[*] Listening on %s:%d" % (local_host, local_port)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # ローカル側からの接続情報を表示
        print "[==>] Received incoming connection from %s:%d" % (addr[0],addr[1])

        # リモートホストと通信するためのスレッドを開始
        proxy_thread = threading.Thread(
                target=proxy_handler,
                args=(client_socket,remote_host,remote_port,receive_first))

        proxy_thread.start()

def main():

    # コマンドライン引数の解釈
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]"
        print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
        sys.exit(0)

    # ローカル側での通信待受を行うための設定
    local_host  = sys.argv[1]
    local_port  = int(sys.argv[2])

    # リモート側の設定
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    # リモート側にデータを送る前にデータ受信を行うかどうかの指定
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    # 通信待機ソケットの起動
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)

def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # リモートホストへの接続
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    # 必要ならリモートホストからデータを受信
    if receive_first:

        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # 受信データ処理関数にデータ受け渡し
        remote_buffer = response_handler(remote_buffer)

        # もしローカル側に対して送るデータがあれば送信
        if len(remote_buffer):
            print "[<==] Sending %d bytes to localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)
    # ローカルからのデータ受信、リモートへの送信、ローカルへの送信
    # の繰り返しを行うループ処理の開始
    while True:

        # ローカルホストからデータ受信
        local_buffer = receive_from(client_socket)

        if len(local_buffer):

            print "[==>] Received %d bytes from localhost." % len(local_buffer)
            hexdump(local_buffer)

            # 送信データ処理関数にデータ受け渡し
            local_buffer = request_handler(local_buffer)

            # リモートホストへのデータ送信
            remote_socket.send(local_buffer)
            print "[==>] Sent to remote."

        # 応答の受信
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):

            print "[<==] Received %d bytes from remote." % len(remote_buffer)
            hexdump(remote_buffer)

            # 受信データ処理関数にデータ受け渡し
            remote_buffer = response_handler(remote_buffer)

            # ローカル側に応答データを送信
            client_socket.send(remote_buffer)

            print "[<==] Sent to localhost."

        # ローカル側・リモート側双方からデータがこなければ接続を閉じる
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print "[*] No more data. Closing connections."

            break

# 16進数ダンプを整形して表示する関数
# 以下のURLのコメント欄から取得したコード
# （折り返しバイト数の指定に関わるデフォルト引数の値のみ修正）
# http://code.activestate.com/recipes/142812-hex-dumper/
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )

    print b'\n'.join(result)


def receive_from(connection):

    buffer = ""

    # タイムアウト値を2秒に設定（ターゲットに応じた調整が必要）
    connection.settimeout(2)

    try:
        # データを受け取らなくなるかタイムアウトになるまでデータを受信して
        # bufferに格納
        while True:
            data = connection.recv(4096)

            if not data:
                break

            buffer += data

    except:
        pass

    return buffer

# リモート側のホストに送る全リクエストデータの改変
def request_handler(buffer):
    # パケットの改変を実施
    return buffer


# ローカル側のホストに送る全レスポンスデータの改変
def response_handler(buffer):
    # パケットの改変を実施
    return buffer

main()
