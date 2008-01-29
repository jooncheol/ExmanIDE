# -*- coding: utf-8 -*-
from wxPython.wx import *
from BackEnd import *
from Language import *

from SourceEditor import DescriptText, stderrText, crustShell
from wx.py import version
import types
import pprint

BASETYPE = ['types.IntType', 'types.StringType', 'types.FloatType', 'types.ComplexType', 'types.UnicodeType']

class VarTree(wxTreeCtrl):
    def __init__(self,sp,parent,config,main, varname='None', varsdic={}):
        #########################################################
        self.parent=parent
        self.config=config
        self.main=main
        self.varsdic=varsdic

        # Get Character Setting / Setting Translate Function
        self.language = self.config.read_config("default_language")

        wxTreeCtrl.__init__(self,sp,500)
        self.root = None

        EVT_LEFT_DCLICK(self, self.onDClick)
        EVT_TREE_SEL_CHANGED(self, -1, self.onClick)
        #EVT_TREE_ITEM_EXPANDING(self, -1, self.onExpanding)
    
        self.handler_dclick = None

        self.varname = varname

        self.InitRoot()

    def InitRoot(self):
        self.root=self.AddRoot(self.varname)
        self.SetPyData(self.root, "Root")
        self.Expand(self.root)


    def set_dclick_handler(self, handler=None):
        self.handler_dclick = handler

    def AddVars(self, parent, vars={}):
        if type(vars)!=types.DictType:
            print vars
            print type(vars)
            print repr(vars)
            return
        keys = vars.keys()
        keys.sort()
        for x in keys:
            newchild = self.AppendItem(parent, x)
            self.SetPyData(newchild, vars[x])

            xtype = eval(vars[x][0])
            if xtype==types.ListType or\
                xtype==types.DictType or\
                xtype==types.InstanceType:
                    self.SetItemHasChildren(newchild, TRUE)
                    self.AddVars(newchild, vars[x][1])
            else:
                    self.SetItemHasChildren(newchild, FALSE)
        
        if parent == self.root:
            self.Expand(parent)



    def onClick(self,event):
        item = self.GetSelection()
        data=self.GetItemData(item).GetData()
        if data=="Root":
            if self.IsExpanded(item):
                self.Collapse(item)
            else:
                self.Expand(item)
        else:
            # make document
            if data[0] in ["types.InstanceType", "types.ClassType"]:
                docs = data[3]
            else:
                docs = eval(data[0]).__doc__

            if docs==None:
                docs=''
            if data[2] == None:
                value = repr(data[1])
            else:
                value = repr(data[2])

            document = '''
Type = %s

Value = %s

"""
%s
"""
            ''' % (data[0], value,  docs)

            self.parent.description.SetText(document)

    def onDClick(self,event):
        self.onClick(event);
        item = self.GetSelection()
        data=self.GetItemData(item).GetData()
        if data=="Root":
            return
        if data[0] in BASETYPE+["types.ListType","types.DictType"]:
            dlg = wxDialog(self, -1, trans("ModifyVariable", self.language), size=wxSize(350, 200), style = wxDEFAULT_DIALOG_STYLE|wxDIALOG_MODAL)
            sizer = wxBoxSizer(wxVERTICAL)

            if data[0] in BASETYPE:
                value = repr(data[1])
            else:
                value = ""

            #frame.f_locals
            # debug variable name
            cur = item
            vname = ''
            while 1:
                parent = self.GetItemParent(cur)
                keyname = self.GetItemText(cur)
                data = self.GetItemData(parent).GetData()
                if data=="Root":
                    vname = "frame.f_locals['"+self.GetItemText(cur)+"']" + vname
                    break
                if data[0] in ["types.ListType","types.DictType"]:
                    vname = keyname + vname 
                else:
                    vname = '.' + keyname + vname 

                cur = parent

            lines=wxTextCtrl(dlg, -1, value, size=wxSize(300,150),style=wxTE_MULTILINE|wxTE_RICH)
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
                val = lines.GetValue().strip()
            else:
                self.tcpreturn = '\0'
            dlg.Destroy()
            print '%s = %s' % (vname, val)
            self.main.tcpreturn = "nextcmd = 'modify'\n%s = %s" % (vname, val)

    def onExpanding(self, event):
        item=event.GetItem()
        debug(self.GetItemText(item)+" Expanding")
        data = self.GetItemData(item).GetData()
        if data[0]=="Root":
            return

        deleteitem = []
        for x in range(self.GetChildrenCount(item)):
            if x==0:
                child, cookie = self.GetFirstChild(item)
            else:
                child, cookie = self.GetNextChild(item, cookie)
            deleteitem.append(child)
        for x in deleteitem:
            self.Delete(x)

        self.create(data[1], data[3], data[5])



class Profile(wxNotebook):    
    def __init__(self,parent,config,main):
        self.parent=parent
        self.config=config
        self.main=main
        wxNotebook.__init__(self, parent, -1)
        self.openedfiles = []

        # Get Character Setting / Setting Translate Function
        self.language = self.config.read_config("default_language")

        intro = 'Welcome To ExmanIDE\nWelcome To PyCrust %s - The Flakiest Python Shell' % version.VERSION

        self.shell=crustShell(self, config, main, id=-1, intro=intro)
        self.shell.SetStyles()
        
        self.stdout=wxTextCtrl(self, -1, style=wxTE_MULTILINE|wxTE_READONLY|wxTE_RICH)
        self.stderr= stderrText(self ,config, main)
        self.stderr.SetText('')


        self.AddPage(self.shell, "PyCrust")
        self.AddPage(self.stdout, "stdout")
        self.AddPage(self.stderr, "stderr")


        if self.config.read_config("locals_not_show")!='1':
            self.SetLocals()

    def SetLocals(self, flag=1):
        if flag == 1:
            # Splitter
            self.sp1=wxSplitterWindow(self,-1)
            self.locals=VarTree(self.sp1 ,self, self.config, self.main, "locals" )
            #self.locals.AddVars(self.locals.root, GetDebugVars(locals()))
            self.locals.AddVars(self.locals.root, {})
            self.description = DescriptText(self.sp1 ,self.config, self.main)
            self.sp1.SplitVertically(self.locals,self.description, 200)
            self.sp1.SetMinimumPaneSize(3)
            self.AddPage(self.sp1, "locals")
        else:
            self.RemovePage(3)



"""
vim600: sw=4 ts=8 sts=4 et bs=2 fdm=marker fileencoding=utf8 encoding=utf8
"""
