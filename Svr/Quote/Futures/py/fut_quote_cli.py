#!/usr/bin/python

import socket
import random

def client(str_):
	HOST, PORT = 'localhost', 22085
	# SOCK_STREAM == a TCP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setblocking(1)
	sock.settimeout(None)
	sock.connect((HOST, PORT))
	print "sending data => [%s]" % (str_)
	sock.send(str_)
	while 1:
		recv_data = sock.recv(1024)  
		print "recv data => \n [%s]" % (recv_data)
	sock.close()

if __name__ == "__main__":
	client('20140321')
