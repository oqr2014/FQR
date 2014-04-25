#!/usr/bin/python
############################################
# Options Quote Client 
############################################
import socket
import random
import wx
import threading
from futures_attr import * 
from option_attr import *
from option_fix import *

class OptQuoteCli:
	def __init__(self, HOST_='localhost', PORT_=22086, sfid_="0"):
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
		tail = ""
		while 1:
			recv_data = self.sock.recv(1024)  
			print "[%s]" % (recv_data)
			if len(recv_data) > 0:
				recv_data = tail + recv_data
				(orders, tail) = FixMsg.str2order(recv_data)
			print "[%s]" % (recv_data)
		self.sock.close()

class OptDataEvent(wx.PyEvent):
	def __init__(self, wxeid_, data_):
		wx.PyEvent.__init__(self)
		self.SetEventType(wxeid_)
		self.data = data_

class OptQuoteThread(threading.Thread):
	def __init__(self, notify_win_, exp_date_=20140321):
		threading.Thread.__init__(self)
		self.wxeid      = wx.NewId()
		self.notify_win = notify_win_
		self.stop       = threading.Event()
		self.opt_attr_ps= OptionAttrParser(filename_="/OMM/data/ES_20140321.xml")
		self.exp_date   = exp_date_ 
		self.exp_date_changed = threading.Event()
		self.ids        = list(self.opt_attr_ps.oid_dict.keys())
		self.oquote     = OptQuoteCli()
#		self.setDaemon(True)
		self.start()
	
	def run(self):
		self.oquote.sock.send(",".join(map(str,self.ids)))
		tail = "" 
		while not self.stop.is_set():
			if self.exp_date_changed.is_set():
				self.oquote.sock.send(",".join(self.ids))
				self.exp_date_changed.clear()
			recv_data = self.oquote.sock.recv(1024)
#			print "recv data=>", recv_data
			if len(recv_data) > 0:
				recv_data = tail + recv_data
				(orders, tail) = FixMsg.str2order(recv_data) 
				if len(orders) > 0:
#					print len(orders), "orders posted"
					wx.PostEvent(self.notify_win, OptDataEvent(self.wxeid, orders))
#		self.fquote.sock.shutdown(socket.SHUT_RDWR)
		self.oquote.sock.close() 
		
	def shutdown(self):
		self.stop.set() 
	
	def set_exp_date_changed(self):
		pass
#		if self.exp_date in self.opt_attr.exp_date_dict.keys(): 
#			self.ids  = self.opt_attr.exp_date_dict[self.exp_date].ids
#			self.exp_date_changed.set()
#		else:
#			print "####Error:exp_date not found:", str(self.exp_date)
#			self.shutdown()

if __name__ == "__main__":
	optAttrPs = OptionAttrParser(filename_="/OMM/data/ES_20140321.xml")
	exp_date  = 20140321
#	fid       = futAttr.exp_date_dict[exp_date].fid 
#	client    = FutQuoteCli(sfid_=str(fid))
#	client.run()

