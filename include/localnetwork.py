import socket

def currentIP(server="home"):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    s.connect(('9.9.9.9',53))
    return s.getsockname()[0]

def isConnected(dns="9.9.9.9"):
    try:
        socket.create_connection((dns, 53))
        return True
    except OSError:
        return False