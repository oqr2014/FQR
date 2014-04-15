#!/usr/bin/python
############################################
# Futures Quote Client 
#
############################################
import socket
import random
from futures_attr import * 
from option_attr import *
from option_fix import *


class FutQuoteCli:
	def __init__(self, HOST_='localhost', PORT_=22085, sfid_="0"):
		self.HOST = HOST_
		self.PORT = PORT_
		self.sfid = sfid_
		# SOCK_STREAM == a TCP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setblocking(1)
		self.sock.settimeout(None)
		self.sock.connect((self.HOST, self.PORT))
		
	def run(self):
		print "sending data => [%s]" % (self.sfid)
		self.sock.send(self.sfid)
		while 1:
			recv_data = self.sock.recv(1024)  
			print "[%s]" % (recv_data)
			tail = ""
			if len(recv_data) > 0:
				if len(tail) > 0:
					recv_data += tail
				(orders, tail) = FixMsg.str2order(recv_data)
				
			print "[%s]" % (recv_data)
		self.sock.close()

if __name__ == "__main__":
	futAttr  = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
	exp_date = 20140321
	fid      = futAttr.exp_date_dict[exp_date].fid 
	client   = FutQuoteCli(sfid_=str(fid))
	client.run()

