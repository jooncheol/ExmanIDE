"""
safe 모듈
박준철 jooncheol@gmail.com
2002. 12

safe 로 시작하는 이 함수들은 
보내려고 하는 길이와 실제 보낸 데이터의 길이의 차이를 해결한 함수들이다.
이 함수들은 저속구간의 네트웍에 특히 효과가 있다.
"""

# 안전한 send
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

# 안전한 recv
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
		# 출력을 이쁘게 하기 위해서
        if debug>0:
            get = size-left
            percent = float(get) / size * 100
            print "\rDownload: ", get, " / ", size, "(%2.2f%%)" % percent,
    if debug>0:
		print 
    return cur

# size 만큼의 데이타를 1024byte씩 받은즉시 넘겨받은 파일포인터에 직접 쓰는 함수
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
