import serial
import time
import serial.tools.list_ports

baudrate = 250000
port = '/dev/ttyUSB0'  # set the correct port before run it

# com = list(serial.tools.list_ports.comports())
# for p in com:
# 	print p

gigabot = serial.Serial(port=port, baudrate=baudrate)
gigabot.timeout = 1  # set read timeout
#gigabot.write('G28 X \n\r')
print (gigabot.is_open)  # True for opened
if gigabot.is_open:
	time.sleep(3)
	gigabot.write('M155 S5\r'.encode('utf-8'))
	while True:
		insize = gigabot.inWaiting()
		if insize:
			data = gigabot.read(insize)
			print (data)
		    #print ('...')
		#gigabot.write('M105\r'.encode('utf-8'))
		time.sleep(0.05)
else:
    print ('gigabot not open')
# z1serial.close()  # close z1serial if z1serial is open.
