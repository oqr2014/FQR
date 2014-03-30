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
# 1023=MDPriceLevel: book level top level=1
# 
# parse and selected MD: 
# () order starts with tag 279
# () Select 269=0/1, 279=1 and 1023=1, i.e. select top level bid/ask orders.
#################################################################################################

import os 

def getSec(s_):
	l = s_.split(':')
	return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

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

	def print_out(self): 
		print self.sid, self.send_time, self.trade_date, \
			self.entry_type, self.price, self.quantity, \
			self.entry_time, self.update_action, self.price_level

class FixMsgParser: 
	def __init__(self, str_=None, filename_=None, filter_=None):
		self.selected_trades = 0
		self.filter_by = filter_
		self.orders=[]
		if str_ is None: 
			if filename_ is None: 
				raise ArgumentError('Error: please input a string or a filename')
			self.parse_fix_file(filename_)
		else:
			self.parse_fix_msg(str_)

	def parse_fix_msg(self, str_): 
		trades=str_.split("279=1")
		send_time = ""
		trade_date = "" 
		for i, trade in enumerate(trades):
			sid = 0
			entry_type = 99
			price = 0.
			quantity = 0
			update_action = 1
			price_level = 99 

			tags=trade.split("\x01")
			if i==0:
				for tag in tags: 
					if "52=" in tag: 
						send_time = tag[3:]
					elif "75=" in tag: 
						trade_date = tag[3:]
			else:
				selected = True
				for tag in tags: 
					if "279=" in tag:
						selected = False
						break
					if "48=" in tag:
						sid = int(tag[3:])
					elif "269=" in tag: 
						entry_type = int(tag[4:])
					elif "270=" in tag: 
						price = float(tag[4:])
					elif "271=" in tag:
						quantity = int(tag[4:])
					elif "273=" in tag:
						entry_time = getSec(tag[4:])
					elif "1023=" in tag:
						price_level = int(tag[5:])
				if selected: 
					if ( entry_type == 0 or entry_type == 1 ) and price_level == 1: 
						fix_msg = None
						if ( self.filter_by is None ) or self.filter_by.has_key(sid):
							fix_msg = FixMsg(sid, send_time, trade_date, entry_type, \
									price, quantity, entry_time, update_action, price_level) 
							self.selected_trades += 1
							self.orders.append(fix_msg)
#							print self.selected_trades
#							fix_msg.print_out()

	def parse_fix_file(self, filename_): 
		ins=open(filename_, "r")
		for line in ins:
			self.parse_fix_msg(line)
		ins.close()

if __name__ == "__main__":
	fixParser = FixMsgParser(filename_='/OMM/data/ESOptions.log')
		
