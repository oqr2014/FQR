#!/usr/bin/python

import os
from liboqr_py import * 

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

def str2Date(str_): 
	#format: MM/DD/YYYY e.g. 03/1/2014
	ll = str_.split("/")
	if len(ll)!=3: 
		print str, " can't convert to Date"
		raise Exception("Error: str2Date() failed!")
	return Date( int(ll[1]), int2Month(int(ll[0])), int(ll[2]) )


if __name__ == "__main__": 
	m = int2Month(10)
	print m
	t = str2call_put("CALL")
	print t 
	d = str2Date("03/1/2014")
	print "day=", d.dayOfMonth(), "month=", d.month(), "year=", d.year()


