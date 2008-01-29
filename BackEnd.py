# -*- coding: utf-8 -*-
import ExmanConfig
import sys
import glob
import zipfile
import os, os.path

# Debug Setting
def debug_true(theMessage):
    print theMessage
def debug_false(theMessage):
    pass

if len(sys.argv)>1 and sys.argv[1]=="--debug":
    debug=debug_true
else:
    debug=debug_false



# Setting the Enviroment
class Config(ExmanConfig.ExmanConfig):
    # Default Setting
    def default_config(self):
        config=[]

        # Default Character Set
        lang = os.getenv("LC_ALL") or os.getenv("LANG")
        if os.name=='posix' and lang.lower()=='ko_kr.euckr':
            config.append(self.get_append_string("default_language","Korean"))
        else:
            config.append(self.get_append_string("default_language","English"))

        # ExmanPickle Version
        config.append(self.get_append_string("exmanide_version","0.9.5"))
        # www.exman.pe.kr
        config.append(self.get_append_string("exmanide_address","http://exman.pe.kr"))

        # Widget Position/Size
        config.append(self.get_append_string("widget_pos",""))
        config.append(self.get_append_string("widget_size",""))
        config.append(self.get_append_string("horizontal_sashposition","280"))
        config.append(self.get_append_string("vertical_sashposition","150"))
        # TCP/UDP Backend Server Port
        config.append(self.get_append_string("udp_backend_port","2115"))
        config.append(self.get_append_string("tcp_backend_port","7291"))

        # opened dir
        config.append(self.get_append_string("opened_dir",""))
        return config

def GetUpdaterRoot():
    return ["http://exman.pe.kr/ExmanUpdater/UpdaterRoot/", ]



"""
vim600: sw=4 ts=8 sts=4 et bs=2 fdm=marker fileencoding=utf8 encoding=utf8
"""
