import os 
import time 
import wx
from option_chain_blot import *
from ivc_blot import * 
from ivc import * 

class MainApp(wx.App):
	def OnInit(self):
		self.opt_data  = OptionData()
		self.opt_frame = OptionChainFrame(None, -1, opt_data_=self.opt_data) 
		self.ivc_frame = IVCFrame(self.opt_frame, -1, opt_data_=self.opt_data)
		self.opt_frame.Show()
		self.ivc_frame.Show()
		return True

if __name__ == "__main__":
	app = MainApp(0)
	app.MainLoop()

