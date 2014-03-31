#!/usr/bin/python
###############################################
# test C++ pricing lib's python wrapper 
###############################################
import os 
from liboqr_py import * 
from option_util import * 
from option import * 

def strDate2Int(str_):
#format: MM/DD/YYYY e.g. 03/1/2014, return 20140301
	ll = str_.split("/")
	if len(ll) != 3: 
		print str_, " can't convert to int date"
		raise Exception("Error: strDate2Int() failed!")
	i = int(ll[2])*10000 + int(ll[0])*100 + int(ll[1])
	return i 

class TestOption:
	def __init__(self, inFile_="./inputs/TestOption.txt", outFile_="./py_outs/TestOption.out"):
		self.inFile=inFile_
		self.outFile=outFile_
		self.options=[]
		self.read_option_file()
		self.calc()
		self.write_option_file() 

	def calc(self): 
		for opt in self.options: 
			opt.calcPrice()
			opt.calcDelta()
			opt.calcVega()
			opt.calcGamma()
			opt.calcTheta()
			opt.calcRho()
			opt.calcImplVol()
			print opt.ex_style, opt.cp_type, opt.price, opt.delta, opt.vega, opt.gamma, opt.theta, opt.rho, opt.impl_vol

	def write_option_file(self): 
		outs = open(self.outFile, "w")
		for opt in self.options: 
			print >> outs, opt.ex_style, opt.cp_type, opt.price, \
				opt.delta, opt.vega, opt.gamma, opt.theta, opt.rho, opt.impl_vol
		outs.close()
		print "done!"

	def read_option_file(self):
		ins = open(self.inFile, "r")
		for line in ins:
			ll = line.split()
			if len(ll)==0 or ll[0][0]=='#': 
				continue
			if len(ll) == 9: 
				option = Option(ex_style_=ll[0], cp_type_=ll[1], T_=float(ll[4]), S_=float(ll[2]), K_=float(ll[3]), \
					sigma_=float(ll[5]), r_=float(ll[6]), q_=float(ll[7]), price_impl_vol_=float(ll[8]))
				self.options.append(option)
			elif len(ll) == 10: 
				option = Option(ex_style_=ll[0], cp_type_=ll[1], trade_date_=strDate2Int(ll[2]), exp_date_=strDate2Int(ll[3]), \
					S_=float(ll[4]), K_=float(ll[5]), sigma_=float(ll[6]), r_=float(ll[7]), q_=float(ll[8]), price_impl_vol_=float(ll[9]))
				self.options.append(option)
		ins.close()

if __name__ == "__main__":
	test_option = TestOption()
