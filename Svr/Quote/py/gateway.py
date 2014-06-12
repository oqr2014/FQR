#!/usr/bin/python
##############################################################################
# Multithreaded gateway server 
# thread 1 Receive multicast data from futures quote 
# thread 2 Receive multicast date from options quote 
# thread 3: 
#  [*] Build implied volatility curve and fit the ivc by polynomial 
#  [*] Execute
##############################################################################

from fix import *
from fut_attr import *
from opt_attr import *
from xml_conf import *
from ivc import *
import socket
import sys
import threading 
import time
import Queue 
import select 
import mcast
import errno

## Futures quotes thread 
class FutQtThrd(threading.Thread, mcast.McastRcvr): 
	opt_data = None
	fid      = 0 

	def __init__(self, MCAST_ADDR_, MCAST_PORT_, opt_data_): 
		threading.Thread.__init__(self)
		mcast.McastRcvr.__init__(self, mcast_addr_=MCAST_ADDR_, mcast_port_=MCAST_PORT_)
		gw_conf       = GatewayConf()
		fut_attr_ps   = FutAttrParser(filename_ = gw_conf.fut_sym)
		self.fid      = fut_attr_ps.exp_date_dict[self.exp_date].fid
		self.opt_data = opt_data_

	def run(self):
		while 1:
			try:
				data, addr = self.sock.recvfrom(10240)
				fixPs = FixMsgParser(str_ = data)
				self.opt_data.fut_lock.acquire()
				for order in fixParser.orders: 
					if order.sid == self.fid and order.price_level == 1: 
						if order.entry_type == 0: ## bid
							self.opt_data.fut_bid = order.price
						else: ## ask
							self.opt_data.fut_ask = order.price
				self.opt_data.fut_lock.release()
			except socket.error, (val, msg):
				print "socket.error caught:", val, msg 

## Options quotes thread
class OptQtThrd(threading.Thread, mcast.McastRcvr): 
	opt_data = None
	oid_dict = {}

	def __init__(self, MCAST_ADDR_, MCAST_PORT_, opt_data_): 
		threading.Thread.__init__(self)
		mcast.McastRcvr.__init__(self, mcast_addr_ = MCAST_ADDR_, mcast_port_ = MCAST_PORT_)
		gw_conf       = GatewayConf()
		opt_attr_ps   = OptAttrParser(filename_ = gw_conf.opt_sym)
		self.oid_dict = opt_attr_ps.oid_dict
		self.opt_data = opt_data_

	def run(self):
		while 1:
			try:
				data, addr = self.sock.recvfrom(10240)
				fixPs = FixMsgParser(str_ = data)
				self.opt_data.opt_lock.acquire()
				for order in fixParser.orders: 
					if order.sid in self.oid_dict.keys() and order.price_level == 1: 
						opt_attr = self.oid_dict[order.sid]
						if opt_attr.cp_type == "P":  ##PUT
							if order.entry_type == 0: ## bid
								self.opt_data.put_K_bid_dict[opt_attr.strike] = ImplVol(price_=order.price, ts_=order.entry_time, cp_type_="PUT")
							else: ## ask
								self.opt_data.put_K_ask_dict[opt_attr.strike] = ImplVol(price_=order.price, ts_=order.entry_time, cp_type_="PUT")
						else: ## CALL 
							if order.entry_type == 0: ## bid
								self.opt_data.call_K_bid_dict[opt_attr.strike] = ImplVol(price_=order.price, ts_=order.entry_time, cp_type_="CALL")
							else: ## ask
								self.opt_data.call_K_ask_dict[opt_attr.strike] = ImplVol(price_=order.price, ts_=order.entry_time, cp_type_="CALL")
				self.opt_data.opt_lock.release()
			except socket.error, (val, msg):
				print "socket.error caught:", val, msg 

## Gateway for execution 
class Gateway(object):
	def __init__(self):
		self.gw_conf     = GatewayConf()
		self.fut_qt_conf = McastXmlConf(quotes_name_ = "FUTURES")
		self.opt_qt_conf = McastXmlConf(quotes_name_ = "OPTIONS")
		self.threads     = []
		self.opt_data    = OptionData()
		self.opt_data.fut_exp_date = self.gw_conf.fut_exp_dt
		self.opt_data.opt_exp_date = self.gw_conf.opt_exp_dt
		
		self.ivc_data    = ImplVolCurve()
		self.ivc_data.val_date = self.gw_conf.val_dt
		self.ivc_data.r  = self.gw_conf.rf_rate
		self.ivc_data.q  = self.gw_conf.div_rate

	def run(self):
		self.running = True
		fut_qt_thrd = FutQtThrd(self, MCAST_ADDR_=self.fut_qt_conf.mcast_addr, MCAST_PORT_=self.fut_qt_conf.mcast_port, self.opt_data) 
		fut_qt_thrd.start()
		self.threads.append(fut_qt_thrd)

		opt_qt_thrd = OptQtThrd(self, MCAST_ADDR_=self.opt_qt_conf.mcast_addr, MCAST_PORT_=self.opt_qt_conf.mcast_port, self.opt_data) 
		opt_qt_thrd.start()
		self.threads.append(opt_qt_thrd)

# client socket
		self.svrSock = socket.socket() 
		self.svrSock.bind(self.ADDRESS)
		self.svrSock.listen(5)
		
		inputs = [self.svrSock] 
		outputs = []
		while 1: 
#			print "waiting for the next event"
			readable, writable, exceptional = select.select(inputs, outputs, inputs, 1) 
			if not (readable or writable or exceptional):
#				print "select timed out"
				print "select inputs", inputs
				continue
			for sock in readable: 
				if sock is self.svrSock:
					(cliSock, cliAddr) = self.svrSock.accept() 
					print "new socket connection from", cliAddr, "accepted"
					cliSock.setblocking(0)
					self.cliSocks.append(cliSock)
					inputs.append(cliSock)
					cliThread = TCPThread(self, cliSock)
					self.threads.append(cliThread)
					self.sock_dict[cliSock] = Channel(sock, cliThread)
					cliThread.start() 
				else:
					if sock in self.cliSocks:
						try: 
							data = ""
							while 1: 
								recv = sock.recv(4096)
								if recv == "": 
									break
								idx = recv.find('\x03') 
								if idx != -1:
									data += recv[:idx]
									if idx < len(recv)-1: 
										print "### ERROR: some unprocessed data", recv[idx+1:]
									break
								data += recv

						except socket.error as e: 
#							if e.errno != errno.ECONNRESET:
#								raise
							print "closing connection from %s, %s" %cliAddr %e
							inputs.remove(sock)
							self.cliSocks.remove(sock)
							self.shutdown_clithread(sock)
						else: 	
							if data != "":
								print 'received %s from %s' %(data, sock.getpeername()) 
								oids = data.strip().split(',') # split by comma 
								oids = map(int, oids)
								self.sock_dict_lock.acquire()
								self.sock_dict[sock].oids = oids; 
								self.sock_dict_dirty = True; 
								self.sock_dict_lock.release()
							else: ## without data is a disconnection 
								print "closing connection from", cliAddr
								inputs.remove(sock)
								self.cliSocks.remove(sock)
								self.shutdown_clithread(sock)
			for sock in exceptional: 
				print "exceptional condition for", sock.getpeername()
				inputs.remove(sock)
				self.shutdown_clithread(sock)

		for t1 in self.threads:
			if t1.isAlive():
				t1.join()
		return 

	def shutdown_clithread(self, cliSock_):
		cliThread = self.sock_dict[cliSock_].thread
		cliThread.shutdown()
		cliThread.join()
		self.sock_dict_lock.acquire()
		del self.sock_dict[cliSock_] 
		self.sock_dict_dirty = True
		self.sock_dict_lock.release()
		
if __name__ == "__main__":
	try:
		svr = Gateway()
		svr.run()
	except KeyboardInterrupt:
	# terminate with Ctrl-C
		sys.exit(0)

