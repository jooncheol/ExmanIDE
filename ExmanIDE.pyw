#!/usr/bin/env python
import sys
from wxPython.wx import *
from FrontEnd import *
from BackEnd import *
from Language import *
import os, sys

DEFAULTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))

# Warning Message
class warn(wxApp):
	def __init__(self,message,caption,style=wxICON_HAND):
		self.message=message
		self.caption=caption
		self.style=style
		wxApp.__init__(self)

	def OnInit(self):
		wxMessageBox(self.message,self.caption,self.style)
		return true


def StartingWork(main):
	main.SetTopWindow(main.window)
	main.SetAppName("ExmanIDE")
	main.SetVendorName("www.exman.pe.kr")

	# Open the Position/Size from Config
	widget_pos = main.window.config.read_config("widget_pos") 
	if widget_pos!="":
		widget_pos = tuple(map(int, widget_pos.split(",")))
		main.window.Move(widget_pos)
	widget_size = main.window.config.read_config("widget_size") 
	if widget_size!="":
		widget_size = tuple(map(int, widget_size.split(",")))
		main.window.SetSize(widget_size)

	return main.window


class MySplashScreen(wx.SplashScreen):
	def __init__(self, main):
		png = wxImage(DEFAULTDIR+"/images/splash.png", wxBITMAP_TYPE_PNG).ConvertToBitmap()
		wx.SplashScreen.__init__(self, png,
								wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT,
								1500, None, -1,
								style = wxSIMPLE_BORDER|wxFRAME_NO_TASKBAR|wxSTAY_ON_TOP)
		self.main = main

		window = StartingWork(self.main)

		EVT_CLOSE(self, self.OnClose)

	def OnClose(self, evt):
		self.main.window.Show(true)
		evt.Skip()  

#---------------------------------------------------------------------------
class ExmanIDE(wxApp):
	def __init__(self,redirect=0,argv=[]):
		self.argv = argv
		wxApp.__init__(self,redirect)
	def OnInit(self):

		wxInitAllImageHandlers()

		self.window=ExmanIDEFrontEnd(self.argv)

		ss = self.window.config.read_config("splash_show")
		if ss=="1" or ss==None:
			splash = MySplashScreen(self)
			splash.Show()
		else:
			self.window = StartingWork(self)
			self.window.Show(true)


		return true
#---------------------------------------------------------------------------

if __name__=='__main__':
	if int(sys.version[0])<2:
		program=warn("ExmanIDE is designed for Python2.0 or higher","ExmanIDE",wxICON_INFORMATION)
		program.MainLoop()
	else:
		import getopt
		optlist, args = getopt.getopt(sys.argv[1:], 'x', ['debug',])
		"""
		if len(args)>0:
			import os
			os.chdir(os.path.abspath(os.path.dirname(args[0])))
		"""
		program=ExmanIDE(redirect=0, argv=args)
		program.MainLoop()
"""
 * Local variables:
 * tab-width: 4
 * c-basic-offset: 4
 * End:
 * vim600: sw=4 ts=4 tw=78 fdm=marker
 * vim<600: sw=4 ts=4 tw=78
"""
