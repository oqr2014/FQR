#!/usr/bin/python
#################################################################################################
# FIX parser
# FIX tags: 
# 48=SecurityID
# 52=SendingTime
# 75=TradeDate
# 268=NoMDEntries: Number of entries in Market Data message, NOT USED
# 269=MDEntryType: bid=0, offer=1 trade=2
# 270=price
# 271=quantity
# 273=MDEntryTime: Time of Market Data Entry
# 279=MDUpdateAction: Type of Market Data update action. '0'=New '1'=Change '2'=Delete
#t 1023=MDPriceLevel: book level top level=1
# 
# parse and selected MD: 
# () order starts with tag 279
# () Select 269=0/1, 279=1 and 1023=1, i.e. select top level bid/ask orders.
#################################################################################################

import os 

def timeStr2Sec(str_): # time string format HH:MM::SS e.g. 14:53:01 
	ll = str_.split(':')
	try: 
		s = int(ll[0]) * 3600 + int(ll[1]) * 60 + int(ll[2])
	except ValueError: 
		pass
#		print "## timeStr2Sec VALUEERROR CAUGHT for $$", str_, "$$"
	except IndexError: 
		pass
#		print "## timeStr2Sec INDEXERROR CAUGHT for $$", str_, "$$"
	else:
		return s

def sec2TimeStr(sec_): 
	hour = sec_ / 3600
	sec_ = sec_ % 3600 
	minute = sec_ / 60 
	sec = sec_ % 60
	ss = str(hour).zfill(2)+":"+str(minute).zfill(2)+":"+str(sec).zfill(2)
	return (ss)

class FixMsg: 
	def __init__(self, sid_, send_time_, trade_date_, \
				entry_type_, price_, quantity_, entry_time_, \
				update_action_, price_level_): 
		self.sid           = sid_
		self.send_time     = send_time_
		self.trade_date    = trade_date_
		self.entry_type    = entry_type_
		self.price         = price_
		self.quantity      = quantity_ 
		self.entry_time    = entry_time_
		self.update_action = update_action_
		self.price_level   = price_level_

	def printout(self): 
		print self.sid, self.send_time, self.trade_date, \
			self.entry_type, self.price, self.quantity, \
			self.entry_time, self.update_action, self.price_level

	def pack2str(self):
		ss = str(self.sid) + "\x01" + self.send_time + "\x01" + \
			str(self.trade_date) + "\x01" + str(self.entry_type) + "\x01" + \
			str(self.price) + "\x01" + str(self.quantity) + "\x01" + \
			str(self.entry_time) + "\x01" + str(self.price_level) + "\x03"
		return ss
	
	@staticmethod
	def str2order(str_): 
#TCP socket recv data contains order list or incomplete order 
		orders = [] 
		tail = ""
		strlist = str_.split('\x03')
		if str_[len(str_)-1] != '\x03': 
			tail = strlist[len(strlist)-1] 
			del strlist[-1]	
		for s1 in strlist: 
			ss = s1.split('\x01')
			try:
				orders.append( FixMsg(int(ss[0]), ss[1], int(ss[2]), \
						int(ss[3]), float(ss[4]), int(ss[5]), \
						int(ss[6]), 1, int(ss[7])) )
			except ValueError: 
				pass
#				print "## FixMsg.str2order VALUEERROR CAUGHT for $$", str_, "$$"
			except IndexError: 
				pass
#				print "## FixMsg.str2order INDEXERROR CAUGHT for $$", str_, "$$"
		return (orders, tail)

class FixMsgParser: 
	def __init__(self, str_=None, filename_=None, filter_=None):
		self.selected_trades = 0
		self.filter_by = filter_
		self.orders=[]
		if str_ is None: 
			if filename_ is None: 
				raise Exception('Error: please input a string or a filename')
			self.parse_fix_file(filename_)
		else:
			self.parse_fix_msg(str_)

	def parse_fix_msg(self, str_): 
		trades=str_.split("\x01279=")
		send_time = ""
		trade_date = 0 
		for i, trade in enumerate(trades):
			sid = 0
			entry_type = 99
			price = 0.
			quantity = 0
			update_action = 1
			price_level = 99 

			tags=trade.split("\x01")
			try:
				if i == 0: ### parse fix msg header 
					for tag in tags: 
						if "52=" in tag: 
							send_time = tag[3:]
						elif "75=" in tag: 
							trade_date = int(tag[3:])
				else: ### parse trade
					update_action = int(tags[0])	
					if update_action != 1: 
						continue 
					for tag in tags: 
						if "48=" in tag:
							sid = int(tag[3:])
						elif "269=" in tag: 
							entry_type = int(tag[4:])
						elif "270=" in tag: 
							price = float(tag[4:])
						elif "271=" in tag:
							quantity = int(tag[4:])
						elif "273=" in tag:
							entry_time = timeStr2Sec(tag[4:])
						elif "1023=" in tag:
							price_level = int(tag[5:])
			except ValueError: 
				pass
#				print "##parse_fix_msg: ValueERROR CAUGHT $$", str_, "$$"
			except IndexError: 
				pass
#				print "##parse_fix_msg: IndexERROR CAUGHT $$", str_, "$$"
			if (entry_type == 0 or entry_type == 1):
#and price_level == 1: open level 2 quotes temporarily, for options, we only need top level price. 
# Select 269=0/1, 279=1 and 1023=1, i.e. select top level bid/ask orders.
				if ( self.filter_by is None ) or self.filter_by.has_key(sid):
					fix_msg = FixMsg(sid, send_time, trade_date, entry_type, \
							price, quantity, entry_time, update_action, price_level) 
					self.selected_trades += 1
					self.orders.append(fix_msg)
#					print self.selected_trades
#					fix_msg.printout()

	def parse_fix_file(self, filename_): 
		ins=open(filename_, "r")
		for line in ins:
			self.parse_fix_msg(line)
		ins.close()

if __name__ == "__main__":
#	fixParser = FixMsgParser(filename_='/OMM/data/fix_options.log')
	fixParser = FixMsgParser(filename_='/OMM/data/futures/ESFutures.log')
	print "total selected trades=", fixParser.selected_trades
#	print fixParser.orders	

