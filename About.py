from wxPython.wx import *
import cPickle
import os
from Language import *




class AboutDialog(wxDialog):
	def __init__(self,parent, config, main):
		self.parent=parent
		self.config=config
		self.main=main
		self.language = self.config.read_config("default_language")

		size = wxSize(400, 300)
		wxDialog.__init__(self, parent, wxNewId(), "About ExmanIDE", wxDefaultPosition, size, wxSYSTEM_MENU|wxCAPTION)

		self.panel = wxPanel(self, wxNewId(), wxDefaultPosition, size)
		self.panel.SetBackgroundColour(wxColour(0x8d,0xb7,0xc4))
		EVT_CLOSE(self, self.Cancel)


		png = wxImage(self.main.DEFAULTDIR+"/images/splash.png", wxBITMAP_TYPE_PNG).ConvertToBitmap()
		wxStaticBitmap(self.panel, -1, png, wxPoint(0, 0), wxSize(png.GetWidth(), png.GetHeight()))

		wxStaticText(self.panel , -1 , trans("about_version",self.language)+self.config.read_config("exmanide_version"), wxPoint(20, 185))
		wxStaticText(self.panel , -1 , trans("about_author",self.language), wxPoint(20, 205))
		wxStaticText(self.panel , -1 , trans("about_license",self.language), wxPoint(20, 225))
		wxStaticText(self.panel , -1 , trans("about_thankto",self.language), wxPoint(20, 245))

		self.prev=wxButton(self,2412,trans("OK", self.language),wxPoint(310,270))
		EVT_BUTTON(self,2412,self.Cancel)


	def Cancel(self,event):
		self.EndModal(1)
		self.Destroy()


if __name__=="__main__":
	from BackEnd import *
	DEFAULTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
	class Pmain:
		DEFAULTDIR = "" 

	class Test2(wxApp):
		def __init__(self,redirect=0,argv=[]):
			self.argv = argv
			wxApp.__init__(self,redirect)
		def OnInit(self):
			wxInitAllImageHandlers()
			main = Pmain()
			main.DEFAULTDIR = DEFAULTDIR
			config=Config(".ExmanIDE","config")

			wizard = AboutDialog(None, config, main)

			self.wizard = wizard
			wizard.Centre(wxBOTH)
			wizard.ShowModal()
			return true

	
	program=Test2()
	program.MainLoop()
