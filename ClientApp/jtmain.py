import time
import serial
import serial.tools.list_ports
from Client.g_serial import *
from Client.g_client import *
from Client.g_data import *

from touchdisplay import *

import sys
import threading
import os

if __name__ == "__main__":

    data_thread = g_data()
    client_conn = g_client(data_thread)
    serial_conn = g_serial(data_thread)
    data_thread.start()

    app = QtWidgets.QApplication(sys.argv)
    display = TouchDisplay(client_conn, serial_conn, False)
    display.show()
    app.exec_()
