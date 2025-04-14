import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QCheckBox
from core.generator import generate_payload
from core.obfuscator import chain_encode, decode_hint
from core.listener import start_listener

class ObfushellGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Obfushell - Linux Payload Crafter")
        self.setGeometry(200, 200, 400, 300)
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

        self.obfuscation_label = QLabel("Select Obfuscation Method:", self)
        layout.addWidget(self.obfuscation_label)

        self.obfuscation_combo = QComboBox(self)
        self.obfuscation_combo.addItems(["base64", "xor", "reverse", "chain"])
        layout.addWidget(self.obfuscation_combo)

        self.chain_check = QCheckBox("Enable Chaining (base64, xor, reverse):", self)
        layout.addWidget(self.chain_check)

        self.generate_button = QPushButton("Generate Payload", self)
        self.generate_button.clicked.connect(self.generate_payload)
        layout.addWidget(self.generate_button)

        self.result_label = QLabel("Generated Payload:", self)
        layout.addWidget(self.result_label)

        self.result_output = QLineEdit(self)
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        self.listen_button = QPushButton("Start Listener", self)
        self.listen_button.clicked.connect(self.start_listener)
        layout.addWidget(self.listen_button)

        self.setLayout(layout)

    def generate_payload(self):
        payload_type = self.payload_combo.currentText()
        lhost = self.lhost_input.text()
        lport = self.lport_input.text()

        payload = generate_payload(payload_type, lhost, lport)
        obfuscation_method = self.obfuscation_combo.currentText()

        if self.chain_check.isChecked():
            methods = ["base64", "xor", "reverse"]
            obfuscated_payload = chain_encode(payload, methods)
            hint = decode_hint(methods)
        else:
            obfuscated_payload = chain_encode(payload, [obfuscation_method])
            hint = decode_hint([obfuscation_method])

        self.result_output.setText(obfuscated_payload)
        self.result_label.setText(f"Obfuscated Payload: \n{obfuscated_payload}")

    def start_listener(self):
        listener_tool = "nc"
        lport = self.lport_input.text()
        start_listener(listener_tool, lport)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ObfushellGUI()
    ex.show()
    sys.exit(app.exec_())
