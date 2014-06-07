#!/usr/bin/python
####################################################
# Parse FIX message and option attributions 
# Normalize data for pricing 
####################################################

import os
from option_attr import *
from futures_attr import * 
from option_fix import *
from liboqr_py import *
from opton_util import * 
from option import * 


class OptionChain:
	def __init__(self, optFixParser_, futFixParser_, optAttrParser_):
		self.optFixParser  = optFixParser_
		self.futFixParser  = futFixParser_
		self.optAttrParser = optAttrParser_
		self.K_puts = {} 
		self.K_calls = {} 
		self.build_option_chain()
			
	def build_option_chain(self): 
		i = 0
		for order in self.optFixParser.orders:
			optAttr = optAttrParser.oid_dict[order.sid]
			while (i < len(self.futFixParser.orders)):
				optAttr.fid
				i += 1
			if optAttr.cp_type == "P":
				self.K_puts[optAttr.strike] = Option(ex_style_=optAttr.ex_style, cp_type_="PUT", trade_date_=order.trade_date, \
					exp_date_=optAttr.exp_date, S_= \
					)
			else:
				self.K_calls[optAttr.strike] = 
		
if __name__ == "__main__":
	optAttrParser = OptionAttrParser(filename_="/OMM/data/ES_20140321.xml")
	futAttrParser = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
	optionAttrParser.set_underlying_fids(futuresAttr.exp_date_dict)
	optFixParser = FixMsgParser(filename_='/OMM/data/options_fix.log', filter_=optAttrParser.oid_dict)
	futFixParser = FixMsgParser(filename_='/OMM/data/futures/futures_fix.log', filter_=futAttrParser.fid_dict)
		
