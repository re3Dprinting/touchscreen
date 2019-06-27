from socket import *
from threading import Thread 
import threading
from SocketServer import ThreadingMixIn 
from gigabotclient import *

# Multithreaded TCP Server Socket Program Stub
TCP_IP = '' 
TCP_PORT = 63200
BUFFER_SIZE = 20  # Usually 1024, but we need quick response 
ackmessage = "OK"
gigabotthreads = []
#data_lock = threading.Lock()
gigabots = []


# Multithreaded Python server : TCP Server Socket Thread Pool
class GigabotThread(Thread): 
    def __init__(self,conn, ip,port): 
        Thread.__init__(self) 
        self.conn = conn
        conn.send("Connected!\n")
        self.ip = ip 
        self.port = port 
        print "A new Gigabot Machine was connected! \n"
        self.machine = 0
 
    def run(self): 
        data = self.conn.recv(2048)

        self.machine = gigabotclient(520,"XLT", str(ip), "On")
        gigabots.append(self.machine)
        self.machine.printdata()

        while True : 
            data = self.conn.recv(2048) 
            print "Recieved data: ", data.decode("utf-8")
            conn.send(ackmessage.encode())  # echo


if __name__ == "__main__":
    print "Chromebook Gigabot Dashboard Data Server : Waiting for connections Gigabot clients..." 
    chromeServer = socket(AF_INET, SOCK_STREAM) 
    chromeServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
    chromeServer.bind((TCP_IP, TCP_PORT)) 
    chromeServer.listen(5)
    print "socket is listening"  

    while True: 
        (conn, (ip,port)) = chromeServer.accept() 

        #Create a new client
        newthread = GigabotThread(conn,ip,port) 
        newthread.start() 
        gigabotthreads.append(newthread) 
     
    for t in gigabotthreads: 
        t.join()
    gigabots.clear()