#!/usr/bin/python

import socket
import random
from futures_attr import * 
from option_attr import *

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
		print "[%s]" % (recv_data)
	sock.close()

if __name__ == "__main__":
	futAttr  = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
	exp_date = 20140321
	fid      = futAttr.exp_date_dict[exp_date].fid 
	client(str(fid))

