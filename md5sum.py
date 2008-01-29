# -*- coding: utf-8 -*-
import md5
def md5sum(filename):
    hexStr = '0123456789abcdefABCDEF'
    m = md5.new()
    f = open(filename,'r')
    for line in f.readlines():
        m.update(line)
    r = ''
    for ch in m.digest():
        i = ord(ch)
        r = r + hexStr[(i >> 4) & 0xF] + hexStr[i & 0xF]
    return r
    



"""
vim600: sw=4 ts=8 sts=4 et bs=2 fdm=marker fileencoding=utf8 encoding=utf8
"""