#from socket import *
from threading import Thread 
import threading
from SocketServer import ThreadingMixIn 
# from gigabotclient import *
import json
import os

# Multithreaded TCP Server Socket Program Stub
TCP_IP = '' 
TCP_PORT = 63200

#   Multithreaded Python server : TCP Server Socket Thread Pool
class GigabotThread(Thread): 
    def __init__(self,conn, ip,port, mach): 
        Thread.__init__(self) 
        self.conn = conn
        self.ipaddress = ip 
        self.port = port 
        self.machine = mach
        self.printstuff = ""
        print "A new Gigabot Client connected! \n"

#   Main while loop of the GigabotThread
    def run(self): 
        # print threading.currentThread().getName()
        while True : 
            try:
                c_data = self.recvdata()
                if(c_data): 
                    self.printstuff = self.machine.parsedata(c_data)
                    print(self.printstuff)

                self.senddata("OK")  # echo
            except error, exc:
                print "Client Disconnected! ", exc
                return

#   Send function encodes data and creates a json object to be sent over TCP
#   Recieve function decodes data and unpacks the json object, then sends a ACK msg to client
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



# if __name__ == "__main__":
# #   Clear the commandline
#     os.system("clear")
#     print "Chromebook Gigabot Dashboard Data Server : \nWaiting for connections Gigabot clients..." 
#     chromeServer = socket(AF_INET, SOCK_STREAM) 
#     chromeServer.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
#     chromeServer.bind((TCP_IP, TCP_PORT)) 
#     chromeServer.listen(5) 

#     while True: 
# #       For each gigabot connected, create a new Thread. 
#         (conn, (ip,port)) = chromeServer.accept() 
# #       Create a new Thread for each new connection
#         newthread = GigabotThread(conn,ip,port) 
#         newthread.start() 
#         gigabotthreads.append(newthread) 
#         # print gigabotthreads
#         # print gigabots

# #   Kill all thread at the end of the program
#     for t in gigabotthreads: 
#         t.join()
#     gigabots.clear()
