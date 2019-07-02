from socket import *
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
        conn.send("Connected!\n")
        self.ip = ip 
        self.port = port 
        print "A new Gigabot Machine was connected! \n"
        self.machine = 0
 
    def run(self): 
        #first data packet is confirmation
        data = self.conn.recv(2048)
        print data

        self.collectheader(data)
        self.machine.printdata()

        while True : 
            data = self.conn.recv(2048) 
            #c_data = data.decode("base64")
            c_data = json.loads(data.decode("base64"))
            #print "Recieved data: ", c_data
            self.machine.parsedata(c_data)
            self.machine.printtemp()

            conn.send(ackmessage.encode())  # echo

    def collectheader(self, d):
        try:
            machine_data = json.loads(self.conn.recv(2048).decode("base64"))
            m=machine_data.split("|")
            self.machine = gigabotclient(520,m[1], str(ip), "On")
            self.machine.dateuploaded = m[0]
            gigabots.append(self.machine)
        except ValueError:
            pass



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
     
    for t in gigabotthreads: 
        t.join()
    gigabots.clear()