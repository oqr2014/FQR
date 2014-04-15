#!/bin/bash
#########################################################
# this is a test program for multicasting fix msgs
#########################################################
import socket
import time

class McastServer:
	def __init__(self, any_="0.0.0.0", sender_port_=1501, mcast_addr_="224.168.2.9", mcast_port_=1600):
		self.ANY         = any_
		self.SENDER_PORT = sender_port_ 
		self.MCAST_ADDR  = mcast_addr_
		self.MCAST_PORT  = mcast_port_
		
	def run(self): 
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#The sender is bound on (0.0.0.0:1501)
		sock.bind((self.ANY, self.SENDER_PORT))
		#Tell the kernel that we want to multicast and that the data is sent
		#to everyone (255 is the level of multicasting)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		while 1:
#			inf=open('/OMM/data/futures/futures_fix.log', "r")
			inf=open('/OMM/data/futures/ESFutures.log', "r")
			for line in inf:
				sock.sendto(line, (self.MCAST_ADDR, self.MCAST_PORT));
#			time.sleep(.01)
			inf.close()
			
class McastClient:
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
		self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
		#Tell the kernel that we want to add ourselves to a multicast group
		#The address for the multicast group is the third param
		status = self.sock.setsockopt(socket.IPPROTO_IP,
				socket.IP_ADD_MEMBERSHIP,
				socket.inet_aton(self.MCAST_ADDR) + socket.inet_aton(self.ANY));
		self.sock.setblocking(0)
	
	def run(self):
		while 1:
			try:
				data, addr = self.sock.recvfrom(1024)
			except socket.error, (val, msg):
#				print "socket.error caught", val, msg
				pass
			else:
				print "FROM: ", addr
				print "DATA: ", data


if __name__ == "__main__":
	mcast_svr = McastServer() 
	mcast_svr.run()

