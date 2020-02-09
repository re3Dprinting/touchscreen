import time
import serial
import serial.tools.list_ports
from Client.g_serial import *
from Client.g_client import *
from Client.g_data import *

from touchdisplay import *
from watchdogthread import *
from personality import Personality

from pathlib import Path

import sys
import threading
import shutil
import os

if __name__ == "__main__":

    data_thread = g_data()
    client_conn = g_client(data_thread)
    serial_conn = g_serial(data_thread)
    data_thread.start()

#   Remove the broken refs/tags
    if(os.path.isdir(Path(__file__).resolve().parents[1].__str__()+"/.git/refs/tags")):
        shutil.rmtree(Path(__file__).resolve().parents[1].__str__()+"/.git/refs/tags")

    personality = Personality(True, "/media/pi", "/home/pi/localgcode")

    app = QtWidgets.QApplication(sys.argv)

    properties = {}
    for line in open("config.properties"):
        properties[line.split("=")[0]] = line.split("=")[1].strip()

    app.setApplicationName(properties["name"])
    app.setApplicationVersion(properties["version"])

    display = TouchDisplay(client_conn, serial_conn, personality)
    display.show()
    jt_thread = WatchdogThread(display.print_pop, personality.watchpoint)
    jt_thread.start()
    app.exec_()