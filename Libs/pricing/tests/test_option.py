#!/usr/bin/python
###############################################
# test C++ pricing lib's python wrapper 
###############################################
import os 
from liboqr_py import * 
from option_util import * 

class TestOption:
	def __init__(self, inFile_="./inputs/TestOption.txt", outFile_="./py_outs/TestOption.out"):
		self.PCT_CHANGE_GREEKS=.001
		self.inFile=inFile_
		self.outFile=outFile_
		self.options=[]
		self.prices_impl_vol=[]
		self.impl_vols=[]
		self.read_option_file()
		self.calc()
		self.write_option_file() 

	def calc(self): 
		for opt, price in zip(self.options, self.prices_impl_vol): 
			opt.calcPrice()
			opt.calcDelta(self.PCT_CHANGE_GREEKS)
			opt.calcVega(self.PCT_CHANGE_GREEKS)
			opt.calcGamma(self.PCT_CHANGE_GREEKS)
			opt.calcTheta(self.PCT_CHANGE_GREEKS)
			opt.calcRho(self.PCT_CHANGE_GREEKS)
			impl_vol = opt.calcImplVol(price)
			self.impl_vols.append(impl_vol)
			print opt.ex_style, opt.cp_type, opt.price, opt.greeks.delta, \
			opt.greeks.vega, opt.greeks.gamma, opt.greeks.theta, opt.greeks.rho, impl_vol

	def write_option_file(self): 
		print "done!"

	def read_option_file(self):
		options = []
		ins = open(self.inFile, "r")
		for line in ins:
			ll = line.split()
			if len(ll)==0 or ll[0][0]=='#': 
				continue
			if ll[0]=="EUROPEAN":
				if len(ll)==9:
					self.options.append( EuroOption(str2call_put(ll[1]), float(ll[2]), float(ll[3]), \
								float(ll[4]), float(ll[5]), float(ll[6]), float(ll[7])) )
					self.prices_impl_vol.append( float(ll[8]) )
				elif len(ll)==10:
					self.options.append( EuroOption(str2call_put(ll[1]), str2Date(ll[2]), str2Date(ll[3]), \
								float(ll[4]), float(ll[5]), float(ll[6]), float(ll[7]), float(ll[8])) )
					self.prices_impl_vol.append( float(ll[9]) )
			elif ll[0]=="AMERICAN": 
				if len(ll)==9:
					self.options.append( AmOption(str2call_put(ll[1]), float(ll[2]), float(ll[3]), \
								float(ll[4]), float(ll[5]), float(ll[6]), float(ll[7])) )
					self.prices_impl_vol.append( float(ll[8]) )
				elif len(ll)==10:
					self.options.append( AmOption(str2call_put(ll[1]), str2Date(ll[2]), str2Date(ll[3]), \
								float(ll[4]), float(ll[5]), float(ll[6]), float(ll[7]), float(ll[8])) )
					self.prices_impl_vol.append( float(ll[9]) )
		ins.close()

if __name__ == "__main__":
	test_option = TestOption()
