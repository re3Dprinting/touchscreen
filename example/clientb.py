# Python TCP Client A
import socket 

host = '192.168.1.49' 
port = 63200
BUFFER_SIZE = 2000 
MESSAGE = raw_input("tcpClientA: Enter message/ Enter exit:") 

tcpClientB = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientB.connect((host, port))


while MESSAGE != 'exit':
    tcpClientB.send(MESSAGE.encode())     
    data = tcpClientB.recv(BUFFER_SIZE)
    print " ACK(B): ", data
    MESSAGE = raw_input("tcpClientB: Enter message to continue/ Enter exit: ")

tcpClientB.close() 
