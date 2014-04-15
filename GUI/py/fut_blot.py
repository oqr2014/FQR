import wx
import wx.grid
import threading
import time
from fut_quote_cli import *

EVT_RESULT_ID = wx.NewId()

def EVT_RESULT(win_, func_):
## Define result event 
	win_.Connect(-1, -1, EVT_RESULT_ID, func_)

class ResultEvent(wx.PyEvent):
	def __init__(self, data_):
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_RESULT_ID)
		self.data = data_

class FutQuoteThread(threading.Thread):
	def __init__(self, notify_win_):
		threading.Thread.__init__(self)
		self.notify_win = notify_win_
		self.want_abort = 0 
		fut_attr    = FuturesAttrParser(filename_="/OMM/data/futures/FuturesSymbols.xml")
		exp_date    = 20140321
		self.fid    = fut_attr.exp_date_dict[exp_date].fid
		self.fquote = FutQuoteCli()
#		self.setDaemon(True)
		self.start()
	
	def run(self):
		self.fquote.sock.send(str(self.fid))
		while 1: 
			if self.want_abort:
				wx.PostEvent(self.notify_win, ResultEvent(None))
				self.fquote.sock.close()
				return
			recv_data = self.fquote.sock.recv(1024)
#			print "recv data=>", recv_data
			tail = "" 
			if len(recv_data) > 0:
				if len(tail) > 0: 
					recv_data += tail 
				(orders, tail) = FixMsg.str2order(recv_data) 
				if len(orders) > 0:
					print len(orders), "orders posted"
					wx.PostEvent(self.notify_win, ResultEvent(orders))
		self.fquote.sock.close() 
		
	def abort(self):
		self.want_abort = 1 

class FutBlotFrame(wx.Frame):
	colLabels = ["bid", "ask"]
	rows = 10
	cols = 2
	def __init__(self, parent_, id_):
		wx.Frame.__init__(self, parent_, id_, title="Futures Level 2",size=(600,300))
		self.grid = wx.grid.Grid(self)
		self.grid.CreateGrid(self.rows, self.cols)
		for col in range(self.cols):
			self.grid.SetColLabelValue(col, self.colLabels[col])
		for row in range(self.rows):
			for col in range(self.cols):
				self.grid.SetCellValue(row, col, "(%s,%s)" % (row, col))
		EVT_RESULT(self, self.OnResult)
		self.fquote_thread = FutQuoteThread(self)

	def OnResult(self, event_):
		for order in event_.data:
			self.grid.SetCellValue(order.price_level-1, order.entry_type, "%.3f" % order.price)
		
class MainApp(wx.App):
	def OnInit(self):
		self.frame = FutBlotFrame(None, -1)
		self.frame.Show(True)
		self.SetTopWindow(self.frame)
		return True

if __name__ == "__main__":
	app = MainApp(0)
	app.MainLoop()

