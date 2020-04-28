import logging
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets


#BaseWindow that is inherited from all windows. 
#Overrides basic functions like close and show
#Implements Fullscreen flags, cleaning up code in the individual windows

class BaseWindow():
	def base_init(self, parent = None):

		# Set up logging
		self._logger = logging.getLogger(__name__)

		self.properties = {}
		config_path = Path(__file__).parent.absolute().__str__() + "/config.properties"
		for line in open(config_path):
			self.properties[line.split("=")[0]] = line.split("=")[1].strip()

		self.fullscreen = False
		self.parent = parent
		self.notification = None
		self.setWindowFlags(self.windowFlags())
		if (parent != None) and (self.parent.fullscreen):
			self.fullscreen = True
			self.setWindowState(self.windowState() | QtCore.Qt.WindowFullScreen)
