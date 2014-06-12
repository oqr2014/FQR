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
from opt_attr import *
from option import *
from xml_conf import *

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
		self.fitIvc      = FitIvc(self.opt_data, self.ivc_data)
		self.gw_conf     = GatewayConf()
		self.opt_attr_ps = OptAttrParser(filename_ = self.gw_conf.opt_sym)
		self.Ks          = sorted(self.opt_attr_ps.K_set)
		self.paused      = True
		self.create_menu()
		self.create_status_bar()
		self.create_main_panel()
		self.timer       = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_recalc_ivc, self.timer)        
		self.timer.Start(5000)  #Every 10 secs

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
		self.valdate_txt_ctrl = wx.TextCtrl(self.panel, value=str(self.gw_conf.val_dt))
		self.r_lb             = wx.StaticText(self.panel, label="Risk free rate")
		self.r_txt_ctrl       = wx.TextCtrl(self.panel, value=str(self.gw_conf.rf_rate))
		self.q_lb             = wx.StaticText(self.panel, label="Dividend rate")
		self.q_txt_ctrl       = wx.TextCtrl(self.panel, value=str(self.gw_conf.div_rate))

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

		tmp_opt = [random.random() for i in range(100)]
		tmp_fit = [random.random() for i in range(100)]
		self.plot_opt = self.axes.plot(range(100), tmp_opt, 'yo', label='Options')[0]
		self.plot_fit = self.axes.plot(range(100), tmp_fit, color='green', label='Poly Fit')[0]
		self.plot_K_line = self.axes.plot(50*np.ones(100), np.arange(100)/100.)[0]

	def draw_ivc(self):
		self.fitIvc.poly_fit_ivc(degree_=5)
		self.axes.set_xbound(lower = min(self.fitIvc.Ks), upper = max(self.fitIvc.Ks))
		self.axes.set_ybound(lower=0., upper=max(self.fitIvc.ivs))
		self.axes.grid(True, color='gray')
		pylab.setp(self.axes.get_xticklabels(), visible=True)
		self.plot_opt.set_xdata(self.fitIvc.Ks)
		self.plot_opt.set_ydata(self.fitIvc.ivs)
		self.plot_fit.set_xdata(self.fitIvc.Ks)
		self.plot_fit.set_ydata(self.fitIvc.fitted_ivs)
		self.plot_K_line.set_xdata(np.ones(100)*self.ivc_data.S)
		self.plot_K_line.set_ydata(np.arange(100)/100.*max(self.fitIvc.ivs))

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
			self.fitIvc.cvrtOpt2Ivc()
			self.draw_ivc()

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

