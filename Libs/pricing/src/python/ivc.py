#!/usr/bin/python
##########################################################
# Implied volatility curve class
##########################################################
import os
import threading 

class ImplVol:
	def __init__(self, price_=0., impl_vol_=0., ts_=0, is_dirty_=False, cp_type_=""):
		self.price    = price_
		self.impl_vol = impl_vol_
		self.ts       = ts_
		self.is_dirty = is_dirty_
		self.cp_type  = cp_type_
	
	def print_out(self): 
		print "price=%f, impl vol=%f, timestamp=%s, is_dirty=%s, cp_type=%s" \
				%(self.price, self.impl_vol, self.ts, self.is_dirty, self.cp_type)
		

class ImplVolCurve(object):
    def __init__(self):
		self.fut_exp_date = 0
		self.S            = 0.
		self.val_date     = 0	
		self.opt_exp_date = 0 
		self.put_K_dict   = {}  #key=Strike, value=ImplVol 
		self.call_K_dict  = {}  #key=Strike, value=ImplVol
		self.T            = 0.
		self.r            = 0. 
		self.q            = 0.


class OptionData(object):
    def __init__(self):
		self.fut_exp_date    = 0
		self.fut_bid         = 0.
		self.fut_ask         = 0.
		self.opt_exp_date    = 0 
		self.put_K_bid_dict  = {}  #key=Strike, value=ImplVol
		self.put_K_ask_dict  = {}  #key=Strike, value=ImplVol
		self.call_K_bid_dict = {}  #key=Strike, value=ImplVol
		self.call_K_ask_dict = {}  #key=Strike, value=ImplVol
		self.fut_lock        = threading.Lock()
		self.opt_lock        = threading.Lock()


if __name__ == '__main__':
	print "Implied volatility curve: "

