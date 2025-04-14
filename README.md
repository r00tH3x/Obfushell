Obfushell

Obfushell adalah tool powerful untuk membuat dan mengobfuscate payload Linux secara interaktif, baik melalui CLI maupun GUI. Dirancang untuk penetration tester, red teamer, dan enthusiast di dunia ethical hacking yang ingin payload-nya tidak mudah terdeteksi dan tetap efektif.

Fitur Utama

Payload Generator (Reverse & Bind Shell)

Obfuscation (base64, XOR, reverse string, chaining)

Interactive CLI Mode

User-Friendly GUI Mode (PyQt5)

Listener otomatis (menggunakan nc)

Modular, clean code, dan mudah dikembangkan


---

Instalasi

1. Clone Repository

git clone https://github.com/username/obfushell.git
cd obfushell

2. Install Dependencies

pip install -r requirements.txt

Jika belum punya PyQt5:

pip install pyqt5


---

Cara Menjalankan

Mode CLI

python main.py
# Pilih: 1 (CLI)

Ikuti petunjuk untuk memilih jenis payload, obfuscation, dan memulai listener.

Mode GUI

python main.py
# Pilih: 2 (GUI)

GUI akan tampil dengan input interaktif untuk membuat dan melihat payload secara visual.


---

Payload yang Didukung

Teknik Obfuscation

base64: Encode payload ke base64

xor: Encode karakter payload dengan XOR

reverse: Membalik urutan karakter payload

chain: Kombinasi ketiga metode di atas untuk obfuscation berlapis



---

Contoh Output

[*] Payload berhasil di-generate dan di-obfuscate:
echo aGVsbG8gd29ybGQ= | base64 -d | bash


---

Kontribusi

Pull request sangat diterima! Silakan fork, buat fitur baru atau perbaikan, lalu submit PR.


---

Catatan Penting

Tool ini dibuat untuk tujuan edukasi dan ethical hacking. Penggunaan untuk aktivitas ilegal bukan tanggung jawab pembuat.


---

Lisensi

MIT License


---

Kontak

Author: r00tH3x Telegram: @yourhandle Github: yourgithub

