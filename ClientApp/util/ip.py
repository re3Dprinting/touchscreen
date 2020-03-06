import socket

def get_ip():
    IP = 'unknown'

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # doesn't even have to be reachable (but we'll use an IP
        # address that we can be sure will require a route that goes
        # through something other than localhost.
        s.connect(('1.1.1.1', 80))

        IP = s.getsockname()[0]

    except:
        IP = '127.0.0.1'

    finally:
        s.close()

    return IP
