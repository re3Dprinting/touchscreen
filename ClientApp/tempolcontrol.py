"""
Temperature Open-Look Control.
"""

import logging
from enum import Enum

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

        # The extruder index, 0, 1, or bed
        self.index_str = index_str

        # Initialize our state
        self.state = State.unknown

        # Initialize the set-point.
        self.set_point = 0

        # Connect handlers for the pushbutton widgets
        self.w_pushbutton_inc.clicked.connect(self._handle_inc_touch)
        self.w_pushbutton_dec.clicked.connect(self._handle_dec_touch)

        # Update the display to reflect the current state and
        # temperature.
        self._update_display()

    def _log(self, message):
        self._logger.debug(message)

    def _handle_inc_touch(self):
        self._log("UI: User touched Increment.")
        self._change_setpoint_by_amount(1)

    def _handle_dec_touch(self):
        self._log("UI: User touched Decrement.")
        self._change_setpoint_by_amount(-1)

    def _change_setpoint_by_amount(self, amount):
        # Change the set point
        self.set_point += amount

        # Change the state to CHANGED, which indicates that the
        # set-point is temporary until the printer echos that value
        # back to us.
        self.state = State.changed

        # Update the display with the temporary value
        self._update_display()

        # Send the new set-point to the printer
        self.printer_if.set_temperature(self.index_str, self.set_point)

    def _update_display(self):
        if self.state == State.unknown:
            self.w_label.setText("-----")
        elif self.state == State.synced or self.state == State.changed:
            self.w_label.setText(str(self.set_point))

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
