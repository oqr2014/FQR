#!/usr/bin/python
##################################################
# option utility functions 
##################################################

import os
from liboqr_py import * 
from datetime import datetime 

def int2Month(i_): 
	if i_ == 1:  
		return Month.Jan
	elif i_ == 2:
		return Month.Feb
	elif i_ == 3:
		return Month.Mar
	elif i_ == 4: 
		return Month.Apr
	elif i_ == 5: 
		return Month.May
	elif i_ == 6:
		return Month.Jun
	elif i_ == 7:
		return Month.Jul
	elif i_ == 8: 
		return Month.Aug
	elif i_ == 9: 
		return Month.Sep
	elif i_ == 10: 
		return Month.Oct
	elif i_ == 11: 
		return Month.Nov
	elif i_ == 12: 
		return Month.Dec
	else: 
		print "invalid Month:", i_
		raise Exception("Error: int2Month failed")

def str2call_put(str_): 
	if str_ == "PUT": 
		return Option.Type.PUT
	elif str_ == "CALL": 
		return Option.Type.CALL
	else:
		print "invalid call/put type:", str_
		raise Exception("Error: str2call_put failed")

def str2qlDate(str_, format_="%Y%m%d"): 
	#default format: YYYYMMDD e.g. 20140321
	d1 = datetime.strptime(str_, format_)
	return Date(d1.day, int2Month(d1.month), d1.year)
	

if __name__ == "__main__": 
	m = int2Month(10)
	print m
	t = str2call_put("CALL")
	print t 
	d = str2qlDate("03/1/2014")
	print "day=", d.dayOfMonth(), "month=", d.month(), "year=", d.year()


