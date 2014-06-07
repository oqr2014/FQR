#!/usr/bin/python
import os 
from xml.dom import minidom 

class GatewayConf:
	fut_exp_dt = 0
	fut_sym    = ""
	fut_fixmsg = "" 
	opt_exp_dt = 0
	opt_sym    = ""
	opt_fixmsg = ""

	def __init__(self, xml_file_="gateway.xml"):
		xml_path = os.environ.get("XML_CONF_DIR")
		xml_path += xml_file_
		if not os.path.exists(xml_path):
			msg = "####ERROR#### " + xml_path + " does not exists!"
			raise Exception(msg)
			
		dom = minidom.parse(xml_path)
		conf = dom.getElementsByTagName('FUTURES')[0]
		self.fut_exp_dt = int(conf.getElementsByTagName('EXP_DATE')[0].childNodes[0].nodeValue) 
		self.fut_sym    = conf.getElementsByTagName('SYMBOL')[0].childNodes[0].nodeValue 
		self.fut_fixmsg = conf.getElementsByTagName('FIXMSG')[0].childNodes[0].nodeValue 

		conf = dom.getElementsByTagName('OPTIONS')[0]
		self.opt_exp_dt = int(conf.getElementsByTagName('EXP_DATE')[0].childNodes[0].nodeValue) 
		self.opt_sym    = conf.getElementsByTagName('SYMBOL')[0].childNodes[0].nodeValue 
		self.opt_fixmsg = conf.getElementsByTagName('FIXMSG')[0].childNodes[0].nodeValue 

	def printout(self):
		print "Gateway conf: " 
		print "futures: exp_date=%d symbol=%s fixmsg=%s" %(self.fut_exp_dt, self.fut_sym, self.fut_fixmsg) 
		print "options: exp_date=%d symbol=%s fixmsg=%s" %(self.opt_exp_dt, self.opt_sym, self.opt_fixmsg) 

class McastXmlConf:
	quotes = ""
	sender_port = 0 
	mcast_addr  = "" 
	mcast_port  = 0

	def __init__(self, xml_file_="mcast_quote_svr.xml", quotes_name_=None):
		self.quotes = quotes_name_
		xml_path = os.environ.get("XML_CONF_DIR")
		xml_path += xml_file_
		if not os.path.exists(xml_path):
			msg = "####ERROR#### " + xml_path + " does not exists!"
			raise Exception(msg)
		if not self.quotes:
			msg = "####ERROR#### quotes name(futures or options) is not set"
			raise Exception(msg)
			
		dom = minidom.parse(xml_path)
		conf = dom.getElementsByTagName(self.quotes)[0]
		self.sender_port = int(conf.getElementsByTagName('sender_port')[0].childNodes[0].nodeValue) 
		self.mcast_addr  = conf.getElementsByTagName('mcast_address')[0].childNodes[0].nodeValue 
		self.mcast_port  = int(conf.getElementsByTagName('mcast_port')[0].childNodes[0].nodeValue)

	def printout(self):
		print "Multicast config: ", self.quotes
		print "sender_port=%d mcast_addr=%s mcast_port=%d" %(self.sender_port, self.mcast_addr, self.mcast_port) 
		

class GUIQtXmlConf:
	quotes = ""
	host  = "" 
	port  = 0

	def __init__(self, xml_file_="gui_quote_svr.xml", quotes_name_=None):
		self.quotes = quotes_name_
		xml_path = os.environ.get("XML_CONF_DIR")
		xml_path += xml_file_
		if not os.path.exists(xml_path):
			msg = "####ERROR#### " + xml_path + " does not exists!"
			raise Exception(msg)
		if not quotes_name_:
			msg = "####ERROR#### quotes name(futures or options) is not set"
			raise Exception(msg)
			
		dom = minidom.parse(xml_path)
		conf = dom.getElementsByTagName(self.quotes)[0]
		self.host  = conf.getElementsByTagName('host')[0].childNodes[0].nodeValue 
		self.port  = int(conf.getElementsByTagName('port')[0].childNodes[0].nodeValue)

	def printout(self):
		print "GUI quotes config: ", self.quotes
		print 'host=%s port=%d' %(self.host, self.port) 

if __name__ == "__main__": 
	gw_conf = GatewayConf()
	gw_conf.printout()

	fut_conf = McastXmlConf(quotes_name_="FUTURES")
	fut_conf.printout()
	opt_conf = McastXmlConf(quotes_name_="OPTIONS")
	opt_conf.printout()

	fut_gui_conf = GUIQtXmlConf(quotes_name_="FUTURES")
	fut_gui_conf.printout()
	opt_gui_conf = GUIQtXmlConf(quotes_name_="OPTIONS")
	opt_gui_conf.printout()

