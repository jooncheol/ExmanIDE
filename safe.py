def safesend(sock,pack,size):
    left=size
    cur=0
    while left:
        ret=sock.send(pack);
        if ret==-1:
            return -1
        if ret==0:
            return cur
        cur = cur + ret
        left = left - ret
    return cur

def saferecv(sock,size,debug=0):
    left=size
    cur=''
    i=0
    while left:
        ret=sock.recv(left);
        if ret==-1:
            return -1
        if ret==0:
            return cur
        cur = cur + ret
        left = left - len(ret)
        i=i+1
        if debug>0:
            get = size-left
            percent = float(get) / size * 100
            print "\rDownload: ", get, " / ", size, "(%2.2f%%)" % percent,
    if debug>0:
		print 
    return cur

def saferecv_fp(sock,size,fp,debug=0):
    buffersize=1024
    left=size
    i=0
    while left:
        ret=sock.recv(buffersize);
        if ret==-1:
            return None
        if ret==0:
            return None
        fp.write(ret)
        left = left - len(ret)
        i=i+1
        if debug>0:
            get = size-left
            percent = float(get) / size * 100
            print "\rDownload: ", get, " / ", size, "(%2.2f%%)" % percent,
    if debug>0:
		print 
    return None
