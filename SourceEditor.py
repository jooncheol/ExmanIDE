from wxPython.wx import *

from BackEnd import *
from Language import *

from threading import *

from wx.stc import *
from wx.py import shell
from StcStyle import *
import keyword
import os
import string
import time
import getext

DEFAULTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
SUPPORT_VIM = False

class DescriptText(wxStyledTextCtrl):
	def __init__(self,parent,config,main):
		self.parent=parent
		self.config=config
		self.main=main
		self.id = wxNewId()

		wxStyledTextCtrl.__init__(self, parent, self.id)

		self.SetMarginWidth(1, 0)
		
		self.SetStyles()
		self.SetViewWhiteSpace(0)
		self.SetTabWidth(4)
		self.SetUseTabs(0)
		self.SetReadOnly(1)
		try:
			self.SetWrapMode(1)
		except AttributeError:
			pass

	def SetStyles(self, language="PYTHON"):
		stcstyle(self, self.config, language)


	def SetText(self, *args, **kwds):
		self.SetReadOnly(0)
		wxStyledTextCtrl.SetText(self, *args, **kwds)
		self.SetReadOnly(1)

#----------------------------------------------------------------------


class stderrText(DescriptText):
	def __init__(self,parent,config,main):
		DescriptText.__init__(self,parent,config,main)
		EVT_STC_DOUBLECLICK(self, self.id, self.onDclick)

	def onDclick(self, event):
		text = self.GetLine(self.GetCurrentLine()).strip()
		if text[:4]!="File":
			# C++ compile 에러인지 검사
			# foo.cpp:38: achogo jchogo...
			elm = text.split(":")
			if len(elm)>=3:
				try:
					lineno = int(elm[1])
				except:
					return
				filename = elm[0].strip()
				if not os.path.exists(filename):
					selection = self.main.editor.GetSelection()
					if filename==self.main.editor.GetPageText(selection):
						filename = self.main.editor.openedfiles[selection][1]					
			else:
				return
		else:
			elm = text.split(",")
			filename = elm[0].strip()[6:-1]
			lineno = int(elm[1].strip()[5:])
			if filename=="<string>":
				return
		
		if not self.main.editor.AddFile(filename):
			return
		selection = self.main.editor.GetSelection()
		self.main.editor.Refresh()
		stc = self.main.editor.GetPage(selection)

		if(lineno!=0):
			stc.ScrollToLine(lineno-1)
			stc.SetSelectionStart(stc.PositionFromLine(lineno-1))
			stc.SetSelectionEnd(stc.GetLineEndPosition(lineno-1))


class crustShell(shell.Shell):
	def __init__(self, parent, config, main,  id=-1, intro=""):
		self.parent=parent
		self.config2=config
		self.main=main
		shell.Shell.__init__(self, parent, id, introText=intro)
		self.SetStyles()
		
		
	def SetStyles(self, language="PYTHON"):
		stcstyle(self, self.config2, language)




#----------------------------------------------------------------------
class ApiTank(Thread):
	def __init__(self, parent, main):
		self.main = main
		self.parent = parent
		Thread.__init__(self)
		self.parent.api = {}
	def run(self):
		self.parent.runningapitank=1
		import gzip, cPickle
		debug("python api loading...")
		self.parent.api = cPickle.load(gzip.open(self.main.DEFAULTDIR+self.main.config.pathsep+"python.api","r"))
		debug("python api loading completed")
		self.parent.runningapitank=0

class PythonSTC(wxStyledTextCtrl):
	def __init__(self, parent, ID):
		wxStyledTextCtrl.__init__(self, parent, ID)

		self.CmdKeyAssign(ord('B'), wxSTC_SCMOD_CTRL, wxSTC_CMD_ZOOMIN)
		self.CmdKeyAssign(ord('N'), wxSTC_SCMOD_CTRL, wxSTC_CMD_ZOOMOUT)

		self.SetProperty("fold", "1")
		self.SetProperty("tab.timmy.whinge.level", "1")
		self.autoindent=1

		self.SetViewWhiteSpace(false)
		#self.SetBufferedDraw(false)

		#self.SetEdgeMode(wxSTC_EDGE_BACKGROUND)
		#self.SetEdgeColumn(78)

		self.MarkerDefine(wxSTC_MARKNUM_FOLDEREND,	 wxSTC_MARK_BOXPLUSCONNECTED,  "white", "black")
		self.MarkerDefine(wxSTC_MARKNUM_FOLDEROPENMID, wxSTC_MARK_BOXMINUSCONNECTED, "white", "black")
		self.MarkerDefine(wxSTC_MARKNUM_FOLDERMIDTAIL, wxSTC_MARK_TCORNER,  "white", "black")
		self.MarkerDefine(wxSTC_MARKNUM_FOLDERTAIL,	wxSTC_MARK_LCORNER,  "white", "black")
		self.MarkerDefine(wxSTC_MARKNUM_FOLDERSUB,	 wxSTC_MARK_VLINE,	"white", "black")
		self.MarkerDefine(wxSTC_MARKNUM_FOLDER,		wxSTC_MARK_BOXPLUS,  "white", "black")
		self.MarkerDefine(wxSTC_MARKNUM_FOLDEROPEN,	wxSTC_MARK_BOXMINUS, "white", "black")


		EVT_STC_UPDATEUI(self,	ID, self.OnUpdateUI)
		EVT_STC_MARGINCLICK(self, ID, self.OnMarginClick)

		self.SetStyles()
		self.SetCaretForeground("BLUE")

		self.CallTipSetBackground(wxColour(255, 255, 232))


		#EVT_CHAR(self, self.OnKeyPressed)
		EVT_KEY_DOWN(self, self.OnKeyPressed)
		EVT_KEY_UP(self, self.OnKeyUp)
		EVT_CHAR(self, self.OnChar)


		self.PosInfoHandler = None
		self.autoindenttime = 0
		# for search
		self.matchcase = 0
		self.wholeword = 0
		self.regexp = 0
		self.reverse = 0
		self.minPos = 0
		self.maxPos = 0
		self.searchword = ''

	def SetStyles(self, language="PYTHON"):
		stcstyle(self, self.config, language)


	def SearchWord(self, searchword='', matchcase=-1, wholeword=-1, regexp=-1, reverse=-1, parent=None):
		if searchword!='':
			self.searchword = searchword
		if matchcase!=-1:
			self.matchcase = matchcase
		if wholeword!=-1:
			self.wholeword = wholeword
		if regexp!=-1:
			self.regexp = regexp
		if reverse!=-1:
			self.reverse = reverse
		if parent==None:
			parent = self

		flag = 0
		if self.matchcase==1:
			flag = flag|wxSTC_FIND_MATCHCASE
		if self.wholeword==1:
			flag = flag|wxSTC_FIND_WHOLEWORD
		if self.regexp==1:
			flag = flag|wxSTC_FIND_REGEXP

		reversedirection = self.reverse


		if reversedirection==1:
			self.SetTargetStart(self.maxPos)
			self.SetTargetEnd(0)
		else:
			self.maxPos = self.GetLength()
			self.SetTargetStart(self.minPos)
			self.SetTargetEnd(self.maxPos)

		self.SetSearchFlags(flag)
		pos = self.SearchInTarget(self.searchword)

		self.minPos = pos + len(self.searchword)

		if reversedirection==1:
			self.maxPos = pos - 1

		if pos==-1:
			wxMessageBox(trans("NoSearchWord",self.language),"Warning",wxICON_HAND,parent)
			self.maxPos = self.GetLength()
		else:
			lineno = self.LineFromPosition(pos)
			#self.ScrollToLine(lineno)
			self.GotoLine(lineno)
			self.SetSelectionStart(pos)
			self.SetSelectionEnd(pos+len(self.searchword))
		return pos

	def GotoLineFromShortcut(self):
		dlg = wxTextEntryDialog(self, trans("GotoLine",self.language), trans("GotoLineTitle",self.language), "") 
		if dlg.ShowModal() == wxID_OK:
			linenumber=dlg.GetValue()
			try:
				lineno = int(linenumber)
				maxlineno = self.GetLineCount()
				if lineno > maxlineno:
					lineno = maxlineno
				if lineno < 1:
					lineno = 1
				self.ScrollToLine(lineno-1)
				self.SetSelectionStart(self.PositionFromLine(lineno-1))
				self.SetSelectionEnd(self.PositionFromLine(lineno-1))
			except:
				pass
		dlg.Destroy()


	def write(self, text):
		self.AddText(text)
		self.EnsureCaretVisible()

	def GetModuleString(self,curpos):
		startpos = self.WordStartPosition(curpos-1, true)
		endpos = self.WordEndPosition(curpos-1, true)
		command = self.GetTextRange(startpos, endpos)
		while startpos>0:
			pword = self.GetTextRange(startpos-1, startpos)
			if pword == '.':
				nstartpos = self.WordStartPosition(startpos-2, true)
				nendpos = self.WordEndPosition(startpos-2, true)
				command = self.GetTextRange(nstartpos, nendpos)+'.'+command
				startpos = nstartpos
			else:
				break
		return command
	def GetApiMember(self,command):
		commandlist = command.split(".")
		curapi = None
		for m in commandlist:
			if curapi==None:
				if self.parent.api.has_key(m):
					curapi = self.parent.api[m]
				else:
					return None
			elif curapi.has_key(m):
				curapi = curapi[m]
			else:
				return None
		return curapi

	def OnChar(self, event):
		"""
		if not self.CanEdit():
			return
		"""
		key = event.KeyCode()

		if key == 46: # .
			self.write(chr(key))
			command=self.GetModuleString(self.GetCurrentPos())
			member = self.GetApiMember(command)
			if member:
				keys = member.keys()
				keys.sort()
				if '__myvalue__' in keys:
					keys.remove('__myvalue__')
				self.AutoCompSetIgnoreCase(false)
				self.AutoCompShow(0, string.join(keys))
		elif key == ord('('): # (
			self.write(chr(key))
			if self.AutoCompActive():
				self.AutoCompCancel()
			curpos = self.GetCurrentPos()
			command=self.GetModuleString(curpos)
			member = self.GetApiMember(command)
			if member != None and member.has_key('__myvalue__'):
				if self.CallTipActive():
					self.CallTipCancel()
				name = command.split(".")[-1]
				arg,value = member['__myvalue__'].split("|",1)
				help=''
				if len(arg)>0:
					help = name+arg
					if len(value)>0:
						help = help+'\n'+value
				else:
					if len(value)>0:
						help = value
					else:
						return
				self.CallTipShow(curpos-len(name)-1, help)
		else:
			event.Skip()
		
	def OnKeyUp(self, event):
		if self.GetModify() and self.parent.GetPageText(self.parent.GetSelection())[-1:]!="*":
			self.GetParent().SetModify(self)
			self.Refresh()
		key = event.KeyCode()

		if key == 308 and self.parent.old_ctrltab_ctrlup == 0:
			# 308 is ctrl
			self.parent.old_ctrltab_ctrlup = 1

		event.Skip()
	

	def OnKeyPressed(self, event):
		if self.CallTipActive():
			self.CallTipCancel()
		key = event.KeyCode()
		debug("KeyPressed: %d" % key)

		if key == 13 and not event.ControlDown():
			self.autoindenttime = 1
		if key == 87 and event.ControlDown():
			# ctrl-w is Closing
			self.GetParent().CloseFile(self)
		elif key == 83 and event.ControlDown():
			# ctrl-s is Saved
			parent = self.GetParent()
			for x in range(parent.GetPageCount()):
				if self == parent.GetPage(x):
					if parent.openedfiles[x][1]=="":
						parent.SaveAs(self)
						return
			parent.SaveFile(self)

		elif key == 350 :
			# F9 Debug Mark
			lineno = self.GetCurrentLine()
			if self.MarkerGet(lineno):
				self.MarkerDelete(lineno, 0)
			else:
				linestring = self.GetLine(lineno)
				stripline = linestring.strip()
				if len(stripline)==0 or stripline[0]=="#" or stripline[:3]=='"""':
					pass
				else:
					self.MarkerAdd(lineno , 0)

		elif key == 344 :
			# F3 Search Next
			if event.ShiftDown():
				self.SearchWord('', -1, -1, -1, 1,self)
			else:
				self.SearchWord('', -1, -1, -1, -1,self)
		elif key == 9 and event.ControlDown() and not event.ShiftDown():
			# Ctrl-Tab
			debug("Ctrl-tab")

			if self.parent.old_ctrltab_ctrlup==1:
				self.parent.SetSelection(self.parent.old_ctrltab_selection)
				self.parent.old_ctrltab_stc.SetFocus()
				count = self.parent.GetPageCount()
				for x in range(count):
					stc = self.parent.GetPage(x)
					if stc==self:
						self.parent.old_ctrltab_stc = self
						self.parent.old_ctrltab_selection = x
						break
				self.parent.old_ctrltab_ctrlup = 0
				event.Skip()
				return
			else:
				self.parent.old_ctrltab_ctrlup = 0

			count = self.parent.GetPageCount()
			for x in range(count):
				stc = self.parent.GetPage(x)
				if stc==self:
					if x+1 == count:
						selection = 0
					else:
						selection = x+1
					self.parent.SetSelection(selection)
					nextstc=self.parent.GetPage(selection)
					nextstc.SetFocus()
					self.parent.old_ctrltab_stc = self
					self.parent.old_ctrltab_selection = x
					break

		elif key == 9 and event.ControlDown() and event.ShiftDown():
			# Ctrl-Tab
			debug("Ctrl-Shift-tab")

			if self.parent.old_ctrltab_ctrlup==1:
				self.parent.SetSelection(self.parent.old_ctrltab_selection)
				self.parent.old_ctrltab_stc.SetFocus()
				count = self.parent.GetPageCount()
				for x in range(count):
					stc = self.parent.GetPage(x)
					if stc==self:
						self.parent.old_ctrltab_stc = self
						self.parent.old_ctrltab_selection = x
						break
				self.parent.old_ctrltab_ctrlup = 0
				event.Skip()
				return
			else:
				self.parent.old_ctrltab_ctrlup = 0

			count = self.parent.GetPageCount()
			for x in range(count):
				stc = self.parent.GetPage(x)
				if stc==self:
					if x == 0:
						selection = count-1
					else:
						selection = x-1
					self.parent.SetSelection(selection)
					nextstc=self.parent.GetPage(selection)
					nextstc.SetFocus()
					self.parent.old_ctrltab_stc = self
					self.parent.old_ctrltab_selection = x
					break
		elif key >= 48 and key <=57 and event.ControlDown():
			# set book mark
			count = self.parent.GetPageCount()
			for x in range(count):
				stc = self.parent.GetPage(x)
				if stc==self:
					if self.parent.bookmark[key-48]!=None:
						markedstc = self.parent.GetPage(self.parent.bookmark[key-48][0])
						lineno = markedstc.LineFromPosition(self.parent.bookmark[key-48][1])
						markedstc.MarkerDelete(lineno, 4)
					self.parent.bookmark[key-48] = [x, self.GetCurrentPos()]
					lineno = self.GetCurrentLine()
					self.MarkerAdd(lineno , 4)
					break
		elif key >= 48 and key <=57 and event.AltDown():
			# goto book mark
			if self.parent.bookmark[key-48]!=None:
				selection = self.parent.bookmark[key-48][0]
				pos = self.parent.bookmark[key-48][1]
				self.parent.SetSelection(selection)
				stc = self.parent.GetPage(selection)
				stc.SetFocus()
				stc.GotoPos(pos)
		

		event.Skip()


	def OnUpdateUI(self, evt):
		if self.autoindent and self.autoindenttime:
			self.autoindenttime = 0
			lineno = self.GetCurrentLine()
			for x in self.GetLine(lineno-1):
				if x in [' ', '\t']:
					self.write(x)
				else:
					break

		if self.PosInfoHandler!=None:
			self.PosInfoHandler(self.GetOvertype(), self.GetCurrentLine()+1, self.GetColumn(self.GetCurrentPos()))

		self.main.SetMenuStatus((507,508,509,510), ())

		if self.CanUndo():
			self.main.SetMenuStatus((502,), ())
		else:
			self.main.SetMenuStatus((), (502,))
		if self.CanRedo():
			self.main.SetMenuStatus((503,), ())
		else:
			self.main.SetMenuStatus((), (503,))
		if self.CanPaste():
			self.main.SetMenuStatus((506,), ())
		else:
			self.main.SetMenuStatus((), (506,))
		start,end = self.GetSelection()
		if start==end:
			self.main.SetMenuStatus((), (504,505))
		else:
			self.main.SetMenuStatus((504,505), ())





	def SetPosInfoHandler(self, handler):
		self.PosInfoHandler = handler

	def OnMarginClick(self, evt):

		if evt.GetMargin() != 2:
			lineno = self.LineFromPosition(evt.GetPosition())
			if self.MarkerGet(lineno):
				self.MarkerDelete(lineno, 0)
			else:
				linestring = self.GetLine(lineno)
				stripline = linestring.strip()
				if len(stripline)==0 or stripline[0]=="#" or stripline[:3]=='"""':
					pass
				else:
					self.MarkerAdd(lineno , 0)
			
		# fold and unfold as needed
		if evt.GetMargin() == 2:
			if evt.GetShift() and evt.GetControl():
				self.FoldAll()
			else:
				lineClicked = self.LineFromPosition(evt.GetPosition())
				if self.GetFoldLevel(lineClicked) & wxSTC_FOLDLEVELHEADERFLAG:
					if evt.GetShift():
						self.SetFoldExpanded(lineClicked, true)
						self.Expand(lineClicked, true, true, 1)
					elif evt.GetControl():
						if self.GetFoldExpanded(lineClicked):
							self.SetFoldExpanded(lineClicked, false)
							self.Expand(lineClicked, false, true, 0)
						else:
							self.SetFoldExpanded(lineClicked, true)
							self.Expand(lineClicked, true, true, 100)
					else:
						self.ToggleFold(lineClicked)


	def FoldAll(self):
		lineCount = self.GetLineCount()
		expanding = true

		# find out if we are folding or unfolding
		for lineNum in range(lineCount):
			if self.GetFoldLevel(lineNum) & wxSTC_FOLDLEVELHEADERFLAG:
				expanding = not self.GetFoldExpanded(lineNum)
				break;


		while lineNum < lineCount:
			level = self.GetFoldLevel(lineNum)
			if level & wxSTC_FOLDLEVELHEADERFLAG and \
			   (level & wxSTC_FOLDLEVELNUMBERMASK) == wxSTC_FOLDLEVELBASE:

				if expanding:
					self.SetFoldExpanded(lineNum, true)
					lineNum = self.Expand(lineNum, true)
					lineNum = lineNum - 1
				else:
					lastChild = self.GetLastChild(lineNum, -1)
					self.SetFoldExpanded(lineNum, false)
					if lastChild > lineNum:
						self.HideLines(lineNum+1, lastChild)

			lineNum = lineNum + 1



	def Expand(self, line, doExpand, force=false, visLevels=0, level=-1):
		lastChild = self.GetLastChild(line, level)
		line = line + 1
		while line <= lastChild:
			if force:
				if visLevels > 0:
					self.ShowLines(line, line)
				else:
					self.HideLines(line, line)
			else:
				if doExpand:
					self.ShowLines(line, line)

			if level == -1:
				level = self.GetFoldLevel(line)

			if level & wxSTC_FOLDLEVELHEADERFLAG:
				if force:
					if visLevels > 1:
						self.SetFoldExpanded(line, true)
					else:
						self.SetFoldExpanded(line, false)
					line = self.Expand(line, doExpand, force, visLevels-1)

				else:
					if doExpand and self.GetFoldExpanded(line):
						line = self.Expand(line, true, force, visLevels-1)
					else:
						line = self.Expand(line, false, force, visLevels-1)
			else:
				line = line + 1;

		return line

class SourceEditor(PythonSTC):
    def __init__(self,parent,config,main):
            #########################################################
            self.parent=parent
            self.config=config
            self.main=main
            PythonSTC.__init__(self,self.parent,wxNewId())
            self.language = self.config.read_config("default_language")


            self.SetMarginType(0, wxSTC_MARGIN_NUMBER)
            self.SetMarginSensitive(0, true)
            self.SetMarginWidth(0, 30)

            self.SetMarginType(1, wxSTC_MARGIN_SYMBOL)
            self.SetMarginSensitive(1, true)
            self.SetMarginWidth(1, 15)

            self.SetMarginType(2, wxSTC_MARGIN_SYMBOL)
            self.SetMarginMask(2, wxSTC_MASK_FOLDERS)
            self.SetMarginSensitive(2, true)
            self.SetMarginWidth(2, 12)

            self.MarkerDefine(0, wxSTC_MARK_ROUNDRECT, "#CCFF00", "RED")
            self.MarkerDefine(1, wxSTC_MARK_CIRCLE, "FOREST GREEN", "SIENNA")
            self.MarkerDefine(2, wxSTC_MARK_SHORTARROW, "blue", "blue")
            self.MarkerDefine(3, wxSTC_MARK_ARROW, "#00FF00", "#00FF00")
            self.MarkerDefine(4, wxSTC_MARK_ARROWDOWN, "black", "green")

            self.SetPosInfoHandler(self.SetPosStatus)

            # view option
            opt=self.config.read_config("view_witespace")
            if opt==None: opt=0
            self.SetViewWhiteSpace(int(opt));

            opt=self.config.read_config("view_endofline")
            if opt==None: opt=0
            self.SetViewEOL(int(opt));

            opt=self.config.read_config("view_indentationguide")
            if opt==None: opt=0
            self.SetIndentationGuides(int(opt))

            opt=self.config.read_config("view_linenumber")
            if opt==None: opt=1
            if int(opt)==0:
                    self.SetMarginWidth(0, 0)

            opt=self.config.read_config("view_margin")
            if opt==None: opt=1
            if int(opt)==0:
                    self.SetMarginWidth(1, 0)

            opt=self.config.read_config("view_foldmargin")
            if opt==None: opt=1
            if int(opt)==0:
                    self.SetMarginWidth(2, 0)

            opt=self.config.read_config("view_autoindent")
            if opt==None: opt=1
            self.autoindent=int(opt)

            opt=self.config.read_config("view_usetabs")
            if opt==None: opt=1
            self.SetUseTabs(int(opt))

            opt=self.config.read_config("view_tabsize")
            if opt==None: opt=0
            self.SetIndent(int(opt))


    def Type(self):
            return "Scintilla"

    def SetPosStatus(self, overtype, line, column):
            if overtype==1:
                    self.main.SetStatusText("Over type", 1)
            else:
                    self.main.SetStatusText("Insert", 1)


            self.main.SetStatusText("Line: %d Col: %d" % (line, column), 2)

    def Find(self):
            wizard = SearchDialog(self.main, self.config, self.main, self)
            self.wizard = wizard
            wizard.Centre(wxBOTH)
            wizard.ShowModal()

    def Replace(self):
            wizard = SearchDialog(self.main, self.config, self.main, self, "Replace")
            self.wizard = wizard
            wizard.Centre(wxBOTH)
            wizard.ShowModal()
    

    def Open(self, filename, readonly=0):
            self.SetLexType(filename)
            try:
                    self.SetText(open(filename,"r").read())
            except IOError:
                    pass
            self.EmptyUndoBuffer()
            self.Colourise(0, -1)
            self.SetReadOnly(readonly)

            

    def SetLexType(self, filename):
            ext = getext.getext(filename).lower()
            if ext in ["py","pyw"]:
                    self.SetStyles("PYTHON")
            elif ext in ["php","php4","php3","phtml"]:
                    self.SetStyles("PHP")
            elif ext in ["c","cc","cpp","cxx","cs","h","hh","hpp","hxx","sma","moc","c++"]:
                    self.SetStyles("CPP")
            else:
                    self.SetStyles("NULL")
    def Quit(self):
        pass
try:
    from wx.vim import *
    class SourceEditorVim(wxPanel):
        def __init__(self,parent,config,main):
            self.parent=parent
            self.config=config
            self.main=main
            wxPanel.__init__(self, parent, wxNewId(), wxDefaultPosition, self.parent.GetSize())
            self.language = self.config.read_config("default_language")
            wxVim.SetOptionStr("-U %s" % DEFAULTDIR+"/vimrc")
            busy = wx.BusyInfo(trans("StartingGVim", self.language))
            wx.Yield()
            self.vim = wxVim(self, wxNewId(), wxDefaultPosition, self.GetSize())
            self.servername = self.vim.GetServerName()
            EVT_SIZE(self, self.OnSize)
            EVT_VIM_PLUG_ADDED(self, self.OnPlugAdded)
            EVT_VIM_PLUG_REMOVED(self, self.OnPlugRemoved)
            EVT_KEY_DOWN(self, self.OnKeyPressed)
            EVT_SET_FOCUS(self, self.OnFocus)
        def OnFocus(self, event):
            self.vim.SetFocus()
        def OnKeyPressed(self, event):
            key = event.KeyCode()
            debug("KeyPressed: %d" % key)
            if key == 87 and event.ControlDown():
                # ctrl-w is Closing
                self.GetParent().CloseFile(self)
            elif key == 9 and event.ControlDown() and not event.ShiftDown():
                # Ctrl-Tab
                debug("Ctrl-tab")

                if self.parent.old_ctrltab_ctrlup==1:
                        self.parent.SetSelection(self.parent.old_ctrltab_selection)
                        self.parent.old_ctrltab_stc.SetFocus()
                        count = self.parent.GetPageCount()
                        for x in range(count):
                                stc = self.parent.GetPage(x)
                                if stc==self:
                                        self.parent.old_ctrltab_stc = self
                                        self.parent.old_ctrltab_selection = x
                                        break
                        self.parent.old_ctrltab_ctrlup = 0
                        event.Skip()
                        return
                else:
                        self.parent.old_ctrltab_ctrlup = 0

                count = self.parent.GetPageCount()
                for x in range(count):
                        stc = self.parent.GetPage(x)
                        if stc==self:
                                if x+1 == count:
                                        selection = 0
                                else:
                                        selection = x+1
                                self.parent.SetSelection(selection)
                                nextstc=self.parent.GetPage(selection)
                                nextstc.SetFocus()
                                self.parent.old_ctrltab_stc = self
                                self.parent.old_ctrltab_selection = x
                                break

            elif key == 9 and event.ControlDown() and event.ShiftDown():
                # Ctrl-Tab
                debug("Ctrl-Shift-tab")

                if self.parent.old_ctrltab_ctrlup==1:
                        self.parent.SetSelection(self.parent.old_ctrltab_selection)
                        self.parent.old_ctrltab_stc.SetFocus()
                        count = self.parent.GetPageCount()
                        for x in range(count):
                                stc = self.parent.GetPage(x)
                                if stc==self:
                                        self.parent.old_ctrltab_stc = self
                                        self.parent.old_ctrltab_selection = x
                                        break
                        self.parent.old_ctrltab_ctrlup = 0
                        event.Skip()
                        return
                else:
                        self.parent.old_ctrltab_ctrlup = 0

                count = self.parent.GetPageCount()
                for x in range(count):
                        stc = self.parent.GetPage(x)
                        if stc==self:
                                if x == 0:
                                        selection = count-1
                                else:
                                        selection = x-1
                                self.parent.SetSelection(selection)
                                nextstc=self.parent.GetPage(selection)
                                nextstc.SetFocus()
                                self.parent.old_ctrltab_stc = self
                                self.parent.old_ctrltab_selection = x
                                break 
            event.Skip()
        def OnPlugAdded(self, event):
            print "Added"
        def OnPlugRemoved(self, event):
            print "Removed"
            self.GetParent().CloseFile(self)
        def OnSize(self, event):
            print "OnSize", event.GetSize()
            size = event.GetSize()
            self.SetSize(size)
            self.vim.SetSize(size)
	def Type(self):
        	return "Vim"
        def SetLexType(self, filename):
            pass
        def SetSavePoint(self):
            pass
        def Open(self, filename, readonly=0):
            busy = wx.BusyInfo(trans("FileOpenByGVim", self.language))
            wx.Yield()
            time.sleep(1)
            self.vim.SetFocus()
            os.system("gvim --servername %s --remote %s" % (self.servername, filename))
            os.system("gvim --servername %s --remote-send '<Esc>:cd %s<Return>'" % (self.servername, os.path.dirname(filename)))
        def Quit(self):
            os.system("gvim --servername %s --remote-send '<Esc>:q!'" % (self.servername))
        def GotoLine(self, line):
            os.system("gvim --servername %s --remote-send '<Esc>:%d<Return>'" % (self.servername, line+1))
        def SetText(self, str):
            pass
	def ScrollToLine(self, line):
            self.GotoLine(line)
        def SetSelectionStart(self, line):
            pass
        def SetSelectionEnd(self, line):
            pass
        def PositionFromLine(self, lineno):
            pass
        def GetLineEndPosition(self, line):
            pass
        def MarkerNext(self, lineno, flag):
            return -1
        def GetFirstVisibleLine(self):
            return 1
        def LineFromPosition(self, pos):
            return 1
        def GetCurrentPos(self):
            return 1,1
        def GetModify(self):
            return False
    SUPPORT_VIM = True
except:
    SUPPORT_VIM = False
    pass

class MultipleEditor(wxNotebook):	
	def __init__(self,parent,config,main):
		self.parent=parent
		self.config=config
		self.main=main
		wxNotebook.__init__(self, parent, -1)
		self.openedfiles = []

		# Get Character Setting / Setting Translate Function
		self.language = self.config.read_config("default_language")

		EVT_RIGHT_UP(self, self.rClick) 
		EVT_NOTEBOOK_PAGE_CHANGED(self, -1, self.OnChanged)

		apis = ApiTank(self, self.main)
		apis.start()

		# for ctrl-tab
		self.old_ctrltab_ctrlup=None
		self.old_ctrltab_stc=None
		self.old_ctrltab_selection=None

		# for bookmark
		self.bookmark = [None,None,None,None,None,None,None,None,None,None,]
		

	def rClick(self, event):
		if self.GetPageCount()==0:
			event.Skip()
			return
		selection = self.GetSelection()
		filename = self.openedfiles[selection][2]
		
		ext = getext.getext(filename).lower()
		
		menu = wxMenu()
		if ext in ["py","pyw"]:
			menuitem = wxMenuItem(menu, 2003,trans("Menu_Debug_Arguments",self.language))
			menu.AppendItem(menuitem)
			EVT_MENU(self, 2003, self.main.OnDebugArgument)		
		elif ext in ["c","cc","cpp","cxx","cs","h","hh","hpp","hxx","sma","moc","c++"]:
			menuitem = wxMenuItem(menu, 2004,trans("Menu_Debug_Build_Command",self.language))
			menu.AppendItem(menuitem)
			EVT_MENU(self, 2004, self.main.OnDebugBuildCommand)
			menuitem = wxMenuItem(menu, 2005,trans("Menu_Debug_Exec_Command",self.language))
			menu.AppendItem(menuitem)
			EVT_MENU(self, 2005, self.main.OnDebugExecCommand)

                if SUPPORT_VIM==True:
                    if self.GetPage(selection).Type()=="Vim":
			menuitem = wxMenuItem(menu, 2006,trans("Menu_File_OpenWithScintilla",self.language))
                    else:
			menuitem = wxMenuItem(menu, 2006,trans("Menu_File_OpenWithVim",self.language))
                    menu.AppendItem(menuitem)
                    EVT_MENU(self, 2006, self.OnSwitchEditor)
			
		menuitem = wxMenuItem(menu, 2002,trans("CloseFile",self.language))
		menu.AppendItem(menuitem)
		EVT_MENU(self, 2002, self.evtCloseFile)
		self.PopupMenu(menu, wxPoint(event.GetX(), event.GetY()))
		menu.Destroy()
		event.Skip() 
	def OnSwitchEditor(self, event):
            if self.GetPageCount()==0:
                event.Skip()
                return
            selection = self.GetSelection()
            path = self.openedfiles[selection][1]
            filename = self.openedfiles[selection][2]
            oldeditor = self.GetPage(selection)
            oldeditor.Quit()
            if oldeditor.Type()=="Vim":
                editor = SourceEditor(self, self.config, self.main)
            else:
                editor = SourceEditorVim(self, self.config, self.main)
            editor.Open(path)
            self.InsertPage(selection, editor, filename)
            self.RemovePage(selection+1)

	def evtCloseFile(self,event):
		try:
			self.CloseFile(self.GetPage(self.GetSelection()))
			self.main.SetMenuStatus((), (507,508,509,510))
		except:
			wxMessageBox("ERROR: Sorry This is wxWindows bug","Warning",wxICON_HAND)
			pass

	def SaveAs(self, stc):
		for x in range(self.GetPageCount()):
			if stc == self.GetPage(x):
				vname = self.openedfiles[x][2]
				wildcard = "All files (*.*)|*.*"
				opened_dir = self.config.read_config("opened_dir")

				if opened_dir=="":
					opened_dir = os.path.abspath(os.path.dirname(sys.argv[0]))

				dlg = wxFileDialog(self, "Save as", opened_dir, vname, wildcard,wxSAVE|wxOVERWRITE_PROMPT) 
				if dlg.ShowModal() == wxID_OK:
					filename = dlg.GetPath()
					dlg.Destroy()
					selection = x
					break
				else:
					dlg.Destroy()
					return
		same = 0
		for x in self.openedfiles:
			if x[1]=="":
				continue
			if x[1]==filename:
				wxMessageBox(trans("AlreadyOpenedFile", self.language),"Warning",wxICON_HAND)
				self.SetSelection(x[0])
				return
			elif x[2]==os.path.basename(filename):
				same = same + 1

		if same==0:
			sametxt = ""
		else:
			sametxt = " (%d)" % same
		basefilename = os.path.basename(filename)
		self.openedfiles[selection][1] = filename
		self.openedfiles[selection][2] = basefilename
		self.openedfiles[selection][3] = ""
		self.SetPageText(selection, basefilename+sametxt)
		self.SetMainTitle(" - "+basefilename+sametxt)
		self.SaveFile(self.GetPage(selection))
		self.SetSelection(selection)


	def AddFile(self, filename, argument="", firstvisible=0, currentline=0, extdata=None, editor="Scintilla"):
		if os.path.exists(filename)==0:
			return 0
		same = 0
		for x in self.openedfiles:
			if os.path.abspath(x[1])==filename:
				self.SetSelection(x[0])
				return 1
			elif x[2]==os.path.basename(filename):
				same = same + 1
				
		self.main.SetRecentFile(os.path.abspath(filename))
		
                if editor=="Scintilla":
                    editor = SourceEditor(self, self.config, self.main)
                elif editor=="Vim":
                    editor = SourceEditorVim(self, self.config, self.main)
		if same==0:
			sametxt = ""
		else:
			sametxt = " (%d)" % same
		basefilename = os.path.basename(filename)
		self.AddPage(editor, basefilename+sametxt)
		editor.Open(filename)
		#print filename, firstvisible
		editor.GotoLine(currentline)
		editor.ScrollToLine(firstvisible)
		self.openedfiles.append([self.GetPageCount()-1, filename, basefilename, argument, extdata])
		self.SetMainTitle(" - "+basefilename+sametxt)
		self.SetSelection(self.GetPageCount()-1)
		return 1

	def AddNewFile(self):
		same = 0
		for x in self.openedfiles:
			if x[1]=="":
				same = same + 1

		editor = SourceEditor(self, self.config, self.main)
		if same==0:
			vname = trans("Noname",self.language)
		else:
			vname = trans("Noname",self.language) +" %d" % same

		self.AddPage(editor, vname)
		editor.SetText("")
		editor.EmptyUndoBuffer()
		editor.Colourise(0, -1)
		editor.SetReadOnly(0)
		editor.SetStyles("NULL")
		self.openedfiles.append([self.GetPageCount()-1, "", vname, ""])
		self.SetMainTitle(" - "+vname)
		self.SetSelection(self.GetPageCount()-1)

	def SetMainTitle(self, subtitle):
		self.main.SetTitle(trans("ProgramTitle",self.language)+" "+self.config.read_config("exmanide_version")+ subtitle)

	def CloseFile(self, stc=None):
		for x in range(self.GetPageCount()):
			if self.GetPage(x)==stc:
				if stc.GetModify():
					title = self.GetPageText(x)
					if title[-1]=="*":
						title = title[:-1]
					ret = wxMessageBox(trans("SaveChangesTo",self.language)+"\n"+title,trans("Information",self.language),wxYES_NO|wxCANCEL)
					if ret==wxYES:
						if self.openedfiles[x][1]=="":
							self.SaveAs(stc)
						else:
							self.SaveFile(stc)
					elif ret==wxCANCEL:
						return 0

				filename = self.openedfiles[x][1]
				debug("Close File: "+filename)
				del self.openedfiles[x]
                                stc.Quit()
				self.RemovePage(x)
				del stc
				wxTheClipboard.Flush()
				self.main.SetStatusText("", 1)
				self.main.SetStatusText("", 2)

				for y in range(len(self.bookmark)):
					if self.bookmark[y]!=None and self.bookmark[y][0]==x:
						self.bookmark[y]=None
				return 1
		return 0

	def SetModify(self, stc):
		for x in range(self.GetPageCount()):
			if self.GetPage(x)==stc:
				basefilename = self.openedfiles[x][2]
				title = self.GetPageText(x)
				if title[-1]!="*":
					title = title + "*"
				self.SetPageText(x, title)
				return 1
		return 0

	def SaveFile(self, stc=None):
		for x in range(self.GetPageCount()):
			if self.GetPage(x)==stc:
				filename = self.openedfiles[x][1]
				stc.SetLexType(filename)
				basefilename = self.openedfiles[x][2]
				debug("Save File: "+filename)
				open(filename,"w").write(stc.GetText())
				stc.SetSavePoint()
				title = self.GetPageText(x)
				if title[-1]=="*":
					self.SetPageText(x, title[:-1])
				return 1
		return 0

	def OnChanged(self,event):
		selectedIndex = event.GetSelection()
		if selectedIndex==-1:
			return
		
		
		subtitle = self.GetPageText(selectedIndex)
		self.SetMainTitle(" - "+subtitle)

		filename = self.openedfiles[selectedIndex][2]
		ext = getext.getext(filename).lower()

		if ext in ["py","pyw"]:
			self.main.SetMenuStatus((305,),(601,602))
		elif ext in ["c","cc","cpp","cxx","cs","h","hh","hpp","hxx","sma","moc","c++"]:
			self.main.SetMenuStatus((601,602),(305,))
		else:
			self.main.SetMenuStatus((),(305,601,602))
			

		
		

		if self.old_ctrltab_ctrlup==1:
			oldselection = event.GetOldSelection()
			if oldselection >= self.GetPageCount():
				return
			self.old_ctrltab_selection = oldselection
			self.old_ctrltab_stc = self.GetPage(oldselection)

class SearchDialog(wxDialog):
	def __init__(self,parent, config, main, stc, kind="Search"):
		self.parent=parent
		self.config=config
		self.main=main
		self.language = self.config.read_config("default_language")
		self.stc = stc
		self.kind = kind

		if kind=="Find":
			plus = 0
		else:
			plus = 30
		size = wxSize(400, 200+plus)
		wxDialog.__init__(self, parent, wxNewId(), kind, wxDefaultPosition, size, wxSYSTEM_MENU|wxCAPTION)

		self.panel = wxPanel(self, wxNewId(), wxDefaultPosition, size)
		EVT_CLOSE(self, self.Cancel)

		if kind=="Find":
			findpos = wxPoint(105,160)
			cancelpos = wxPoint(195,160)
		else:
			findpos = wxPoint(25,160+plus)
			replacepos = wxPoint(115,160+plus)
			replaceallpos = wxPoint(205,160+plus)
			cancelpos = wxPoint(295,160+plus)

		self.findbutton=wxButton(self,2412,trans("find", self.language),findpos)
		self.findbutton.Enable(false)
		EVT_BUTTON(self,2412,self.Find)
		self.prev=wxButton(self,wxID_CANCEL,trans("Cancel", self.language),cancelpos)
		EVT_BUTTON(self,wxID_CANCEL,self.Cancel)
		if kind=="Replace":
			self.replace=wxButton(self,2413,trans("Replace", self.language),replacepos)
			EVT_BUTTON(self,2413,self.onReplace)
			self.replace.Enable(false)
			self.replaceall=wxButton(self,2414,trans("ReplaceAll", self.language),replaceallpos)
			EVT_BUTTON(self,2414,self.onReplaceAll)
			self.replaceall.Enable(false)



		wxStaticText(self.panel, -1, trans("find_text",self.language)+":",wxPoint(20,20))

		findqueue = []
		for x in range(30):
			keyword = self.config.read_config("recent_search_%d" % x)
			if keyword=="" or keyword==None:
				break
			findqueue.append(keyword)
		if len(findqueue)>0:
			word = findqueue[0]
		else:
			word = ''

		self.text =  wxComboBox(self.panel, 2666, word, wxPoint(100, 18), wxSize(280, 20), findqueue, wxCB_DROPDOWN)
		searchword = self.text.GetValue()
		self.text.SetMark(0, len(searchword))
		EVT_COMBOBOX(self.text, 2666, self.onChangeCombo)
		EVT_KEY_UP(self.text, self.onKeyDown)
		EVT_KEY_DOWN(self.text, self.onKeyDown)
		if len(word)>0:
			self.findbutton.Enable(true)
			if kind=="Replace":
				self.replace.Enable(true)
				self.replaceall.Enable(true)

		if kind=="Replace":
			wxStaticText(self.panel, -1, trans("replace_text",self.language)+":",wxPoint(20,48))
			self.replacetext = wxTextCtrl(self.panel, 2667, "", wxPoint(100, 46), wxSize(280, 20))

		self.matchcase = wxCheckBox(self.panel, wxNewId(), trans("find_matchcase",self.language), wxPoint(100, 45+plus))
		self.wholeword = wxCheckBox(self.panel, wxNewId(), trans("find_wholeword",self.language), wxPoint(100, 70+plus))
		self.regexp = wxCheckBox(self.panel, wxNewId(), trans("find_regexp",self.language), wxPoint(100, 95+plus))
		self.reverse = wxCheckBox(self.panel, wxNewId(), trans("find_reverse",self.language), wxPoint(100, 120+plus))

	def onReplace(self, event):
		if self.Find(event)==-1:
			return
		self.stc.ReplaceSelection(self.replacetext.GetValue())

	def onReplaceAll(self, event):
		while 1:
			if self.Find(event)==-1:
				return
			self.stc.ReplaceSelection(self.replacetext.GetValue())

	def onChangeCombo(self, event):
		searchword = self.text.GetValue()
		if len(searchword)>0:
			self.findbutton.Enable(true)
			if self.kind=="Replace":
				self.replace.Enable(true)
				self.replaceall.Enable(true)
		else:
			self.findbutton.Enable(false)
			if self.kind=="Replace":
				self.replace.Enable(false)
				self.replaceall.Enable(false)
		event.Skip()

	def onKeyDown(self, event):
		searchword = self.text.GetValue()
		if len(searchword)>0:
			self.findbutton.Enable(true)
			if self.kind=="Replace":
				self.replace.Enable(true)
				self.replaceall.Enable(true)
		else:
			self.findbutton.Enable(false)
			if self.kind=="Replace":
				self.replace.Enable(false)
				self.replaceall.Enable(false)
			event.Skip()
			return
		if event.GetKeyCode()==13:
			self.Find(event)
		event.Skip()

	def Find(self, event):
		searchword = self.text.GetValue()
		findqueue = [searchword,]
		for x in range(30):
			keyword = self.config.read_config("recent_search_%d" % x)
			if keyword=="" or keyword==None:
				break
			if x==0 and keyword==searchword:
				continue
			findqueue.append(keyword)
		if len(findqueue)>30:
			findqueue.pop()

		self.text.Clear()
		for x in range(len(findqueue)):
			self.config.modify_config("recent_search_%d" % x, findqueue[x])
			self.text.Append(findqueue[x])
		else:
			if x<30:
				self.config.modify_config("recent_search_%d" % (x+1), "")

		return self.stc.SearchWord(searchword ,self.matchcase.GetValue(), self.wholeword.GetValue(), self.regexp.GetValue(), self.reverse.GetValue(), self)


		

	def Cancel(self,event):
		self.EndModal(true)
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

			wizard = SearchDialog(None, config, main, None, "Replace")

			self.wizard = wizard
			wizard.Centre(wxBOTH)
			#wizard.Show(true)
			wizard.ShowModal()
			return true

	
	program=Test2()
	program.MainLoop()
