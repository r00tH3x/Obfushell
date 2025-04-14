# Obfushell - Linux Payload Crafter
<p align="center">
   <img src="https://img.shields.io/badge/Python-3.8%2B-blue" />
   <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

## Overview
**Obfushell** adalah alat untuk membuat dan mengobfuscate payload Linux secara interaktif. Alat ini memungkinkan pengguna untuk membuat payload yang lebih tersembunyi menggunakan metode obfuscation seperti **base64**, **XOR**, dan **reverse string**. Tool ini dapat dijalankan dalam mode **CLI** atau **GUI** untuk memudahkan penggunaan, baik oleh pemula atau profesional di dunia **ethical hacking**.

---

## Fitur
- 💻 **Payload Generator**: Membuat reverse shell dan bind shell dalam berbagai format (bash, python, perl, socat, ncat).
- 🔒 **Obfuscation**: Menyembunyikan payload dengan teknik obfuscation seperti base64, XOR, dan reverse string.
- 🎮 **Mode Interaktif**: Bisa memilih antara mode **CLI** (Command Line Interface) atau **GUI** (Graphical User Interface) dengan PyQt5.
- 🖥️ **Listener**: Mengaktifkan listener otomatis menggunakan `nc` untuk menangkap koneksi dari payload.
- 🧑‍💻 **Modular**: Kode yang bersih, mudah dikembangkan, dan dapat disesuaikan dengan kebutuhan Anda.

---

## Prasyarat
Sebelum memulai, pastikan Anda telah menginstal hal-hal berikut di sistem Anda:

- **Python 3.8+** — [Download](https://www.python.org/downloads/)
- **PyQt5** — Library untuk membuat GUI berbasis Qt.
- **nc (Netcat)** — Untuk menjalankan listener (biasa sudah terpasang di sebagian besar distribusi Linux).

---

## Instalasi

### 1. Kloning Repositori
```bash
git clone https://github.com/r00tH3x/obfushell.git
cd obfushell
```

### 2. Buat Virtual Environment (Opsional, tapi Disarankan)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependensi Python
```bash
pip install -r requirements.txt
```

### 4. Pastikan `nc` Terpasang
Jika `nc` (Netcat) belum terpasang, Anda bisa menginstalnya melalui paket manager:
#### Debian/Ubuntu:
```bash
sudo apt install netcat
```
#### RedHat/CentOS:
```bash
sudo yum install nmap-ncat
```

---

## Cara Penggunaan

### Mode CLI
```bash
python main.py
# Pilih: 1 (CLI)
```
Di mode CLI, Anda akan diminta untuk memilih jenis payload (reverse shell atau bind shell), obfuscation yang diinginkan, serta menentukan LHOST dan LPORT.

### Mode GUI
```bash
python main.py
# Pilih: 2 (GUI)
```
GUI akan muncul dengan antarmuka pengguna yang mudah untuk memilih opsi payload dan obfuscation.

---

## Jenis Payload yang Didukung

| Jenis Payload     | Deskripsi                  |
|-------------------|----------------------------|
| bash_reverse      | Reverse shell via bash     |
| python_reverse    | Reverse shell via python   |
| perl_reverse      | Reverse shell via perl     |
| socat_reverse     | Reverse shell via socat    |
| socat_bind        | Bind shell via socat       |
| ncat_reverse      | Reverse shell via ncat     |
| ncat_bind         | Bind shell via ncat        |

---

## Teknik Obfuscation

- **base64**: Encode payload menjadi base64 agar sulit dibaca.
- **xor**: Obfuscate payload dengan teknik XOR.
- **reverse**: Membalik urutan karakter payload.
- **chain**: Gabungkan beberapa teknik obfuscation untuk menyembunyikan payload lebih dalam.

---

## Contoh Output
```bash
[*] Payload berhasil di-generate dan di-obfuscate:
echo aGVsbG8gd29ybGQ= | base64 -d | bash
```

---

## Lisensi
Distribusikan di bawah lisensi MIT. Lihat file `LICENSE` untuk detail lengkapnya.

---

## Kontribusi
Pull request sangat diterima! Untuk perubahan besar, harap buka issue terlebih dahulu untuk diskusi.

---

> **r00tH3x** — Tools built to educate, not to exploit.
