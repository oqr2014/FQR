#!/usr/bin/python
################################################################## 
# Multithreaded TCP Socket Quote Server.
# Create a TCP socket each for each client connection. 
###################################################################

from futures_attr import * 
from option_fix import *
import socket
import sys
import threading 
import time


class FutTCPThread(threading.Thread):
#One instance per connection.
#Override handle(self) to customize action.
	def __init__(self, svr_, cliSock_, futAttr_):
		threading.Thread.__init__(self)
		self.server  = svr_
		self.cliSock = cliSock_
		self.futAttr = futAttr_
		self.running = True
		print "FutTCPThread is running..."

	def run(self):
		exp_date = int(self.cliSock.recv(1024).strip())
		print "expiration date=", exp_date 
		fid = self.futAttr.exp_date_dict[exp_date].fid 	
		print "Requested expiration date: =>[%d], fid: =>[%d]"%(exp_date, fid)
		while 1:
			inf=open('/OMM/data/futures/futures_fix.log', "r")
			for line in inf:
				fixParser = FixMsgParser(str_=line)
				for order in fixParser.orders: 
					if fid == order.sid:
						strData = self.pack_order_data(order)
						print "sending data:", strData
						self.cliSock.send(strData)
		self.cliSock.close()

	def pack_order_data(self, order_):
		ss = str(order_.sid) + "\x01" + order_.send_time + "\x01" + str(order_.trade_date) + "\x01" \
			+ str(order_.entry_type) + "\x01"  + str(order_.price) + "\x01" + str(order_.quantity) + "\x03"
		return ss

class FutQuoteSvr(object):
	def __init__(self, futAttr_):
		self.futAttr     = futAttr_
		self.HOST        = 'localhost'
		self.PORT        = 22085
		self.ADDRESS     = (self.HOST, self.PORT)
		self.cliSockList = [] 
		self.threads     = []

	def run(self):
		self.running = True
		self.serverSock = socket.socket() 
		self.serverSock.bind(self.ADDRESS)
		self.serverSock.listen(5)
		while 1: 
			(cliSock, address) = self.serverSock.accept() 
			self.cliSockList.append(cliSock)
			cliThread = FutTCPThread(self, cliSock, self.futAttr)
			cliThread.start() 
			self.threads.append(cliThread)
		for t1 in self.threads:
			t1.join()
		return 

if __name__ == "__main__":
	try:
		futAttr = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
		svr = FutQuoteSvr(futAttr)
		svr.run()
	except KeyboardInterrupt:
	# terminate with Ctrl-C
		sys.exit(0)

