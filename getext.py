"""
2003 박준철
jooncheol@gmail.com
"""
import string
def getext(filename):
	unit = map(string.lower, filename.split("."))
	count = len(unit)
	if count==1:
		return ""
	ext = unit[-1]
	if ext=="gz" and count>2 and unit[-2]=="tar":
		return "tar.gz"
	elif ext=="bz2" and count>2 and unit[-2]=="tar":
		return "tar.bz2"
	else:
		return ext
	

if __name__=='__main__':
	import unittest
	class Testgetext(unittest.TestCase):
		def testNone(self):
			self.assertEquals("",getext("test"))
		def testpy(self):
			self.assertEquals("py",getext("test.py"))
			self.assertEquals("py",getext("test.foo.py"))
		def testgz(self):
			self.assertEquals("gz",getext("test.gz"))
			self.assertEquals("gz",getext("test.foo.gz"))
			self.assertEquals("gz",getext("tar.gz"))
		def testtargz(self):
			self.assertEquals("tar.gz",getext("test.tar.gz"))
			self.assertEquals("tar.gz",getext("test.foo.tar.gz"))

	unittest.main(argv=('','-v'))
