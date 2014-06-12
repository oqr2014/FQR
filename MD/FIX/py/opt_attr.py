#!/usr/bin/python

######################################################################
# 
# Parse option attributions by ID
# Attributes: 
# (OID, Strike, ExpirationDate, Call_Put_Type, Exercise_Type)
#
#######################################################################
import os
import glob
from xml.dom import minidom
from xml_conf import * 

class OptAttr: 
	def __init__(self, oid_, strike_, exp_date_, cp_type_, ex_style_):
		self.oid = oid_
		self.strike = strike_
		self.exp_date = exp_date_
		self.cp_type = cp_type_
		self.ex_style = ex_style_ 
		self.fid = 0  #underlying futures id 

	def print_out(self): 
		print self.oid, self.strike, self.exp_date, self.cp_type, self.ex_style

class OptAttrParser: 
	def __init__(self, filename_ = None, dirname_ = None): 
		self.oid_dict = {}
		self.K_set = set()

		if filename_ is None: 
			file_list = self.read_dir_file(dirname_)
		else: 
			file_list = [filename_]
		
		for file1 in file_list: 
			self.parse_file(file1)
	
	def set_underlying_fids(fut_exp_date_dict_): 
		for oid in self.oid_dict.keys():
			date = self.oid_dict[oid].exp_date
			self.oid_dict[oid].fid = fut_exp_date_dict_[date].fid

	def read_dir_file(self, dirname_ = None): 
		if dirname_ is None:
			dirname_ = './'
		file_list = glob.glob(dirname_ + '/*.xml')
		return file_list 

	def parse_file(self, filename_):
#		print 'parsing:', filename_ 
		dom = minidom.parse(filename_)
#		print xmldoc.toxml()	
		for option in dom.getElementsByTagName('OptionProduct'):
			oid = int(option.getElementsByTagName('SecurityID')[0].childNodes[0].nodeValue)
			strike = float(option.getElementsByTagName('Strike')[0].childNodes[0].nodeValue)
			exp_date = int(option.getElementsByTagName('ExpirationDate')[0].childNodes[0].nodeValue)
			cp_type = option.getElementsByTagName('Type')[0].childNodes[0].nodeValue.upper()
			ex_style = option.getElementsByTagName('ExerciseStyle')[0].childNodes[0].nodeValue.upper()
			opt_attr = OptAttr(oid, strike, exp_date, cp_type, ex_style)
#			opt_attr.print_out()
			self.oid_dict[opt_attr.oid] = opt_attr
			self.K_set.add(strike)

if __name__ == "__main__":	
	gw_conf   = GatewayConf()
#	optAttrParser = OptAttrParser(dirname_="/OMM/data")
	optAttrPs = OptAttrParser(filename_ = gw_conf.opt_sym) 
	print optAttrPs.oid_dict 
#	print optionAttr.strike_dict
		
