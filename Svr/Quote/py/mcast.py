#!/bin/bash
#################################################################
# Test program for multicasting fix msgs of futures
#################################################################
import os 
import socket
import time
import threading
from option_fix import *

class McastSndrThrd(threading.Thread):
	def __init__(self, sndr_port_, mcast_addr_, mcast_port_, fix_file_):
		threading.Thread.__init__(self)
		self.ANY         = "0.0.0.0"
		self.SNDR_PORT   = sndr_port_ 
		self.MCAST_ADDR  = mcast_addr_
		self.MCAST_PORT  = mcast_port_
		self.fix_file    = fix_file_
#		self.cv          = cv_
		
	def run(self): 
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#The sender is bound on (0.0.0.0:1501)
		sock.bind((self.ANY, self.SNDR_PORT))
		#Tell kernel that we want to multicast and data is sent
		#to everyone (255 is the level of multicasting)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
		if not os.path.isfile(self.fix_file):
			raise Exception("fix file: %s does not exist" %self.fix_file)
		while 1:
			pre_ts  = 0
			cur_ts  = 0 
			in_f = open(self.fix_file, "r")
			real_pre_ts = time.time()
			order_num_cur_ts = 0
			for line in in_f:
				fixPs = FixMsgParser(str_=line)
				if len(fixPs.orders) == 0:
					continue
				cur_ts = fixPs.orders[0].entry_time
				if pre_ts == 0:
					pre_ts = cur_ts
					order_num_cur_ts = 1
					sock.sendto(line, (self.MCAST_ADDR, self.MCAST_PORT));
					real_pre_ts = time.time()
					continue
				if pre_ts < cur_ts: 
					order_num_cur_ts = 0 
					wait_time = cur_ts - pre_ts - (time.time() - real_pre_ts)
#					print "wait_time", wait_time 
					if wait_time > 0:
						time.sleep(wait_time)
				else:
					order_num_cur_ts += 1 
					if order_num_cur_ts == 1: 
						real_pre_ts = time.time()
				pre_ts = cur_ts
				sock.sendto(line, (self.MCAST_ADDR, self.MCAST_PORT));
#				print line 
				time.sleep(.001)
			in_f.close()
				
			
class McastSvr(object):
	def __init__(self):
		self.threads = [] 
		self.cv = threading.Condition()
		self.cv_counter = 0

	def run(self):		
		self.start_time = int(time.time())
		fut_thrd = McastSndrThrd(sndr_port_=1501, mcast_addr_="224.168.2.9", mcast_port_=1600, fix_file_="/OMM/data/futures/ESFutures.log")
		fut_thrd.start()
		self.threads.append(fut_thrd) 
		opt_thrd = McastSndrThrd(sndr_port_=1502, mcast_addr_="224.168.2.10", mcast_port_=1601, fix_file_="/OMM/data/options/ESOptions.log")
		opt_thrd.start()
		self.threads.append(opt_thrd) 
	
	def close(self):
		for t1 in self.threads:
			if t1.isAlive():
				t1.join()

class McastRcvr:
	def __init__(self, any_="0.0.0.0", mcast_addr_="224.168.2.9", mcast_port_=1600): 
		self.ANY        = any_
		self.MCAST_ADDR = mcast_addr_
		self.MCAST_PORT = mcast_port_
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#allow multiple sockets to use the same PORT number
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		#Bind to the port that we know will receive multicast data
		self.sock.bind((self.ANY, self.MCAST_PORT))
		#tell the kernel that we are a multicast socket
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
		#Tell the kernel that we want to add ourselves to a multicast group
		#The address for the multicast group is the third param
		status = self.sock.setsockopt(socket.IPPROTO_IP,
				socket.IP_ADD_MEMBERSHIP,
				socket.inet_aton(self.MCAST_ADDR) + socket.inet_aton(self.ANY));
		self.sock.setblocking(0)
	
	def run(self):
		while 1:
			try:
				data, addr = self.sock.recvfrom(8192)
			except socket.error, (val, msg):
#				print "socket.error caught", val, msg
				pass
			else:
				print "FROM: ", addr
				print "DATA: ", data

if __name__ == "__main__":
	mcast_svr = McastSvr() 
	mcast_svr.run()
	mcast_svr.close()

