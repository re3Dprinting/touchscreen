# Dummy comment - delete me.
# Delete me too
import sys, traceback
import re
import pprint
import logging

from octoprint.printer.standard import PrinterCallback
import octoprint.events
from octoprint.util.comm import MachineCom

position_regex = re.compile("x:([0-9]+\.[0-9]+) y:([0-9]+\.[0-9]+) z:([0-9]+\.[0-9]+)", re.IGNORECASE)
runout_message_regex = re.compile("echo:(R[0-9]+) (.*)")

class PrinterIF(PrinterCallback):
    def __init__(self, printer):

        # Keep a reference to the OctoPrint printer object and register to receive callbacks
        # from it.
        self.printer = printer
        self.printer.register_callback(self)

        # Set up logging
        self._logger = logging.getLogger(__name__)
        self._log("PrinterIF starting up")

        # Were not received the SD file list or doing an SD print
        self.state_getting_sd_list = False
        self.printing_from_sd = False

        # Null out all our callbacks.
        self.temperature_callback = None
        self.printer_state_callback = None
        self.position_callback = None
        self.printer_state_change_callback = None
        self.printer_progress_callback = None
        self.runout_callback = None
        self.file_list_update_callback = None
        self.print_finished_callback = None

        # Subscribe to printer state change events so we know what state the OctoPrint
        # printer is in at all times.
        self.event_manager = octoprint.events.eventManager()
        self.event_manager.subscribe(octoprint.events.Events.PRINTER_STATE_CHANGED, self.cb_printer_state_changed)

        # Set default values
        self.file_name = ""
        self.feed_rate = 100
        self.flow_rate = 100

        # We don't know where the print head is or has been.
        self.last_known_position = None

        # The maximum number of M114 commands to send to the printer
        self.M114_QUEUE_LIMIT = 2

        # The number of M114 commands we have sent to the printer
        # without a response.
        self.m114_sent_count = 0

        # A pretty-printer for diagnostic use.
        self.pp = pprint.PrettyPrinter(indent=4)

    def printer(self):
        return self.printer

    def _log(self, message):
        self._logger.debug(message)

    def get_connection_options(self):

        # Ask the printer to scan the ports and return those it thinks
        # are suitable for a printer to be on.
        options_dict = self.printer.get_connection_options()

        # Get just the list of available ports and return it.
        ports = options_dict["ports"]
        return ports
    
    def connect(self, device):
        # print("CONNECT to device <%s>." % (device))
        # Connect to the specified device using the default Gigabot bit rate.
        self.printer.connect(device, 250000)
        # self.printer.connect(device, 115200)

    def disconnect(self):
        # Disconnect
        self.printer.disconnect()

    def set_feed_rate(self, rate):
        # Record the specified feed rate and send it to the printer.
        self.feed_rate = rate
        self.printer.feed_rate(rate)

    def set_flow_rate(self, rate):
        # Record the specified flow rate and send it to the printer.
        self.flow_rate = rate
        self.printer.flow_rate(rate)

    def set_babystep(self, value):
        babystep_command = "M290 P0 Z" + str(value)
        print("BABYSTEP command", babystep_command)
        self.printer.commands(babystep_command)
        # self.tempwindow.serial.send_serial("M290 Z " + str(self.babystep))        

    def send_acknowledgement(self):
        # Send an M108 acknowledgement to the printer. This is how we respond to prompts
        # during filament change.
        self.printer.commands("M108")

    def fans_on(self):
        self.printer.commands("M106 S0")
        
    def fans_off(self):
        self.printer.commands("M106 S255")

    def homexy(self):
        self.printer.commands('G28 XY')

    def homez(self):
        self.printer.commands("G28 Z")

    def homeall(self):
        self.printer.commands("G28")

    def relative_positioning(self):
        # self.parent.serial.send_serial('G91')
        self.printer.commands("G91")

    def commands(self, command, force=False):
        self.printer.commands(command, force=force)

    def release_sd_card(self):
        self.printer.commands("M22")

    def init_sd_card(self):
        self.printer.commands("M21")

    def list_sd_card(self):
        self.printer.commands("M20")

    def select_sd_file(self, filename):
        self.file_name = filename
        self.printing_from_sd = True
        self.printer.select_file(filename, True, True)

    def start_print(self):
        # self.printer.start_print()
        pass

    def select_local_file(self, filename):
        self.file_name = filename
        self.printing_from_sd = False
        self.printer.select_file(filename, False, True)

    def cancel_printing(self):
        self.printer.cancel_print()

    def pause_print(self):
        if self.printing_from_sd:
            self.printer.pause_print()
            return

        # Record the last known position as the position to move back
        # to when we resume the print. This is necessary because the
        # park command below (G27) will move the print head and we
        # need to be able to move it back before resuming.
        self.resume_position = self.last_known_position

        # Pause the print...
        self.printer.pause_print()

        # ...and park the print head.
        self.printer.commands("G27")

    def resume_print(self):
        if self.printing_from_sd:
            self.printer.resume_print()
            return

        # Set positioning back to absolute. If the control screen was
        # used to move the print head, then the printer will be in
        # relative mode. We need to set it back to absolute mode
        # before printing resumes.
        self.printer.commands("G90")

        # We also need to undo the homing (G27) when we paused. We do
        # this by moving back to the last known position.
        if self.resume_position is not None:
            resume_pos_str = "G1 X%.3f Y%.3f Z%.3f" % self.resume_position
            print("Sending resume-position <%s>" % resume_pos_str)
            self.printer.commands(resume_pos_str)

        # And now we can resume the print.
        self.printer.resume_print()

    def get_current_temperatures(self):
        return self.printer.get_current_temperatures()

    def set_temperature(self, name, temp):
        self.printer.set_temperature(name, temp)
        
    def set_printer_state_callback(self, callback):
        self.printer_state_callback = callback
        
    def set_temperature_callback(self, callback):
        # Save the provided object as a temperature callback. NOTE:
        # must implement the update_temperature(self, data) function.
        self.temperature_callback = callback

    def set_runout_callback(self, calback):
        self.runout_callback = callback

    ### PrinterCallback stuff:

    show_add_log = False
    show_add_message = False
    show_add_temperature = False
    show_receive_registered_message = False
    show_send_current_data = False

    def on_printer_add_log(self, data):
        if self.show_add_log:
            # By definition, these are already in the log, so we don't log them again (but
            # we might want to print them out.)
            print("*** PRINTER ADD LOG: <%s>" % data)

    def on_printer_add_message(self, data):
        # This is a callback message from the OctoPrint printer object. We handle messages
        # depending upon their contents.

        # If we're configured to show these messages, do so now.
        if self.show_add_message:
            if data.startswith("echo:"):
                print("Printer add message: <%s>" % data)

        # Determine whether the message contains a filament-change
        # message
        match = runout_message_regex.match(data)
        # self._log("Matched in <%s>" % data)

        # If it does contain a match...
        if match:

            # Extract the code and text from the message
            code = match.group(1)
            text = match.group(2)
            self._log("Match groups 1:<%s>, 2:<%s>." % (code, text))

            # If a callback is set up for filament-change messages, call it now.
            if self.runout_callback is not None:
                self._log("We have callback, calling...")
                self.runout_callback.handle_runout_message(code, text)

        # Determine whether the message contains position data.
        match = position_regex.match(data)

        # If so, extract and display it...
        if match:

            # First, reset the M114 counter. This indicates that we're
            # getting data from the printer.
            self.m114_sent_count = 0

            # Now extract each of the x, y, z positions using the
            # regex groups that matched them.
            x = match.group(1)
            y = match.group(2)
            z = match.group(3)

            # Save the last known position. We'll use this in resuming
            # a print.
            self.last_known_position = (float(x), float(y), float(z))

            # And, if there's a callback, call it now.
            if self.position_callback is not None:
                self.position_callback.update_position(x, y, z)

        # Track incoming messages that list the files on the SD card
        # in responds to an M20 command.

        message = data.lower()
        if message == "begin file list":
            self.getting_sd_file_list = True
        elif message == "end file list":
            if self.getting_sd_file_list:
                if self.file_list_update_callback is not None:
                    sd_file_list = self.printer.get_sd_files()
                    self.getting_sd_file_list = False
                    # print("?CALLING CALLBACK?")
                    self.file_list_update_callback(sd_file_list)
            else:
                print("*** UNEXPECTED end of file list received")
        
    def on_printer_add_temperature(self, data):
      try:
        if self.show_add_temperature:
            print("*** ADD TEMPERATURE:")
            self.pp.pprint(data)
            
        # If a temperature callback has been registered, call it now.
        if self.temperature_callback is not None:
            self.temperature_callback.update_temperatures(data)

        # Because this is a convenient place to do it, send an M114 to
        # cause the printer to send us its position... BUT don't queue
        # up too many. The count is reset when we receive the next
        # position data.
        # print("B Sent count =", self.m114_sent_count)

        if (self.m114_sent_count < self.M114_QUEUE_LIMIT):
            # self.printer.commands("M114")
            self.m114_sent_count += 1
        else:
            state_string = self.printer.get_state_string()
            if state_string == "Operational":
                self.printer.fake_ack()
      except Exception as e:
          print("SOMETHING IS WRONG")
          traceback.print_exc()
          
                

    def on_printer_received_registered_message(name, output):
        if self.show_receive_registered_message:
            print("REGISTERED MESSAGE: <%s> - <%s>" % (name, output))

    def on_printer_send_current_data(self, data):

        if self.show_send_current_data:
            print("PRINTER SEND CURRENT DATA:")
            self.pp.pprint(data)
        
        try:
            progress = data["progress"]

            if progress is not None:
                # self.pp.pprint(progress)
        
                completion = progress["completion"]

                if completion is None:
                    completion = "N/A"

                print_time_left = progress["printTimeLeft"]

                if print_time_left is None:
                    print_time_left = "N/A"

                # print("Percent done: %s, Estimated time remaining: %s" % (completion, print_time_left))

                if self.printer_state_change_callback is not None:
                    self.printer_state_change_callback.update_printer_state(data)

                if self.printer_progress_callback is not None:
                    self.printer_progress_callback.update_progress(completion, print_time_left)

        except Exception as e:
            print("SOMETHING IS WRONG")
            traceback.print_exc()

            
    def on_printer_send_initial_data(self, data):
        print("*** INITIAL DATA:")
        self.pp.pprint(data)

    ### Event stuff:

    _printer_state_finishing = "FINISHING"
    _printer_state_operational = "OPERATIONAL"
    _printer_state = None
    
    def cb_printer_state_changed (self, event, payload):
        # pre = "####"
        # print("%s Received event: %s (Payload: %r)" % (pre, event, payload))

        if payload['state_id'] == self._printer_state_finishing:
            # print("******** FINISHING")
            self._printer_state = self._printer_state_finishing

        if payload['state_id'] == self._printer_state_finishing:
            # print("******** OPERATIONAL")
            if self._printer_state == self._printer_state_finishing:
                if self.print_finished_callback is not None:
                    # print("Transition from finishing to operational, do print-finished stuff.")
                    self.print_finished_callback()
        
    def set_file_list_update_callback(self, callback):
        self.file_list_update_callback = callback

    def set_print_finished_callback(self, callback):
        # print("Saving print finished callback")
        self.print_finished_callback = callback

    def set_position_callback(self, callback):
        self.position_callback = callback

    def set_progress_callback(self, callback):
        self.printer_progress_callback = callback

    def set_runout_callback(self, callback):
        self.runout_callback = callback
        
