import threading
import socket
import subprocess
import datetime
import os

def log_activity(message):
    """Log listener activity."""
    with open("listener.log", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def nc_listener(lport):
    """Netcat listener."""
    log_activity(f"Starting Netcat listener on port {lport}")
    try:
        subprocess.call(["nc", "-lvnp", str(lport)])
    except KeyboardInterrupt:
        log_activity("Netcat listener stopped")
        print("\n[!] Listener stopped.")
    except Exception as e:
        log_activity(f"Netcat error: {str(e)}")
        print(f"[!] Error: {str(e)}")

def threaded_listener(lport):
    """Custom multi-session listener."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind(("0.0.0.0", lport))
        server.listen(5)
        log_activity(f"Custom listener started on port {lport}")
        print(f"[*] Listening on port {lport}...")

        def handle_client(client_socket, addr):
            log_activity(f"New connection from {addr}")
            try:
                while True:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    decoded_data = data.decode(errors="ignore")
                    log_activity(f"Received from {addr}: {decoded_data}")
                    print(f"[>] {addr}: {decoded_data}")
            except Exception as e:
                log_activity(f"Error with {addr}: {str(e)}")
            finally:
                client_socket.close()
                log_activity(f"Connection closed with {addr}")

        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client, addr))
            client_handler.start()
    except KeyboardInterrupt:
        log_activity("Custom listener stopped")
        print("\n[!] Listener stopped.")
    except Exception as e:
        log_activity(f"Custom listener error: {str(e)}")
        print(f"[!] Error: {str(e)}")
    finally:
        server.close()

def start_listener(tool, lport):
    """Start listener."""
    try:
        if tool == "nc":
            nc_listener(lport)
        elif tool == "socat":
            log_activity(f"Starting Socat listener on port {lport}")
            subprocess.call(f"socat TCP-LISTEN:{lport},reuseaddr,fork EXEC:/bin/sh", shell=True)
        elif tool == "threaded":
            threaded_listener(lport)
        else:
            raise ValueError("[!] Unsupported listener: " + tool)
    except Exception as e:
        log_activity(f"Listener error: {str(e)}")
        print(f"[!] Error: {str(e)}")
