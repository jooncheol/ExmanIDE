from wxPython.wx import *
import cPickle
import os
from Language import *
import string
import urllib2
import time

class Project:
	def __init__(self, filename=None):
		if filename!=None:
			self.projectfilename = filename
			self.LoadProject(filename)
		else:
			self.projectfilename = None
			self.project = {
				"name": "",
				"version": "0.1",
				"author": "",
				"email": "",
				"homepage": "",
				"sourceheader": "",
				"openfiles": [],
				"extra": None,
			}
	def GetName(self):
		return self.project["name"]
	def GetVersion(self):
		return self.project["version"]
	def GetAuthor(self):
		return self.project["author"]
	def GetEmail(self):
		return self.project["email"]
	def GetHomepage(self):
		return self.project["homepage"]
	def GetSourceHeader(self):
		return self.project["sourceheader"]
	def GetOpenFiles(self):
		return self.project["openfiles"]

	def SetName(self, value):
		self.project["name"] = value
	def SetVersion(self, value):
		self.project["version"] = value
	def SetAuthor(self, value):
		self.project["author"] = value
	def SetEmail(self, value):
		self.project["email"] = value
	def SetHomepage(self, value):
		self.project["homepage"] = value
	def SetSourceHeader(self, value):
		self.project["sourceheader"] = value

	def SetValue(self, key, value):
		self.project[key] = value

	def GetValue(self, key):
		return self.project[key]

	def SaveProject(self, filename=None):
		if filename==None:
			filename = self.projectfilename
		else:
			filename = os.path.abspath(filename)

		cPickle.dump(self.project, open(filename,"wb"), 1)

	def LoadProject(self, filename):
		if os.name=='nt':
			self.projectdir = os.path.dirname(filename).replace("\\","/")
		else:
			self.projectdir = os.path.dirname(filename)
		self.projectfilename = os.path.abspath(filename)
		self.project = cPickle.load(open(filename,"rb"))

	def AddOpenFile(self, dir, filename, breakpoints, argument="", firstvisible=0, currentline=0, extdata=None):
		if os.name=='nt':
			dir = dir.replace("\\","/")
		if dir[-1:]=="/":
			dir=dir[-1:]
		if dir==self.projectdir:
			dir=None
		self.project["openfiles"].append([dir, filename, breakpoints, argument, firstvisible, currentline, extdata])

	def DelOpenFile(self, filename):
		if os.name=='nt':
			filename = filename.replace("\\","/")
		newopenfiles = []
		for x in self.project["openfiles"]:
			if x[0]+self.pathsep+x[1] != filename:
				newopenfiles.append(x)

		self.project["openfiles"]=newopenfiles



#---------------------------------------------------------------------------
# Wizard Panel
class WizardPanel(wxPanel):
	def __init__(self,parent, config, main, Size, menu, default, title, info):
		wxPanel.__init__(self, parent, wxNewId(), wxPoint(0,0), Size)
		self.panel = [self, ]
		#self.SetBackgroundColour(wxColour(255,255,255));
		self.menu=menu
		self.default=default
		self.info=info
		self.parent=parent
		self.config=config
		self.main=main
		self.language = self.config.read_config("default_language")

		# top menu
		png = wxImage(self.info["setup_path"]+'/images/projectwizard.png', wxBITMAP_TYPE_PNG).ConvertToBitmap()
		wxStaticBitmap(self, -1, png, wxPoint(0, 0), wxSize(png.GetWidth(), png.GetHeight()))
		
		# top menu title
		wxStaticText(self,-1, title ,wxPoint(40,90),wxDefaultSize)


		self.prev=wxButton(self,400,trans("Cancel", self.language),wxPoint(20,520))
		EVT_BUTTON(self,400,self.Cancel)

		self.prev=wxButton(self,100,trans("Back", self.language),wxPoint(320,520))
		EVT_BUTTON(self,100,self.Previous)
		self.next=wxButton(self,200,trans("Next", self.language),wxPoint(410,520))
		if default == 0:
			self.prev.Enable(false)

		if default == len(menu)-1:
			self.next.SetLabel(trans("Finish",self.language))
			EVT_BUTTON(self,200,self.Finish)
		else:
			EVT_BUTTON(self,200,self.Next)

		self.view()

	# derived method
	def view(self):
		pass
	
	def EnableNext(self):
		if self.default != len(self.menu)-1:
			self.next.Enable(true)

	def DisableNext(self):
		self.next.Enable(false)

	def autoPrev(self,prevcount=1):
		self.Show(false)
		self.panel[self.default-prevcount].Show(true)
	def autoNext(self,nextcount=1):
		self.Show(false)
		self.panel[self.default+nextcount].Show(true)
	def Previous(self,event):
		self.Show(false)
		self.panel[self.default-1].Show(true)

	def Next(self,event):
		self.autoNext()

	def Finish(self,event):
		self.parent.EndModal(1)
		self.parent.Destroy()

	def Cancel(self,event):
		self.parent.Close()

	def SetPanel(self, panel):
		self.panel = panel


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



class ProjectNewintro(WizardPanel):
	def view(self):
		wxStaticBox(self,-1,trans("ProjectType", self.language),wxPoint(20,130),wxSize(200,360))
		self.treeid = wxNewId()
		self.tree = wxTreeCtrl(self,self.treeid, wxPoint(30, 150), wxSize(180, 305),wxTR_HIDE_ROOT)
		self.root = self.tree.AddRoot(trans("Project",self.language))
		self.tree.SetPyData(self.root, "Root")

		custom = self.tree.AppendItem(self.root, trans("Project_Custom",self.language))
		self.tree.SetPyData(custom, "custom")

		#self.tree.Expand(self.root)
		EVT_TREE_SEL_CHANGED(self, self.treeid, self.onClick)
		self.tree.SelectItem(custom)

		# Getting project template from Internet
		self.fromInternet=wxButton(self,611,trans("GettingProjectFromInternet", self.language),wxPoint(30,460),wxSize(180, 20))
		EVT_BUTTON(self,611,self.GettingProjectFromInternet)

		# use project list cache
		cachefile = os.getenv("HOME")+"/.ExmanIDE/ExmanIDEProjectsList.txt"
		if os.path.exists(cachefile):
			list = open(cachefile).readlines()
			self.FillProjectFromInternet(list)


		wxStaticBox(self,-1,trans("ProjectSetting", self.language),wxPoint(225,130),wxSize(260,360))
		wxStaticText(self,-1, trans("ProjectName", self.language)+" :" ,wxPoint(235,150),wxDefaultSize)
		self.pname = wxTextCtrl(self, 610 , "", wxPoint(235, 170), wxSize(205,20), validator = MyValidator(HOSTNAME))
		EVT_TEXT(self, 610, self.onPname)

		wxStaticText(self,-1, trans("ProjectDir", self.language)+" :" ,wxPoint(235,195),wxDefaultSize)
		opened_dir = self.config.read_config("opened_dir")
		if opened_dir=="" or opened_dir==None:
			opened_dir = os.getenv("HOME")
		if len(opened_dir)>0 and opened_dir[-1:]!=self.config.pathsep:
			opened_dir = opened_dir + self.config.pathsep
		self.pdir = wxTextCtrl(self, -1, opened_dir, wxPoint(235, 215), wxSize(205,20))
		self.pdir.SetEditable(false)

		png = wxImage(self.info["setup_path"]+'/images/fileopen16.png', wxBITMAP_TYPE_PNG).ConvertToBitmap()
		wxBitmapButton(self, 630, png, wxPoint(445, 210), wxSize(png.GetWidth()+10, png.GetHeight()+10))
		EVT_BUTTON(self, 630, self.OnOpenDir)

		wxStaticText(self,-1, trans("ProjectVersion", self.language)+" :" ,wxPoint(235,240),wxDefaultSize)
		self.pver = wxTextCtrl(self, -1, "0.1", wxPoint(235, 260), wxSize(205,20))

		author = self.config.read_config("author")
		if author==None:
			author=""
		wxStaticText(self,-1, trans("ProjectAuthor", self.language)+" :" ,wxPoint(235,285),wxDefaultSize)
		self.pauthor = wxTextCtrl(self, -1, author, wxPoint(235, 305), wxSize(205,20))

		email = self.config.read_config("email")
		if email==None:
			email=""
		wxStaticText(self,-1, trans("ProjectAuthorEmail", self.language)+" :" ,wxPoint(235,330),wxDefaultSize)
		self.pemail = wxTextCtrl(self, -1, email, wxPoint(235, 350), wxSize(205,20), validator = MyValidator(EMAIL))

		homepage = self.config.read_config("homepage")
		if homepage==None:
			homepage=""
		wxStaticText(self,-1, trans("ProjectHomepage", self.language)+" :" ,wxPoint(235,375),wxDefaultSize)
		self.phomepage = wxTextCtrl(self, -1, homepage, wxPoint(235, 395), wxSize(205,20), validator = MyValidator(HOSTNAME))


		self.DisableNext()

	def FillProjectFromInternet(self, list):
		for x in list:

			temp = map(string.strip, x.split("|"))
			Path = temp[0]
			defaultString = "N/A"
			listString = None
			for y in temp[1:]:
				try:
					language,str = y.split(":",1)
				except:
					return
				if language=="English":
					defaultString = str
				if language == self.language:
					listString = str
					break
			else:
				listString = defaultString
			
			for x in range(self.tree.GetCount()):
				child, cookie = self.tree.GetNextChild(self.root, x)
				data = self.tree.GetItemData(child).GetData()
				if data==Path:
					break
			else:
				project = self.tree.AppendItem(self.root, listString)
				self.tree.SetPyData(project, Path)
				
			
			

	def GettingProjectFromInternet(self, event):
		url = 'http://exmanide.kldp.net/ExmanIDEProjectsList.txt'
		try:
			con = urllib2.urlopen(url)
		except urllib2.URLError, str:
			return
		list = con.readlines()

		self.FillProjectFromInternet(list)
        

	def OnOpenDir(self, event):
		opened_dir = self.pdir.GetValue()
		dlg = wxDirDialog(self, "Choose a Project directory", defaultPath=opened_dir, style=wxDD_DEFAULT_STYLE|wxDD_NEW_DIR_BUTTON)
		if dlg.ShowModal() == wxID_OK:
			path = dlg.GetPath()
			self.config.modify_config("opened_dir",path)
			dlg.Destroy()
			if len(path)>0 and path[-1:]!=self.config.pathsep:
				path = path + self.config.pathsep
			self.pdir.SetValue(path)
			self.pname.SetValue("")
		else:
			return

	def onPname(self, event):
		opened_dir = os.path.dirname(self.pdir.GetValue())
		if os.path.exists(opened_dir):
			self.pdir.SetValue(opened_dir+self.config.pathsep+self.pname.GetValue())
		self.checkNext()


	def checkNext(self):
		item = self.tree.GetSelection()
		data=self.tree.GetItemData(item).GetData()
		if data=="Root":
			self.DisableNext()
			return
		try:
			if len(self.pname.GetValue())==0:
				self.DisableNext()
				return
		except:
			pass

		self.EnableNext()

	def onClick(self, event):
		item = self.tree.GetSelection()
		data=self.tree.GetItemData(item).GetData()
		#print data
		self.checkNext()
	
	def Next(self, event):
		self.info["project_name"] = self.pname.GetValue()
		self.info["project_dir"] = self.pdir.GetValue()
		self.info["project_version"] = self.pver.GetValue()
		self.info["project_author"] = self.pauthor.GetValue()
		self.info["project_email"] = self.pemail.GetValue()
		self.info["project_homepage"] = self.phomepage.GetValue()
		self.info["project_template"] = self.tree.GetItemData(self.tree.GetSelection()).GetData()

		self.autoNext()


class ProjectHeader(WizardPanel):
	def view(self):
		header = '''"""
	This file is .
"""
#***************************************************************************
#                          %FILENAME%  -  description
#
#    begin                : %DATE%
#    copyright            : (C) %YEAR% by %AUTHOR%
#    email                : %EMAIL%
#    homepage             : %HOMEPAGE%
#
#***************************************************************************

#***************************************************************************
#                                                                          
#   This program is free software; you can redistribute it and/or modify   
#   it under the terms of the GNU General Public License as published by   
#   the Free Software Foundation; either version 2 of the License, or      
#   (at your option) any later version.                                    
#                                                                          
#***************************************************************************
'''
		wxStaticText(self,-1, trans("SourceHeaderTemplate",self.language) ,wxPoint(20,130),wxDefaultSize)
		self.header=wxTextCtrl(self, -1, header, pos=wxPoint(20,155), size=wxSize(460,345),style=wxTE_MULTILINE|wxTE_RICH)

	def Next(self, event):
		self.info["project_sourceheader"]=self.header.GetValue()
		self.autoNext()


class ProjectFinish(WizardPanel):
	def Finish(self, event):
		try:
			os.makedirs(self.info["project_dir"])
		except OSError:
			if wxMessageBox(trans("AlreadyProjectDir", self.language),"Information",wxYES_NO|wxNO_DEFAULT) == wxNO:
				return
		except:
			wxMessageBox(trans("FailtoMakeProject", self.language),"Warning",wxICON_HAND)
			return
		if self.info["project_dir"][-1:]==self.config.pathsep:
			self.info["project_dir"] = self.info["project_dir"][-1:]

		projectfile = self.info["project_dir"]+self.config.pathsep + self.info["project_name"] + ".exprj"

		prj = Project()
		prj.SetName(self.info["project_name"])
		prj.SetVersion(self.info["project_version"])
		prj.SetAuthor(self.info["project_author"])
		prj.SetEmail(self.info["project_email"])
		prj.SetHomepage(self.info["project_homepage"])
		prj.SetSourceHeader(self.info["project_sourceheader"])
		prj.SaveProject(projectfile)
		
		self.config.modify_config("author",self.info["project_author"])
		self.config.modify_config("email",self.info["project_email"])
		self.config.modify_config("homepage",self.info["project_homepage"])
		
		# project template from Internet
		if self.info["project_template"] != "custom":
			wait = wxBusyInfo(trans("WaitForDownloadProject", self.language))
			wxYield()
			import time
			time.sleep(3)
			try:
				con = urllib2.urlopen(self.info["project_template"] )
			except urllib2.URLError, str:
				wxMessageBox(trans("DownloadFail", self.language),"Warning",wxICON_HAND)
				return
			open("/tmp/aaa.zip","wb").write( con.read())
				
			
		
		WizardPanel.Finish(self, event)

		self.main.explorer.AddProject(projectfile)
		self.main.SetRecentProject(projectfile)


class ProjectConfigurator(wxDialog):
	def __init__(self,parent, config, main, projectfile = ""):
		self.parent=parent
		self.config=config
		self.main=main
		self.language = self.config.read_config("default_language")

		size = wxSize(500, 490)
		wxDialog.__init__(self, parent, wxNewId(), "Project Configurator", wxDefaultPosition, size, wxSYSTEM_MENU|wxCAPTION)

		self.panel = wxPanel(self, wxNewId(), wxDefaultPosition, size)
		EVT_CLOSE(self, self.Cancel)


		self.projectlist = self.main.explorer.GetOpenProject()

		self.prj = []
		for x in self.projectlist:
			self.prj.append(Project(x))

		if projectfile=="":
			projectfile = self.projectlist[0]

		wxStaticText(self.panel,-1, trans("ProjectName", self.language)+" :" ,wxPoint(20, 20),wxDefaultSize)
		self.combo =  wxComboBox(self.panel, 640, projectfile, wxPoint(100, 18), wxDefaultSize, self.projectlist, wxCB_DROPDOWN|wxCB_READONLY)
		size = self.combo.GetSize()
		if size[0] > 385:
			self.combo.SetSize((385, 20))
		else:
			self.combo.SetSize((size[0], 20))
		EVT_COMBOBOX(self.panel, 640, self.onChangeProject)

		wxStaticBox(self.panel,-1,trans("ProjectSetting", self.language),wxPoint(15,50),wxSize(472,400))

		wxStaticText(self.panel,-1, trans("ProjectVersion", self.language)+" :" ,wxPoint(25,80),wxDefaultSize)
		self.pver = wxTextCtrl(self.panel, 680, self.prj[0].GetVersion(), wxPoint(120, 75), wxSize(330,20))
		EVT_TEXT(self, 680, self.onChangeValue)

		wxStaticText(self.panel,-1, trans("ProjectAuthor", self.language)+" :" ,wxPoint(25,110),wxDefaultSize)
		self.pauthor = wxTextCtrl(self.panel, 681, self.prj[0].GetAuthor(), wxPoint(120, 105), wxSize(330,20))
		EVT_TEXT(self, 681, self.onChangeValue)

		wxStaticText(self.panel,-1, trans("ProjectAuthorEmail", self.language)+" :" ,wxPoint(25,140),wxDefaultSize)
		self.pemail = wxTextCtrl(self.panel, 682, self.prj[0].GetEmail(), wxPoint(120, 135), wxSize(330,20), validator = MyValidator(EMAIL))
		EVT_TEXT(self, 682, self.onChangeValue)

		wxStaticText(self.panel,-1, trans("ProjectHomepage", self.language)+" :" ,wxPoint(25,170),wxDefaultSize)
		self.phomepage = wxTextCtrl(self.panel, 683, self.prj[0].GetHomepage(), wxPoint(120, 165), wxSize(330,20), validator = MyValidator(HOSTNAME))
		EVT_TEXT(self, 683, self.onChangeValue)

		wxStaticText(self.panel, -1, trans("SourceHeaderTemplate", self.language), wxPoint(25, 200), wxDefaultSize)
		self.header=wxTextCtrl(self.panel, 684, self.prj[0].GetSourceHeader(), pos=wxPoint(25,220), size=wxSize(450,220),style=wxTE_MULTILINE|wxTE_RICH)
		EVT_TEXT(self, 684, self.onChangeValue)


		self.cancel=wxButton(self,670,trans("Cancel", self.language),wxPoint(15,460))
		EVT_BUTTON(self,670,self.Cancel)

		self.save=wxButton(self,671,trans("Apply", self.language),wxPoint(315,460))
		EVT_BUTTON(self,671,self.Save)
		self.next=wxButton(self,672,trans("OK", self.language),wxPoint(405,460))
		EVT_BUTTON(self,672,self.SaveClose)
	
	def onChangeValue(self, event):
		projectfile = self.combo.GetValue()
		for x in range(len(self.projectlist)):
			if self.projectlist[x] == projectfile:
				prj = self.prj[x]
				break
		else:
			event.Skip()
			return
		value = event.GetString()
		if event.GetId()==680:
			prj.SetVersion(value)
		if event.GetId()==681:
			prj.SetAuthor(value)
		if event.GetId()==682:
			prj.SetEmail(value)
		if event.GetId()==683:
			prj.SetHomepage(value)
		if event.GetId()==684:
			prj.SetSourceHeader(value)

	def onChangeProject(self, event):
		projectfile = self.combo.GetValue()
		for x in range(len(self.projectlist)):
			if self.projectlist[x] == projectfile:
				prj = self.prj[x]
				break
		else:
			event.Skip()
			return
		self.pver.SetValue(prj.GetVersion())
		self.pauthor.SetValue(prj.GetAuthor())
		self.pemail.SetValue(prj.GetEmail())
		self.phomepage.SetValue(prj.GetHomepage())
		self.header.SetValue(prj.GetSourceHeader())


	def Save(self,event):
		projectfile = self.combo.GetValue()
		for x in range(len(self.projectlist)):
			if self.projectlist[x] == projectfile:
				prj = self.prj[x]
				break
		else:
			event.Skip()
			return
		prj.SaveProject()

	def SaveClose(self,event):
		self.Save(event)
		self.Cancel(event)

	def Cancel(self,event):
		self.EndModal(1)
		self.Destroy()


if __name__=="__main__":
	from BackEnd import *
	DEFAULTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
	class Test(wxApp):
		def __init__(self,redirect=0,argv=[]):
			self.argv = argv
			wxApp.__init__(self,redirect)
		def OnInit(self):
			wxInitAllImageHandlers()
			config=Config(".ExmanIDE","config")

			size = wxSize(500, 550)
			wizard = wxDialog(NULL, wxNewId(), "Project Wizard", wxDefaultPosition, size, wxSYSTEM_MENU|wxCAPTION)

			menutitle = ["새 프로젝트","소스헤더 템플릿", "마침"]
			menupanel = [ProjectNewintro, ProjectHeader, ProjectFinish]

			setupinfo = {"setup_path":DEFAULTDIR,"opened_dir":"/source/Python/test"}

			panel = []
			for x in range(len(menupanel)):
				panel.append(menupanel[x](wizard, config, NULL, size, menupanel, x, menutitle[x], setupinfo))
				panel[x].Show(false)
			for x in panel:
				x.SetPanel(panel)

			panel[0].Show(true)

			wizard.Centre(wxBOTH)
			wizard.ShowModal()
			return true

	class Test2(wxApp):
		def __init__(self,redirect=0,argv=[]):
			self.argv = argv
			wxApp.__init__(self,redirect)
		def OnInit(self):
			wxInitAllImageHandlers()
			config=Config(".ExmanIDE","config")

			wizard = ProjectConfigurator(None, config, None)

			self.wizard = wizard
			wizard.Centre(wxBOTH)
			wizard.Show(true)
			return true

	
	program=Test2()
	program.MainLoop()
