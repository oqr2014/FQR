#!/usr/bin/python
#################################################################
# Test program for multicasting fix msgs of options 
#################################################################
import socket
import time
from option_fix import *
from option_attr import *

class McastServer:
	def __init__(self, any_="0.0.0.0", sender_port_=1502, mcast_addr_="224.168.2.10", mcast_port_=1601):
		self.ANY         = any_
		self.SENDER_PORT = sender_port_ 
		self.MCAST_ADDR  = mcast_addr_
		self.MCAST_PORT  = mcast_port_
		self.optAttrParser = OptionAttrParser(filename_="/OMM/data/ES_20140321.xml")
		
	def run(self): 
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		#The sender is bound on (0.0.0.0:1501)
		sock.bind((self.ANY, self.SENDER_PORT))
		#Tell kernel that we want to multicast and data is sent
		#to everyone (255 is the level of multicasting)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
		while 1:
			inf=open('/OMM/data/ESOptions.log', "r")
			for line in inf:
				fixParser = FixMsgParser(str_=line)
				selected = False
				for order in fixParser.orders: 
					if order.price_level == 1 and order.sid in self.optAttrParser.oid_dict.keys():
						selected = True
						break
				if selected: ## only top price level and exp date is 20140321
#					print line 
					sock.sendto(line, (self.MCAST_ADDR, self.MCAST_PORT));
					time.sleep(.01)
			inf.close()
			
if __name__ == "__main__":
	mcast_svr = McastServer() 
	mcast_svr.run()

