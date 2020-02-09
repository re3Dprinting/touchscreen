import time
import serial
import serial.tools.list_ports

from PyQt5 import QtWidgets

from ClientApp.Client.g_serial import g_serial
from ClientApp.Client.g_client import g_client
from ClientApp.Client.g_data import g_data

from ClientApp.touchdisplay import TouchDisplay
from ClientApp.watchdogthread import WatchdogThread
from ClientApp.personality import Personality

import sys
import threading
import os

if __name__ == "__main__":

    data_thread = g_data()
    client_conn = g_client(data_thread)
    serial_conn = g_serial(data_thread)
    data_thread.start()

    persona = Personality(False, "/Volumes", "/Users/jct/localgcode")

    app = QtWidgets.QApplication(sys.argv)
    display = TouchDisplay(client_conn, serial_conn, persona)
    display.show()
    jt_thread = WatchdogThread(display.print_pop, persona.watchpoint)
    jt_thread.start()
    app.exec_()
