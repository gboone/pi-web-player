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

def isPiHoleConnected(ip):
    return isConnected(ip)

def getPiHoleData(servers):
    piHoles = {}
    for server in servers:
        piHole = servers[server]
        ip = piHole['ip']
        connected = isPiHoleConnected(ip)
        piHoles.append(
            {server: {
                'ip':  ip,
                'connected': connected,
                'hostname': server + ".local"
            }}
        )
    return piHoles