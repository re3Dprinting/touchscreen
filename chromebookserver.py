from socket import *
import select
from threading import Thread 
import threading
from SocketServer import ThreadingMixIn 
from gigabotclient import *
import json

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
        self.senddata("Server Confirmed Connection\n")
        self.ipaddress = ip 
        self.port = port 
        self.check_dup()
        print "A new Gigabot Client connected! \n"
        #Recieve first packet which is Client Confirmation
        print self.recvdata()
        self.senddata("OK") #ACK
    def run(self): 
        # print threading.currentThread().getName()
        while True : 
            try:
                c_data = self.recvdata()
                self.machine.parsedata(c_data)
                self.senddata("OK")  # echo
            except error, exc:
                print "Client Disconnected! ", exc
                return
    def check_dup(self):
        for bot in gigabots:
            if bot.ipaddress == self.ipaddress:
                self.machine = bot
                return
        self.machine = gigabotclient(str(ip))
        gigabots.append(self.machine)
        return

    def senddata(self, msg):
        if(msg):
            temp = json.dumps(msg).encode("base64")
            self.conn.send(temp)

    def recvdata(self):
        data = self.conn.recv(2048)
        if(data):
            m_data = json.loads(data.decode("base64"))
            self.senddata("OK") #Send ACK message
            return m_data



if __name__ == "__main__":
    print "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    print "Chromebook Gigabot Dashboard Data Server : \nWaiting for connections Gigabot clients..." 
    chromeServer = socket(AF_INET, SOCK_STREAM) 
    chromeServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
    chromeServer.bind((TCP_IP, TCP_PORT)) 
    chromeServer.listen(5) 

    while True: 
        (conn, (ip,port)) = chromeServer.accept() 

        #Create a new client
        newthread = GigabotThread(conn,ip,port) 
        newthread.start() 
        gigabotthreads.append(newthread) 
        # print threading.currentThread().getName()
        # print gigabotthreads
        # print gigabots
     
    for t in gigabotthreads: 
        t.join()
    gigabots.clear()