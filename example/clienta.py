# Python TCP Client A
import socket 

host = '192.168.1.49' 
port = 6677 
BUFFER_SIZE = 2000 
MESSAGE = raw_input("tcpClientA: Enter message/ Enter exit:") 

tcpClientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpClientA.connect((host, port))


while MESSAGE != 'exit':
    tcpClientA.send(MESSAGE.encode())     
    data = tcpClientA.recv(BUFFER_SIZE)
    print " ACK(A): ", data
    MESSAGE = raw_input("tcpClientA: Enter message to continue/ Enter exit: ")

tcpClientA.close() 