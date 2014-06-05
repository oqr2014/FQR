#!/usr/bin/python
#################################################################################
# Multithreaded TCP Socket Quote Server.
# This quote server is used to feed data for GUIs 
# Create a TCP socket each for each client connection. 
# fix message quote for both futures and options
################################################################################

from option_fix import *
from xml_conf import * 
import socket
import sys
import threading 
import time
import Queue 
import select 
import mcast
import errno

class Channel: 
	def __init__(self, sock_, thread_, oids_=[], max_size_=10000):
		self.sock   = sock_
		self.thread = thread_ 
		self.oids   = oids_
		self.que    = Queue.Queue(max_size_)
	
class McastQuoteThrd(threading.Thread, mcast.McastRcvr): 
# Receiving quotes from multicast quotes and add the data into its Queue, respectively
	def __init__(self, svr_, MCAST_ADDR_, MCAST_PORT_): 
		threading.Thread.__init__(self)
		mcast.McastRcvr.__init__(self, mcast_addr_=MCAST_ADDR_, mcast_port_=MCAST_PORT_)
		self.svr = svr_
		self.oid_ques_dict = {}
			
	def run(self):
		ts1 = time.time()
		while 1:
			elapsed_time = time.time() - ts1
			if elapsed_time >= 1: 
				self.update_oid_que()
				ts1 = time.time() 
			try:
				data, addr = self.sock.recvfrom(8192)
#				print "FROM: ", addr
#				print "DATA: ", data
				fixParser = FixMsgParser(str_=data)
				for order in fixParser.orders: 
					if order.sid in self.oid_ques_dict.keys():
						if order.price_level != 1: 
							continue
						strData = order.pack2str()
#						print "queue data:", strData
						ques = self.oid_ques_dict[order.sid]
						for que in ques: 
							if que.full():
								que.get()
							que.put(strData)
			except socket.error, (val, msg):
				pass
#				print "socket.error caught", val, msg 

	def update_oid_que(self):
		self.svr.sock_dict_lock.acquire()
		if self.svr.sock_dict_dirty:
			self.oid_ques_dict = {}
			for sock in self.svr.sock_dict.keys():
				oids = self.svr.sock_dict[sock].oids
				for oid in oids:
					if oid in self.oid_ques_dict.keys():
						self.oid_ques_dict[oid].append(self.svr.sock_dict[sock].que)
					else:
						self.oid_ques_dict[oid] = [self.svr.sock_dict[sock].que]
			self.svr.sock_dict_dirty = False
#			print "oid_ques_dict", self.oid_ques_dict
		self.svr.sock_dict_lock.release()

class TCPThread(threading.Thread):
#One instance per connection.
#Override handle(self) to customize action.
	def __init__(self, svr_, cliSock_):
		threading.Thread.__init__(self)
		self.svr     = svr_
		self.cliSock = cliSock_
		self.que     = None
		self.stop    = threading.Event()
		print "TCPThread is running..."

	def run(self):
		ts1 = time.time()
		self.que = self.svr.sock_dict[self.cliSock].que
		while not self.stop.is_set():
			strData = self.que.get() 
			try:
				self.cliSock.send(strData)
			except socket.error as e:
#				if e.errno != errno.ECONNRESET:
#					raise
				print "####TCPThread exception caught %s" %e 
				return 
#				self.cliSock.close()
#			else: 
#				print "data sending to GUI", strData
#		self.cliSock.shutdown(socket.SHUT_RDWR)
		self.cliSock.close()

	def shutdown(self):
		self.stop.set()

class QuoteSvr(object):
	def __init__(self, quotes_ = ""):
		mcast_conf      = McastXmlConf(quotes_name_ = quotes)
		gui_conf        = GUIQuoteXmlConf(quotes_name_ = quotes)
		self.HOST       = gui_conf.host
		self.PORT       = gui_conf.port
		self.ADDRESS    = (self.HOST, self.PORT)
		self.MCAST_ADDR = mcast_conf.mcast_addr
		self.MCAST_PORT = mcast_conf.mcast_port
		self.cliSocks   = [] 
		self.threads    = []
		self.sock_dict  = {}  ## socket:Channel 
		self.sock_dict_lock = threading.Lock()
		self.sock_dict_dirty = False

	def run(self):
		self.running = True
		mcastThread = McastQuoteThrd(self, MCAST_ADDR_=self.MCAST_ADDR, MCAST_PORT_=self.MCAST_PORT) 
		mcastThread.start()
		self.threads.append(mcastThread)
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
		svr = QuoteSvr(quotes="FUTURES")
		svr.run()
	except KeyboardInterrupt:
	# terminate with Ctrl-C
		sys.exit(0)

