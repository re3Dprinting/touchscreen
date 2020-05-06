import logging
import os
import json
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets


#BaseWindow that is inherited from all windows. 
#Overrides basic functions like close and show
#Implements Fullscreen flags, cleaning up code in the individual windows

class BaseWindow():
	def base_init(self, parent = None):

		# Set up logging
		self._logger = logging.getLogger(__name__)

		# #Load the properties from the config.properties file.
		# #Preload the expected values and update the values from the the json file. 
		# self.properties = {"name": "", 
                # "motherboard" : "", 
                # "wifissd" : "",
                # "wifipassword" : "",
                # "permission" : ""
                # }
		# tmp_path = Path(__file__).parent.absolute()
		# config_path = Path(os.path.realpath(tmp_path)).parent.parent.__str__()+ "/config.properties"
		# if(Path(config_path).is_file()):
		# 	with open(config_path) as config_in:
		# 		load_properties = json.load(config_in)
		# 		self.properties = {**self.properties, **load_properties}
		# else:
		# 	self._log("Please create a config.properties file within the same directory as Octoprint and Touchscreen!")

		self.fullscreen = False
		self.parent = parent
		self.notification = None
		self.setWindowFlags(self.windowFlags())
		if (parent != None) and (self.parent.fullscreen):
			self.fullscreen = True
			self.setWindowState(self.windowState() | QtCore.Qt.WindowFullScreen)
