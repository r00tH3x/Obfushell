import socket

def check_open_port(host, port):
    """Check if a given port is open on the target host."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, int(port)))
        return True
    except:
        return False

def is_valid_ip(ip):
    """Validate if the provided string is a valid IP address."""
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True
