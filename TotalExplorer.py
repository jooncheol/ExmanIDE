from wxPython.wx import *
from BackEnd import *
from Language import *
from Project import *

import os.path
import dircache
import explorericon
import getext


class TotalExplorer(wxTreeCtrl):
	def __init__(self,parent,config,main):
		#########################################################
		self.parent=parent
		self.config=config
		self.main=main

		# Get Character Setting / Setting Translate Function
		self.language = self.config.read_config("default_language")

		wxTreeCtrl.__init__(self,self.parent,500)#,style=wxTR_HIDE_ROOT)
		self.root = None
		self.root_dir = []

		EVT_LEFT_DCLICK(self, self.onDClick)
		EVT_TREE_ITEM_EXPANDING(self, -1, self.onExpanding)
	
		self.handler_dclick = None

		"""
		wxInitAllImageHandlers()
		"""

		self.il=wxImageList(16,16)
		self.idx1=self.il.Add(explorericon.getBitmap_folder())
		self.idx2=self.il.Add(explorericon.getBitmap_folderopen())
		self.idx_filefind=self.il.Add(explorericon.getfilefindBitmap())
		self.idx_project_open=self.il.Add(explorericon.getproject_openBitmap())
		self.idx_app=self.il.Add(explorericon.getappBitmap())
		self.idx_bookmark=self.il.Add(explorericon.getbookmark_Bitmap())

		self.idx_txt=self.il.Add(explorericon.getBitmap_text())
		self.idx_source=self.il.Add(explorericon.getsourceBitmap())
		self.idx_cpp=self.il.Add(explorericon.getcppBitmap())
		self.idx_h=self.il.Add(explorericon.gethBitmap())
		self.idx_l=self.il.Add(explorericon.getlBitmap())
		self.idx_y=self.il.Add(explorericon.getyBitmap())
		self.idx_c=self.il.Add(explorericon.getcBitmap())
		self.idx_o=self.il.Add(explorericon.getoBitmap())
		self.idx_f=self.il.Add(explorericon.getfBitmap())
		self.idx_java=self.il.Add(explorericon.getjavaBitmap())
		self.idx_moc=self.il.Add(explorericon.getmocBitmap())
		self.idx_pl=self.il.Add(explorericon.getplBitmap())
		self.idx_s=self.il.Add(explorericon.getsBitmap())
		self.idx_py=self.il.Add(explorericon.getpyBitmap())
		self.idx_pyw=self.idx_py
		self.idx_html=self.il.Add(explorericon.gethtmlBitmap())
		self.idx_htm=self.idx_html
		self.idx_image=self.il.Add(explorericon.getimageBitmap())
		self.idx_png=self.idx_image
		self.idx_gif=self.idx_image
		self.idx_jpg=self.idx_image
		self.idx_bmp=self.idx_image
		self.idx_xpm=self.idx_image
		self.idx_xls=self.il.Add(explorericon.getxlsBitmap())
		self.idx_ppt=self.il.Add(explorericon.getpptBitmap())
		self.idx_doc=self.il.Add(explorericon.getdocBitmap())
		self.idx_pdf=self.il.Add(explorericon.getpdfBitmap())
		self.idx_ps=self.idx_pdf
		self.idx_rpm=self.il.Add(explorericon.getrpmBitmap())
		self.idx_shellscript=self.il.Add(explorericon.getshellscriptBitmap())
		self.idx_sh=self.idx_shellscript
		self.idx_sound=self.il.Add(explorericon.getsoundBitmap())
		self.idx_wav=self.idx_sound
		self.idx_mp3=self.idx_sound
		self.idx_ogg=self.idx_sound


		self.SetImageList(self.il)

		self.root=self.AddRoot(trans("OpenProjects",self.language),self.idx_project_open, self.idx_project_open)
		self.SetPyData(self.root, ["Root",])
		self.Expand(self.root)

		EVT_RIGHT_UP(self, self.onRightUp) 


	def onRightUp(self, event):
		self.x = event.GetX()
		self.y = event.GetY()
		item, flag = self.HitTest((self.x, self.y))
		try:
			data=self.GetItemData(item).GetData()
			self.SelectItem(item)
		except:
			event.Skip()
			return

		if data[0]=="Root" or data[0]=="DirRoot" or data[0]=="ProjectRoot":
			menu = wxMenu()
			if data[0]=="ProjectRoot":
				menuitem = wxMenuItem(menu, 2021,trans("Menu_File_Project_File_New",self.language))
				menu.AppendItem(menuitem)
				EVT_MENU(self, 2021, self.onProjectFileNew)
				menuitem = wxMenuItem(menu, 2028,trans("Menu_File_Project_Configurator",self.language))
				menu.AppendItem(menuitem)
				EVT_MENU(self, 2028, self.onProjectConfigurator)
				menuitem = wxMenuItem(menu, 2022,trans("Menu_File_Project_Close",self.language))
				menu.AppendItem(menuitem)
				EVT_MENU(self, 2022, self.onProjectClose)
			elif data[0]=="DirRoot":
				menuitem = wxMenuItem(menu, 2023,trans("Menu_File_Directory_Close",self.language))
				menu.AppendItem(menuitem)
				EVT_MENU(self, 2023, self.onDirectoryClose)

			elif data[0]=="Root":
				menuitem = wxMenuItem(menu, 2025,trans("Menu_File_Project_New",self.language))
				menu.AppendItem(menuitem)
				EVT_MENU(self, 2025, self.onProjectNew)
				menuitem = wxMenuItem(menu, 2026,trans("Menu_File_Project_Open",self.language))
				menu.AppendItem(menuitem)
				EVT_MENU(self, 2026, self.onProjectOpen)
				menuitem = wxMenuItem(menu, 2027,trans("Menu_File_Directory_Open",self.language))
				menu.AppendItem(menuitem)
				EVT_MENU(self, 2027, self.onDirectoryOpen)

			menuitem = wxMenuItem(menu, 2024,trans("RefreshDir",self.language))
			menu.AppendItem(menuitem)
			EVT_MENU(self, 2024, self.onRefreshDir)

			self.PopupMenu(menu, wxPoint(event.GetX(), event.GetY()))
			menu.Destroy()

		event.Skip()
	
	def onProjectConfigurator(self, event):
		item = self.GetSelection()
		data=self.GetItemData(item).GetData()
		wizard = ProjectConfigurator(self, self.config, self.main, data[2])
		wizard.Centre(wxBOTH)
		wizard.ShowModal()

	def onProjectOpen(self, event):
		self.main.OnFileProjectOpen(event)
	
	def onDirectoryOpen(self, event):
		self.main.OnFileDirectoryOpen(event)

	
	def onProjectNew(self, event):
		self.main.OnFileProjectNew(event)

	def GetOpenProject(self):
		projectinfo = []
		order = range(len(self.root_dir))
		for x in order:
			child, cookie = self.GetNextChild(self.root, x)
			data=self.GetItemData(child).GetData()
			if data[0]=="ProjectRoot":
				projectfile = data[2]
				projectinfo.append(projectfile)

		return projectinfo

	def onRefreshDir(self, event):
		self.Show(false)
		projectinfo = []
		order = range(len(self.root_dir))
		order.reverse()
		for x in order:
			child, cookie = self.GetNextChild(self.root, x)
			data=self.GetItemData(child).GetData()
			if data[0]=="ProjectRoot":
				projectfile = data[2]
				self.Delete(child)
				self.root_dir.remove(data[1])
				projectinfo.append(("ProjectRoot",projectfile))
			else:
				dir = data[1]
				self.Delete(child)
				self.root_dir.remove(data[1])
				projectinfo.append(("DirRoot",dir))

		projectinfo.reverse()
		for x in projectinfo:
			if x[0]=="ProjectRoot":
				self.AddProject(x[1])
			else:
				self.AddDirectory(x[1])
		self.Show(true)

	def onProjectFileNew(self, event):
		item = self.GetSelection()
		data=self.GetItemData(item).GetData()
		if data[0]!="ProjectRoot":
			return


		self.config.modify_config("opened_dir", data[1])

		wildcard = "Python source (*.py)|*.py|Python source (*.pyw)|*.pyw"
		opened_dir = self.config.read_config("opened_dir")

		if opened_dir=="":
			opened_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

		dlg = wxFileDialog(self, "New Project File", opened_dir, "", wildcard,wxSAVE|wxOVERWRITE_PROMPT) 
		if dlg.ShowModal() == wxID_OK:
			filename = dlg.GetPath()
			dlg.Destroy()
		else:
			dlg.Destroy()
			return

		import time
		prj = Project(data[2])
		data = prj.GetSourceHeader()
		data = data.replace("%FILENAME%",os.path.basename(filename))
		data = data.replace("%DATE%",time.strftime("%Y-%m-%d"))
		data = data.replace("%YEAR%",time.strftime("%Y-%m-%d"))
		data = data.replace("%EMAIL%",prj.GetEmail())
		data = data.replace("%HOMEPAGE%",prj.GetHomepage())
		data = data.replace("%AUTHOR%",prj.GetAuthor())

		open(filename,"w").write(data)
		self.main.editor.AddFile(filename)
		self.onRefreshDir(event)
	
	def ProjectClose(self, item, data):
		if data[0]=="ProjectRoot":
			self.Delete(item)
			self.root_dir.remove(data[1])

			prj = Project(data[2])
			prj.SetValue("openfiles",[])

			for x in range(self.main.editor.GetPageCount()-1, -1, -1):
				dir = os.path.dirname(self.main.editor.openedfiles[x][1])
				if dir.replace("\\","/").find(data[1].replace("\\","/"))!=-1:
					filename = self.main.editor.openedfiles[x][1].replace("\\","/")[len(data[1].replace("\\","/")):]
					stc = self.main.editor.GetPage(x)
					marker = []
					lineno = 0
					while 1:
						lineno = stc.MarkerNext(lineno, 1)
						if lineno==-1:
							break
						else:
							lineno = lineno + 1
							marker.append(lineno)
					try:
						argument = self.main.editor.openedfiles[x][3]
						try:
							extdata = self.main.editor.openedfiles[x][4]
						except:
							extdata = None
					except:
						argument = ""
					prj.AddOpenFile(data[1], filename, marker, argument, stc.GetFirstVisibleLine(), stc.LineFromPosition(stc.GetCurrentPos()), extdata)
					self.main.editor.CloseFile(stc)
			prj.SaveProject()


	def onProjectClose(self, event):
		item = self.GetSelection()
		data=self.GetItemData(item).GetData()
		self.ProjectClose(item, data)

	def onDirectoryClose(self, event):
		item = self.GetSelection()
		data=self.GetItemData(item).GetData()
		if data[0]=="DirRoot":
			self.Delete(item)
			self.root_dir.remove(data[1])


	def set_dclick_handler(self, handler=None):
		self.handler_dclick = handler


	def AddDirectory(self, dir):
		if dir[-1:]==self.config.pathsep:
			dir=dir[:-1]

		if dir not in self.root_dir:
			self.root_dir.append(dir)

			child=self.AppendItem(self.root, dir,self.idx_bookmark, self.idx_bookmark)
			self.SetPyData(child, ["DirRoot",dir])
			self.create(child, dir, dir)
			self.Expand(self.root)
			self.Expand(child)
			
			self.main.SetRecentDir(os.path.abspath(dir))

	def AddProject(self, projectfile):
		dir = os.path.dirname(projectfile)

		if dir[-1:]==self.config.pathsep:
			dir=dir[:-1]

		if dir not in self.root_dir:
			self.root_dir.append(dir)

			child=self.AppendItem(self.root, dir,self.idx_app, self.idx_app)
			self.SetPyData(child, ["ProjectRoot",dir, projectfile])
			self.create(child, dir, dir)
			self.Expand(self.root)
			self.Expand(child)
			self.main.OpenProjectFiles(projectfile)


	def create(self,theParent,thePath, theRootPath):
		l=dircache.listdir(thePath)
		for x in l:
			if os.path.isdir(thePath+self.config.pathsep+x):
				child=self.AppendItem(theParent,x,self.idx1,self.idx2)
				self.SetPyData(child, ["Dir",child, thePath, thePath+self.config.pathsep+x, x, theRootPath])
				if len(dircache.listdir(thePath+self.config.pathsep+x))>0:
					self.SetItemHasChildren(child, TRUE)
				else:
					self.SetItemHasChildren(child, FALSE)
			else:
				ext = getext.getext(x)
				bindata = ['pyc','pyo','pyd'
				'o','obj','exe','dll','so','a','la','lib',
				'cab','zip','gz','tar','tar.gz','tgz','arj','rar','alz','lha','lzh',
				'bak','exprj','png','gif','jpg','bmp','xpm','xls','ppt','doc','pdf','ps','rpm','sh','wav','mp3','ogg','tar','tgz'
				]
				iconext = ['txt','cpp','h','l','o','y','c','f','java','moc','pl','s','py','pyw','html','htm']
				if x[0]!='.' and ext[-1:]!="~" and ext not in bindata:
					if ext in iconext:
						exec("child=self.AppendItem(theParent, x ,self.idx_"+ext+")")
					else:
						child=self.AppendItem(theParent, x ,self.idx_source)
					self.SetPyData(child, ["file",child, thePath, thePath+self.config.pathsep+x, x, theRootPath])

	def onDClick(self,event):
		item = self.GetSelection()
		data=self.GetItemData(item).GetData()
		if data[0]=="Root" or data[0]=="Dir":
			if self.IsExpanded(item):
				self.Collapse(item)
			else:
				self.Expand(item)
		elif data[0]=="file":
			"""
			try:
				self.SetItemBold(self.previousitem,false)
			except:
				pass
			self.SetItemBold(item,true)
			self.previousitem=item
			"""

			if self.handler_dclick != None:
				self.handler_dclick(data[3])

	def onExpanding(self, event):
		item=event.GetItem()
		debug(self.GetItemText(item)+" Expanding")
		data = self.GetItemData(item).GetData()
		if data[0]=="Root" or data[0]=="ProjectRoot" or data[0]=="DirRoot":
			return

		deleteitem = []
		for x in range(self.GetChildrenCount(item)):
			child, cookie = self.GetNextChild(item, x)
			deleteitem.append(child)
		for x in deleteitem:
			self.Delete(x)

		self.create(data[1], data[3], data[5])
