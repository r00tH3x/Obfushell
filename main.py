import sys
from cli import main as cli_main
from gui import ObfushellGUI
from PyQt5.QtWidgets import QApplication

def start_cli():
    cli_main()

def start_gui():
    app = QApplication(sys.argv)
    ex = ObfushellGUI()
    ex.show()
    sys.exit(app.exec_())

def main():
    display_banner()
    print("[Obfushell] Payload Crafter - Select Mode\n")
    mode = input("Pilih mode: (1) CLI (2) GUI: ")

    if mode == "1":
        start_cli()
    elif mode == "2":
        start_gui()
    else:
        print("[!] Invalid choice. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    main()
