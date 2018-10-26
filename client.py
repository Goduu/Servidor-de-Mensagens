#!/usr/bin/env python3

import socket
import select
import sys

localHost = "127.0.0.1"
localPort = int(sys.argv[1])
serverIP = str(sys.argv[2])
serverPort = int(sys.argv[3])

bufferSize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((localHost, localPort))

while True:
	readers, _, _ = select.select([sys.stdin, s], [], [])
	for reader in readers:
		if reader is s:
			message, _ = s.recvfrom(bufferSize)
			print(message.decode('utf-8'))
		elif reader is sys.stdin:
			msg = input()
			s.sendto(msg.encode('utf-8'), (serverIP, serverPort))
