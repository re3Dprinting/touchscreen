"""
Temperature Open-Look Control.
"""

import logging
from enum import Enum

from PyQt5.QtCore import QTimer

class TempOLControl:
    """Class to implement open-look control of a heater temperature
    set-point. This class is instantiated with the widgets used to
    control and display the set-point, and the extruder index.
    """
    def __init__(self, context, ui_context, index_str):

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("TemperaturePage __init__")

        # The printer interface
        self.printer_if = context.printer_if

        # The label widget used to display the temperature set
        # point, a PyQt5 QLabel
        self.w_label = ui_context.w_label

        # The pushbutton used to increment the set point, a PyQt5
        # QPushButton
        
        self.w_pushbutton_inc = ui_context.w_pushbutton_inc

        # The pushbutton used to decrement the set point, a PyQt5
        # QPushButton
        self.w_pushbutton_dec = ui_context.w_pushbutton_dec

        # The extruder index string: "tool0", "tool1", or "bed"
        self.index_str = index_str
        self.index = ['bed', 'tool0', 'tool1'].index(index_str)

        # Initialize our state
        self.state = State.unknown

        # Initialize the set-point.
        self.set_point = 0
        self.last_received_setpoint = 0

        # Initialize the operational/not operational state
        self.is_operational = False

        # Connect handlers for the pushbutton widgets
        self.w_pushbutton_inc.pressed.connect(self._handle_inc_press)
        self.w_pushbutton_inc.released.connect(self._handle_inc_release)
        self.w_pushbutton_dec.pressed.connect(self._handle_dec_press)
        self.w_pushbutton_dec.released.connect(self._handle_inc_release)

        # Update the display to reflect the current state and
        # temperature.
        self._update_display()

        ctor = self.printer_if.state_change_connector()
        ctor.register(self._state_change_callback)

        ctor = self.printer_if.temperature_change_connector()
        ctor.register(self._temperature_change_callback)

        # Create the timer object that will be used to implement
        # repeating.
        self.repeat_timer = QTimer()
        self.repeat_timer.timeout.connect(self._handle_button_timeout)

        # And create the time object that will be used to implement
        # the sync timeout
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self._handle_sync_timeout)

    def _log(self, message):
        self._logger.debug(message)

    def _is_operational_state(self, state):
        # This is the equivalent of the OPERATIONAL_STATES tuple found
        # at about line 371 of src/octoprint/util/comm.py.
        if (state == "PRINTING") or \
           (state == "STARTING") or \
           (state == "OPERATIONAL") or \
           (state == "PAUSED") or \
           (state == "CANCELLING") or \
           (state == "PAUSING") or \
           (state == "RESUMING") or \
           (state == "FINISHING") or \
           (state == "TRANSFERING_FILE"):
               return True
        return False
            
    def _state_change_callback(self, from_state, to_state):
        self._log("=========================== new state: %s ===========================" % to_state)
        if self._is_operational_state(to_state):
            self.is_operational = True
        else:
            self.is_operational = False
            self._reset()

    def _temperature_change_callback(self, tuple):
        sub_tuple = tuple[self.index]
        (setpoint, actual) = sub_tuple

        # self._log("setpoint = <%s>, actual = <%s> (state = <%s>)" % (str(setpoint), str(actual), self.state))

        if setpoint is None:
            self._log("Received temperature with invalid setpoint.")
            return

        # If we're in UNKNOWN state, then transition to SYNC state,
        # and the logic below will then track the temperature as if we
        # were already in SYNC state. This can happen if the user
        # starts a print before manually setting a temperature. The
        # new setpoint will come from the Gcode file being printed.
        if self.state == State.unknown:
            self.state = State.synced

        # If we're in CHANGED state, which means that the user has
        # changed the set-point, but we haven't received a temperature
        # message showing the same set-point, then we have to test the
        # just received set-point to see if it's equal to the user
        # entered set-point. If the two are equal, then we're in sync,
        # and we'll change the state to SYNCED.
        if self.state == State.changed:
            if self.set_point == setpoint:
                self._log("New set-point (%d) equals local set-point: entering SYNC state." % setpoint)
                self.state = State.synced

                # The sync timer is running (because its timeout will
                # cause is to reset state if we don't SYNC before
                # then). Now that we have synced, we no longer need
                # the timer, and can stop it.
                self.sync_timer.stop()

        elif self.state == State.synced:
            # While in SYNC state, our set-point will track the
            # printer's set-point even if it's changed by Gcode in the
            # file being printed.
            if self.set_point != setpoint:
                self._log("Received new set-point (%d) while in SYNC stat: tracking new set point." % setpoint)
                self.set_point = setpoint
                self._update_display()

    def _reset(self):
        self.state = State.unknown
        self.set_point = 0
        self._update_display()
        self.repeat_timer.stop()

    def _handle_inc_press(self):
        if not self.is_operational:
            return
        self._log("UI: User pressed Increment.")
        self.change_amount = 1
        self._change_setpoint_by_amount(self.change_amount)
        self.repeat_timer.start(500)

    def _handle_inc_release(self):
        if not self.is_operational:
            return
        self._log("UI: User released Increment.")
        self._send_setpoint()
        self.repeat_timer.stop()

    def _handle_dec_press(self):
        if not self.is_operational:
            return
        self._log("UI: User pressed Decrement.")
        self.change_amount = -1
        self._change_setpoint_by_amount(self.change_amount)
        self.repeat_timer.start(500)

    def _handle_dec_release(self):
        if not self.is_operational:
            return
        self._log("UI: User released Decrement.")
        self._send_setpoint()
        self.repeat_timer.stop()

    def _handle_button_timeout(self):
        if not self.is_operational:
            return
        self._change_setpoint_by_amount(self.change_amount)
        self.repeat_timer.start(20)
        pass

    def _handle_sync_timeout(self):
        # We're in CHANGED state, but we have not received a set-point
        # from the printer that's equal to ours. We will revert our
        # set-point to the last received from the printer and go to
        # SYNCED state.
        self._log("Sync TIMEOUT has occurred in state = %s" % self.state)

        if self.state == State.changed:
            self.state = State.synced
            self.set_point = self.last_received_setpoint
            self._log("Timed out in CHANGED state. Reverting to sync last received set-point (%d)." % self.set_point)
            self._update_display()
        self.sync_timer.stop()

    def _change_setpoint_by_amount(self, amount):
        # Change the set point
        self.set_point += amount

        # Change the state to CHANGED, which indicates that the
        # set-point is temporary until the printer echos that value
        # back to us.
        self.state = State.changed

        # Update the display with the temporary value
        self._update_display()

    def set_setpoint(self, value):
        self.set_point = value
        self.state = State.changed
        self._update_display()
        self._send_setpoint()

    def _send_setpoint(self):
        # Send the new set-point to the printer
        self._log("Sending setpoint <%s> to <%d>." % (self.index_str, self.set_point))
        self.printer_if.set_temperature(self.index_str, self.set_point)
        self.sync_timer.start(10000)

    def _update_display(self):
        if self.state == State.unknown:
            self.w_label.setText("-----")
        elif self.state == State.synced or self.state == State.changed:
            self.w_label.setText(str(int(self.set_point)))

class TempUIContext:
    """The widgets necessary for open-loop control.
    """
    def __init__(self, w_label, w_pushbutton_dec, w_pushbutton_inc):
        self.w_label = w_label
        self.w_pushbutton_dec = w_pushbutton_dec
        self.w_pushbutton_inc = w_pushbutton_inc

class State(Enum):
    """Class to track the various status of the TempOLControl"""
    unknown = 0                 # We don't know what the set-point is.

    synced = 1                  # We've received the set-point from
                                # the printer and are displaying it.

    changed = 2                 # The user has changed the set-point,
                                # but we have not received the
                                # corresponding temperature set-point
                                # from the printer.
