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

class OptionData: 
	def __init__(self, ):
		 
class OptionChain:
	def __init__(self, optFixParser_, futFixParser_, optAttrParser_):
		self.optFixParser  = optFixParser_
		self.futFixParser = futFixParser_
		self.optAttrParser  = optAttrParser_
		self.strike_dict = {} 
		self.build_option_chain()
	
	def build_option_chain(self): 
		for order in self.optFixParser.orders:
			strike = self.optAttrParser.oid_dict[order.sid].strike
			self.strike_dict 
		

if __name__ == "__main__":
	optAttrParser = OptionAttrParser(filename_="/OMM/data/ES_20140321.xml")
	futAttrParser = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
	optionAttrParser.set_underlying_fids(futuresAttr.exp_date_dict)
	optFixParser = FixMsgParser(filename_='/OMM/data/options_fix.log', filter_=optAttrParser.oid_dict)
	futFixParser = FixMsgParser(filename_='/OMM/data/futures/futures_fix.log', filter_=futAttrParser.fid_dict)
		
				
