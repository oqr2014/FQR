#!/usr/bin/python
##########################################################
#
# Implied volatility curve generator & plotting
# 
##########################################################
import os
import time
import pprint
import random
import sys
import wx
from ivc import *
from option_attr import *
from option import *
# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas 
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab
import matplotlib.pyplot as plt

class IVCFrame(wx.Frame):
	def __init__(self, parent_, id_, title_='Implied Volatility Curve', pos_=(600, 100), opt_data_=OptionData()):
		wx.Frame.__init__(self, parent_, id_, title_, pos_)
		self.opt_data    = opt_data_
		self.ivc_data    = ImplVolCurve()
		self.opt_attr_ps = OptionAttrParser(filename_="/OMM/data/ES_20140321.xml")
		self.Ks          = sorted(self.opt_attr_ps.K_set)
		self.paused      = True
		self.create_menu()
		self.create_status_bar()
		self.create_main_panel()
		self.timer       = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_recalc_ivc, self.timer)        
		self.timer.Start(2000)  #Every 10 secs

	def create_menu(self):
		self.menubar = wx.MenuBar()
		menu_file    = wx.Menu()
		m_expt       = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
		self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
		menu_file.AppendSeparator()
		m_exit       = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
		self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
		self.menubar.Append(menu_file, "&File")
		self.SetMenuBar(self.menubar)

	def create_ctrls(self): 
		self.pause_button     = wx.Button(self.panel, -1, "Resume")
		self.valdate_lb       = wx.StaticText(self.panel, label="Value date")
		self.valdate_txt_ctrl = wx.TextCtrl(self.panel, value="20140301")
		self.r_lb             = wx.StaticText(self.panel, label="Risk free rate")
		self.r_txt_ctrl       = wx.TextCtrl(self.panel, value="0.01")
		self.q_lb             = wx.StaticText(self.panel, label="Dividend rate")
		self.q_txt_ctrl       = wx.TextCtrl(self.panel, value="0.01")

	def create_main_panel(self):
		self.panel   = wx.Panel(self)
		self.init_plot()
		self.canvas  = FigCanvas(self.panel, -1, self.fig)
		self.toolbar = NavigationToolbar(self.canvas)
#		self.toolbar.Show()
			
		self.create_ctrls()
		self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
		self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)
	
		self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.h_sizer.Add(self.pause_button, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		self.h_sizer.AddSpacer(20)
		self.h_sizer.Add(self.valdate_lb, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		self.h_sizer.Add(self.valdate_txt_ctrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		self.h_sizer.AddSpacer(20)
		self.h_sizer.Add(self.r_lb, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		self.h_sizer.Add(self.r_txt_ctrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		self.h_sizer.AddSpacer(20)
		self.h_sizer.Add(self.q_lb, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		self.h_sizer.Add(self.q_txt_ctrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
	
		self.v_sizer = wx.BoxSizer(wx.VERTICAL)
		self.v_sizer.Add(self.canvas, 2, flag=wx.LEFT | wx.TOP | wx.GROW)        
		self.v_sizer.Add(self.toolbar, 0, wx.EXPAND)
		self.v_sizer.Add(self.h_sizer, 0, wx.EXPAND)
	
		self.panel.SetSizerAndFit(self.v_sizer)

	def create_status_bar(self):
		self.statusbar = self.CreateStatusBar()

	def init_plot(self):
		self.dpi = 100
		self.fig = Figure((3.0, 3.0), dpi=self.dpi)
		self.axes = self.fig.add_subplot(111)
		self.axes.set_axis_bgcolor('black')
		self.axes.set_title('Implied Volatility Curve', size=12)

		pylab.setp(self.axes.get_xticklabels(), fontsize=10)
		pylab.setp(self.axes.get_yticklabels(), fontsize=10)

		tmp_put = [random.random() for i in range(100)]
		tmp_call = [random.random() for i in range(100)]
		self.plot_put = self.axes.plot(range(100), tmp_put, 'yo', label='PUT')[0]
		self.plot_call = self.axes.plot(range(100), tmp_call, 'g+', label='CALL')[0]
		self.plot_K_line = self.axes.plot(50*np.ones(100), np.arange(100)/100.)[0]

	def draw_ivc(self):
#		Ks = sorted(set(list(self.ivc_data.put_K_dict.keys()) + list(self.call_K_dict.keys())))
		put_Ks = sorted(list(self.ivc_data.put_K_dict.keys()))
		put_ivc = list(np.zeros(len(put_Ks)))
		for i, k in enumerate(put_Ks):
			put_ivc[i] = self.ivc_data.put_K_dict[k].impl_vol

		call_Ks = sorted(list(self.ivc_data.call_K_dict.keys()))
		call_ivc = list(np.zeros(len(call_Ks)))
		for i, k in enumerate(call_Ks):
			call_ivc[i] = self.ivc_data.call_K_dict[k].impl_vol

		self.axes.set_xbound(lower = min(put_Ks[0], call_Ks[0]), upper = max(put_Ks[-1], call_Ks[-1]))
		self.axes.set_ybound(lower=0., upper=1.)
		self.axes.grid(True, color='gray')
		pylab.setp(self.axes.get_xticklabels(), visible=True)
		self.plot_put.set_xdata(put_Ks)
		self.plot_put.set_ydata(put_ivc)
		self.plot_call.set_xdata(call_Ks)
		self.plot_call.set_ydata(call_ivc)
		self.plot_K_line.set_xdata(np.ones(100)*self.ivc_data.S)
		self.plot_K_line.set_ydata(np.arange(100)/100.)

		self.canvas.draw()

	def on_pause_button(self, event):
		self.paused = not self.paused

	def on_update_pause_button(self, event):
		label = "Resume" if self.paused else "Pause"
		self.pause_button.SetLabel(label)

	def on_save_plot(self, event):
		file_choices = "PNG (*.png)|*.png"
		dlg = wx.FileDialog(
					self, 
					message="Save plot as...",
					defaultDir=os.getcwd(),
					defaultFile="plot.png",
					wildcard=file_choices,
					style=wx.SAVE)
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			self.canvas.print_figure(path, dpi=self.dpi)
			self.flash_status_message("Saved to %s" % path)

	def on_recalc_ivc(self, event):
		if not self.paused:
			print "repaint called", time.ctime()
			msg = "repaint at " + time.ctime()
			self.statusbar.SetStatusText(msg)
			self.ivc_data.val_date = int(self.valdate_txt_ctrl.GetValue())
			self.ivc_data.r        = float(self.r_txt_ctrl.GetValue()) 
			self.ivc_data.q        = float(self.q_txt_ctrl.GetValue())
			self.cvrt_opt_ivc()
			self.draw_ivc()

	def cvrt_opt_ivc(self):
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
		self.opt_data.fut_lock.release()

		self.opt_data.opt_lock.acquire()
		self.ivc_data.opt_exp_date = self.opt_data.opt_exp_date
		self.ivc_data.put_K_dict   = self.cp_opt_ivc_data(self.opt_data.put_K_bid_dict, self.opt_data.put_K_ask_dict, cp_="PUT")
		self.ivc_data.call_K_dict  = self.cp_opt_ivc_data(self.opt_data.call_K_bid_dict, self.opt_data.call_K_ask_dict, cp_="CALL")
		self.opt_data.opt_lock.release()
		for k in self.ivc_data.put_K_dict.keys(): 
			self.calc_impl_vol(k, self.ivc_data.put_K_dict[k])
		for k in self.ivc_data.call_K_dict.keys(): 
			self.calc_impl_vol(k, self.ivc_data.call_K_dict[k])
	
	def calc_impl_vol(self, strike_, iv_):
		opt = Option(ex_style_ = "AMERICAN", cp_type_ = iv_.cp_type, \
					trade_date_ = self.ivc_data.val_date, exp_date_ = self.ivc_data.opt_exp_date, \
					S_ = self.ivc_data.S, K_ = strike_, sigma_ = .0, r_ = self.ivc_data.r, \
					q_ = self.ivc_data.q, price_impl_vol_ = iv_.price)
		try: 
			iv_.impl_vol = opt.calcImplVol()
		except RuntimeError, e:
			print "RuntimeError caught: ", e.message
		except:
			print "Unexpected error caught"
		opt.print_out()
		iv_.print_out()

	def cp_opt_ivc_data(self, K_bid_dict_, K_ask_dict_, cp_=""):
		Ks = sorted(set(list(K_bid_dict_.keys()) + list(K_ask_dict_.keys())))
		num = 0
		price = 0.
		ts = 0
		K_dict = {}
		for k in Ks:
			if k in K_bid_dict_.keys(): 
				num += 1
				price += K_bid_dict_[k].price
				if K_bid_dict_[k].ts > ts:
					ts = K_bid_dict_[k].ts
			if k in K_ask_dict_.keys(): 
				num += 1
				price += K_ask_dict_[k].price
				if K_ask_dict_[k].ts > ts:
					ts = K_ask_dict_[k].ts
			K_dict[k] = ImplVol(price_ = price/(num*100.), ts_ = ts, cp_type_ = cp_)
		return K_dict


	def on_exit(self, event):
		self.Destroy()

	def flash_status_message(self, msg, flash_len_ms=1500):
		self.statusbar.SetStatusText(msg)
		self.timeroff = wx.Timer(self)
		self.Bind(
				wx.EVT_TIMER, 
				self.on_flash_status_off, 
				self.timeroff)
		self.timeroff.Start(flash_len_ms, oneShot=True)

	def on_flash_status_off(self, event):
		txt = "fitting at " + time.ctime()
		self.statusbar.SetStatusText(txt)


if __name__ == '__main__':
	app = wx.PySimpleApp()
	app.frame = IVCFrame(None, -1)
	app.frame.Show()
	app.MainLoop()

