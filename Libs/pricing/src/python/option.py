#!/usr/bin/python
###########################################################
#  python option class 
#  convert python option class to C++ option class 
###########################################################

import os
from liboqr_py import *
from option_util import * 

class Option:
	def __init__(self, ex_style_ = "", cp_type_ = "", trade_date_ = 0, exp_date_ = 0, \
			T_ = 0., S_ = 0., K_ = 0., sigma_ = 0., r_ =0., q_ = 0., price_impl_vol_ = 0.): 
		self.PCT_CHANGE_GREEKS = .001
		self.ex_style   = ex_style_
		self.cp_type    = cp_type_
		self.trade_date = trade_date_   # int type in python 
		self.exp_date   = exp_date_     # int type 
		self.T          = T_
		self.S          = S_ 
		self.K          = K_
		self.sigma      = sigma_
		self.r          = r_
		self.q          = q_
		self.price_impl_vol = price_impl_vol_

		self.option   = None
		self.price    = 0. 
		self.impl_vol = 0. 
		self.delta    = 0.
		self.vega     = 0. 
		self.gamma    = 0.
		self.theta    = 0. 
		self.rho      = 0.

		if self.ex_style == "EUROPEAN":
			self.create_euro_option()
		elif self.ex_style == "AMERICAN": 
			self.create_am_option()
		else: 
			print "Error: excise style: ", self.ex_style, "invalid"
			raise Exception("Option::__init__ failed")
			
	def create_euro_option(self):
		if self.trade_date != 0 and self.exp_date != 0: 
			self.option = EuroOption(str2call_put(self.cp_type), str2qlDate(str(self.trade_date)), \
				str2qlDate(str(self.exp_date)), self.S, self.K, self.sigma, self.r, self.q) 
		else:
			self.option = EuroOption(str2call_put(self.cp_type), self.S, self.K, self.T, self.sigma, self.r, self.q) 

	def create_am_option(self): 
		if self.trade_date != 0 and self.exp_date != 0: 
			self.option = AmOption(str2call_put(self.cp_type), str2qlDate(str(self.trade_date)), \
				str2qlDate(str(self.exp_date)), self.S, self.K, self.sigma, self.r, self.q) 
		else:
			self.option = AmOption(str2call_put(self.cp_type), self.S, self.K, self.T, self.sigma, self.r, self.q) 

	def calcPrice(self): 
		self.option.calcPrice()
		self.price = self.option.price 
		return self.price 	

	def calcImplVol(self, price_ = 0.):
		if price_ <= 0.: 
			self.impl_vol = self.option.calcImplVol(self.price_impl_vol)
		else:
			self.impl_vol = self.option.calcImplVol(price_)
		return self.impl_vol 

	def calcDelta(self): 
		self.option.calcDelta(self.PCT_CHANGE_GREEKS)
		self.delta = self.option.greeks.delta
		return self.delta

	def calcVega(self): 
		self.option.calcVega(self.PCT_CHANGE_GREEKS)
		self.vega = self.option.greeks.vega
		return self.vega
	
	def calcGamma(self): 
		self.option.calcGamma(self.PCT_CHANGE_GREEKS)
		self.gamma = self.option.greeks.gamma
		return self.gamma

	def calcTheta(self): 
		self.option.calcTheta(self.PCT_CHANGE_GREEKS)
		self.theta = self.option.greeks.theta
		return self.theta

	def calcRho(self): 
		self.option.calcRho(self.PCT_CHANGE_GREEKS)
		self.rho = self.option.greeks.rho
		return self.rho

if __name__ == "__main__": 
	option1 = Option(ex_style_ = "AMERICAN", cp_type_ = "PUT", \
				T_ = 1., S_ = 36, K_ = 40, sigma_ = .2, r_ = .06, q_ = .06, price_impl_vol_ = 6) 
	option1.calcPrice()	
	option1.calcImplVol() 
	print "price=", option1.price, "impl_vol=", option1.impl_vol 

	option2 = Option(ex_style_ = "AMERICAN", cp_type_ = "PUT", trade_date_ = 20140301, exp_date_ = 20150317, \
				S_ = 36, K_ = 40, sigma_ = .2, r_ = .06, q_ = .06, price_impl_vol_ = 6) 
	option2.calcPrice()	
	option2.calcImplVol() 
	print "price=", option2.price, "impl_vol=", option2.impl_vol 


