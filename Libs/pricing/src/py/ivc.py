#!/usr/bin/python
##########################################################
# Implied volatility curve classes
##########################################################
import os
import threading 
import numpy as np
from option import *

# Implied volatility class 
class ImplVol:
	def __init__(self, price_ = 0., impl_vol_ = 0., ts_ = 0, is_dirty_ = False, cp_type_ = "", delta_ = 0.):
		self.price    = price_
		self.impl_vol = impl_vol_
		self.ts       = ts_
		self.is_dirty = is_dirty_
		self.cp_type  = cp_type_
		self.delta    = delta_
	
	def print_out(self): 
		print "price=%f, impl vol=%f, timestamp=%s, is_dirty=%s, cp_type=%s, delta=%f" \
				%(self.price, self.impl_vol, self.ts, self.is_dirty, self.cp_type, self.delta)

# Implied volatility curve class 
class ImplVolCurve(object):
    def __init__(self):
		self.fut_exp_date = 0
		self.S            = 0.
		self.val_date     = 0	
		self.opt_exp_date = 0 
		self.put_K_dict   = {}  #key=Strike, value=ImplVol 
		self.call_K_dict  = {}  #key=Strike, value=ImplVol
		self.T            = 0.
		self.r            = 0. 
		self.q            = 0.
		self.minK         = -1.e5
		self.maxK         = 1.e5  

# Option data class is used for calculating implied volatility curve 
class OptionData(object):
    def __init__(self):
		self.fut_exp_date    = 0
		self.fut_bid         = 0.
		self.fut_ask         = 0.
		self.opt_exp_date    = 0 
		self.put_K_bid_dict  = {}  #key=Strike, value=ImplVol
		self.put_K_ask_dict  = {}  #key=Strike, value=ImplVol
		self.call_K_bid_dict = {}  #key=Strike, value=ImplVol
		self.call_K_ask_dict = {}  #key=Strike, value=ImplVol
		self.fut_lock        = threading.Lock()
		self.opt_lock        = threading.Lock()

class FitIvc(object):
	opt_data   = None
	ivc_data   = None
	Ks         = []
	ivs        = []
	fitted_ivs = []

	def __init__(self, opt_data_=None, ivc_data_=None):
		self.opt_data = opt_data_
		self.ivc_data = ivc_data_

	def cp_opt2ivc(self, K_bid_dict_, K_ask_dict_, cp_=""):
		K0s = sorted(set(list(K_bid_dict_.keys()) + list(K_ask_dict_.keys())))
		K_dict = {}
		for k in K0s:
			if k < self.ivc_data.minK or k > self.ivc_data.maxK:
				continue
			num = 0
			price = 0.
			ts = 0
			if k in K_bid_dict_.keys(): 
				num += 1
				price += K_bid_dict_[k].price
				if K_bid_dict_[k].ts > ts:
					ts = K_bid_dict_[k].ts # get the latest timestamp 
			if k in K_ask_dict_.keys(): 
				num += 1
				price += K_ask_dict_[k].price
				if K_ask_dict_[k].ts > ts:
					ts = K_ask_dict_[k].ts
			K_dict[k] = ImplVol(price_ = price/(num*100.), ts_ = ts, cp_type_ = cp_)
		return K_dict

	def calc_impl_vol(self, strike_, iv_):
		opt = Option(ex_style_ = "AMERICAN", cp_type_ = iv_.cp_type, \
					trade_date_ = self.ivc_data.val_date, exp_date_ = self.ivc_data.opt_exp_date, \
					S_ = self.ivc_data.S, K_ = strike_, sigma_ = 0., r_ = self.ivc_data.r, \
					q_ = self.ivc_data.q, price_impl_vol_ = iv_.price)
		try: 
			iv_.impl_vol = opt.calcImplVol()
			opt.price    = iv_.price
			opt.sigma    = iv_.impl_vol
#			iv_.delta    = opt.calcDelta()
		except RuntimeError, e:
			print "RuntimeError caught: ", e.message
		except:
			print "Unexpected error caught"
		opt.print_out()
		iv_.print_out()

	def cvrtOpt2Ivc(self):
		self.opt_data.fut_lock.acquire()
		self.ivc_data.fut_exp_date = self.opt_data.fut_exp_date
		if self.opt_data.fut_bid == 0. and self.opt_data.fut_ask == 0.: 
			raise ValueError('Underlying futures price not available!')
		num = 0	
		if self.opt_data.fut_bid > 0.:
			num += 1 
		if self.opt_data.fut_ask > 0.: 
			num += 1 
		self.ivc_data.S = (self.opt_data.fut_bid + self.opt_data.fut_ask) / (num * 100.)
		self.ivc_data.minK = self.ivc_data.S - 50*5. ### 50 points
		self.ivc_data.maxK = self.ivc_data.S + 50*5. ### 50 points
		self.opt_data.fut_lock.release()

		self.opt_data.opt_lock.acquire()
		self.ivc_data.opt_exp_date = self.opt_data.opt_exp_date
		self.ivc_data.put_K_dict   = self.cp_opt2ivc(self.opt_data.put_K_bid_dict, self.opt_data.put_K_ask_dict, cp_="PUT")
		self.ivc_data.call_K_dict  = self.cp_opt2ivc(self.opt_data.call_K_bid_dict, self.opt_data.call_K_ask_dict, cp_="CALL")
		self.opt_data.opt_lock.release()

		for k in self.ivc_data.put_K_dict.keys(): 
			self.calc_impl_vol(k, self.ivc_data.put_K_dict[k])
		for k in self.ivc_data.call_K_dict.keys(): 
			self.calc_impl_vol(k, self.ivc_data.call_K_dict[k])

	def poly_fit_ivc(self, degree_=6):
		K0s  = np.array( sorted(set(list(self.ivc_data.put_K_dict.keys()) \
									+list(self.ivc_data.call_K_dict.keys()))) )	
		self.Ks = []
		self.ivs = []
#		ivs = np.array(np.zeros(len(K0s)))
		for i, k in enumerate(K0s):
			if k < self.ivc_data.minK or k > self.ivc_data.maxK:
				continue
			if k < self.ivc_data.S:
#				if abs(self.ivc_data.put_K_dict[k].delta) > .05: 
					self.Ks.append(k)
					self.ivs.append(self.ivc_data.put_K_dict[k].impl_vol)
#				else:
#					print "## Skipped small delta PUT: K=%f delta=%f" %(k, self.ivc_data.put_K_dict[k].delta) 
			elif k == self.ivc_data.S:
				self.Ks.append(k)
				self.ivs.append( (self.ivc_data.put_K_dict[i].impl_vol + self.ivc_data.call_K_dict[k].impl_vol)/2. )
			else: 
#				if self.ivc_data.call_K_dict[k].delta > .05: 
					self.Ks.append(k)
					self.ivs.append(self.ivc_data.call_K_dict[k].impl_vol)
#				else:
#					print "## Skipped small delta CALL: K=%f delta=%f" %(k, self.ivc_data.call_K_dict[k].delta) 

		coeffs = np.polyfit(self.Ks, self.ivs, degree_)
		poly_n = np.poly1d(coeffs)
		self.fitted_ivs = poly_n(self.Ks)

if __name__ == '__main__':
	print "Implied volatility curve: "

