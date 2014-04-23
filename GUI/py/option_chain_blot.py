import wx
import wx.grid
import wx.lib.scrolledpanel as scrolled 
import threading
import time
from fut_quote_cli import *

class OptionChainPanel(wx.Panel):
	fut_col_labels = ["time", "size", "bid", "ask", "size", "time"]
#	rowColors = ["rosybrown", "sandybrown", "goldenrod", "darkgoldenrod", "peru", \
#			"chocolate", "saddlebrown", "sienna", "brown", "maroon"]
#	rowColors = ["lavender", "thistle", "plum", "violet", "orchid", \
#				"fuchsia", "magenta", "mediumorchid", "blueviolet", "darkviolet"]
	fut_row_colors = ["black"]
	fut_rows = 1
	fut_cols = 6
	fut_exp_dates = ["20140321", "20140620"]
	
	opt_col_labels = ["time", "size", "bid", "ask", "size", "time", "strike", \
					"time", "size", "bid", "ask", "size", "time"]
	opt_row_colors = ["rosybrown", "sandybrown", "goldenrod", "darkgoldenrod", "peru", \
			"chocolate", "saddlebrown", "sienna", "brown", "maroon"]
#	rowColors = ["lavender", "thistle", "plum", "violet", "orchid", \
#				"fuchsia", "magenta", "mediumorchid", "blueviolet", "darkviolet"]
	opt_rows = 250
	opt_cols = 13
	opt_exp_dates = ["20140321", "20140620"]
	
	def __init__(self, parent_, id_):
		wx.Panel.__init__(self, parent_, id_)
		self.fquote_thread = None
		self.fut_exp_date = ""
		self.opt_exp_date = ""
		self.createControls()
		self.bindEvents()
		self.doLayout()

	def createControls(self):
		self.label = wx.StaticText(self, label="Expiration Date")
		self.combBox = wx.ComboBox(self, choices=self.fut_exp_dates, style=wx.CB_DROPDOWN)
		self.connBut = wx.Button(self, label="Connect") 
		self.disConnBut = wx.Button(self, label="Disconnect") 
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
				self.fut_grid.SetCellBackgroundColour(row, col, self.fut_row_colors[row])
				self.fut_grid.SetCellValue(row, col, "(%s,%s)" % (row, col))

		self.opt_grid = wx.grid.Grid(self)
		self.opt_grid.CreateGrid(self.opt_rows, self.opt_cols)
		self.opt_grid.EnableGridLines(False)
		self.opt_grid.SetRowLabelSize(0)
		self.opt_grid.SetDefaultCellBackgroundColour("black")
		for col in range(self.opt_cols):
			self.opt_grid.SetColLabelValue(col, self.opt_col_labels[col])
		for row in range(self.opt_rows):
			for col in range(self.opt_cols):
				self.opt_grid.SetCellTextColour(row, col, "springgreen")
				self.opt_grid.SetCellBackgroundColour(row, col, "black")
				self.opt_grid.SetCellValue(row, col, "(%s,%s)" % (row, col))
		
	def bindEvents(self):
		self.Bind(wx.EVT_CLOSE, self.onClose)
#		self.combBox.Bind(wx.EVT_COMBOBOX, self.onExpDateSel)
		self.combBox.Bind(wx.EVT_TEXT, self.onExpDateSel)
		self.connBut.Bind(wx.EVT_BUTTON, self.onConnect)
		self.disConnBut.Bind(wx.EVT_BUTTON, self.onDisConnect)

	def doLayout(self):
		fut_sizer = wx.BoxSizer(wx.HORIZONTAL)	
		fut_sizer.Add(self.fut_grid, 0, wx.EXPAND)
		fut_sizer.Add(self.label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		fut_sizer.Add(self.combBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		fut_sizer.Add(self.connBut, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		fut_sizer.Add(self.disConnBut, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		
		opt_sizer = wx.BoxSizer(wx.VERTICAL)
		opt_sizer.Add(self.opt_grid, 1, wx.EXPAND)

		blot_sizer = wx.BoxSizer(wx.VERTICAL)
		blot_sizer.Add(fut_sizer, 0, wx.EXPAND)
		blot_sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
		blot_sizer.Add(opt_sizer, 1, wx.EXPAND)
		self.SetSizer(blot_sizer)

	def onExpDateSel(self, event_):
		print "expiration date selected:", event_.GetString()	
		self.fut_exp_date = int(event_.GetString())
		if self.fquote_thread != None:
			self.fquote_thread.exp_date = self.fut_exp_date
			self.fquote_thread.set_exp_date_changed()

	def onConnect(self, event_):
		print "Connecting..."
		if self.fquote_thread == None:
			self.fquote_thread = FutQuoteThread(self, self.fut_exp_date)
			self.Connect(-1, -1, self.fquote_thread.wxeid, self.onData)
	
	def onDisConnect(self, event_=None): 
		print "Disconnecting..."
		if self.fquote_thread != None:
			self.fquote_thread.shutdown()
			self.fquote_thread.join()
			self.fquote_thread = None
		
	def onData(self, event_):
		for order in event_.data:
			if order.entry_type == 0: 
				self.fut_grid.SetCellValue(order.price_level-1, 2, "%.2f" % order.price)
				self.fut_grid.SetCellValue(order.price_level-1, 1, "%d" % order.quantity)
				self.fut_grid.SetCellValue(order.price_level-1, 0, "%s" % sec2TimeStr(order.entry_time))
			else:
				self.fut_grid.SetCellValue(order.price_level-1, 3, "%.2f" % order.price)
				self.fut_grid.SetCellValue(order.price_level-1, 4, "%d" % order.quantity)
				self.fut_grid.SetCellValue(order.price_level-1, 5, "%s" % sec2TimeStr(order.entry_time))
	
	def onClose(self, event_=None):
		self.onDisConnect()
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

