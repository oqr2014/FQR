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
	def __init__(self, notify_win_):
		threading.Thread.__init__(self)
		self.wxeid = wx.NewId()
		self.notify_win = notify_win_
		self.stop   = threading.Event()
		fut_attr    = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
		exp_date    = 20140321
		self.fid    = fut_attr.exp_date_dict[exp_date].fid
		self.fquote = FutQuoteCli()
#		self.setDaemon(True)
		self.start()
	
	def run(self):
		self.fquote.sock.send(str(self.fid))
		while not self.stop.is_set():
			recv_data = self.fquote.sock.recv(1024)
#			print "recv data=>", recv_data
			tail = "" 
			if len(recv_data) > 0:
				if len(tail) > 0: 
					recv_data += tail 
				(orders, tail) = FixMsg.str2order(recv_data) 
				if len(orders) > 0:
					print len(orders), "orders posted"
					wx.PostEvent(self.notify_win, DataEvent(self.wxeid, orders))
		self.fquote.sock.shutdown(socket.SHUT_RDWR)
		self.fquote.sock.close() 
		
	def shutdown(self):
		self.stop.set() 

class FutBlotFrame(wx.Frame):
	colLabels = ["time", "size", "bid", "ask", "size", "time"]
	rowColors = ["rosybrown", "sandybrown", "goldenrod", "darkgoldenrod", "peru", \
				"chocolate", "saddlebrown", "sienna", "brown", "maroon"]
#	rowColors = ["lavender", "thistle", "plum", "violet", "orchid", \
#				"fuchsia", "magenta", "mediumorchid", "blueviolet", "darkviolet"]
	rows = 10
	cols = 6
	def __init__(self, parent_, id_):
		wx.Frame.__init__(self, parent_, id_, title="Futures Level 2",size=(600,300))
		self.Bind(wx.EVT_CLOSE, self.onClose)
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
		self.fquote_thread = FutQuoteThread(self)
		self.Connect(-1, -1, self.fquote_thread.wxeid, self.onData)

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
	
	def onClose(self, event_):
		print "Frame closed!"
		self.fquote_thread.shutdown()
		self.fquote_thread.join()
		self.Destroy()
		
class MainApp(wx.App):
	def OnInit(self):
		self.frame = FutBlotFrame(None, -1)
		self.frame.Show(True)
		self.SetTopWindow(self.frame)
		return True

if __name__ == "__main__":
	app = MainApp(0)
	app.MainLoop()

