#!/usr/bin/python
###############################################################
# Multithreaded TCP Socket Quote Server.
# Create a TCP socket each for each client connection. 
###############################################################

from option_fix import *
import socket
import sys
import threading 
import time
import Queue 
import select 
import mcast 

class Channel: 
	def __init__(self, sock_, thread_, fid_=0, max_size_ = 10000):
		self.sock   = sock_
		self.thread = thread_ 
		self.fid    = fid_
		self.queue  = Queue.Queue(max_size_)
	
class McastQuoteThread(threading.Thread, mcast.McastClient): 
# Receiving quotes from C++ quote server and add the data into the Queue
	def __init__(self, svr_): 
		threading.Thread.__init__(self)
		mcast.McastClient.__init__(self)
		self.svr = svr_
		self.fid_que_dict = {}
			
	def run(self):
		ts1 = time.time()
		while 1:
			elapsed_time = time.time() - ts1
			if elapsed_time >= 1: 
				self.update_fid_que()
				ts1 = time.time() 
			try:
				data, addr = self.sock.recvfrom(1024)
#				print "FROM: ", addr
#				print "DATA: ", data
				fixParser = FixMsgParser(str_=data)
				for order in fixParser.orders: 
					if order.sid in self.fid_que_dict.keys():
						strData = self.pack_order_data(order)
						print "queue data:", strData
						que = self.fid_que_dict[order.sid]
						if que.full():
							que.get()
						que.put(strData)
			except socket.error, (val, msg):
				pass
#				print "socket.error caught", val, msg 

	def update_fid_que(self):
		self.svr.sock_dict_lock.acquire()
		if self.svr.sock_dict_dirty:
			self.fid_que_dict = {}
			for sock in self.svr.sock_dict.keys():
				self.fid_que_dict[self.svr.sock_dict[sock].fid] = self.svr.sock_dict[sock].queue
			self.svr.sock_dict_dirty = False
		self.svr.sock_dict_lock.release()

	def pack_order_data(self, order_):
		ss = str(order_.sid) + "\x01" + order_.send_time + "\x01" + str(order_.trade_date) + "\x01" \
			+ str(order_.entry_type) + "\x01"  + str(order_.price) + "\x01" + str(order_.quantity) + "\x03"
		return ss


class FutTCPThread(threading.Thread):
#One instance per connection.
#Override handle(self) to customize action.
	def __init__(self, svr_, cliSock_):
		threading.Thread.__init__(self)
		self.svr     = svr_
		self.cliSock = cliSock_
		self.que     = None
		self.running = True
		print "FutTCPThread is running..."

	def run(self):
		ts1 = time.time()
		self.que = self.svr.sock_dict[self.cliSock].queue
		while 1:
			strData = self.que.get() 
			try:
				self.cliSock.send(strData)
			except socket.error:
				self.cliSock.close()
			else: 
				print "data sending to GUI", strData

class FutQuoteSvr(object):
	def __init__(self):
		self.HOST     = 'localhost'
		self.PORT     = 22085
		self.ADDRESS  = (self.HOST, self.PORT)
		self.cliSocks = [] 
		self.threads  = []
		self.sock_dict = {}  ## socket:Channel 
		self.sock_dict_lock = threading.Lock()
		self.sock_dict_dirty = False

	def run(self):
		self.running = True
		mcastThread = McastQuoteThread(self) 
		mcastThread.start()
		self.threads.append(mcastThread)
# client socket
		self.svrSock = socket.socket() 
		self.svrSock.bind(self.ADDRESS)
		self.svrSock.listen(5)
		
		inputs = [self.svrSock] 
		outputs = []
		while 1: 
			print "waiting for the next event"
			readable, writable, exceptional = select.select(inputs, outputs, inputs, 1) 
			if not (readable or writable or exceptional):
				print "select timed out"
				continue
			for sock in readable: 
				if sock is self.svrSock:
					(cliSock, cliAddr) = self.svrSock.accept() 
					print "new socket connection from", cliAddr, "accepted"
					cliSock.setblocking(0)
					self.cliSocks.append(cliSock)
					inputs.append(cliSock)
					cliThread = FutTCPThread(self, cliSock)
					self.threads.append(cliThread)
					self.sock_dict[cliSock] = Channel(sock, cliThread)
					cliThread.start() 
				else:
					if sock in self.cliSocks:
						data = sock.recv(1024)
						if data:
							print 'received %s from %s' %(data, sock.getpeername()) 
							fid = int(data.strip())
							self.sock_dict_lock.acquire()
							self.sock_dict[sock].fid = fid; 
							self.sock_dict_dirty = True; 
							self.sock_dict_lock.release()
						else: ## without data is a disconnection 
							print "closing connection from", cliAddr
							inputs.remove(sock)
							sock.close() 
							self.sock_dict_lock.acquire()
							del self.sock_dict[sock] 
							self.sock_dict_dirty = True
							self.sock_dict_lock.release()
			for sock in exceptional: 
				print "exceptional condiction for", sock.getpeername()
				inputs.remove(sock)
				s.close()

		for t1 in self.threads:
			t1.join()
		return 

if __name__ == "__main__":
	try:
		svr = FutQuoteSvr()
		svr.run()
	except KeyboardInterrupt:
	# terminate with Ctrl-C
		sys.exit(0)

