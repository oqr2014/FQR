#!/bin/bash
#################################################################
# Test program for multicasting fix msgs of futures and options
#################################################################
import os 
import socket
import time
import threading
from fix import *
from xml_conf import *

class McastSndrThrd(threading.Thread):
	def __init__(self, sndr_port_, mcast_addr_, mcast_port_, fix_file_, start_time_):
		threading.Thread.__init__(self)
		self.ANY         = "0.0.0.0"
		self.SNDR_PORT   = sndr_port_ 
		self.MCAST_ADDR  = mcast_addr_
		self.MCAST_PORT  = mcast_port_
		self.fix_file    = fix_file_
		self.start_time  = start_time_
		
	def run(self): 
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#The sender is bound on (0.0.0.0:1501)
		sock.bind((self.ANY, self.SNDR_PORT))
		#Tell kernel that we want to multicast and data is sent
		#to everyone (255 is the level of multicasting)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
		if not os.path.isfile(self.fix_file):
			raise Exception("fix file: %s does not exist" %self.fix_file)
		
		bFirst = True
		while 1:
			et0 = 0
			in_f = open(self.fix_file, "r")
			for line in in_f:
				fixPs = FixMsgParser(str_ = line)
				if len(fixPs.orders) == 0:
					continue
				if bFirst:
					et0 = fixPs.orders[0].entry_time
					bFirst = False 
					sock.sendto(line, (self.MCAST_ADDR, self.MCAST_PORT))
					continue
				et = fixPs.orders[0].entry_time
				while 1:
					cts = int(time.time()) + 1
					if cts >= (self.start_time + et - et0):
						break
					time.sleep(.5)
				sock.sendto(line, (self.MCAST_ADDR, self.MCAST_PORT))
				time.sleep(.001)
			in_f.close()
			return 
			
class McastSvr(object):
	def __init__(self):
		self.threads = [] 

	def run(self):		
		gw_conf  = GatewayConf()
		fut_conf = McastXmlConf(quotes_name_="FUTURES")
		self.start_time = int(time.time()) + 1
		fut_thrd = McastSndrThrd(sndr_port_ = fut_conf.sender_port, mcast_addr_ = fut_conf.mcast_addr, \
					mcast_port_ = fut_conf.mcast_port, fix_file_ = gw_conf.fut_fixmsg, start_time_ = self.start_time)
		fut_thrd.start()
		self.threads.append(fut_thrd) 
		
		opt_conf = McastXmlConf(quotes_name_="OPTIONS")
		opt_thrd = McastSndrThrd(sndr_port_ = opt_conf.sender_port, mcast_addr_ = opt_conf.mcast_addr, \
					mcast_port_ = opt_conf.mcast_port, fix_file_ = gw_conf.opt_fixmsg, start_time_ = self.start_time)
		opt_thrd.start()
		self.threads.append(opt_thrd) 
	
	def close(self):
		for t1 in self.threads:
			if t1.isAlive():
				t1.join()

class McastRcvr:
	def __init__(self, any_ = "0.0.0.0", mcast_addr_ = "", mcast_port_ = 0): 
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

