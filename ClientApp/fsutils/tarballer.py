import glob
from datetime import datetime
import os.path

from PyQt5.QtCore import QRunnable, QThreadPool
                         
from octoprint.util.commandline import CommandlineCaller
from constants import LogConstants
from fsutils.mountfinder import MountFinder

import logging

class Tarballer(QRunnable):
    def __init__(self, proxy, personality):
        super(QRunnable, self).__init__()

        self.proxy = proxy
        self.personality = personality
        
        self._logger = logging.getLogger(__name__)
        self._log("DebugWindow __init__()")

    def do_copy_log(self):
        QThreadPool.globalInstance().start(self)

    def run(self):
        self._do_copy_log()

    def display(self, message):
        self.proxy.signal_display(message)

    def _log(self, message):
        self._logger.debug(message)

    def build_tarball_filename(self):
            # Build up a string to represent the tarball filename, starting with the date.
        now = datetime.now()
        nowstr = now.strftime("%Y-%m-%d-%H-%M-%S")

        # Names will look like ts.log-2020-01-01-12-00-00.tar.
        tarball_filename = "ts.log-" + nowstr + ".tar"

        return tarball_filename
    
    def get_log_file_names(self):
        # Use globbing to get a list of the logfiles that will go into
        # the tarball.
        logfiles = glob.glob(LogConstants.LOGNAME + '*')

        # Glob returns an array; turn it into a space-separated string.
        logstring = ' '.join(logfiles)

        return logstring

    def get_local_logpath(self):
        logpath = self.personality.logpath

        # If the logpath exists, it must be a directory and it must be writable.
        if os.path.exists(logpath):

            # We have to ensure that it's a writable directory
            if not os.path.isdir(logpath) or not os.access(logpath, os.W_OK):

                self.display('Cannot write to "%s", logs not written.' % logpath)
                self._log('Cannot write to "%s", logs not written.' % logpath)

                return None
        else:
            # It doesn't exist, so create it.
            self._log("Creating <%s>" % logpath)
            os.mkdir(logpath)

        return logpath

    def find_logpath(self):
        # The first thing we're going to look for is a USB drive. If
        # we don't find one, we'll copy the log files to a local
        # directory.

        paths = MountFinder.thumbdrive_candidates()

        if len(paths) == 0:
            self._log("(!) Could not find USB drive, copying log files to local path.")
            self.display("(!) Could not find USB drive, copying log files to local path.")

            return self.get_local_logpath()

        # Return the first USB mountpoint found
        return paths[0]

    def _do_copy_log(self):

        # Get the name of the tarball we're going to copy the log
        # files to.
        tarball_filename = self.build_tarball_filename()
        self._log("tarball = <%s>" % tarball_filename)

        # Get the location where we're going to save the tarball.
        logpath = self.find_logpath()
        self._log("logpath = <%s>" % logpath)

        # Build the full path to the tarball
        tarball_path = os.path.join(logpath, tarball_filename)
        self._log("tarball_path = <%s>" % tarball_path)

        # Get the names of the log files
        logfiles = self.get_log_file_names()
        self._log("logfiles = <%s>" % logfiles)

        # Now build the command.
        command = "tar cvf %s %s" % (tarball_path, logfiles)
        self._log("command = <%s>" % command)

        # Construct a commandline caller to run the tar command.
        caller = CommandlineCaller()
        caller.on_log_call = self.display_call_stdout
        caller.on_log_stdout = self.display_call_stdout
        caller.on_log_stderr = self.display_stderr

        # Execute the command.
        self.display("")
        caller.call(command)

        # Finish off with a message stating that the tarball has been
        # created.
        done_message = "Logs copied to file \"%s\"" % tarball_path
        self._log(done_message)
        self.display("\n" + done_message)
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

            if 'ts.log: Truncated write; file may have grown while being archived' in line or 'file changed as we read it' in line:
               self._log(line)
               continue

            # Display and log the error line
            self.display(line)
            self._log(line)

