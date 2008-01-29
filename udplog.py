# -*- coding: utf-8 -*-
import socket, select, time, random
from threading import *
from errno import *
import os, sys

class udpLog(Thread):
    def __init__(self, ip='127.0.0.1', port=2115):
        Thread.__init__(self)

        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.setblocking(0)
        while 1:
            try:
                self.sock.bind((ip, self.port))
                break
            except socket.error:
                self.port = self.port + 1

        self.handler = None

    

    def set_handler(self, handler):
        self.handler = handler

    def run(self):
        sfds = [self.sock.fileno()]

        self.keepgoing = 1

        while self.keepgoing:
            if select.select(sfds, [], [], 0.1):
                try:
                    r = self.sock.recvfrom(8192)
                    if r:
                        t = time.localtime()
                        receivetime = "%d-%d-%d %d:%d:%d\r\n" %(t[0],t[1],t[2],t[3],t[4],t[5])
                        sendip, sendport = r[1]
                        content = r[0]

                        if content == '__stop__':
                            self.stop()
                        else:
                            if self.handler!=None:
                                self.handler(content, (sendip, sendport))

                except socket.error, why:
                    if why[0] not in [EAGAIN, EWOULDBLOCK, ECONNRESET]:
                        raise socket.error, why
                        error += 'r'

        self.sock.close()

    def stop(self):
        self.keepgoing = 0

def sendlog(message, ip='127.0.0.1',port=2115):
    c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    c.sendto(message,(ip, port))




if __name__=='__main__':
    """
    if os.fork()>0:
        sys.exit(0);
    """
    logth = udpLog()
    logth.start()
    time.sleep(20)
    print logth.stop()



"""
vim600: sw=4 ts=8 sts=4 et bs=2 fdm=marker fileencoding=utf8 encoding=utf8
"""