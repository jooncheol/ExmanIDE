from wxPython.wx import *
from BackEnd import *
import Language
import sys
import os, signal
import icon
from TotalExplorer import *
from SourceEditor import *
from Profile import *
from Project import *
from Environment import *
from About import *
import cPickle
import getext
from ExmanUpdaterClient import *
import thread

# Backend UDP Server Associated
from udplog import *
wxEvt_RecvUDP=wxNewId()
def EVT_RECEIVEUDPSERVER(theParent, theFunc):
	theParent.Connect(-1,-1, wxEvt_RecvUDP, theFunc)
class RecvUDPServerMessage(wxPyEvent):
	def __init__(self,content='',addr=()):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEvt_RecvUDP)
		self.content = content
		self.addr=addr
		

# Backend TCP Server Associated
from tcplog import *
wxEvt_RecvTCP=wxNewId()
def EVT_RECEIVETCPSERVER(theParent, theFunc):
	theParent.Connect(-1,-1, wxEvt_RecvTCP, theFunc)
class RecvTCPServerMessage(wxPyEvent):
	def __init__(self,content='',addr=()):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEvt_RecvTCP)
		self.content = content
		self.addr=addr




# Updater Associated
wxEvt_Updater=wxNewId()
def EVT_UPDATER(theParent, theFunc):
	theParent.Connect(-1,-1, wxEvt_Updater, theFunc)
class UpdaterAction(wxPyEvent):
	def __init__(self, updater):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEvt_Updater)
		self.updater = updater




# Translate Function Pointer
trans = None

# Default Dir
DEFAULTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))


class ExmanIDEFrontEnd(wxFrame):
	def __init__(self, argv=[]):
		self.argv = argv
		# Load a Config
		debug("Loading Configurator File")
		self.config=Config(".ExmanIDE","config")
		self.DEFAULTDIR = DEFAULTDIR

		# Get Character Setting / Setting Translate Function
		language = self.config.read_config("default_language")
		global trans
		trans = lambda x: Language.trans(x, language)

		# Execute Path
		self.their_default_dir=os.path.dirname(sys.argv[0])
		if self.their_default_dir=='':
			self.their_default_dir='.'

		wxFrame.__init__(self, None, -1, trans("ProgramTitle")+" "+self.config.read_config("exmanide_version"), wxPyDefaultPosition, wxSize(700,500),wxDEFAULT_FRAME_STYLE)
		
		
		# Set up the icon
		debug("Loading Icon File")
		self.SetIcon(icon.getIcon())

		# Bind Event
		EVT_CLOSE(self, self.OnCloseWindow)
		
		# Create Status bar
		self.CreateStatusBar(3)
		self.SetStatusWidths([-1, 70,140])
		
		# Prepare the menubar
		self.menubar = wxMenuBar()
		
		self.menuFile = wxMenu()
		self.menuFile.Append(104, trans("Menu_File_New"), trans("Menu_File_New"))
		self.menuFile.Append(102, trans("Menu_File_Open"), trans("Menu_File_Open"))
		self.menuFile.Append(105, trans("Menu_File_Save"), trans("Menu_File_Save"))
		self.menuFile.Append(106, trans("Menu_File_SaveAs"), trans("Menu_File_SaveAs"))
		self.menuFile.AppendSeparator()
		self.menuFile.Append(108, trans("Menu_File_Directory_Open"), trans("Menu_File_Directory_Open"))

		self.MenuRecentDirs = wxMenu()
		self.menuFile.AppendMenu(249, trans("Menu_File_RecentDir"), self.MenuRecentDirs)
		self.GetRecentDirs()

		self.MenuRecentFiles = wxMenu()
		self.menuFile.AppendMenu(149, trans("Menu_File_RecentFile"), self.MenuRecentFiles)
		self.GetRecentFiles()

		self.menuFile.AppendSeparator()
		self.menuFile.Append(101, trans("Menu_File_Exit"), trans("Menu_File_Exit_Status"))
		self.menubar.Append(self.menuFile,trans("Menu_File"))


		self.menuEdit = wxMenu()
		self.menuEdit.AppendSeparator()
		self.menuEdit.Append(502, trans("Menu_Edit_Undo"), trans("Menu_Edit_Undo"))
		self.menuEdit.Append(503, trans("Menu_Edit_Redo"), trans("Menu_Edit_Redo"))
		self.menuEdit.AppendSeparator()
		self.menuEdit.Append(504, trans("Menu_Edit_Cut"), trans("Menu_Edit_Cut"))
		self.menuEdit.Append(505, trans("Menu_Edit_Copy"), trans("Menu_Edit_Copy"))
		self.menuEdit.Append(506, trans("Menu_Edit_Paste"), trans("Menu_Edit_Paste"))
		self.menuEdit.Append(507, trans("Menu_Edit_SelectAll"), trans("Menu_Edit_SelectAll"))
		self.menuEdit.AppendSeparator()
		self.menuEdit.Append(508, trans("Menu_Edit_Find"), trans("Menu_Edit_Find"))
		self.menuEdit.Append(509, trans("Menu_Edit_Replace"), trans("Menu_Edit_Replace"))
		self.menuEdit.Append(510, trans("Menu_Edit_Goto"), trans("Menu_Edit_Goto"))
		self.menuEdit.AppendSeparator()
		self.menuEdit.Append(501, trans("Menu_Edit_Preference"), trans("Menu_Edit_Preference"))
		self.menubar.Append(self.menuEdit,trans("Menu_Edit"))


		self.menuProject = wxMenu()
		self.menuProject.Append(107, trans("Menu_File_Project_New"), trans("Menu_File_Project_New"))
		self.menuProject.Append(103, trans("Menu_File_Project_Open"), trans("Menu_File_Project_Open"))
		self.menuProject.Append(109, trans("Menu_File_Project_Configurator"), trans("Menu_File_Project_Configurator"))
		self.menuProject.AppendSeparator()
		self.MenuRecentProjects = wxMenu()
		self.menuProject.AppendMenu(179, trans("Menu_File_RecentProject"), self.MenuRecentProjects)
		self.GetRecentProjects()
		self.menubar.Append(self.menuProject,trans("Project"))


		self.menuDebug = wxMenu()
		self.menuDebug.Append(301, trans("Menu_Debug_Execute"), trans("Menu_Debug_Execute"))
		self.menuDebug.Append(302, trans("Menu_Debug_Execute_Stop"), trans("Menu_Debug_Execute_Stop"))
		self.menuDebug.Append(303, trans("Menu_Debug_Next"), trans("Menu_Debug_Next"))
		self.menuDebug.Append(304, trans("Menu_Debug_Step"), trans("Menu_Debug_Step"))
		self.menuDebug.AppendSeparator()
		self.menuDebug.Append(201, trans("Menu_Build_Execute"), trans("Menu_Build_Execute"))
		self.menuDebug.Append(202, trans("Menu_Build_Execute_Stop"), trans("Menu_Build_Execute_Stop"))
		self.menuDebug.AppendSeparator()
		self.menuDebug.Append(305, trans("Menu_Debug_Arguments"), trans("Menu_Debug_Arguments"))
		self.menubar.Append(self.menuDebug,trans("Menu_Debug"))
		
		self.menuBuild = wxMenu()
		self.menuBuild.Append(601, trans("Menu_Build_Compile"), trans("Menu_Build_Compile"))
		self.menuBuild.Append(602, trans("Menu_Debug_Build_Command"), trans("Menu_Debug_Build_Command"))
		self.menubar.Append(self.menuBuild,trans("Menu_Build"))
		
				

		if wxPlatform == '__WXGTK__':
			"""
    wxSIGNONE = 0,  // verify if the process exists under Unix
    wxSIGHUP,
    wxSIGINT,
    wxSIGQUIT,
    wxSIGILL,
    wxSIGTRAP,
    wxSIGABRT,
    wxSIGEMT,
    wxSIGFPE,
    wxSIGKILL,      // forcefully kill, dangerous!
    wxSIGBUS,
    wxSIGSEGV,
    wxSIGSYS,
    wxSIGPIPE,
    wxSIGALRM,
    wxSIGTERM       // terminate the process gently
			"""
			self.menuSignal = wxMenu()
			id = 401
			self.menuSignal.Append(id, "SIGHUP", trans("SIGHUP"));id=id+1
			self.menuSignal.Append(id, "SIGINT", trans("SIGINT"));id=id+1
			self.menuSignal.Append(id, "SIGQUIT", trans("SIGQUIT"));id=id+1
			self.menuSignal.Append(id, "SIGILL", trans("SIGILL"));id=id+1
			self.menuSignal.Append(id, "SIGABRT", trans("SIGABRT"));id=id+1
			self.menuSignal.Append(id, "SIGFPE", trans("SIGFPE"));id=id+1
			self.menuSignal.Append(id, "SIGKILL", trans("SIGKILL"));id=id+1
			self.menuSignal.Append(id, "SIGSEGV", trans("SIGSEGV"));id=id+1
			self.menuSignal.Append(id, "SIGPIPE", trans("SIGPIPE"));id=id+1
			self.menuSignal.Append(id, "SIGALRM", trans("SIGALRM"));id=id+1
			self.menuSignal.Append(id, "SIGTERM", trans("SIGTERM"));id=id+1
			self.menuSignal.AppendSeparator()
			submenu = wxMenu()
			submenu.Append(id, "SIGUSR1", trans("SIGUSR1"));id=id+1
			submenu.Append(id, "SIGUSR2", trans("SIGUSR2"));id=id+1
			submenu.Append(id, "SIGCHLD", trans("SIGCHLD"));id=id+1
			submenu.Append(id, "SIGCONT", trans("SIGCONT"));id=id+1
			submenu.Append(id, "SIGSTOP", trans("SIGSTOP"));id=id+1
			submenu.Append(id, "SIGTSTP", trans("SIGTSTP"));id=id+1
			submenu.Append(id, "SIGTTIN", trans("SIGTTIN"));id=id+1
			submenu.Append(id, "SIGTTOU", trans("SIGTTOU"));id=id+1
			submenu.AppendSeparator()
			submenu.Append(id, "SIGBUS", trans("SIGBUS"));id=id+1
			submenu.Append(id, "SIGPOLL", trans("SIGPOLL"));id=id+1
			submenu.Append(id, "SIGPROF", trans("SIGPROF"));id=id+1
			submenu.Append(id, "SIGSYS", trans("SIGSYS"));id=id+1
			submenu.Append(id, "SIGTRAP", trans("SIGTRAP"));id=id+1
			submenu.Append(id, "SIGURG", trans("SIGURG"));id=id+1
			submenu.Append(id, "SIGVTALRM", trans("SIGVTALRM"));id=id+1
			submenu.Append(id, "SIGXCPU", trans("SIGXCPU"));id=id+1
			submenu.Append(id, "SIGXFSZ", trans("SIGXFSZ"));id=id+1
			submenu.AppendSeparator()
			submenu.Append(id, "SIGIOT", trans("SIGIOT"));id=id+1
			submenu.Append(id, "SIGIO", trans("SIGIO"));id=id+1
			submenu.Append(id, "SIGCLD", trans("SIGCLD"));id=id+1
			submenu.Append(id, "SIGPWR", trans("SIGPWR"))
			self.menuSignal.AppendMenu(wxNewId(), "More", submenu)
			self.menubar.Append(self.menuSignal,trans("Signal"))
		
		self.menuHelp = wxMenu()
		self.menuHelp.Append(904, trans("Menu_Help_Homepage"), trans("Menu_Help_Homepage"))
		self.menuHelp.Append(903, trans("Menu_Help_BugIdea"), trans("Menu_Help_BugIdea"))
		self.menuHelp.AppendSeparator()
		self.menuHelp.Append(902, trans("Menu_Help_Upgrade"), trans("Menu_Help_Upgrade"))
		self.menuHelp.Append(901, trans("Menu_Help_About"), trans("Menu_Help_About_Status"))
		self.menubar.Append(self.menuHelp,trans("Menu_Help"))

		# Toolbar
		self.tb = self.CreateToolBar(wxTB_HORIZONTAL|wxNO_BORDER|wxTB_FLAT)
		self.tb.SetToolBitmapSize(wxSize(22,22))

		imgdir = DEFAULTDIR+self.config.pathsep+"images"+self.config.pathsep

		self.tb.AddSimpleTool(104, wxBitmap(imgdir+'filenew.png',wxBITMAP_TYPE_PNG),trans("Menu_File_New"), trans("Menu_File_New"))
		self.tb.AddSimpleTool(102, wxBitmap(imgdir+'fileopen.png',wxBITMAP_TYPE_PNG),trans("Menu_File_Open"), trans("Menu_File_Open"))
		self.tb.AddSimpleTool(105, wxBitmap(imgdir+'filesave.png',wxBITMAP_TYPE_PNG),trans("Menu_File_Save"), trans("Menu_File_Save"))
		self.tb.AddSeparator()
		self.tb.AddSimpleTool(201, wxBitmap(imgdir+'1rightarrow.png',wxBITMAP_TYPE_PNG),trans("Menu_Build_Execute"), trans("Menu_Build_Execute"))
		self.tb.AddSimpleTool(301, wxBitmap(imgdir+'dbgrun.png',wxBITMAP_TYPE_PNG),trans("Menu_Debug_Execute"), trans("Menu_Debug_Execute"))
		self.tb.AddSimpleTool(303, wxBitmap(imgdir+'dbgrunto.png',wxBITMAP_TYPE_PNG),trans("Menu_Debug_Next"), trans("Menu_Debug_Next"))
		self.tb.AddSimpleTool(304, wxBitmap(imgdir+'dbgstep.png',wxBITMAP_TYPE_PNG),trans("Menu_Debug_Step"), trans("Menu_Debug_Step"))
		self.tb.AddSimpleTool(302, wxBitmap(imgdir+'player_stop.png',wxBITMAP_TYPE_PNG),trans("Menu_Debug_Execute_Stop"), trans("Menu_Debug_Execute_Stop"))
		self.tb.Realize()

		
		
		# Menu Event
		EVT_MENU(self, 101, self.OnCloseWindow)
		EVT_MENU(self, 102, self.OnFileOpen)
		EVT_MENU(self, 103, self.OnFileProjectOpen)
		EVT_MENU(self, 104, self.OnFileNew)
		EVT_MENU(self, 105, self.OnFileSave)
		EVT_MENU(self, 106, self.OnFileSaveAs)
		EVT_MENU(self, 107, self.OnFileProjectNew)
		EVT_MENU(self, 108, self.OnFileDirectoryOpen)
		EVT_MENU(self, 108, self.OnFileProjectAddNewFile)
		EVT_MENU(self, 109, self.OnFileProjectConfigurator)
		EVT_MENU(self, 201, self.OnExecute)
		EVT_MENU(self, 202, self.OnExecuteStop)
		EVT_MENU(self, 301, self.OnDebug)
		EVT_MENU(self, 302, self.OnExecuteStop)
		EVT_MENU(self, 303, self.OnDebugNext)
		EVT_MENU(self, 304, self.OnDebugStep)
		EVT_MENU(self, 305, self.OnDebugArgument)
		EVT_MENU(self, 501, self.OnPreference)
		EVT_MENU(self, 901, self.OnAbout)
		EVT_MENU(self, 902, self.OnUpdaterTimerEvent)
		EVT_MENU(self, 903, self.SubmitBug)
		EVT_MENU(self, 904, self.Homepage)
		EVT_MENU(self, 601, self.OnCompile)
		EVT_MENU(self, 602, self.OnDebugBuildCommand)
		

		for x in range(401, 433):
			EVT_MENU(self, x, self.OnSignal)
		for x in range(502, 511):
			EVT_MENU(self, x, self.OnEditorEvent)



		self.SetMenuBar(self.menubar)

		self.SetMenuStatus((), [202, 302, 303, 304]+range(401, 433))
		self.SetMenuStatus((), range(502, 511))


		
		


		# Splitter
		self.horizontal=wxSplitterWindow(self,-1)
		self.vertical=wxSplitterWindow(self.horizontal,-1)

		self.explorer=TotalExplorer(self.vertical,self.config,self)
		self.editor=MultipleEditor(self.vertical,self.config,self)
		self.profile=Profile(self.horizontal,self.config,self)

		self.horizontal.SplitHorizontally(self.vertical,self.profile, int(self.config.read_config("horizontal_sashposition")))
		self.vertical.SplitVertically(self.explorer,self.editor, int(self.config.read_config("vertical_sashposition")))

		self.horizontal.SetMinimumPaneSize(3)
		self.vertical.SetMinimumPaneSize(3)

		self.explorer.set_dclick_handler(self.editor.AddFile)

		if len(self.argv)>0:
			for x in self.argv:
				if os.path.isdir(x):
					self.explorer.AddDirectory(x)
				else:
					if getext.getext(x)=="exprj" and os.path.exists(os.path.abspath(x)):
						self.explorer.AddProject(os.path.abspath(x))
					else: 
						self.editor.AddFile(x)

		self.process = None
		EVT_IDLE(self, self.OnIdle)
		EVT_END_PROCESS(self, -1, self.OnProcessEnded)

		# backend UDP Server
		EVT_RECEIVEUDPSERVER(self, self.BackendEventUDP)
		self.udpth = udpLog()
		self.udpport = self.udpth.port
		self.udpth.set_handler(self.udpmessage)
		self.udpth.start()
		# backend UDP Server
		EVT_RECEIVETCPSERVER(self, self.BackendEventTCP)
		self.tcpth = tcpLog()
		self.tcpport = self.tcpth.port
		wxEvt_RecvTCP=self.tcpport
		self.tcpth.set_handler(self.tcpmessage)
		self.tcpth.start()

		self.tcpreturn = None
		self.debugrunning = 0
		self.execrunning = 0

		ss = self.config.read_config("autoupdater")
		self.UpdaterTimer = None
		#if ss=="1" or ss==None:
		if ss=="1":
			ID_Timer = wxNewId()
			self.UpdaterTimer = wxTimer(self, ID_Timer)
			EVT_TIMER(self, ID_Timer, self.OnUpdaterTimerEvent)
			self.UpdaterTimer.Start(3000)

	def Homepage(self, event):
		language = self.config.read_config("default_language")
		url = "http://exman.pe.kr/ExmanIDE/"
		try:
			import webbrowser
			webbrowser.open_new(url)
		except:
			wxMessageBox(trans("NOBROWSER"),"Information",wxICON_INFORMATION)

	def SubmitBug(self, event):
		language = self.config.read_config("default_language")
		if language=="Korean":
			url = "http://exman.pe.kr/ExmanIDE/bug_ko.php?mode=regist_view&board_url=/ExmanIDE/bug_ko.php"
		else:
			url = "http://exman.pe.kr/ExmanIDE/bug_en.php?mode=regist_view&board_url=/ExmanIDE/bug_en.php"
		try:
			import webbrowser
			webbrowser.open_new(url)
		except:
			wxMessageBox(trans("NOBROWSER"),"Information",wxICON_INFORMATION)
	
	def OnUpdaterTimerEvent(self, event):
		debug("Execute the Realtime Updater")
		if self.UpdaterTimer!=None:
			self.UpdaterTimer.Stop()
		self.UpdaterTimer=None

		EVT_UPDATER(self, self.OnUpdaterEvent)
		thread.start_new_thread(self.UpdaterThread,())

	def UpdaterThread(self):
		updater = ExmanUpdaterClient(GetUpdaterRoot()[0], "ExmanIDE", DEFAULTDIR)
		updater.SetUpdaterServerList(GetUpdaterRoot())
			
		debug("Compare Module Start")
		modify = updater.CompareModules()
		debug("Compare Module End")

		if len(modify)>0:
			evt = UpdaterAction(updater)
			wxPostEvent(self,evt)
			del evt

	def OnUpdaterEvent(self, event):
		updater = event.updater
		if wxMessageBox(trans("WouldYouUpdate")+"\nNew version: %s" % updater.version,"Information",wxYES_NO|wxNO_DEFAULT, self) == wxNO:
			return
		updater.UpdateModuleGUI(self)
		wxMessageBox(trans("YouMustRestartForUpgrade"), "Information", wxICON_INFORMATION, self)
		self.config.modify_config("exmanide_version", updater.version)


	def OnEditorEvent(self, event):
		eid = event.GetId()
		selection = self.editor.GetSelection()
		if selection==-1 or self.editor.GetPageCount()==0:
			wxMessageBox(trans("NoSelectedFile"),"Warning",wxICON_HAND)
			return
		stc = self.editor.GetPage(selection)
		if eid==502:
			stc.Undo()
		elif eid==503:
			stc.Redo()
		elif eid==504:
			stc.Cut()
		elif eid==505:
			stc.Copy()
		elif eid==506:
			stc.Paste()
		elif eid==507:
			stc.SelectAll()
		elif eid==508:
			stc.Find()
		elif eid==509:
			stc.Replace()
		elif eid==510:
			stc.GotoLineFromShortcut()


	def SetMenuStatus(self, enable=(), disable=()):
		for x in enable:
			try:
				self.menubar.Enable(x, true)
			except:
				pass
			try:
				self.tb.EnableTool(x, true)
			except:
				pass
		for x in disable:
			try:
				self.menubar.Enable(x, false)
			except:
				pass
			try:
				self.tb.EnableTool(x, false)
			except:
				pass

	def OnPreference(self, event):
		dialog = Environment(self, self.config, self)
		dialog.Centre(wxBOTH)
		dialog.ShowModal()

	def OnAbout(self, event):
		dialog = AboutDialog(self, self.config, self)
		dialog.Centre(wxBOTH)
		dialog.ShowModal()

	def OnFileProjectNew(self, event):
		size = wxSize(500, 550)
		wizard = wxDialog(self, wxNewId(), trans("Menu_File_Project_New"), wxDefaultPosition, size, wxSYSTEM_MENU|wxCAPTION)

		menutitle = [trans("Menu_File_Project_New"),trans("SourceHeaderTemplate"), trans("Finish")]
		menupanel = [ProjectNewintro, ProjectHeader, ProjectFinish]

		opened_dir = self.config.read_config("opened_dir")
		setupinfo = {"setup_path":DEFAULTDIR,"opened_dir":opened_dir}

		panel = []
		for x in range(len(menupanel)):
			panel.append(menupanel[x](wizard, self.config, self, size, menupanel, x, menutitle[x], setupinfo))
			panel[x].Show(false)
		for x in panel:
			x.SetPanel(panel)

		panel[0].Show(true)

		wizard.Centre(wxBOTH)
		wizard.ShowModal()
	def OnFileProjectConfigurator(self, event):
		if len(self.explorer.GetOpenProject())==0:
			wxMessageBox(trans("NotOpenProject"),"Warning",wxICON_HAND)
			event.Skip()
			return
		wizard = ProjectConfigurator(self, self.config, self)
		wizard.Centre(wxBOTH)
		wizard.ShowModal()

	def OnFileDirectoryOpen(self, event):
		opened_dir = self.config.read_config("opened_dir")

		if opened_dir=="":
			opened_dir=DEFAULTDIR

		dlg = wxDirDialog(self, "Choose a Project directory", defaultPath=opened_dir, style=wxDD_DEFAULT_STYLE|wxDD_NEW_DIR_BUTTON)
		if dlg.ShowModal() == wxID_OK:
			path = dlg.GetPath()
			self.config.modify_config("opened_dir",path)
			dlg.Destroy()
			self.explorer.AddDirectory(path)
		else:
			return

	def OnRecentDirOpen(self, event):
		order = event.GetId() - 250
		dirname = self.config.read_config("recent_dir_%d" % order)
		self.explorer.AddDirectory(dirname)
		

	def OnRecentFileOpen(self, event):
		order = event.GetId() - 150
		filename = self.config.read_config("recent_file_%d" % order)
		self.editor.AddFile(filename)

	def OnRecentProjectOpen(self, event):
		order = event.GetId() - 180
		filename = self.config.read_config("recent_project_%d" % order)
		self.explorer.AddProject(filename)
	
	def GetRecentDirs(self):
		queue = []
		for x in range(10):
			dirname = self.config.read_config("recent_dir_%d" % x)
			if dirname=="" or dirname==None:
				break
			queue.append(dirname)

		for x in range(self.MenuRecentDirs.GetMenuItemCount()):
			self.MenuRecentDirs.Remove(250 + x)

		order = 0
		for x in queue:
			self.MenuRecentDirs.Append(250+order, x,"")
			EVT_MENU(self, 250+order, self.OnRecentDirOpen)
			order=order+1
		return queue
		
	def GetRecentFiles(self):
		queue = []
		for x in range(10):
			filename = self.config.read_config("recent_file_%d" % x)
			if filename=="" or filename==None:
				break
			queue.append(filename)

		for x in range(self.MenuRecentFiles.GetMenuItemCount()):
			self.MenuRecentFiles.Remove(150 + x)

		order = 0
		for x in queue:
			self.MenuRecentFiles.Append(150+order, x,"")
			EVT_MENU(self, 150+order, self.OnRecentFileOpen)
			order=order+1

		return queue

	def GetRecentProjects(self):
		queue = []
		for x in range(10):
			filename = self.config.read_config("recent_project_%d" % x)
			if filename=="" or filename==None:
				break
			queue.append(filename)

		for x in range(self.MenuRecentProjects.GetMenuItemCount()):
			self.MenuRecentProjects.Remove(180 + x)

		order = 0
		for x in queue:
			self.MenuRecentProjects.Append(180+order, x,"")
			EVT_MENU(self, 180+order, self.OnRecentProjectOpen)
			order=order+1

		return queue

	def SetRecentDir(self, dirname):
		queue = [dirname, ]
		for x in range(10):
			dname = self.config.read_config("recent_dir_%d" % x)
			if dname=="" or dname==None:
				break
			if x==0 and dirname==dname:
				return
			queue.append(dname)
		if len(queue)>10:
			queue.pop()
		for x in range(len(queue)):
			self.config.modify_config("recent_dir_%d" % x, queue[x])
		else:
			if x<9:
				self.config.modify_config("recent_dir_%d" % (x+1), "")

		self.GetRecentDirs()
		
	def SetRecentFile(self, filename):
		queue = [filename, ]
		for x in range(10):
			fname = self.config.read_config("recent_file_%d" % x)
			if fname=="" or fname==None:
				break
			if x==0 and filename==fname:
				return
			queue.append(fname)
		if len(queue)>10:
			queue.pop()
		for x in range(len(queue)):
			self.config.modify_config("recent_file_%d" % x, queue[x])
		else:
			if x<9:
				self.config.modify_config("recent_file_%d" % (x+1), "")

		self.GetRecentFiles()

	def SetRecentProject(self, filename):
		queue = [filename, ]
		for x in range(10):
			fname = self.config.read_config("recent_project_%d" % x)
			if fname=="" or fname==None:
				break
			if x==0 and filename==fname:
				return
			queue.append(fname)
		if len(queue)>10:
			queue.pop()
		for x in range(len(queue)):
			self.config.modify_config("recent_project_%d" % x, queue[x])
		else:
			if x<9:
				self.config.modify_config("recent_project_%d" % (x+1), "")

		self.GetRecentProjects()
	
	def OpenProjectFiles(self, path):
		if not os.path.exists(path):
			return
		prj = Project(path)
		dir = os.path.dirname(path)
		openfiles = prj.GetValue("openfiles")
		openfiles.reverse()
		for x in openfiles:
			if x[0]==None:
				if x[1][0]=="/":
					filename = dir  +  x[1]
				else:
					filename = dir + self.config.pathsep +  x[1]
				if len(x)>=5:
					firstvisible = x[4]
				else:
					firstvisible = 0

				if len(x)>=6:
					currentline = x[5]
				else:
					currentline = 0
					
				if len(x)>=7:
					extdata = x[6]
				else:
					extdata = 0

				self.editor.AddFile(filename, x[3], firstvisible, currentline, extdata)
				for y in range(self.editor.GetPageCount()-1, -1, -1):
					if filename== self.editor.openedfiles[y][1]:
						stc = self.editor.GetPage(y)
						for z in x[2]:
							stc.MarkerAdd(z-1 , 0)
		self.SetRecentProject(path)

	def OnFileProjectOpen(self, event):
		wildcard = "ExmanIDE Project (*.exprj)|*.exprj"

		opened_dir = self.config.read_config("opened_dir")

		if opened_dir=="":
			opened_dir=DEFAULTDIR

		dlg = wxFileDialog(self, "Choose a Project", opened_dir, "", wildcard, wxOPEN)
		if dlg.ShowModal() == wxID_OK:
			path=dlg.GetPath()
			if os.path.exists(path)==0:
				dlg.Destroy()
				return
			self.explorer.AddProject(path)
			self.OpenProjectFiles(path)
			self.config.modify_config("opened_dir",os.path.dirname(path))
			dlg.Destroy()
		else:
			dlg.Destroy()
			return






	def OnFileSave(self, event):
		selection = self.editor.GetSelection()
		if selection==-1 or self.editor.GetPageCount()==0:
			wxMessageBox(trans("NoSelectedFile"),"Warning",wxICON_HAND)
			return
		stc = self.editor.GetPage(selection)
		for x in range(self.editor.GetPageCount()):
			if stc == self.editor.GetPage(x):
				if self.editor.openedfiles[x][1]=="":
					self.editor.SaveAs(stc)
					return

		self.editor.SaveFile(stc)

	def OnFileSaveAs(self, event):
		selection = self.editor.GetSelection()
		if selection==-1 or self.editor.GetPageCount()==0:
			wxMessageBox(trans("NoSelectedFile"),"Warning",wxICON_HAND)
			return
		stc = self.editor.GetPage(selection)
		for x in range(self.editor.GetPageCount()):
			if stc == self.editor.GetPage(x):
				self.editor.SaveAs(stc)




	def OnFileNew(self, event):
		self.editor.AddNewFile()
	
	def OnFileProjectAddNewFile(self, event):
		self.editor.AddFile('')

	def OnFileOpen(self, event):
		wildcard = "Python source (*.py)|*.py|Python source (*.pyw)|*.pyw|All files (*.*)|*.*"

		opened_dir = self.config.read_config("opened_dir")

		if opened_dir=="":
			opened_dir=DEFAULTDIR

		dlg = wxFileDialog(self, "Choose a file", opened_dir, "", wildcard, wxOPEN|wxMULTIPLE)
		if dlg.ShowModal() == wxID_OK:
			for path in dlg.GetPaths():
				self.editor.AddFile(path)
			else:
				self.config.modify_config("opened_dir",os.path.dirname(path))
			
		dlg.Destroy()


	def BackendEventUDP(self, event):
		#print "UDP",event.content, event.addr
		pass

	def udpmessage(self, content, addr):
		evt = RecvUDPServerMessage(content, addr)
		wxPostEvent(self,evt)
		del evt

	def BackendEventTCP(self, event):
		content = event.content
		array = content.split(" ")
		command = array[0]
		if command in ["read","readline","raw_input","input"]:
			if command in ["raw_input","input"] and len(array)>1:
				title = content[len(command)+1:]
			else:
				title = ""

			dlg = wxTextEntryDialog(self, title, command , style=wxOK)
			dlg.ShowModal()
			self.tcpreturn = dlg.GetValue()+"\n"
			dlg.Destroy()
		elif command=="readlines":
			dlg = wxDialog(self, -1, "sys.stdin.readlines()", size=wxSize(350, 200), style = wxDEFAULT_DIALOG_STYLE|wxDIALOG_MODAL)
			sizer = wxBoxSizer(wxVERTICAL)
			lines=wxTextCtrl(dlg, -1, size=wxSize(300,150),style=wxTE_MULTILINE|wxTE_RICH)
			sizer.Add(lines, 0, wxALIGN_CENTRE|wxALL, 5)
			btn = wxButton(dlg, wxID_OK, "OK")
			btn.SetDefault()
			sizer.Add(btn, 0, wxALIGN_CENTRE|wxALL, 5)
			dlg.SetSizer(sizer)
			dlg.SetAutoLayout(true)
			sizer.Fit(dlg)
			dlg.Centre()
			val = dlg.ShowModal()
			if val == wxID_OK:
				val = lines.GetValue()
				if len(val)==0:
					self.tcpreturn = '\0'
				else:
					self.tcpreturn = val
			else:
				self.tcpreturn = '\0'
			dlg.Destroy()

		elif command =="GetDebugRunningCommands":
			currentfile = array[1]
			currentline = int(array[2])
			if os.path.basename(currentfile)=="<string>":
				debug("Debuging Extension Module Functions")
				self.tcpreturn = "nextcmd = 'next'"
				return
			self.editor.AddFile(currentfile)
			selection = self.editor.GetSelection()
			stc = self.editor.GetPage(selection)

			if array[3:] and array[3]=="end":
				stc.MarkerDelete(currentline-1,2)
				return

			if(currentline!=0):
				stc.MarkerAdd(currentline-1, 2)
				#stc.ScrollToLine(currentline-1)
				stc.GotoLine(currentline-1)

			self.SetMenuStatus((301,),())
		elif command =="SetLocals":
			self.profile.locals.DeleteAllItems()
			self.profile.locals.InitRoot()
			val = cPickle.loads(content[10:])
			self.profile.locals.AddVars(self.profile.locals.root, val)
			self.tcpreturn="OK"
		elif command =="Error":
			wxMessageBox(content[6:],"Traceback",wxICON_HAND)
			self.tcpreturn="OK"



	def tcpmessage(self, content, addr):
		array = content.split(" ")
		command = array[0]
		self.tcpreturn=None
		if command in ["read","readline","raw_input","input","readlines"]:
			if command in ["raw_input","input"] and len(array)>1:
				title = content[len(command)+1:]
			else:
				title = ""

			evt = RecvTCPServerMessage(content, addr)
			wxPostEvent(self,evt)
			del evt
			while self.tcpreturn==None:
				wxUsleep(200)
				if self.tcpreturn!=None:
					break
			ret = self.tcpreturn
			self.tcpreturn = None
			return ret

		elif command == "GetDebugCommands":
			if self.editor.GetPageCount()==0:
				return

			code = "breakpoints = []"
			for x in range(self.editor.GetPageCount()):
				stc = self.editor.GetPage(x)
				filename = self.editor.openedfiles[x][1]

				lineno = 0
				while 1:
					lineno = stc.MarkerNext(lineno, 1)
					if lineno==-1:
						break
					else:
						lineno = lineno + 1
					code = code + "\nbreakpoints.append(('"+filename+"', %d))" % (lineno)
			return code
		elif command == "GetDebugRunningCommands":
			if self.editor.GetPageCount()==0:
				return


			evt = RecvTCPServerMessage(content, addr)
			wxPostEvent(self,evt)
			del evt

			code = "nextcmd = ''"
			while self.tcpreturn==None:
				wxUsleep(200)
				if self.tcpreturn!=None:
					break
			ret = self.tcpreturn
			self.tcpreturn = None

			evt = RecvTCPServerMessage(content+" end", addr)
			wxPostEvent(self,evt)
			del evt

			code = "breakpoints = []"
			for x in range(self.editor.GetPageCount()):
				stc = self.editor.GetPage(x)
				filename = self.editor.openedfiles[x][1]

				lineno = 0
				while 1:
					lineno = stc.MarkerNext(lineno, 1)
					if lineno==-1:
						break
					else:
						lineno = lineno + 1
					code = code + "\nbreakpoints.append(('"+filename+"', %d))" % (lineno)

			return code + "\n" + ret + "\n" + code

		elif command =="SetLocals":
			evt = RecvTCPServerMessage(content, addr)
			wxPostEvent(self,evt)
			del evt
			while self.tcpreturn==None:
				wxUsleep(200)
				if self.tcpreturn!=None:
					break
			return self.tcpreturn
		elif command =="Error":
			evt = RecvTCPServerMessage(content, addr)
			wxPostEvent(self,evt)
			del evt
			while self.tcpreturn==None:
				wxUsleep(200)
				if self.tcpreturn!=None:
					break
			return self.tcpreturn
		else:
			evt = RecvTCPServerMessage(content, addr)
			wxPostEvent(self,evt)
			del evt
	
	def Execute(self, type="execute"):
		# Shift-F5 Run
		if type=="execute":
			debug("Ctrl-F5 Run")
		elif type=="compile":
			debug("F7 Compile")
		else:
			debug("F5 Debug Run")

		selection = self.editor.GetSelection()
		if selection==-1:
			return
		if self.editor.GetPageCount()==0:
			return

		
		# save editor
		stc = self.editor.GetPage(selection)
		if stc.GetModify():
			self.editor.SaveFile(stc)


		filename = self.editor.openedfiles[selection][1]
		if filename=="":
			self.editor.SaveAs(self.editor.GetPage(selection))
			filename = self.editor.openedfiles[selection][1]
		argument = self.editor.openedfiles[selection][3]
		try:
			buildcommand=self.editor.openedfiles[selection][4][0]
			execcommand=self.editor.openedfiles[selection][4][1]
		except:
			buildcommand=''
			execcommand=''
			
		ext = getext.getext(filename).lower()
		# 파이썬이 아니면 모두 실행모드
		if ext not in ["py","pyw"] and type=="debug":
			type="execute"
			
		pythonbinpath = self.config.read_config("pythonbinpath")
		if pythonbinpath==None or pythonbinpath=='':
			pythonbinpath = 'python'

		ls = self.config.read_config("locals_not_show")
		if ls==None or ls=='0':
			ls='locals_visible'
		else:
			ls='locals_invisible'

		if type=="execute":
			ext = getext.getext(filename).lower()
			if ext in ["py","pyw"]:
				cmd = pythonbinpath +" -u "+DEFAULTDIR+self.config.pathsep+"InitExecute.py %d " % self.tcpport + filename + " " + argument
			elif execcommand!='':
				cmd = "sh -c '"+execcommand+"'"
			else:
				self._OnDebugExecCommand()
				return
		elif type=="compile":
			if buildcommand.strip()=='':
				self._OnDebugBuildCommand()
				return
			cmd = "sh -c '"+buildcommand+"'"
		else:
			cmd = pythonbinpath +" -u "+DEFAULTDIR+self.config.pathsep+"InitDebug.py %d %s " % (self.tcpport,ls) + filename + " " + argument

		debug("cmd: "+cmd)


		if type=="execute" or type=="compile":
			self.SetMenuStatus([202,302],(303, 304 ,201,301,601))
		else:
			self.SetMenuStatus((202, 302, 303, 304, 601),(201,301))
		self.SetMenuStatus(range(401, 433),())


		self.profile.stdout.Clear()
		self.profile.stderr.SetText('')
		self.process = wxProcess(self)
		self.process.Redirect()

		os.chdir(os.path.abspath(os.path.dirname(filename)))
		self.debug_pid = wxExecute(cmd, wxEXEC_ASYNC, self.process)
		self.profile.stdout.AppendText('Execute pid: %s\n' % self.debug_pid)
		self.profile.SetSelection(1) # stdout

		if type=="execute":
			self.execrunning = 1
		else:
			self.debugrunning = 1


	def OnExecute(self, event):
		self.Execute("execute")

	def OnDebug(self, event):
		debug("debugrunnig: %d" % self.debugrunning)
		if self.debugrunning == 1:
			self.tcpreturn = "nextcmd = 'run'"
			return
		self.Execute("debug")
		
	def OnCompile(self, event):
		debug("debugrunnig: %d" % self.debugrunning)
		self.Execute("compile")
		
	def OnDebugNext(self, event):
		if self.debugrunning == 1:
			self.tcpreturn = "nextcmd = 'next'"
			return

	def OnDebugStep(self, event):
		if self.debugrunning == 1:
			self.tcpreturn = "nextcmd = 'step'"
			return
			
	def OnDebugArgument(self, event):
		selection = self.editor.GetSelection()
		if selection==-1 or self.editor.GetPageCount()==0:
			wxMessageBox(trans("NoSelectedFile"),"Warning",wxICON_HAND)
			return
		debug(self.editor.openedfiles[selection])
		argument = self.editor.openedfiles[selection][3]
		filename = self.editor.openedfiles[selection][2]

		dlg = wxTextEntryDialog(self, filename, trans("Menu_Debug_Arguments"), style=wxOK)
		dlg.SetValue(argument)
		dlg.ShowModal()
		self.editor.openedfiles[selection][3] = dlg.GetValue()
		dlg.Destroy()
	def OnDebugBuildCommand(self, event):
		self._OnDebugBuildCommand()
	def _OnDebugBuildCommand(self):
		selection = self.editor.GetSelection()
		if selection==-1 or self.editor.GetPageCount()==0:
			wxMessageBox(trans("NoSelectedFile"),"Warning",wxICON_HAND)
			return
		debug(self.editor.openedfiles[selection])
		argument = self.editor.openedfiles[selection][3]
		filename = self.editor.openedfiles[selection][2]
		try:
			extdata = self.editor.openedfiles[selection][4]
			buildcommand = extdata[0]
			execcommand = extdata[1]
		except:
			exdata = ['','']
			buildcommand = ''
			execcommand = ''
		
		dlg = wxTextEntryDialog(self, "Command for compile", trans("Menu_Debug_Build_Command"), style=wxOK)
		dlg.SetValue(buildcommand)
		dlg.ShowModal()
		buildcommand =dlg.GetValue().strip()
		self.editor.openedfiles[selection][4] = [buildcommand, execcommand]
		dlg.Destroy()

		
	
	def OnDebugExecCommand(self, event):
		self._OnDebugExecCommand()
	def _OnDebugExecCommand(self):
		selection = self.editor.GetSelection()
		if selection==-1 or self.editor.GetPageCount()==0:
			wxMessageBox(trans("NoSelectedFile"),"Warning",wxICON_HAND)
			return
		debug(self.editor.openedfiles[selection])
		argument = self.editor.openedfiles[selection][3]
		filename = self.editor.openedfiles[selection][2]
		try:
			extdata = self.editor.openedfiles[selection][4]
			buildcommand = extdata[0]
			execcommand = extdata[1]
		except:
			exdata = ['','']
			buildcommand = ''
			execcommand = ''
		
		dlg = wxTextEntryDialog(self, "", trans("Menu_Debug_Exec_Command"), style=wxOK)
		dlg.SetValue(execcommand)
		dlg.ShowModal()
		execcommand = dlg.GetValue().strip()
		self.editor.openedfiles[selection][4] = [buildcommand, execcommand]
		dlg.Destroy()



	def OnSignal(self, event):
		if self.debugrunning == 1 or self.execrunning == 1:
			s = (signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGILL, signal.SIGABRT, signal.SIGFPE, signal.SIGKILL, signal.SIGSEGV, signal.SIGPIPE, signal.SIGALRM, signal.SIGTERM, signal.SIGUSR1, signal.SIGUSR2, signal.SIGCHLD, signal.SIGCONT, signal.SIGSTOP, signal.SIGTSTP, signal.SIGTTIN, signal.SIGTTOU, signal.SIGBUS, signal.SIGPOLL, signal.SIGPROF, signal.SIGSYS, signal.SIGTRAP, signal.SIGURG, signal.SIGVTALRM, signal.SIGXCPU, signal.SIGXFSZ, signal.SIGIOT, signal.SIGIO, signal.SIGCLD, signal.SIGPWR)
			x = event.GetId() - 401
			os.kill(self.debug_pid, s[x])


	def OnExecuteStop(self, event):
		# Shift-F5 Run
		debug("F5 Stop")
		if self.debugrunning == 1:
			self.tcpreturn = "nextcmd = 'quit'"

		self.profile.stdout.AppendText('Exit...\n')
		#os.kill(self.debug_pid, signal.SIGTERM)
		#os.waitpid(pid, 0)
		#win32/scripts/killProcName.py
		if wxPlatform == '__WXGTK__':
			os.kill(self.debug_pid, signal.SIGTERM)
		"""
		if self.debugrunning == 1:
			self.process.CloseOutput()
			self.process=None
		os.chdir(DEFAULTDIR)

		#self.SetMenuStatus((201,301),(202, 302, 303, 304))

		self.debugrunning = 0

		for x in range(self.editor.GetPageCount()):
			stc = self.editor.GetPage(x)
			filename = self.editor.openedfiles[x][1]
			stc.MarkerDeleteAll(2)

		self.profile.locals.DeleteAllItems()
		self.profile.locals.InitRoot()
		"""
   
	
    
	def OnIdle(self, evt):
		if self.process is not None:
			stdout = self.process.GetInputStream()
			if stdout.CanRead():
				text = stdout.read()
				self.profile.stdout.AppendText(text)
				self.profile.SetSelection(1) # stdout

			stderr = self.process.GetErrorStream()
			if stderr.CanRead():
				text = stderr.read()
				self.profile.stderr.SetText(self.profile.stderr.GetText()+text)
				self.profile.stderr.GotoLine(self.profile.stderr.GetLineCount())
				self.profile.SetSelection(2) # stderr
    
	def OnProcessEnded(self, evt):
		self.OnIdle(evt)

		self.profile.stdout.AppendText('OnProcessEnded, pid:%s,  exitCode: %s\n' % (evt.GetPid(), evt.GetExitCode()))
		self.profile.SetSelection(1) # stdout

		if self.process!=None:
			self.process.Destroy()
		self.process = None

		os.chdir(DEFAULTDIR)

		self.SetMenuStatus((201,301, 601),(202, 302, 303, 304))
		self.SetMenuStatus((), range(401, 433))

		self.debugrunning = 0
		self.execrunning  = 0

		for x in range(self.editor.GetPageCount()):
			stc = self.editor.GetPage(x)
			filename = self.editor.openedfiles[x][1]
			stc.MarkerDeleteAll(2)

		if self.config.read_config("locals_not_show")!='1':
			self.profile.locals.DeleteAllItems()
			self.profile.locals.InitRoot()

	def OnCloseWindow(self,event):
		if self.debugrunning==1 or self.execrunning == 1:
			wxMessageBox(trans("DontCloseForDebug"),"Information",wxICON_INFORMATION)
			return 
		# udp server stop
		self.udpth.stop()
		# tcpp server stop
		self.tcpth.stop()

		while 1:
			if self.editor.runningapitank==0:
				break
			else:
				wxUsleep(200)


		# project close
		order = range(len(self.explorer.root_dir))
		order.reverse()
		for x in order:
			child, cookie = self.explorer.GetNextChild(self.explorer.root, x)
			data=self.explorer.GetItemData(child).GetData()
			if data[0]=="ProjectRoot":
				self.explorer.ProjectClose(child, data)

		# modify file check
		for x in range(self.editor.GetPageCount()-1, -1, -1):
			stc = self.editor.GetPage(x)
			if self.editor.CloseFile(stc)==0:
				return

		# Save a Position/Size
		pos=self.GetPosition()
		debug("Save Frame Position (%d,%d)" % (pos[0],pos[1]))
		self.config.modify_config("widget_pos","%d,%d" % (pos[0],pos[1]))
		size=self.GetSize()
		debug("Save Frame Size (%d,%d)" % (size[0],size[1]))
		self.config.modify_config("widget_size","%d,%d" % (size[0],size[1]))
		debug("Save Horizontal SashPosition: %d" % self.horizontal.GetSashPosition())
		self.config.modify_config("horizontal_sashposition","%d" % self.horizontal.GetSashPosition())
		debug("Save Vertical SashPosition: %d" % self.vertical.GetSashPosition())
		self.config.modify_config("vertical_sashposition","%d" % self.vertical.GetSashPosition())
		
		self.Destroy()
