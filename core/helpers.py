import socket
import time
import random

def check_open_port(host, port):
    """Check if port is open with latency."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)  
    try:
        start_time = time.time()
        s.connect((host, int(port)))
        latency = (time.time() - start_time) * 1000
        s.close()
        return True, latency
    except:
        return False, None

def scan_ports(host, port_range=(1000, 5000)):
    """Scan ports for open ones."""
    open_ports = []
    print(f"[*] Scanning ports {port_range[0]}-{port_range[1]} on {host}...")
    for port in random.sample(range(port_range[0], port_range[1] + 1), min(100, port_range[1] - port_range[0] + 1)):
        is_open, latency = check_open_port(host, port)
        if is_open:
            open_ports.append((port, latency))
    return open_ports

def recommend_port(host):
    """Recommend best port."""
    try:
        open_ports = scan_ports(host)
        if open_ports:
            best_port = min(open_ports, key=lambda x: x[1])[0]
            print(f"[+] Recommended port: {best_port}")
            return best_port
        print("[!] No open ports found.")
        return None
    except Exception as e:
        print(f"[!] Error scanning ports: {str(e)}")
        return None

def is_valid_ip(ip):
    """Validate IP."""
    try:
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False
