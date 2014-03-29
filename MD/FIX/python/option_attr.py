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

class OptionAttr: 
	def __init__(self, oid_, strike_, exp_date_, cp_type_, ex_style_):
		self.oid = oid_
		self.strike = strike_
		self.exp_date = exp_date_
		self.cp_type = cp_type_
		self.ex_style = ex_style_ 
		 
	def print_out(self): 
		print self.oid, self.strike, self.exp_date, self.cp_type, self.ex_style

class OptionAttrParser: 
	def __init__(self, filename_=None, dirname_=None): 
		self.oid_dict = {}
#		self.strike_dict = {} // duplicate keys

		if filename_ is None: 
			file_list = self.read_dir_file(dirname_)
		else: 
			file_list = [filename_]
		
		for file1 in file_list: 
			self.parse_file(file1)
	
	def read_dir_file(self, dirname_=None): 
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
			cp_type = option.getElementsByTagName('Type')[0].childNodes[0].nodeValue
			ex_style = option.getElementsByTagName('ExerciseStyle')[0].childNodes[0].nodeValue
			option_attr = OptionAttr(oid, strike, exp_date, cp_type, ex_style)
#			option_attr.print_out()
			self.oid_dict[option_attr.oid] = option_attr
#			self.strike_dict[option_attr.strike] = option_attr

if __name__ == "__main__":
#	optionAttr = OptionAttrParser(dirname_="/OMM/data")
	optionAttr = OptionAttrParser(filename_="/OMM/data/ES_20140321.xml")
	print optionAttr.oid_dict 
#	print optionAttr.strike_dict
		
