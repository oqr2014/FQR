#!/usr/bin/python
##################################################
# option utility functions 
##################################################

import os
import liboqr_py as oqr 
from datetime import datetime 

def int2Month(i_): 
	if i_ == 1:  
		return oqr.Month.Jan
	elif i_ == 2:
		return oqr.Month.Feb
	elif i_ == 3:
		return oqr.Month.Mar
	elif i_ == 4: 
		return oqr.Month.Apr
	elif i_ == 5: 
		return oqr.Month.May
	elif i_ == 6:
		return oqr.Month.Jun
	elif i_ == 7:
		return oqr.Month.Jul
	elif i_ == 8: 
		return oqr.Month.Aug
	elif i_ == 9: 
		return oqr.Month.Sep
	elif i_ == 10: 
		return oqr.Month.Oct
	elif i_ == 11: 
		return oqr.Month.Nov
	elif i_ == 12: 
		return oqr.Month.Dec
	else: 
		print "invalid Month:", i_
		raise Exception("Error: int2Month failed")

def month2Int(month_): 
	if month_ == oqr.Month.Jan:  
		return 1
	elif month_ == oqr.Month.Feb:
		return 2
	elif month_ == oqr.Month.Mar:
		return 3
	elif month_ == oqr.Month.Apr: 
		return 4
	elif month_ == oqr.Month.May: 
		return 5
	elif month_ == oqr.Month.Jun:
		return 6
	elif month_ == oqr.Month.Jul:
		return 7
	elif month_ == oqr.Month.Aug: 
		return 8
	elif month_ == oqr.Month.Sep: 
		return 9
	elif month_ == oqr.Month.Oct: 
		return 10
	elif month_ == oqr.Month.Nov: 
		return 11
	elif month_ == oqr.Month.Dec: 
		return 12
	else: 
		print "invalid Month:", month_
		raise Exception("Error: month2Int failed")

def str2cp_type(str_): 
	if str_ == "PUT": 
		return oqr.Option.Type.PUT
	elif str_ == "CALL": 
		return oqr.Option.Type.CALL
	else:
		print "invalid call/put type:", str_
		raise Exception("Error: str2cp_type failed")

def cp_type2str(type_): 
	if type_ == oqr.Option.Type.PUT:
		return "PUT"
	elif type_ == oqr.Option.Type.CALL: 
		return "CALL"
	else:
		print "invalid call/put type:", type_
		raise Exception("Error: cp_type2str failed")

def str2qlDate(str_, format_="%Y%m%d"): 
	#default format: YYYYMMDD e.g. 20140321
	d1 = datetime.strptime(str_, format_)
	return oqr.Date(d1.day, int2Month(d1.month), d1.year)
	
def qlDate2str(date_):
#string format: YYYYMMDD e.g. 20140321
	ss = str(date_.year()).zfill(4) + str(month2Int(date_.month())).zfill(2) + str(date_.dayOfMonth()).zfill(2)
	return ss

if __name__ == "__main__": 
	print int2Month(10)
	print month2Int(oqr.Month.Oct)

	print str2cp_type("CALL")
	print cp_type2str(oqr.Option.Type.CALL)

	d = str2qlDate("20140624")
	print "day=", d.dayOfMonth(), "month=", d.month(), "year=", d.year()
	ss = qlDate2str(d)
	print "date string=", ss


