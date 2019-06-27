from socket import *
import time
import serial
import serial.tools.list_ports
import gigabotconnection
import sys


host = '192.168.1.49'
baudrate = 250000
port = 3000


if __name__ == "__main__":
	#connect to the server
	gigabotclient= socket(AF_INET,SOCK_STREAM)
	gigabotclient.connect((host,port))
	data = gigabotclient.recv(1024)
	if len(data) > 0:
		print data


	com = list(serial.tools.list_ports.comports())
	for p in com:
		print p.device
		if "/dev/ttyUSB" in p.device:
			com = p.device
	try:
		#open up serial port.
		serialconn = serial.Serial(com, baudrate=baudrate)
	except:
		print "COM port is unavalible/ or run program with root permission."
		exit()

	serialconn.timeout = 1  # set read timeout
	if serialconn.is_open:
		time.sleep(1)
		print("SEND: M155 S5\r")
		serialconn.write('M155 S5\r'.encode('utf-8'))
		gcodedata = gigabotconnection.gcodedata()
		while True:
			insize = serialconn.inWaiting()
			if insize:
				#Once recieved data, wait 50ms for the rest of the data to come in.
				time.sleep(0.05)
				insize = serialconn.inWaiting()
				print(insize)
			 	serial_recv = serialconn.read(insize)
			 	print(serial_recv)
			 	d_serial_recv = serial_recv.decode('utf-8')
			 	gcodedata.parsedata(d_serial_recv)
			 	print(gcodedata.temp)
				#conn.send(giga.temp.encode())

	# conn.close()