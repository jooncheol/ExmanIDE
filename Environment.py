from wxPython.wx import *
from wxPython.stc import *
import cPickle
import os
from Language import *
import string



# validator
ALPHA_ONLY=1
DIGIT_ONLY=2
ALPHADIGIT=3
EMAIL=4
HOSTNAME=5
class MyValidator(wxPyValidator):
	def __init__(self, flag=None, pyVar=None):
		wxPyValidator.__init__(self)
		self.flag = flag
		EVT_CHAR(self, self.OnChar)
	def Clone(self):
		return MyValidator(self.flag)
	def Validate(self, win):
		tc = self.GetWindow()
		val = tc.GetValue()
		if self.flag == ALPHA_ONLY:
			for x in val:
				if x not in string.letters:
					return false
		elif self.flag == DIGIT_ONLY:
			for x in val:
				if x not in string.digits:
					return false
		return true
	def OnChar(self, event):
		key = event.KeyCode()
		if key < WXK_SPACE or key == WXK_DELETE or key > 255:
			event.Skip()
			return
		if self.flag == ALPHA_ONLY and chr(key) in string.letters:
			event.Skip()
			return
		if self.flag == DIGIT_ONLY and chr(key) in string.digits:
			event.Skip()
			return
		if self.flag == ALPHADIGIT and (chr(key) in string.letters or chr(key) in string.digits):
			event.Skip()
			return
		if self.flag == EMAIL and (chr(key) in string.letters or chr(key) in string.digits or chr(key) in ['-','_','@','.']):
			event.Skip()
			return
		if self.flag == HOSTNAME and (chr(key) in string.letters or chr(key) in string.digits or chr(key) in ['-','_','.',':','/']):
			event.Skip()
			return
		if not wxValidator_IsSilent():
			wxBell()
		# Returning without calling even.Skip eats the event before it
		# gets to the text control
		return




class PanelEnv(wxPanel):
	def __init__(self,parent, config, main):
		self.parent=parent
		self.config=config
		self.main=main
		self.language = self.config.read_config("default_language")
		wxPanel.__init__(self, parent, wxNewId(), wxDefaultPosition, self.parent.GetSize())

	def SetEnv(self):
		pass

class CommonEnv(PanelEnv):
	def __init__(self,parent, config, main):
		PanelEnv.__init__(self, parent, config, main,)
		self.Show(false)

		wxStaticBox(self, wxNewId(), trans("LanguageSetting",self.language),pos=wxPoint(5,5), size=wxSize(380,125))

		self.languagesel = wxListBox(self, wxNewId(), wxPoint(20, 30), wxDefaultSize, ['Korean','English'])
		self.languagesel.SetStringSelection(self.language)
		wxStaticText(self, wxNewId(), trans("ChangeToRestart",self.language), wxPoint(20, 100));

		wxStaticBox(self, wxNewId(), trans("SplashWindow",self.language),pos=wxPoint(5,140), size=wxSize(380,70))
		self.splashshow = wxCheckBox(self, wxNewId(), trans("WhenStartingShowSplash",self.language), wxPoint(20, 165))
		ss = self.config.read_config("splash_show")
		if ss=="1" or ss==None:
			self.splashshow.SetValue(true)
		
		pythonbinpath = self.config.read_config("pythonbinpath")
		pythonfiles = ['/usr/bin/python',
					'/usr/bin/python1.5',
					'/usr/bin/python2.1',
					'/usr/bin/python2.2',
					'/usr/bin/python2.3',
					'/usr/bin/python2.4',
					'/usr/bin/python2.5',
					'/usr/bin/python2.6',
					'/usr/bin/python2.7',
					'/usr/bin/python2.8',
					'/usr/bin/python2.9',
					'/usr/bin/python3.1',
					'/usr/bin/python3.2',
					'/usr/bin/python3.3',
					'/usr/bin/python3.4',
					'/usr/bin/python3.5',
					'/usr/bin/python3.6',
					'/usr/bin/python3.7',
					'/usr/bin/python3.8',
					'/usr/bin/python3.9',
					'/usr/local/bin/python1.5',
					'/usr/local/bin/python2.1',
					'/usr/local/bin/python2.2',
					'/usr/local/bin/python2.3',
					'/usr/local/bin/python2.4',
					'/usr/local/bin/python2.5',
					'/usr/local/bin/python2.6',
					'/usr/local/bin/python2.7',
					'/usr/local/bin/python2.8',
					'/usr/local/bin/python2.9',
					'/usr/local/bin/python3.1',
					'/usr/local/bin/python3.2',
					'/usr/local/bin/python3.3',
					'/usr/local/bin/python3.4',
					'/usr/local/bin/python3.5',
					'/usr/local/bin/python3.6',
					'/usr/local/bin/python3.7',
					'/usr/local/bin/python3.8',
					'/usr/local/bin/python3.9']

		if pythonbinpath==None or pythonbinpath=='':
			if os.name=='posix':
				for x in pythonfiles:
					if os.path.exists(x):
						pythonbinpath = x
						break
			else:
				pythonbinpath=''

		wxStaticBox(self, wxNewId(), trans("PythonBinPath",self.language),pos=wxPoint(5,220), size=wxSize(380,70))
		self.pdir = wxTextCtrl(self, -1, pythonbinpath, wxPoint(20, 245), wxSize(320,20))
		png = wxImage(self.main.DEFAULTDIR+'/images/fileopen16.png', wxBITMAP_TYPE_PNG).ConvertToBitmap()
		wxBitmapButton(self, 630, png, wxPoint(345, 240), wxSize(png.GetWidth()+10, png.GetHeight()+10))
		EVT_BUTTON(self, 630, self.OnOpenDir)

		wxStaticBox(self, wxNewId(), trans("RealTimeUpdater",self.language),pos=wxPoint(5,300), size=wxSize(380,70))
		self.autoupdater = wxCheckBox(self, wxNewId(), trans("SetUsingUpdater",self.language), wxPoint(20, 325))
		ss = self.config.read_config("autoupdater")
		#if ss=="1" or ss==None:
		if ss=="1":
			self.autoupdater.SetValue(true)

	def OnOpenDir(self, event):
		opened_dir = os.path.dirname(self.pdir.GetValue())
		wildcard = "All files (*.*)|*.*"
		if opened_dir=="":
			opened_dir=self.main.DEFAULTDIR
		dlg = wxFileDialog(self, "Choose a Project", opened_dir, "", wildcard, wxOPEN)
		if dlg.ShowModal() == wxID_OK:
			path = dlg.GetPath()
			self.config.modify_config("opened_dir",os.path.dirname(path))
			dlg.Destroy()
			self.pdir.SetValue(path)
		else:
			return

	def SetEnv(self):
		self.config.modify_config("default_language",self.languagesel.GetStringSelection())
		self.config.modify_config("splash_show","%d" % int(self.splashshow.GetValue()))
		pythonbinpath = self.pdir.GetValue()
		if pythonbinpath!='' and not os.path.exists(pythonbinpath):
			wxMessageBox(trans("PythonFileNotExist", self.language),"Warning",wxICON_HAND)
			pythonbinpath=''
			self.pdir.SetValue('')
		self.config.modify_config("pythonbinpath",pythonbinpath)

		self.config.modify_config("autoupdater","%d" % int(self.autoupdater.GetValue()))

class EditorEnv(PanelEnv):
	def __init__(self,parent, config, main):
		PanelEnv.__init__(self, parent, config, main,)
		self.Show(false)
		wxStaticBox(self, wxNewId(), "View",pos=wxPoint(5,5), size=wxSize(380,180))
		top = 25; sep=25
		self.witespace = wxCheckBox(self, wxNewId(), trans("view_witespace",self.language), wxPoint(20, top+(sep*0)))
		opt = self.config.read_config("view_witespace")
		if opt=="1": self.witespace.SetValue(true)

		self.endofline = wxCheckBox(self, wxNewId(), trans("view_endofline",self.language), wxPoint(20, top+(sep*1)))
		opt = self.config.read_config("view_endofline")
		if opt=="1": self.endofline.SetValue(true)

		self.indentationguide = wxCheckBox(self, wxNewId(), trans("view_indentationguide",self.language), wxPoint(20, top+(sep*2)))
		opt = self.config.read_config("view_indentationguide")
		if opt=="1": self.indentationguide.SetValue(true)

		self.linenumber = wxCheckBox(self, wxNewId(), trans("view_linenumber",self.language), wxPoint(20, top+(sep*3)))
		opt = self.config.read_config("view_linenumber")
		if opt=="1" or opt==None: self.linenumber.SetValue(true)

		self.margin = wxCheckBox(self, wxNewId(), trans("view_margin",self.language), wxPoint(20, top+(sep*4)))
		opt = self.config.read_config("view_margin")
		if opt=="1" or opt==None: self.margin.SetValue(true)

		self.foldmargin = wxCheckBox(self, wxNewId(), trans("view_foldmargin",self.language), wxPoint(20, top+(sep*5)))
		opt = self.config.read_config("view_foldmargin")
		if opt=="1" or opt==None: self.foldmargin.SetValue(true)


		wxStaticBox(self, wxNewId(), "Tab",pos=wxPoint(5,190), size=wxSize(380,110))
		top = 215; sep=25
		self.autoindent = wxCheckBox(self, wxNewId(), trans("view_autoindent",self.language), wxPoint(20, top+(sep*0)))
		opt = self.config.read_config("view_autoindent")
		if opt=="1" or opt==None: self.autoindent.SetValue(true)

		self.usetabs = wxCheckBox(self, wxNewId(), trans("view_usetabs",self.language), wxPoint(20, top+(sep*1)))
		opt = self.config.read_config("view_usetabs")
		if opt=="1" or opt==None: self.usetabs.SetValue(true)

		wxStaticText(self, wxNewId(), trans("view_tabsize",self.language)+" :", wxPoint(20, top+(sep*2)))
		opt = self.config.read_config("view_tabsize")
		if opt==None: opt = '0'
		self.tabsize = wxTextCtrl(self, wxNewId() , opt, wxPoint(90, top+(sep*2)-3), wxSize(20,20), validator = MyValidator(DIGIT_ONLY))


		wxStaticBox(self, wxNewId(), "Font",pos=wxPoint(5,305), size=wxSize(380,80))
		top = 280; sep=25
		wxStaticText(self, wxNewId(), trans("font_setting",self.language)+" :", wxPoint(20, top+(sep*2)))
		opt = self.config.read_config("font_string")
		if opt==None and self.language=='Korean': opt = 'gothic,times'
		elif opt==None: opt='times'
		self.font_setting = wxTextCtrl(self, wxNewId() , opt, wxPoint(90, top+(sep*2)-3), wxSize(120,20))

		wxStaticText(self, wxNewId(), trans("font_size",self.language)+" :", wxPoint(20, top+(sep*3)))
		opt = self.config.read_config("font_size")
		if opt==None:
			opt="12"
		self.font_size = wxTextCtrl(self, wxNewId() , opt, wxPoint(90, top+(sep*3)-3), wxSize(120,20), validator = MyValidator(DIGIT_ONLY))

	def SetEnv(self):
		opt=self.witespace.GetValue()
		self.config.modify_config("view_witespace",'%d' % int(opt))
		for x in range(self.main.editor.GetPageCount()):
			self.main.editor.GetPage(x).SetViewWhiteSpace(int(opt))

		opt=self.endofline.GetValue()
		self.config.modify_config("view_endofline",'%d' % int(opt))
		for x in range(self.main.editor.GetPageCount()):
			self.main.editor.GetPage(x).SetViewEOL(int(opt))

		opt=self.indentationguide.GetValue()
		self.config.modify_config("view_indentationguide",'%d' % int(opt))
		for x in range(self.main.editor.GetPageCount()):
			self.main.editor.GetPage(x).SetIndentationGuides(int(opt))

		opt=self.linenumber.GetValue()
		self.config.modify_config("view_linenumber",'%d' % int(opt))
		for x in range(self.main.editor.GetPageCount()):
			if int(opt):
				self.main.editor.GetPage(x).SetMarginWidth(0,25)
			else:
				self.main.editor.GetPage(x).SetMarginWidth(0,0)

		opt=self.margin.GetValue()
		self.config.modify_config("view_margin",'%d' % int(opt))
		for x in range(self.main.editor.GetPageCount()):
			if int(opt):
				self.main.editor.GetPage(x).SetMarginWidth(1,15)
			else:
				self.main.editor.GetPage(x).SetMarginWidth(1,0)

		opt=self.foldmargin.GetValue()
		self.config.modify_config("view_foldmargin",'%d' % int(opt))
		for x in range(self.main.editor.GetPageCount()):
			if int(opt):
				self.main.editor.GetPage(x).SetMarginWidth(2,12)
			else:
				self.main.editor.GetPage(x).SetMarginWidth(2,0)

		opt=self.autoindent.GetValue()
		self.config.modify_config("view_autoindent",'%d' % int(opt))
		for x in range(self.main.editor.GetPageCount()):
			if int(opt):
				self.main.editor.GetPage(x).autoindent = 1
			else:
				self.main.editor.GetPage(x).autoindent = 0

		opt=self.usetabs.GetValue()
		self.config.modify_config("view_usetabs",'%d' % int(opt))
		for x in range(self.main.editor.GetPageCount()):
			self.main.editor.GetPage(x).SetUseTabs(int(opt))

		opt=self.tabsize.GetValue()
		if int(opt)<0:
			self.tabsize.SetValue('0')
		self.config.modify_config("view_tabsize",'%d' % int(self.tabsize.GetValue()))
		for x in range(self.main.editor.GetPageCount()):
			self.main.editor.GetPage(x).SetIndent(int(opt))

		opt=self.font_setting.GetValue()
		opt2=self.font_size.GetValue()
		if opt.strip()=='':
			if self.language=='Korean': 
				opt = 'gothic,times'
			else: 
				opt='times'
		a=self.config.modify_config("font_string",'%s' % opt)
		a=self.config.modify_config("font_size",'%d' % int(opt2))
		
		# 두번씩 실행해야지 되는 원인은?
		for x in range(self.main.editor.GetPageCount()):
			self.main.editor.GetPage(x).SetStyles()
			self.main.editor.GetPage(x).SetStyles()
		self.main.profile.stderr.SetStyles()
		self.main.profile.stderr.SetStyles()
		if self.config.read_config("locals_not_show")!='1':
			self.main.profile.description.SetStyles()
			self.main.profile.description.SetStyles()
		self.main.profile.shell.SetStyles()
		self.main.profile.shell.SetStyles()
		self.main.Refresh()


class DebuggerEnv(PanelEnv):
	def __init__(self,parent, config, main):
		PanelEnv.__init__(self, parent, config, main,)
		self.Show(false)
		wxStaticBox(self, wxNewId(), "Locals",pos=wxPoint(5,5), size=wxSize(380,70))
		self.localsshow = wxCheckBox(self, wxNewId(), trans("ForSpeedLocalsOff",self.language), wxPoint(20, 25))
		ss = self.config.read_config("locals_not_show")
		if ss=="1":
			self.localsshow.SetValue(true)
	def SetEnv(self):
		if self.config.read_config("locals_not_show")!='1' and int(self.localsshow.GetValue())==1:
			self.main.profile.SetLocals(0)
		elif self.config.read_config("locals_not_show")=='1' and int(self.localsshow.GetValue())==0:
			self.main.profile.SetLocals(1)
		self.config.modify_config("locals_not_show","%d" % int(self.localsshow.GetValue()))

class Environment(wxDialog):
	def __init__(self,parent, config, main):
		self.parent=parent
		self.config=config
		self.main=main
		self.language = self.config.read_config("default_language")

		size = wxSize(600, 500)
		wxDialog.__init__(self, parent, wxNewId(), "ExmanIDE Setup", wxDefaultPosition, size, wxSYSTEM_MENU|wxCAPTION)

		self.panel = wxPanel(self, wxNewId(), wxDefaultPosition, size)
		EVT_CLOSE(self, self.Cancel)

		self.menu = wxPanel(self.panel, wxNewId(), pos=wxPoint(15, 12), size=wxSize(180,450), style=wxSUNKEN_BORDER)

		self.title = wxPanel(self, wxNewId(), pos=wxPoint(200,10), size=wxSize(390,25), style=wxSUNKEN_BORDER)
		self.title.SetBackgroundColour(wxColour(0x6C,0x8B,0xB9))
		str = "Title"
		self.titletext = wxStaticText(self.title, -1, str, pos=wxPoint(3, 3))
		self.titletext.SetForegroundColour(wxColour(0xff,0xff,0xff))


		self.left = wxTreeCtrl(self.menu, wxNewId(), size=wxSize(180, 420), pos=wxPoint(0, 23),style=wxTR_HIDE_ROOT)
		self.root = self.left.AddRoot("Envirionment")
		self.left.SetPyData(self.root, "Root")


		bodysize = wxSize(390, 420)
		self.body = wxPanel(self, wxNewId(), pos=wxPoint(200,40), size=bodysize, style=wxSUNKEN_BORDER)
		self.body.title = self.titletext
		self.body.left = self.left

		wxButton(self.menu, wxNewId(), trans("Sections",self.language), size=wxSize(176,22), pos=wxPoint(1,1))

		default = self.left.AppendItem(self.root, trans("Env_Common",self.language))
		self.left.SetPyData(default, CommonEnv(self.body, config, main))
		newchild = self.left.AppendItem(self.root, trans("Env_Editor",self.language))
		self.left.SetPyData(newchild, EditorEnv(self.body, config, main))
		newchild = self.left.AppendItem(self.root, trans("Env_Debugger",self.language))
		self.left.SetPyData(newchild, DebuggerEnv(self.body, config, main))

		EVT_TREE_SEL_CHANGED(self.left, -1, self.onSelectEnv)




		self.prev=wxButton(self,2410,trans("OK", self.language),wxPoint(330,470))
		EVT_BUTTON(self,2410,self.DoOk)
		self.prev=wxButton(self,2411,trans("Apply", self.language),wxPoint(415,470))
		EVT_BUTTON(self,2411,self.DoApply)
		self.prev=wxButton(self,2412,trans("Cancel", self.language),wxPoint(500,470))
		EVT_BUTTON(self,2412,self.Cancel)

		self.currentBody = self.left.GetItemData(default).GetData()
		self.currentBody.Show(true)
		self.left.SelectItem(default)

	def onSelectEnv(self,event):
		item = self.left.GetSelection()
		data=self.left.GetItemData(item).GetData()
		if data!="Root":
			self.titletext.SetLabel(self.left.GetItemText(self.left.GetSelection()))
			if self.currentBody!=None:
				self.currentBody.Show(false)
			data.Show(true)
			self.currentBody=data


	def DoOk(self,event):
		self.DoApply(event)
		self.Cancel(event)

	def DoApply(self,event):
		for x in range(self.left.GetChildrenCount(self.root)):
			item, cookie = self.left.GetNextChild(self.root, x)
			data=self.left.GetItemData(item).GetData()
			data.SetEnv()

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

			wizard = Environment(None, config, main)

			self.wizard = wizard
			wizard.Centre(wxBOTH)
			wizard.ShowModal()
			return true

	
	program=Test2()
	program.MainLoop()
