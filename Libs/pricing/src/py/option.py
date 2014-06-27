#!/usr/bin/python
###########################################################
#  python option class 
#  convert python option class to C++ option class 
###########################################################

import os
import liboqr_py as oqr
import option_util as util

class AmOption(oqr.AmOption):
	PCT_CHG_GREEKS = .001

	def __init__(self, cp_type_ = "", trade_date_ = 0, exp_date_ = 0, \
			T_ = 0., S_ = 0., K_ = 0., sigma_ = 0., r_ =0., q_ = 0., price_impl_vol_ = 0.): 
		if trade_date_ != 0 and exp_date_ != 0:
			oqr.AmOption.__init__(self, util.str2cp_type(cp_type_), util.str2qlDate(str(trade_date_)), \
							util.str2qlDate(str(exp_date_)), S_, K_, sigma_, r_, q_) 
		else:
			oqr.AmOption.__init__(self, util.str2cp_type(cp_type_), S_, K_, T_, sigma_, r_, q_) 

		self.price_impl_vol = price_impl_vol_
		self.impl_vol       = .0
		self.delta          = .0
		self.vega           = .0
		self.gamma          = .0
		self.theta          = .0
		self.rho            = .0 

	def setSigma(self, sigma_):
		self.sigma = sigma_

	def print_out(self):
		print "ex_style=AMERICAN", "cp_type=", util.cp_type2str(self.cp_type), \
			"trade_date=", util.qlDate2str(self.valueDate), "exp_date=", util.qlDate2str(self.maturityDate), \
			"T=", self.T, "S=", self.S, "K=", self.K, "sigma=", self.sigma, "r=", self.r, "q=", self.q, \
			"price=", self.price, "price_impl_vol=", self.price_impl_vol, "impl_vol=", self.impl_vol 
	
	def print_greeks(self): 
		print "delta=%f gamma=%f vega=%f theta=%f rho=%f" %(self.delta, self.gamma, self.vega, self.theta, self.rho) 

	def calcPrice(self): 
		super(AmOption, self).calcPrice()
		return self.price 	

	def calcImplVol(self, price_ = 0.):
		if price_ <= 0.: 
			self.impl_vol = super(AmOption, self).calcImplVol(self.price_impl_vol)
		else:
			self.impl_vol = super(AmOption, self).calcImplVol(price_)
		return self.impl_vol 

	def calcDelta(self): 
		oqr.Option.calcDelta(self, self.PCT_CHG_GREEKS)
		self.delta = self.greeks.delta
		return self.delta

	def calcVega(self): 
		oqr.Option.calcVega(self, self.PCT_CHG_GREEKS)
		self.vega = self.greeks.vega
		return self.vega
	
	def calcGamma(self): 
		oqr.Option.calcGamma(self, self.PCT_CHG_GREEKS)
		self.gamma = self.greeks.gamma
		return self.gamma

	def calcTheta(self): 
		oqr.Option.calcTheta(self, self.PCT_CHG_GREEKS)
		self.theta = self.greeks.theta
		return self.theta

	def calcRho(self): 
		oqr.Option.calcRho(self, self.PCT_CHG_GREEKS)
		self.rho = self.greeks.rho
		return self.rho

if __name__ == "__main__": 
#	option1 = Option(ex_style_ = "AMERICAN", cp_type_ = "PUT", \
#		T_ = 1., S_ = 36, K_ = 40, sigma_ = .2, r_ = .06, q_ = .06, price_impl_vol_ = 6) 
#	option1.calcPrice()	
#	option1.calcImplVol() 
#	option1.print_out()
#	print "price=", option1.price, "impl_vol=", option1.impl_vol 

	option2 = AmOption(cp_type_ = "CALL", trade_date_ = 20140301, exp_date_ = 20140321, \
			S_ = 1866., K_ = 1865., sigma_ = .0, r_ = .00155, q_ = .00155, price_impl_vol_ = 11.121) 
	option2.print_out()
	iv = option2.calcImplVol() 
	option2.setSigma(iv)
	option2.calcDelta() 
	option2.calcVega() 
	option2.calcGamma() 
	option2.calcTheta() 
	option2.calcRho() 
	print "#############IV=", iv
	option2.calcPrice()
	option2.print_out()
	option2.print_greeks()

