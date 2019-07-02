from socket import *
import time
import serial
import serial.tools.list_ports
import gigabotconnection
import sys
import json

host = '192.168.1.49'
baudrate = 250000
port = 63200

def connecttocom():
	com = list(serial.tools.list_ports.comports())
	for p in com:
		print p.device
		if "/dev/ttyUSB" in p.device:
			com = p.device
	try:
		#open up serial port.
		serconn = serial.Serial(com, baudrate=baudrate)
		serconn.timeout = 1 # set serial read timeout
		return serconn
	except:
		print "COM port is unavalible/ or run program with root permission."
		exit()

def extractheader(client, conn, serdata):
	insiz = conn.inWaiting()
	if insiz: time.sleep(0.5)
	insiz = conn.inWaiting()
	serdata.parsedata(insiz, conn.read(insiz).decode("utf-8"))
	client.send((serdata.uploaddate + "|" + serdata.model).encode("base64"))



if __name__ == "__main__":
	#connect to the server
	gigabotclient= socket(AF_INET,SOCK_STREAM)
	gigabotclient.connect((host,port))
	data = gigabotclient.recv(1024)
	while(len(data) == 0): #Wait for the Connected transmission
		data = gigabotclient.recv(1024)
	print(data)

	#connect to the serial device
	serialconn = connecttocom() 

	if serialconn.is_open:
		time.sleep(1)
		print("SEND: M155 S5\r")
		#send to serial a M155 code to enable temperture reportings every 5s
		serialconn.write('M155 S5\r'.encode('utf-8'))
		time.sleep(1)
		#create new serial data object. 
		serial_data = gigabotconnection.serialdata()

		extractheader(gigabotclient, serialconn, serial_data)

		while True:
			try:
				insize = serialconn.inWaiting()
				if insize:
					#Once recieved data, wait 50ms for the rest of the data to come in.
					time.sleep(0.05)
					insize = serialconn.inWaiting()
					
					print(insize)
				 	serial_recv = serialconn.read(insize)
				 	print(serial_recv)
				 	d_serial_recv = serial_recv.decode('utf-8')
				 	serial_data.parsedata(insize, d_serial_recv)


					t = json.dumps(serial_data.temp).encode("base64")
				 	print(serial_data.temp)
					gigabotclient.send(t)
			except IOError:
				print "Device Disconnected!\n"
				break
	print "program ended"

	# conn.close()
