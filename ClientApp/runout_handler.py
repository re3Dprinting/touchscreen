import logging
from PyQt5.QtCore import Qt, pyqtSignal
from .qt.runout import *

class RunoutHandlerDialog(QtWidgets.QWidget, Ui_WRunoutDialog):
    runout_signal = pyqtSignal(str, str)

    def __init__(self, parent, printer_if):
        super(RunoutHandlerDialog, self).__init__()
        self._logger = logging.getLogger("re3D.runout_handler")
        self._log("Runout handler starting up")

        self.setupUi(self)
        self.w_buttonBox.setEnabled(False)
        self.printer_if = printer_if
        self.printer_if.set_runout_callback(self)
        self.runout_signal.connect(self.runout_handler_slot)
        self.hide_on_ok = False
        self.send_m108_on_ok = False

    def _log(self, message):
        self._logger.debug(message)

    # Called when the user clicks OK:
    def accept(self):

        # If the filament change phase we're handling requires a
        # response to be sent to Marlin do it here.
        if self.send_m108_on_ok:
            self.printer_if.send_acknowledgement()
            self.send_m108_on_ok = False

        # If this is the last message we expect to handle, hide the
        # dialog.
        if self.hide_on_ok:
            self.hide()

    # Called when the user clicks Cancel; we have no cancel button,
    # but the UI code seems to expect a reject function anyway.
    def reject(self):
        pass

    # Close() is a superclass method that will hide the dialog when
    # the user presses a dialog button. We override it here because we
    # don't always want to hide the dialog; if we don't override this,
    # we show the dialog again at the next filament-change message,
    # but that causes the UI to flash. By doing nothing on close(), we
    # avoid that flash.
    def close(self):
        pass

    # There are some phases of the filament change handling where
    # we're not expecting any input from the user (phases where the
    # dialog is just notifying the user what's happening). In those
    # phases, disable the OK button.
    def disable_ok(self):
        self.w_buttonBox.setEnabled(False)

    # Enable the OK button so the user may click it.
    def enable_ok(self):
        self.w_buttonBox.setEnabled(True)

    # This method is called by the PrinterIF when it recognizes a
    # filament-change message coming from Marlin on the printer. This
    # typically happens on filament run-out, but can also be embedded
    # in the job's gcode.
    # This method runs in the printer thread; emit a signal so we can
    # handle the message in the UI thread.
    def handle_runout_message(self, code, mess):
        self._log("Received runout message <%s>, <%s>, sending signal..." % (code, mess))
        self.runout_signal.emit(code, mess)

    # Slot called when the filament-change signal emits a message. We
    # expect two strings: on with the message code (Rxxx) and one with
    # the message ("Insert filament and press button to continue").

    # Note that in some cases we override the default message with one
    # that makes more sense for a touchscreen
    def runout_handler_slot(self, code, mess):
        self._log("Received runout signal <%s>, <%s>, handling..." % (code, mess))

        # "Wait for start of the filament change."
        if code == "R301":
            self.disable_ok()
            self.send_m108_on_ok = False
            # mess = "Filament change beginning; please wait..."

        # Insert filament and press button to continue."
        elif code == "R302":
            self.enable_ok()
            self.send_m108_on_ok = True
            # mess = "Insert filament and touch OK to continue."

        # Press button to heat nozzle."
        elif code == "R303":
            self.enable_ok()
            self.send_m108_on_ok = True
            # mess = "Nozzle cooldown in progress. Touch OK to heat nozzle."

        # Heating nozzle, please wait...
        elif code == "R304":
            self.disable_ok()
            self.send_m108_on_ok = False

        # Wait for filament change."
        elif code == "R305":
            self.disable_ok()
            self.send_m108_on_ok = False
            # mess = "Filament purge in progress. Please wait..."

        # Press button to continue.
        elif code == "R306":
            self.enable_ok()
            self.send_m108_on_ok = True
            # mess = "Touch OK to continue..."

        # Wait for print to resume.
        elif code == "R307":
            self.hide_on_ok = True
            # mess = "Print resuming. Touch OK."

        # Make sure the dialog box is showing.
        self.w_runout_message_label.setText(mess)
        self.show()
