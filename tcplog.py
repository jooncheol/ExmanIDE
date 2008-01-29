# -*- coding: utf-8 -*-
import socket, select, time, random
from threading import *
from errno import *
import os, sys

from safe import *

class tcpLog(Thread):
    def __init__(self, ip='127.0.0.1', port=7291):
        Thread.__init__(self)

        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        while 1:
            try:
                self.sock.bind((ip, self.port))
                self.sock.listen(5)
                break
            except socket.error:
                self.port = self.port + 1

        self.handler = None

    

    def set_handler(self, handler):
        self.handler = handler

    def run(self):
        self.keepgoing = 1

        while self.keepgoing:
            c, addr = self.sock.accept()
            content = c.recv(4096)
            t = time.localtime()
            receivetime = "%d-%d-%d %d:%d:%d\r\n" %(t[0],t[1],t[2],t[3],t[4],t[5])
            if content == '__stop__':
                self.keepgoing = 0
                safesend(c,content,len(content))
                break
            else:
                if content[:7] == '__len__':
                    # __len__: 99
                    while 1:
                        try:
                            length = int(content[8:].strip())
                            safesend(c, "OK", 2)
                            break
                        except:
                            safesend(c, "NO", 2)
                    content = saferecv(c, length)

                if self.handler!=None:
                    value = self.handler(content, addr)
                    try:
                        safesend(c, value,len(value))
                    except TypeError:
                        safesend(c, 'None',4)
                else:
                    safesend(c, content,len(content))

        self.sock.close()

    def stop(self):
        sendmessage('__stop__',self.ip, self.port)

def sendmessage(message, ip='127.0.0.1',port=7291):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        c.connect((ip,port))
        if message=="__stop__":
            safesend(c, message,len(message))
        else:
            while 1:
                l = "__len__: %d" % len(message)
                safesend(c, l,len(l))
                if "OK"==saferecv(c, 2):
                    break
            safesend(c, message,len(message))
        return c.recv(4096)
    except:
        return None


if __name__=='__main__':
    """
    if os.fork()>0:
        sys.exit(0);
    """
    logth = tcpLog()
    logth.start()
    time.sleep(20)
    logth.stop()



"""
vim600: sw=4 ts=8 sts=4 et bs=2 fdm=marker fileencoding=utf8 encoding=utf8
"""