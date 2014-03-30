#!/usr/bin/python
####################################################
# Parse FIX message and option attributions 
# Normalize data for pricing 
####################################################

import os
from option_attr import *
from futures_attr import * 
from option_fix import *


if __name__ == "__main__":
	optionAttr = OptionAttrParser(filename_="/OMM/data/ES_20140321.xml")
	futuresAttr = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
	optionFix = FixMsgParser(filename_='/OMM/data/ESOptions.log', filter_=optionAttr.oid_dict)
	futuresFix = FixMsgParser(filename_='/OMM/data/futures/ESFutures.log', filter_=futuresAttr.fid_dict)
	for order in optionFix.orders:
		order.entry_time 
	
