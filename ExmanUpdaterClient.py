#***************************************************************************
#                          ExmanUpdaterClient.py  -  description
#
#    begin                : 2003-03-11
#    copyright            : (C) 2003-03-11 by 박준철
#    email                : jooncheol@gmail.com
#    homepage             : http://www.exman.pe.kr
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
import md5sum
import urllib2
import cStringIO
import os
from wxPython.wx import *

class ExmanUpdaterClient:
	def __init__(self, updaterserver, updatermodulename, clientmoduledir):
		if updaterserver[-1:]!='/':
			updaterserver = updaterserver+'/'
		self.UpdaterServer = updaterserver
		self.UpdaterServerList = [self.UpdaterServer, ]
		self.UpdaterModuleName = updatermodulename
		self.ClientModuleDir = clientmoduledir
		self.UpdateModules = []
		self.version=""
	
	def SetUpdaterServerList(self, list):
		self.UpdaterServerList = self.UpdaterServerList + list
		
	def CompareModules(self):
		for info in self.UpdaterServerList:
			url = info+self.UpdaterModuleName+'.md5sum'
			try:
				con = urllib2.urlopen(url)
				break
			except urllib2.URLError, str:
				continue
		else:
			return []
			
		updateinfo = con.read()
		f = cStringIO.StringIO(updateinfo )
		self.UpdateModules = []
		self.version = f.readline().strip()
		
		for line in f.readlines():
			info = line.split("\t")
			info[-1] = info[-1].strip()
			
			clienturi = self.ClientModuleDir+'/'+info[0]
			if info[1]=='__dir__':
				if not os.path.exists(clienturi):
					self.UpdateModules.append(info)
			else:
				info[-1] = int(info[-1])
				if not os.path.exists(clienturi):
					self.UpdateModules.append(info)
				elif info[1]!=md5sum.md5sum(clienturi):
					self.UpdateModules.append(info)
		return self.UpdateModules
	
	def UpdateModule(self, updatemodule=None):
		if updatemodule!=None:
			self.UpdateModules = updatemodule
		if not os.path.exists(self.ClientModuleDir):
			os.mkdir(self.ClientModuleDir)
		for info in self.UpdateModules :
			clienturi = self.ClientModuleDir+'/'+info[0]
			if info[1]=='__dir__':
				os.mkdir(clienturi)
			else:
				fp = open(clienturi+'.up','wb')
				url = self.UpdaterServer+self.UpdaterModuleName+'/'+info[0]
				con = urllib2.urlopen(url)
				fp.write(con.read())
				fp.close()
				
		for info in self.UpdateModules :
			clienturi = self.ClientModuleDir+'/'+info[0]
			if info[1]!='__dir__':
				os.rename(clienturi+'.up', clienturi)

	def UpdateModuleGUI(self, parent=None, updatemodule=None):		

		if updatemodule!=None:
			self.UpdateModules = updatemodule
		if not os.path.exists(self.ClientModuleDir):
			os.mkdir(self.ClientModuleDir)

		max = len(self.UpdateModules)
		dlg = wxProgressDialog("ExmanUpdater",
				"Initializing Updater",
				max,
				parent,
				wxPD_CAN_ABORT | wxPD_APP_MODAL | wxPD_AUTO_HIDE)
		
		keepGoing = true
		count = 0 
		while keepGoing and count < max:
			info = self.UpdateModules[count]
			count = count + 1
			wxUsleep(100)
			
			clienturi = self.ClientModuleDir+'/'+info[0]
			if info[1]=='__dir__':
				os.mkdir(clienturi)
			else:
				fp = open(clienturi+'.up','wb')
				url = self.UpdaterServer+self.UpdaterModuleName+'/'+info[0]
				con = urllib2.urlopen(url)
				fp.write(con.read())
				fp.close()
			
			if count==max:
				keepGoing = dlg.Update(0, "Download: "+clienturi)
			else:
				keepGoing = dlg.Update(count, "Download: "+clienturi+" (%d/%d)" % (count, max))

		
		keepGoing = true
		count = 0
		while keepGoing and count < max:
			info = self.UpdateModules[count]
			count = count + 1
			wxUsleep(100)
			
			clienturi = self.ClientModuleDir+'/'+info[0]
			if info[1]!='__dir__':
				os.rename(clienturi+'.up', clienturi)
				
			keepGoing = dlg.Update(count, "Updated: "+clienturi+" (%d/%d)" % (count, max))

		dlg.Destroy()

		
if __name__=='__main__':

	updater = ExmanUpdaterClient("http://localhost/UpdaterRoot", "TestModule", "TestModule")
	modify = updater.CompareModules()
	if len(modify)>0:
		print updater.version
		updater.UpdateModule()
