from enum import Enum
# Values to create a rotating log with each file 100 megabytes and
# 10 files for a total of one gigabyte:

class LogConstants(Enum):
    LOGNAME = "ts.log"
    LOGMAXBYTES = 2**30
    LOGCOUNT = 9

class Pages(Enum):
    HOME_PAGE = "home"
    PRINT_PAGE = "print"
    CONTROL_PAGE = "control"
    TEMPERATURE_PAGE = "temperature"
    SETTINGS_PAGE = "settings"
    DEBUG_PAGE = "debug"
    INFO_PAGE = "info"
    SERIAL_PAGE = "serial"
    USERUPDATE_PAGE = "userupdate"
    DUEXSETUP_PAGE = "duexsetup"
