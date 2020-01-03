from octoprint.printer.standard import PrinterCallback
import octoprint.events
from octoprint.util.comm import MachineCom

class PrinterIF(PrinterCallback):
    def __init__(self, printer):
        self.printer = printer
        self.printer.register_callback(self)
        self.state_getting_sd_list = False

        self.temperature_callback = None
        self.printer_state_callback = None

        self.file_list_update_callback = None
        self.print_finished_callback = None

        self.event_manager = octoprint.events.eventManager()
        self.event_manager.subscribe(octoprint.events.Events.PRINTER_STATE_CHANGED, self.cb_printer_state_changed)

        self.file_name = ""
        self.feed_rate = 100
        self.flow_rate = 100

    def printer(self):
        return self.printer

    def get_connection_options(self):

        # Ask the printer to scan the ports and return those it thinks
        # are suitable for a printer to be on.
        options_dict = self.printer.get_connection_options()

        # Get just the list of available ports and return it.
        ports = options_dict["ports"]
        return ports
    
    def connect(self, device):
        # print("CONNECT to device <%s>." % (device))
        # self.printer.connect(device, 115200)
        self.printer.connect(device, 250000)

    def disconnect(self):
        self.printer.disconnect()

    def set_feed_rate(self, rate):
        self.feed_rate = rate
        printer.feed_rate(rate)

    def set_flow_rate(self, rate):
        self.flow_rate = rate
        printer.flow_rate(rate)
        
    def fans_on(self):
        self.printer.commands("M106 S0")

        
    def fans_off(self):
        self.printer.commands("M106 S255")

    def homexy(self):
        self.printer.commands('G28 XY')

    def homez(self):
        self.printer.commands("G28 z")

    def homeall(self):
        self.printer.commands("G28")

    def relative_positioning(self):
        # self.parent.serial.send_serial('G91')
        self.printer.commands("G91")

    def commands(self, command):
        self.printer.commands(command)

    def release_sd_card(self):
        self.printer.commands("M22")

    def init_sd_card(self):
        self.printer.commands("M21")

    def list_sd_card(self):
        self.printer.commands("M20")

    def select_sd_file(self, filename):
        self.file_name = filename
        self.printer.select_file(filename, True, True)

    def start_print(self):
        # self.printer.start_print()
        pass

    def cancel_printing(self):
        self.printer.cancel_print()

    def pause_print(self):
        self.printer.pause_print()

    def resume_print(self):
        self.printer.resume_print()

    def get_current_temperatures(self):
        return self.printer.get_current_temperatures()

    ### PrinterCallback stuff:

    def on_printer_add_temperature(self, data):

        # If a temperature callback has been registered, call it now.
        if self.temperature_callback is not None:
            self.temperature_callback.update_temperatures(data)
        else:
            print("No callback")
        
    def set_temperature_callback(self, callback):
        # Save the provided object as a temperature callback. NOTE:
        # must implement the update_temperature(self, data) function.
        self.temperature_callback = callback

    def set_temperature(self, name, temp):
        self.printer.set_temperature(name, temp)

    def on_printer_send_current_data(self, data):
        if self.printer_state_change_callback is not None:
            self.printer_state_change_callback.update_printer_stat(data)
        
    def set_printer_state_callback(self, callback):
        self.printer_state_callback = callback

    def on_printer_add_message(self, data):
        if type(data) is str:
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
