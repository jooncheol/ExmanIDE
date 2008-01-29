# -*- coding: utf-8 -*-
import sys, os, bdb
from Stdin import *
import types
import cPickle
ALLTYPES = {
types.BufferType:'types.BufferType',
types.BuiltinFunctionType:'types.BuiltinFunctionType',
types.BuiltinMethodType:'types.BuiltinMethodType',
types.ClassType:'types.ClassType',
types.CodeType:'types.CodeType',
types.ComplexType:'types.ComplexType',
types.DictProxyType:'types.DictProxyType',
types.DictType:'types.DictType',
types.EllipsisType:'types.EllipsisType',
types.FileType:'types.FileType',
types.FloatType:'types.FloatType',
types.FrameType:'types.FrameType',
types.FunctionType:'types.FunctionType',
types.GeneratorType:'types.GeneratorType',
types.InstanceType:'types.InstanceType',
types.IntType:'types.IntType',
types.LambdaType:'types.LambdaType',
types.ListType:'types.ListType',
types.LongType:'types.LongType',
types.MethodType:'types.MethodType',
types.ModuleType:'types.ModuleType',
types.NoneType:'types.NoneType',
types.ObjectType:'types.ObjectType',
types.SliceType:'types.SliceType',
types.StringType:'types.StringType',
types.TracebackType:'types.TracebackType',
types.TupleType:'types.TupleType',
types.TypeType:'types.TypeType',
types.UnboundMethodType:'types.UnboundMethodType',
types.UnicodeType:'types.UnicodeType',
types.XRangeType:'types.XRangeType'
}
#types.DictionaryType:'types.DictionaryType',
BASETYPE = ['types.IntType', 'types.StringType', 'types.FloatType', 'types.ComplexType', 'types.UnicodeType']
ENUMTYPE = ['types.DictType', 'types.ListType', 'types.InstanceType']
DELETELOCALS = {}

def RemoveLocals(var):
    global DELETELOCALS
    ret = {}
    for x in var.keys():
        if DELETELOCALS.has_key(x) and var[x]==DELETELOCALS[x]:
            pass
        else:
            ret[x] = var[x]
    if ret.has_key('x') and ret['x']=='GetTypes':
        del ret['x']
    return ret
    

def GetTypes(type):
    if ALLTYPES.has_key(type):
        return ALLTYPES[type]
    else:
        return "types.NoneType"

def GetDebugVars(vars, depth=0):
    ret = {}
    if depth==900:
        return ret
    varstype = type(vars)
    if varstype==types.DictType:
        for x in vars.keys():
            try:
                xtype = GetTypes(type(vars[x]))
                if depth>0:
                    if type(x)==types.StringType:
                        name = "['"+x+"']"
                    else:
                        name = "["+x+"]"
                else:
                    name = x
                if xtype in BASETYPE:
                    ret[name] = [xtype, vars[x], None]
                elif xtype in ENUMTYPE:
                    ret[name] = [xtype, GetDebugVars(vars[x], depth+1), repr(vars[x])]
                else:
                    ret[name] = [xtype, repr(vars[x]), None]
                if xtype in ["types.InstanceType", "types.ClassType"]:
                    ret[name].append(vars[x].__doc__)
                else:
                    ret[name].append(None)
            except:
                continue

    elif varstype==types.ListType:
        no = 0
        for x in vars:
            try:
                xtype = GetTypes(type(x))
                name = '[%d]' % no
                if xtype in BASETYPE:
                    ret[name] = [xtype, x, None]
                elif xtype in ENUMTYPE:
                    ret[name] = [xtype, GetDebugVars(x, depth+1), repr(x)]
                else:
                    ret[name] = [xtype, repr(x), None]

                if xtype in ["types.InstanceType", "types.ClassType"]:
                    ret[name].append(vars[x].__doc__)
                else:
                    ret[name].append(None)
                no = no + 1
            except:
                continue
    elif varstype==types.InstanceType:
        for x in dir(vars.__class__):
            try:
                xvalue = getattr(vars, x)
                xtype = GetTypes(type(xvalue))
                if xtype in BASETYPE:
                    ret[x] = [xtype, xvalue, None]
                elif xtype in ENUMTYPE:
                    ret[x] = [xtype, GetDebugVars(xvalue, depth+1), repr(xvalue)]
                else:
                    ret[x] = [xtype, repr(xvalue), None]
                if xtype in ["types.InstanceType", "types.ClassType"]:
                    ret[x].append(xvalue.__doc__)
                else:
                    ret[x].append(None)
            except:
                continue
    """
    elif varstype==types.ClassType:
        for x in vars.__dict__.keys():
            xvalue = getattr(vars, x)
            xtype = GetTypes(type(xvalue))
            if xtype in BASETYPE:
                    ret[x] = [xtype, xvalue]
            elif xtype in ENUMTYPE:
                    ret[x] = [xtype, GetDebugVars(xvalue)]
            else:
                    ret[x] = [xtype, repr(xvalue)]
    """
    return ret

class ExmanDebug(bdb.Bdb):
    def GetDebugRunningCommands(self,frame):
        fname = os.path.abspath(frame.f_code.co_filename)
        lineno = frame.f_lineno

        """
        import pprint
        for x in dir(frame):
            pprint.pprint(x)
        pprint.pprint(frame.f_locals)
        """

        self.set_continue()
        while 1:
            if self.localsshow!='locals_invisible':
                localvals = cPickle.dumps(GetDebugVars(RemoveLocals(frame.f_locals)),1)
                codes = sendmessage("SetLocals %s" % localvals, port = self.port)
            codes = sendmessage("GetDebugRunningCommands %s %d" % (fname,lineno), port=self.port)
            try:
                exec(codes)
            except:
                info = sys.exc_info()
                sendmessage("Error %s:\n\n%s" % (info[0], info[1]), port = self.port)
                continue

            if nextcmd != "modify":
                break


        self.clear_all_breaks()
        for x in breakpoints:
            #print "break point: ", x
            self.set_break(x[0], x[1])

        #print nextcmd
        if nextcmd=="run":
            self.set_continue()
        elif nextcmd=="next":
            self.set_next(frame)
        elif nextcmd=="step":
            self.set_step()
        elif nextcmd=="quit":
            self.set_quit()
        else:
            self.set_continue()

    def __init__(self, filename, port, localsshow='locals_visible'):
        bdb.Bdb.__init__(self)
        self.filename = filename
        self.port = port
        self.localsshow = localsshow

    def user_line(self, frame):
        fn = self.canonic(frame.f_code.co_filename)

        if fn=="<string>":
            self.set_continue()
            return
        self.GetDebugRunningCommands(frame) 

    def user_return(self, frame, retval):
        self.GetDebugRunningCommands(frame) 
    def user_exception(self, frame, exc_stuff):
        self.set_continue()




if __name__=='__main__':
    if not sys.argv[3:]:
        print "usage: ExmanDebug.py tcpport localsshow scriptfile [arg] ..."
        sys.exit(2)

    localsshow = sys.argv[2]
    if localsshow!='locals_invisible':
        localsshow = 'locals_visible'
    tcpport = int(sys.argv[1])


    sys.stdin = Stdin(tcpport)
    _raw_input = raw_input
    _input = input
    raw_input = sys.stdin.fake_raw_input
    input = sys.stdin.fake_input

    filename = sys.argv[3]     # Get script filename
    if not os.path.exists(filename):
        print 'Error:', `filename`, 'does not exist'
        sys.exit(1)

    del sys.argv[2]         # Hide locals show
    del sys.argv[1]         # Hide tcpport
    del sys.argv[0]         # Hide "pdb.py" from argument list

    sys.path.insert(0, os.path.dirname(filename))

    d = ExmanDebug(filename,tcpport,localsshow)
    codes = sendmessage("GetDebugCommands",port=tcpport)
    exec(codes)
    for x in breakpoints:
        #print "break point", x
        d.set_break(x[0], x[1])


    for x in locals().keys():
        DELETELOCALS[x] = locals()[x]
    d.run('execfile("' + filename + '")')



"""
vim600: sw=4 ts=8 sts=4 et bs=2 fdm=marker fileencoding=utf8 encoding=utf8
"""