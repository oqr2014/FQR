import wx
import wx.grid
import threading
import time
from fut_quote_cli import *
from opt_quote_cli import *

class OptionChainPanel(wx.Panel):
	fut_col_labels = ["time", "size", "bid", "ask", "size", "time"]
#	rowColors = ["lavender", "thistle", "plum", "violet", "orchid", \
#				"fuchsia", "magenta", "mediumorchid", "blueviolet", "darkviolet"]
	fut_row_clrs = ["black"]
	fut_rows = 1
	fut_cols = 6
	fut_exp_dates = ["20140321", "20140620"]
	
	opt_col_labels = ["time", "size", "bid", "ask", "size", "time", "strike", \
					"time", "size", "bid", "ask", "size", "time"]
#	opt_row_clrs = ["cornsilk", "blanchedalmond", "bisque", "navajowhite", "wheat", "burlywood", "tan", "rosybrown", \
	opt_row_clrs = ["rosybrown", "sandybrown", "goldenrod", "darkgoldenrod", \
				"peru", "chocolate", "saddlebrown", "sienna", "brown", "maroon"]
	opt_rows = 250
	opt_cols = 13
	opt_exp_dates = ["20140321", "20140620"]
	
	def __init__(self, parent_, id_):
		wx.Panel.__init__(self, parent_, id_)
		self.fqt_trd = None
		self.oqt_trd = None
		self.oid_dict = {}
		self.K_dict = {}
		self.fut_exp_date = int(self.fut_exp_dates[0])
		self.opt_exp_date = int(self.opt_exp_dates[0])
		self.createCtrls()
		self.bindEvents()
		self.doLayout()

	def createCtrls(self):
		self.fut_label = wx.StaticText(self, label="Futures exp date")
		self.fut_combBox = wx.ComboBox(self, value=self.fut_exp_dates[0], \
							choices=self.fut_exp_dates, style=wx.CB_DROPDOWN)
		self.fut_connBut = wx.Button(self, label="Connect") 
		self.fut_stopBut = wx.Button(self, label="Stop") 
		self.fut_grid = wx.grid.Grid(self)
		self.fut_grid.CreateGrid(self.fut_rows, self.fut_cols)
		self.fut_grid.EnableGridLines(False)
		self.fut_grid.SetRowLabelSize(0)
		self.fut_grid.SetDefaultCellBackgroundColour("black")
		for col in range(self.fut_cols):
			self.fut_grid.SetColLabelValue(col, self.fut_col_labels[col])
		for row in range(self.fut_rows):
			for col in range(self.fut_cols):
				self.fut_grid.SetCellTextColour(row, col, "springgreen")
				self.fut_grid.SetCellBackgroundColour(row, col, self.fut_row_clrs[row])
#				self.fut_grid.SetCellValue(row, col, "(%s,%s)" % (row, col))

		self.opt_label = wx.StaticText(self, label="Options exp date")
		self.opt_combBox = wx.ComboBox(self, value=self.opt_exp_dates[0], \
							choices=self.opt_exp_dates, style=wx.CB_DROPDOWN)
		self.opt_connBut = wx.Button(self, label="Connect") 
		self.opt_stopBut = wx.Button(self, label="Stop") 
		self.opt_grid = wx.grid.Grid(self)
		self.opt_grid.CreateGrid(self.opt_rows, self.opt_cols)
		self.opt_grid.EnableGridLines(False)
		self.opt_grid.SetRowLabelSize(0)
		self.opt_grid.SetDefaultCellBackgroundColour("black")
		for col in range(self.opt_cols):
			self.opt_grid.SetColLabelValue(col, self.opt_col_labels[col])
		for row in range(self.opt_rows):
			for col in range(self.opt_cols):
				if col == 6:
					self.opt_grid.SetCellTextColour(row, col, "springgreen")
				else: 
					self.opt_grid.SetCellTextColour(row, col, "black")
				if col == 6: 
					self.opt_grid.SetCellBackgroundColour(row, col, "black")
				else:
					self.opt_grid.SetCellBackgroundColour(row, col, self.opt_row_clrs[row%len(self.opt_row_clrs)])
#				self.opt_grid.SetCellValue(row, col, "(%s,%s)" % (row, col))
		
	def bindEvents(self):
		self.Bind(wx.EVT_CLOSE, self.onClose)
#		self.combBox.Bind(wx.EVT_COMBOBOX, self.onExpDateSel)
		self.fut_combBox.Bind(wx.EVT_TEXT, self.onFutExpDateSel)
		self.fut_connBut.Bind(wx.EVT_BUTTON, self.onFutConn)
		self.fut_stopBut.Bind(wx.EVT_BUTTON, self.onFutStop)
		self.opt_combBox.Bind(wx.EVT_TEXT, self.onOptExpDateSel)
		self.opt_connBut.Bind(wx.EVT_BUTTON, self.onOptConn)
		self.opt_stopBut.Bind(wx.EVT_BUTTON, self.onOptStop)

	def doLayout(self):
		fut_sizer = wx.BoxSizer(wx.HORIZONTAL)	
		self.oid_dict = {}
		fut_sizer.Add(self.fut_grid, 0, wx.EXPAND)
		fut_sizer.Add(self.fut_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		fut_sizer.Add(self.fut_combBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		fut_sizer.Add(self.fut_connBut, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		fut_sizer.Add(self.fut_stopBut, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		
		opt_sizer1 = wx.BoxSizer(wx.HORIZONTAL)	
		opt_sizer1.Add(self.opt_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		opt_sizer1.Add(self.opt_combBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		opt_sizer1.Add(self.opt_connBut, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		opt_sizer1.Add(self.opt_stopBut, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)

		opt_sizer = wx.BoxSizer(wx.VERTICAL)
		opt_sizer.Add(opt_sizer1, 0, wx.EXPAND)
		opt_sizer.Add(self.opt_grid, 1, wx.EXPAND)

		blot_sizer = wx.BoxSizer(wx.VERTICAL)
		blot_sizer.Add(fut_sizer, 0, wx.EXPAND)
		blot_sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
		blot_sizer.Add(opt_sizer, 1, wx.EXPAND)
		self.SetSizer(blot_sizer)

	def onFutExpDateSel(self, event_):
		print "expiration date selected:", event_.GetString()	
		self.fut_exp_date = int(event_.GetString())
		if self.fqt_trd != None:
			self.fqt_trd.exp_date = self.fut_exp_date
			self.fqt_trd.set_exp_date_changed()

	def onFutConn(self, event_):
		print "Connecting futures quote svr ..."
		if self.fqt_trd == None:
			self.fqt_trd = FutQuoteThread(self, self.fut_exp_date)
			self.Connect(-1, -1, self.fqt_trd.wxeid, self.onFutData)
	
	def onFutStop(self, event_=None): 
		print "Disconnecting futures quote svr ..."
		if self.fqt_trd != None:
			self.fqt_trd.shutdown()
			self.fqt_trd.join()
			self.fqt_trd = None
		
	def onFutData(self, event_):
		for order in event_.data:
			if order.entry_type == 0: 
				self.fut_grid.SetCellValue(order.price_level-1, 2, "%.2f" % order.price)
				self.fut_grid.SetCellValue(order.price_level-1, 1, "%d" % order.quantity)
				self.fut_grid.SetCellValue(order.price_level-1, 0, "%s" % sec2TimeStr(order.entry_time))
			else:
				self.fut_grid.SetCellValue(order.price_level-1, 3, "%.2f" % order.price)
				self.fut_grid.SetCellValue(order.price_level-1, 4, "%d" % order.quantity)
				self.fut_grid.SetCellValue(order.price_level-1, 5, "%s" % sec2TimeStr(order.entry_time))
	
	def onOptExpDateSel(self, event_):
		print "option expiration date selected:", event_.GetString()	
		self.opt_exp_date = int(event_.GetString())
		if self.oqt_trd != None:
			self.oqt_trd.exp_date = self.opt_exp_date
			self.oqt_trd.set_exp_date_changed()

	def onOptConn(self, event_):
		print "Connecting options quote svr ..."
		if self.oqt_trd == None:
			self.oqt_trd = OptQuoteThread(self, self.opt_exp_date)
			self.Connect(-1, -1, self.oqt_trd.wxeid, self.onOptData)
			self.oid_dict = self.oqt_trd.opt_attr_ps.oid_dict
			Ks = sorted(self.oqt_trd.opt_attr_ps.K_set)
			for idx, x in enumerate(Ks): 
				self.K_dict[x] = idx
	
	def onOptStop(self, event_=None): 
		print "Disconnecting options quote svr ..."
		if self.oqt_trd != None:
			self.oqt_trd.shutdown()
			self.oqt_trd.join()
			self.oqt_trd = None
		
	def onOptData(self, event_):
		for order in event_.data:
#			print "order received" 
#			order.printout()
			if not order.sid in self.oid_dict.keys(): 
				print "##### onOptData Error, order not found: "
				order.printout()
				continue 
			opt_attr = self.oid_dict[order.sid]
			row = self.K_dict[opt_attr.strike]
			self.opt_grid.SetCellValue(row, 6, "%.2f" % opt_attr.strike)
			if opt_attr.cp_type == "P":  ##PUT 
				if order.entry_type == 0: ## bid 
					self.opt_grid.SetCellValue(row, 2, "%.2f" % order.price)
					self.opt_grid.SetCellValue(row, 1, "%d" % order.quantity)
					self.opt_grid.SetCellValue(row, 0, "%s" % sec2TimeStr(order.entry_time))
				else:  ## ask 
					self.opt_grid.SetCellValue(row, 3, "%.2f" % order.price)
					self.opt_grid.SetCellValue(row, 4, "%d" % order.quantity)
					self.opt_grid.SetCellValue(row, 5, "%s" % sec2TimeStr(order.entry_time))
			else:  ## CALL
				if order.entry_type == 0: ## bid 
					self.opt_grid.SetCellValue(row, 9, "%.2f" % order.price)
					self.opt_grid.SetCellValue(row, 8, "%d" % order.quantity)
					self.opt_grid.SetCellValue(row, 7, "%s" % sec2TimeStr(order.entry_time))
				else:  ## ask 
					self.opt_grid.SetCellValue(row, 10, "%.2f" % order.price)
					self.opt_grid.SetCellValue(row, 11, "%d" % order.quantity)
					self.opt_grid.SetCellValue(row, 12, "%s" % sec2TimeStr(order.entry_time))


	def onClose(self, event_=None):
		self.onFutStop()
		self.onOptStop()
		self.Destroy()
		print "Panel closed!"
		
class OptionChainFrame(wx.Frame):
	def __init__(self, parent_, id_, title_="Option Chain"):
		wx.Frame.__init__(self, parent_, id_, title_)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.panel = OptionChainPanel(self, -1)
#		sizer = wx.BoxSizer(wx.VERTICAL)
#		sizer.Add(self.panel, 1, wx.EXPAND)
#		self.SetSizer(sizer)

	def onClose(self, event_):
		self.panel.onClose()
		self.Destroy()
		print "Option Chain closed!"

class MainApp(wx.App):
	def OnInit(self):
		self.frame = OptionChainFrame(None, -1)
		self.frame.Show(True)
		self.SetTopWindow(self.frame)
		return True

if __name__ == "__main__":
	app = MainApp(0)
	app.MainLoop()

