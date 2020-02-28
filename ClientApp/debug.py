import glob
from datetime import datetime

import os.path
import logging
from .basewindow import BaseWindow
from qt.debugwindow import *
from octoprint.util.commandline import CommandlineCaller

from constants import k_logname

class DebugWindow(BaseWindow, Ui_DebugWindow):
    def __init__(self, personality, parent=None):
        super(DebugWindow, self).__init__(parent)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("DebugWindow __init__()")

        # Savepersonality
        self.personality = personality

        # Set up user interface
        self.setupUi(self)
        self.parent = parent

        # Set up callback functions
        self.w_pushbutton_add_marker.clicked.connect(self.handle_add_marker)
        self.w_pushbutton_copy_log.clicked.connect(self.handle_copy_log)
        self.Back.clicked.connect(self.back)

    def handle_add_marker(self):
        self._log("UI: User touched Add Marker")

        message = self.w_lineedit_message.text()

        self._log("******************************************************************************")
        self._log("* User log message <%s>" % message)
        self._log("******************************************************************************")

        self.display("Log marker added.")


    def handle_copy_log(self):
        self._log("UI: User touched Copy Log")

        logpath = self.personality.logpath
        self.display(logpath)

        # If the logpath exists, it must be a directory and it must be writable.
        if os.path.exists(logpath):
            if not os.path.isdir(logpath) or not os.access(logpath, os.W_OK):
                self.display('Cannot write to "%s", logs not written.' % logpath)
        else:
            # It doesn't exist, so create it.
            os.mkdir(logpath)

        # Build up a string to represent the tarball filename, starting with the date.
        now = datetime.now()
        nowstr = now.strftime("%Y-%m-%d-%H-%M-%S")

        # Names will look like ts.log-2020-01-01-12-00-00.tar.
        tarball_filename = "ts.log-" + nowstr + ".tar"
        tarball_path = os.path.join(logpath, tarball_filename)

        # Use globbing to get a list of the logfiles that will go into
        # the tarball.
        logfiles = glob.glob(k_logname + '*')

        # Glob returns an array; turn it into a space-separated string.
        logstring = ' '.join(logfiles)

        # Now build the command.
        command = "tar cvf %s %s" % (tarball_path, logstring)

        # Construct a commandline caller to run the tar command.
        caller = CommandlineCaller()
        caller.on_log_call = self.display_call_stdout
        caller.on_log_stdout = self.display_call_stdout
        caller.on_log_stderr = self.display_stderr

        # Execute the command.
        caller.call(command)

        # Finish off with a message stating that the tarball has been
        # created.
        done_message = "* Done: logs copied to file \"%s\" *" % tarball_filename
        self._log(done_message)
        self.display(done_message)
        self.display("")

    # Display the function call and any lines written to stdout.
    def display_call_stdout(self, *lines):

        # loop through the lines
        for line in lines:
            
            # Strip the CR/LF 
            line = line.strip()

            # Display and log the line
            self.display(line)
            self._log(line)

    # Display some lines written to stderr
    def display_stderr(self, *lines):

        # Loop through the lines
        for line in lines:
            
            # Strip the CR/LF
            line = line.strip()

            # It will sometimes happen (actually, almost every time)
            # that tar will report an error stating that ts.log has
            # changed while tar was trying to write it to the
            # tarball. We will avoid reporting this error to users so
            # as not to confuse people (we expect it to happen, so
            # it's not really an error).

            if 'ts.log: Truncated write; file may have grown while being archived' in line:
                self._log(line)
                continue

            # Display and log the error line
            self.display(line)
            self._log(line)

    # Display a line on the screen
    def display(self, message):
        self.w_message_text.moveCursor(QtGui.QTextCursor.End)
        self.w_message_text.append(message)
