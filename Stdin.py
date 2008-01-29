# -*- coding: utf-8 -*-
import sys
from tcplog import sendmessage

class Stdin:
    def __init__(self, port=7291):
        self.real_file = sys.stdin
        self.buffer = ""
        self.closed = 0
        self.port = port

    def __getattr__(self, name):
        return getattr(self.real_file, name)

    def isatty(self):
        return 1

    def read(self, size = -1):
        if self.closed:
            return self.real_file.read(size)
        return sendmessage('read %d' % size, port=self.port)


    def readline(self, size = -1):
        if self.closed:
            return self.real_file.readline(size)
        return sendmessage('readline %d' % size, port=self.port)

    def readlines(self, *sizehint): 
        if self.closed:
            return apply(self.real_file.readlines, sizehint)
        return sendmessage('readlines', port=self.port)

    def fake_raw_input(self, prompt=''):
        return sendmessage('raw_input '+prompt, port=self.port)
    def fake_input(self, prompt=''):
        return eval(sendmessage('input '+prompt, port=self.port))




if __name__=='__main__':
    """
    import unittest
    class TestBaseVar(unittest.TestCase):
        def testNull(self):
            self.assertEquals("",Stdin().read())

    unittest.main(argv=('','-v'))
    """
else:
    import sys
    sys.stdin = Stdin()
    _raw_input = raw_input
    _input = input
    raw_input = sys.stdin.fake_raw_input
    input = sys.stdin.fake_input



"""
vim600: sw=4 ts=8 sts=4 et bs=2 fdm=marker fileencoding=utf8 encoding=utf8
"""