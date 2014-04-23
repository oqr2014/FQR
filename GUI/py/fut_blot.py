import wx
import wx.grid
import threading
import time
from fut_quote_cli import *


class DataEvent(wx.PyEvent):
	def __init__(self, wxeid_, data_):
		wx.PyEvent.__init__(self)
		self.SetEventType(wxeid_)
		self.data = data_

class FutQuoteThread(threading.Thread):
	def __init__(self, notify_win_, exp_date_=20140321):
		threading.Thread.__init__(self)
		self.wxeid      = wx.NewId()
		self.notify_win = notify_win_
		self.stop       = threading.Event()
		self.fut_attr   = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
		self.exp_date   = exp_date_ 
		self.exp_date_changed = threading.Event()
		self.fid        = self.fut_attr.exp_date_dict[self.exp_date].fid
		self.fquote     = FutQuoteCli()
#		self.setDaemon(True)
		self.start()
	
	def run(self):
		self.fquote.sock.send(str(self.fid))
		while not self.stop.is_set():
			if self.exp_date_changed.is_set():
				self.fquote.sock.send(str(self.fid))
				self.exp_date_changed.clear()
			recv_data = self.fquote.sock.recv(1024)
#			print "recv data=>", recv_data
			tail = "" 
			if len(recv_data) > 0:
				if len(tail) > 0: 
					recv_data += tail 
				(orders, tail) = FixMsg.str2order(recv_data) 
				if len(orders) > 0:
#					print len(orders), "orders posted"
					wx.PostEvent(self.notify_win, DataEvent(self.wxeid, orders))
#		self.fquote.sock.shutdown(socket.SHUT_RDWR)
		self.fquote.sock.close() 
		
	def shutdown(self):
		self.stop.set() 
	
	def set_exp_date_changed(self):
		if self.exp_date in self.fut_attr.exp_date_dict.keys(): 
			self.fid  = self.fut_attr.exp_date_dict[self.exp_date].fid
			self.exp_date_changed.set()
		else:
			print "####Error:exp_date not found:", str(self.exp_date)
			self.shutdown()

class FutBlotPanel(wx.Panel):
	colLabels = ["time", "size", "bid", "ask", "size", "time"]
	rowColors = ["rosybrown", "sandybrown", "goldenrod", "darkgoldenrod", "peru", \
				"chocolate", "saddlebrown", "sienna", "brown", "maroon"]
#	rowColors = ["lavender", "thistle", "plum", "violet", "orchid", \
#				"fuchsia", "magenta", "mediumorchid", "blueviolet", "darkviolet"]
	rows = 10
	cols = 6
	exp_dates = ["20140321", "20140620"]
	
	def __init__(self, parent_, id_):
		wx.Panel.__init__(self, parent_, id_)
		self.fquote_thread = None
		self.exp_date = ""
		self.createControls()
		self.bindEvents()
		self.doLayout()

	def createControls(self):
		self.grid = wx.grid.Grid(self)
		self.grid.CreateGrid(self.rows, self.cols)
		self.grid.EnableGridLines(False)
		self.grid.SetRowLabelSize(0)
		self.grid.SetDefaultCellBackgroundColour("black")
		for col in range(self.cols):
			self.grid.SetColLabelValue(col, self.colLabels[col])
		for row in range(self.rows):
			for col in range(self.cols):
				self.grid.SetCellTextColour(row, col, "springgreen")
				self.grid.SetCellBackgroundColour(row, col, self.rowColors[row])
				self.grid.SetCellValue(row, col, "(%s,%s)" % (row, col))

		self.label = wx.StaticText(self, label="Expiration Date")
		self.combBox = wx.ComboBox(self, choices=self.exp_dates, style=wx.CB_DROPDOWN)
		self.connBut = wx.Button(self, label="Connect") 
		self.disConnBut = wx.Button(self, label="Disconnect") 
		
	def bindEvents(self):
		self.Bind(wx.EVT_CLOSE, self.onClose)
#		self.combBox.Bind(wx.EVT_COMBOBOX, self.onExpDateSel)
		self.combBox.Bind(wx.EVT_TEXT, self.onExpDateSel)
		self.connBut.Bind(wx.EVT_BUTTON, self.onConnect)
		self.disConnBut.Bind(wx.EVT_BUTTON, self.onDisConnect)

	def doLayout(self):
		box_sizer = wx.BoxSizer(wx.HORIZONTAL)
		box_sizer.Add(self.label)
		box_sizer.Add(self.combBox)
		box_sizer.Add(self.connBut)
		box_sizer.Add(self.disConnBut)
		blot_sizer = wx.BoxSizer(wx.VERTICAL)	
		blot_sizer.Add(self.grid, 1, wx.EXPAND)
		blot_sizer.Add(box_sizer, 1, wx.EXPAND)
		self.SetSizerAndFit(blot_sizer)

	def onExpDateSel(self, event_):
		print "expiration date selected:", event_.GetString()	
		self.exp_date = int(event_.GetString())
		if self.fquote_thread != None:
			self.fquote_thread.exp_date = self.exp_date
			self.fquote_thread.set_exp_date_changed()

	def onConnect(self, event_):
		print "Connecting..."
		if self.fquote_thread == None:
			self.fquote_thread = FutQuoteThread(self, self.exp_date)
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
				self.grid.SetCellValue(order.price_level-1, 2, "%.2f" % order.price)
				self.grid.SetCellValue(order.price_level-1, 1, "%d" % order.quantity)
				self.grid.SetCellValue(order.price_level-1, 0, "%s" % sec2TimeStr(order.entry_time))
			else:
				self.grid.SetCellValue(order.price_level-1, 3, "%.2f" % order.price)
				self.grid.SetCellValue(order.price_level-1, 4, "%d" % order.quantity)
				self.grid.SetCellValue(order.price_level-1, 5, "%s" % sec2TimeStr(order.entry_time))
	
	def onClose(self, event_=None):
		self.onDisConnect()
		self.Destroy()
		print "Panel closed!"
		
class FutBlotFrame(wx.Frame):
	def __init__(self, parent_, id_, title_="Futures Level 2"):
		wx.Frame.__init__(self, parent_, id_, title_)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.panel = FutBlotPanel(self, -1)
#		sizer = wx.BoxSizer(wx.VERTICAL)
#		sizer.Add(self.panel, 1, wx.EXPAND)
#		self.SetSizer(sizer)

	def onClose(self, event_):
		self.panel.onClose()
		self.Destroy()
		print "Frame closed!"

class MainApp(wx.App):
	def OnInit(self):
		self.frame = FutBlotFrame(None, -1)
		self.frame.Show(True)
		self.SetTopWindow(self.frame)
		return True

if __name__ == "__main__":
	app = MainApp(0)
	app.MainLoop()

