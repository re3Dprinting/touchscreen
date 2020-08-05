class Context():
    """
    The Context object is a singlton object that holds reference to resources that all windows can access
    """
    def __init__(self, printer_if, personality, ui_controller, properties):
        """
        Initializes the context object with the printer instance, personality object, UI instance, and the project properties.

        Arguments:
            printer_if {[type]} -- Printerif is the printer interface wrapper class around Octoprint's printer class. All interactions with the printer go through this object.
            personality {[type]} -- Personality object that sets up the paths of the project directory depending on the machine that the application is running on.
            ui_controller {[type]} -- static UI instance
            properties {[type]} -- Project properties object, holding the board type, permission level, and wifi configuration. 
        """
        self.printer_if = printer_if
        self.personality = personality
        self.ui_controller = ui_controller
        self.properties = properties
