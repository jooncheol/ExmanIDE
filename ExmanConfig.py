import os, os.path
import string
import portalocker
import shutil

class ExmanConfig:
	def __init__(self,theConfigDir=".Exmanconfig",theConfigFile="ExmanConfig"):
		if os.name=='nt':
			# 레지스트리 이용
			self.pathsep='\\';
			self.theirConfigDir=os.getenv('TEMP')+self.pathsep+theConfigDir
		else:
			# 파일 이용
			self.pathsep='/';
			self.theirConfigDir=os.getenv('HOME')+self.pathsep+theConfigDir

		self.theirConfigFile=self.theirConfigDir+self.pathsep+theConfigFile

		# 환경 설정 정보를 가지고 있음
		self.their_configlines=None

		# is_exist_config 
		if self.is_exist_config()==0:
			self.create_config()

		
	def create_config(self):
		try:
			os.mkdir(self.theirConfigDir)
		except:
			pass
		self.save_config(self.default_config())
		return 1

	def is_exist_config(self):
		# 파일 이용
		if os.path.isdir(self.theirConfigDir) and os.path.isfile(self.theirConfigFile):
			return 1
		else:
			return 0

	def save_config(self,theConfiglines=None):
		if theConfiglines==None:
			theConfiglines=self.their_configlines

		fp=open(self.theirConfigFile,"w")
		portalocker.lock(fp, portalocker.LOCK_EX)
		fp.writelines(theConfiglines)
		portalocker.unlock(fp)
		fp.close()
		self.load_config()

	def get_append_string(self,theKey, theValue):
		return theKey+' = "'+theValue+'"\n'

	def load_config(self):
		fp=open(self.theirConfigFile,"r")
		portalocker.lock(fp, portalocker.LOCK_EX)
		self.their_configlines=fp.readlines()
		portalocker.unlock(fp)
		fp.close()
	
	def default_config(self):
		# 재정의 하여 사용
		return []

	def read_config(self,theKey):
		if self.their_configlines==None:
			self.load_config()
		for x in self.their_configlines:
			key,value=map(string.strip,string.split(x,"="))
			if key==theKey:
				return value[1:-1]
		else:
			return None

	def modify_config(self,theKey,theValue):
		if self.their_configlines==None:
			self.load_config()

		tmp=[]
		flag=0
		for x in self.their_configlines:
			key,value=map(string.strip,string.split(x,"="))
			value=value[1:-1]
			if key==theKey:
				value=theValue
				flag=1
			tmp.append(self.get_append_string(key,value));

		if flag==1:
			self.save_config(tmp)
		else:
			self.append_config(theKey,theValue)

	def append_config(self,theKey,theValue):
		if self.their_configlines==None:
			self.load_config()
		# 추가
		self.their_configlines.append(self.get_append_string(theKey,theValue));

		# 저장
		self.save_config()
	def remove_config(self):
		shutil.rmtree(self.theirConfigDir)

	def get_config_dir(self):
		return self.theirConfigDir

	def get_config_file(self):
		return self.theirConfigFile

	def get_path_sep(self):
		return self.pathsep

if __name__=='__main__':
	class testconfig(ExmanConfig):
		def default_config(self):
			return [self.get_append_string("myHome","우리집")]

	config=testconfig("testconfig","default")
	config.append_config("myCompany","미디어랜드")
	print config.read_config("myCompany")
	config.modify_config("myCompany","우주프로젝트")
	print config.read_config("myCompany")
	#config.remove_config()

