#!/usr/bin/python
############################################
# Futures Quote Client 
#
############################################
import socket
import random
import wx
import threading
from futures_attr import * 
from option_attr import *
from option_fix import *
from xml_conf import *

class FutQuoteCli:
	def __init__(self, sfid_="0"):
		gui_conf = GUIQuoteXmlConf(quotes_name_="FUTURES")
		self.HOST = gui_conf.host
		self.PORT = gui_conf.port
		self.sfid = sfid_
		# SOCK_STREAM == a TCP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setblocking(1)
		self.sock.settimeout(None)
		self.sock.connect((self.HOST, self.PORT))
		
	def run(self):
		print "sending data => [%s]" % (self.sfid)
		self.sock.send(self.sfid+'\x03')
		tail = ""
		while 1:
			recv_data = self.sock.recv(4096)  
			print "[%s]" % (recv_data)
			if len(recv_data) > 0:
				recv_data = tail + recv_data
				(orders, tail) = FixMsg.str2order(recv_data)
				
			print "[%s]" % (recv_data)
		self.sock.close()

class FutDataEvent(wx.PyEvent):
	def __init__(self, wxeid_, data_):
		wx.PyEvent.__init__(self)
		self.SetEventType(wxeid_)
		self.data = data_

class FutQuoteThread(threading.Thread):
	def __init__(self, notify_win_, exp_date_=20140321):
		threading.Thread.__init__(self)
		self.wxeid       = wx.NewId()
		self.notify_win  = notify_win_
		self.stop        = threading.Event()
		self.fut_attr_ps = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
		self.exp_date    = exp_date_ 
		self.exp_date_changed = threading.Event()
		self.fid        = self.fut_attr_ps.exp_date_dict[self.exp_date].fid
		self.fquote     = FutQuoteCli()
#		self.setDaemon(True)
		self.start()
	
	def run(self):
		self.fquote.sock.send(str(self.fid)+'\x03')
		tail = "" 
		while not self.stop.is_set():
			if self.exp_date_changed.is_set():
				self.fquote.sock.send(str(self.fid)+'\x03')
				self.exp_date_changed.clear()
			recv_data = self.fquote.sock.recv(4096)
#			print "recv data=>", recv_data
			if len(recv_data) > 0:
				recv_data = tail + recv_data
				(orders, tail) = FixMsg.str2order(recv_data) 
				if len(orders) > 0:
#					print len(orders), "futures orders posted" 
					wx.PostEvent(self.notify_win, FutDataEvent(self.wxeid, orders))

#		self.fquote.sock.shutdown(socket.SHUT_RDWR)
		self.fquote.sock.close() 
		
	def shutdown(self):
		self.stop.set() 
	
	def set_exp_date_changed(self):
		if self.exp_date in self.fut_attr_ps.exp_date_dict.keys(): 
			self.fid  = self.fut_attr_ps.exp_date_dict[self.exp_date].fid
			self.exp_date_changed.set()
		else:
			print "####Error:exp_date not found:", str(self.exp_date)
			self.shutdown()

if __name__ == "__main__":
	futAttr  = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
	exp_date = 20140321
	fid      = futAttr.exp_date_dict[exp_date].fid 
	client   = FutQuoteCli(sfid_=str(fid))
	client.run()

