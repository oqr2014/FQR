#!/usr/bin/python
############################################
# Options Quote Client 
############################################
import socket
import random
import wx
import threading
from fut_attr import * 
from opt_attr import *
from fix import *
from xml_conf import *

class OptQtCli:
	def __init__(self, sfid_="0"):
		gui_conf = GUIQtXmlConf(quotes_name_="OPTIONS")
		self.HOST = gui_conf.host
		self.PORT = gui_conf.port
		self.sfid = sfid_
		# SOCK_STREAM == a TCP socket
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setblocking(1)
		self.sock.settimeout(None)
		self.sock.connect((self.HOST, self.PORT))
		
class OptDataEvt(wx.PyEvent):
	def __init__(self, wxeid_, data_):
		wx.PyEvent.__init__(self)
		self.SetEventType(wxeid_)
		self.data = data_

class OptQtThrd(threading.Thread):
	def __init__(self, notify_win_, exp_date_ = 0):
		threading.Thread.__init__(self)
		self.wxeid       = wx.NewId()
		self.notify_win  = notify_win_
		self.stop        = threading.Event()
		gw_conf          = GatewayConf()
		self.opt_attr_ps = OptAttrParser(filename_ = gw_conf.opt_sym)
		self.exp_date    = exp_date_ 
		self.exp_date_changed = threading.Event()
		self.ids         = list(self.opt_attr_ps.oid_dict.keys())
		self.oquote      = OptQtCli()
#		self.setDaemon(True)
		self.start()
	
	def run(self):
		ids_str = ",".join(map(str,self.ids)) + '\x03'
		self.oquote.sock.send(ids_str)
		tail = "" 
		while not self.stop.is_set():
			if self.exp_date_changed.is_set():
				ids_str = ",".join(map(str,self.ids)) + '\x03'
				self.oquote.sock.send(ids_str)
				self.exp_date_changed.clear()
			recv_data = self.oquote.sock.recv(4096)
#			print "recv data=>", recv_data
			if len(recv_data) > 0:
				recv_data = tail + recv_data
				(orders, tail) = FixMsg.str2order(recv_data) 
				if len(orders) > 0:
#					print len(orders), "option orders posted"
					wx.PostEvent(self.notify_win, OptDataEvt(self.wxeid, orders))
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
	gw_conf   = GatewayConf()
	optAttrPs = OptAttrParser(filename_ = gw_conf.fut_sym)
	exp_date  = 20140321
#	fid       = futAttr.exp_date_dict[exp_date].fid 
#	client    = FutQuoteCli(sfid_=str(fid))
#	client.run()

