#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

target_host = "127.0.0.1"
target_port = 80

# socketオブジェクトの作成
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# データの送信
client.sendto("AAABBBCCC",(target_host,target_port))

# データの受信
data, addr = client.recvfrom(4096)

print data
