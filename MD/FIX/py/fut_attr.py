#!/usr/bin/python

################################################ 
# Parse futures attributions by ID
# Attributes: 
# (FID, ExpirationDate)
################################################
import os
import glob
from xml.dom import minidom
from xml_conf import *

class FutAttr: 
	def __init__(self, fid_, exp_date_):
		self.fid = fid_
		self.exp_date = exp_date_
		 
	def print_out(self): 
		print self.fid, self.exp_date

class FutAttrParser: 
	def __init__(self, filename_ = None, dirname_ = None): 
		self.fid_dict = {}
		self.exp_date_dict = {}

		if filename_ is None: 
			file_list = self.read_dir_file(dirname_)
		else: 
			file_list = [filename_]
		
		for file1 in file_list: 
			self.parse_file(file1)
	
	def read_dir_file(self, dirname_ = None): 
		if dirname_ is None:
			dirname_ = './'
		file_list = glob.glob(dirname_ + '/*.xml')
		return file_list 

	def parse_file(self, filename_):
#		print 'parsing:', filename_ 
		dom = minidom.parse(filename_)
		for futures in dom.getElementsByTagName('Product'):
			fid = int(futures.getElementsByTagName('SecurityID')[0].childNodes[0].nodeValue)
			security_desc = futures.getElementsByTagName('SecurityDesc')[0].childNodes[0].nodeValue
			if security_desc != "ESH4": 
				continue
			exp_date = int(futures.getElementsByTagName('ExpirationDate')[0].childNodes[0].nodeValue)
			futures_attr = FutAttr(fid, exp_date)
			self.fid_dict[futures_attr.fid] = futures_attr
			self.exp_date_dict[futures_attr.exp_date] = futures_attr

if __name__ == "__main__":
	gw_conf = GatewayConf()
	futAttrPs = FutAttrParser(filename_ = gw_conf.fut_sym)
	print futAttrPs.fid_dict 
	print futAttrPs.exp_date_dict 
		
