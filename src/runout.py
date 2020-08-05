import logging
from PyQt5.QtCore import Qt, pyqtSignal
from popup import PopUp

class RunOut(PopUp):
    runout_signal = pyqtSignal(str, str)

    def __init__(self, parent, printer_if):
        super(RunOut, self).__init__(parent)
        self._logger = logging.getLogger(__name__)
        self._log_d("Runout __init__()")

        self.popup_button.setEnabled(False)
        self.printer_if = printer_if

        self.runout_signal.connect(self.runout_handler_slot)
        self.hide_on_ok = False
        self.send_m108_on_ok = False

        self.popup_button.clicked.connect(self.accept)

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

            # We have to activate the parent window to ensure it will
            # receive keyboard focus again.
            self.parent.activateWindow()
            self.parent.setWindowState(Qt.WindowActive)

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
        self.popup_button.setEnabled(False)

    # Enable the OK button so the user may click it.
    def enable_ok(self):
        self.popup_button.setEnabled(True)

    # This method is called by the PrinterIF when it recognizes a
    # filament-change message coming from Marlin on the printer. This
    # typically happens on filament run-out, but can also be embedded
    # in the job's gcode.
    # This method runs in the printer thread; emit a signal so we can
    # handle the message in the UI thread.
    def handle_runout_message(self, code, mess):
        self._log_d("Received runout message <%s>, <%s>, sending signal..." % (code, mess))
        self.runout_signal.emit(code, mess)

    # Slot called when the filament-change signal emits a message. We
    # expect two strings: on with the message code (Rxxx) and one with
    # the message ("Insert filament and press button to continue").

    # Note that in some cases we override the default message with one
    # that makes more sense for a touchscreen
    def runout_handler_slot(self, code, mess):
        self._log_d("Received runout signal <%s>, <%s>, handling..." % (code, mess))

        # "Wait for start of the filament change."
        if code == "R301":
            self.disable_ok()
            self.send_m108_on_ok = False

        # Insert filament and press button to continue."
        elif code == "R302":
            self.enable_ok()
            self.send_m108_on_ok = True

        # Press button to heat nozzle."
        elif code == "R303":
            self.enable_ok()
            self.send_m108_on_ok = True

        # Heating nozzle, please wait...
        elif code == "R304":
            self.disable_ok()
            self.send_m108_on_ok = False

        # Wait for filament change."
        elif code == "R305":
            self.disable_ok()
            self.send_m108_on_ok = False

        # Press button to continue.
        elif code == "R306":
            self.enable_ok()
            self.send_m108_on_ok = True

        # Wait for print to resume.
        elif code == "R307":
            self.hide_on_ok = True

        # Make sure the dialog box is showing.
        self.popup_title = "Filament Change"
        self.popup_message.setText(mess)
        self.show()
