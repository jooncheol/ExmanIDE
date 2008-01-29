# -*- coding: utf-8 -*-
import os, sys
from Stdin import *


if __name__=='__main__':
    if not sys.argv[2:]:
        print "usage: InitExecute.py tcpport scriptfile [arg] ..."
        sys.exit(2)
    
    tcpport = int(sys.argv[1])
    sys.stdin = Stdin(tcpport)
    _raw_input = raw_input
    _input = input
    raw_input = sys.stdin.fake_raw_input
    input = sys.stdin.fake_input

    filename = sys.argv[2]     # Get script filename
    if not os.path.exists(filename):
        print 'Error:', `filename`, 'does not exist'
        sys.exit(1)

    del sys.argv[1]         # Hide tcp port
    del sys.argv[0]         # Hide "InitExecute.py" from argument list

    # Insert script directory in front of module search path
    sys.path.insert(0, os.path.dirname(filename))

    execfile(filename)



"""
vim600: sw=4 ts=8 sts=4 et bs=2 fdm=marker fileencoding=utf8 encoding=utf8
"""