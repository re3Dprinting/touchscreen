import socket 
from threading import Thread 
from SocketServer import ThreadingMixIn 

ackmessage = "OK"

# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
    def __init__(self,ip,port): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port = port 
        print "[+] New server socket thread started for " + ip + ":" + str(port) 
 
    def run(self): 
        while True : 
            data = conn.recv(2048) 
            print "Server received data:", data.decode("utf-8")
            conn.send(ackmessage.encode())  # echo


# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = '' 
TCP_PORT = 63200
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
tcpServer.listen(5)
print "socket is listening" 
threads = []   
 
while True: 
    print "Multithreaded Python server : Waiting for connections from TCP clients..." 
    (conn, (ip,port)) = tcpServer.accept() 
    newthread = ClientThread(ip,port) 
    newthread.start() 
    threads.append(newthread) 
 
for t in threads: 
    t.join()