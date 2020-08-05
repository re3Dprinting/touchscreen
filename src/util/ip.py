import socket
import logging
import time

def setup_local_logger(name):
    global logger
    logger = logging.getLogger(name)

def _log(message):
    global logger
    logger.debug(message)

setup_local_logger(__name__)

def get_ip():
    IP = 'unknown'

    for i in range(1, 30):
        _log("Getting IP address, try %d of 10:" % i)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # doesn't even have to be reachable (but we'll use an IP
            # address that we can be sure will require a route that goes
            # through something other than localhost.
            s.connect(('1.1.1.1', 80))

            IP = s.getsockname()[0]

            _log("Returning <%s>" % IP)
            return IP

        except:
            _log("  OOPS: Exception occured")

        finally:
            s.close()

        # Wait a second before trying again
        time.sleep(1.0)

    _log("Returning <%s>" % IP)
    return IP
