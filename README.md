# 🤖 WhatsApp Bot Termux

Bot WhatsApp sederhana untuk mengirim pesan teks. Berjalan di Termux tanpa root.
Verifikasi via SMS (tidak perlu scan QR code).

## ⭐ Fitur
- Kirim pesan teks ke nomor WhatsApp manapun
- Verifikasi via SMS (tidak perlu QR code)
- Berjalan di Termux tanpa root
- Simpel dan mudah digunakan
- Interface bahasa Indonesia

## 📱 Persiapan Awal

### 1. Install Termux
- ⚠️ JANGAN install Termux dari Play Store (sudah tidak diupdate)
- ✅ Install Termux dari F-Droid: https://f-droid.org/en/packages/com.termux/
- Buka link di browser HP
- Download & Install aplikasi F-Droid
- Buka F-Droid, cari "Termux", Install

### 2. Persiapan WhatsApp
- Install WhatsApp dari Play Store
- Siapkan nomor HP yang akan dijadikan bot
- Pastikan bisa menerima SMS untuk verifikasi

## 📲 Cara Install di Termux (100% Work)

### 1. Install Termux
- Download Termux F-Droid: https://f-droid.org/en/packages/com.termux/
- JANGAN download dari Play Store!
- Install dan buka Termux

### 2. Setup Python 3.8 (WAJIB)
```bash
# 1. Bersihkan cache package
pkg clean
rm -rf /data/data/com.termux/files/usr/var/cache/*

# 2. Update repository (WAJIB)
pkg update -y
apt update -y
apt upgrade -y
pkg upgrade -y

# 3. Install Python 3.8 (WAJIB versi ini)
pkg remove python -y
pkg install python3.8 -y
pkg install python3.8-pip -y

# 4. Set Python 3.8 sebagai default
ln -sf /data/data/com.termux/files/usr/bin/python3.8 /data/data/com.termux/files/usr/bin/python
ln -sf /data/data/com.termux/files/usr/bin/pip3.8 /data/data/com.termux/files/usr/bin/pip

# 5. Cek versi Python (HARUS 3.8.x)
python --version
pkg update -y

# 5. Install dependencies dasar
pkg install build-essential binutils pkg-config -y
pkg install python-dev openssl libffi-dev -y
pkg install git curl wget -y
```

### 3. Install & Fix PIP
```bash
# 1. Hapus pip lama (jika ada)
rm -rf ~/.local/lib/python*/site-packages/*
rm -rf /data/data/com.termux/files/usr/lib/python*/site-packages/*

# 2. Install pip baru
pkg install python-pip -y

# 3. Jika error, install manual:
curl -L https://bootstrap.pypa.io/get-pip.py > get-pip.py
python3 get-pip.py --no-cache-dir

# 4. Fix pip
python3 -m pip install --upgrade pip --no-cache-dir
export PATH=$PATH:$HOME/.local/bin

# 5. Test pip
pip --version
```

### 3. Fix Permission
```bash
# Fix permission storage
termux-setup-storage

# Buat folder kerja
cd /sdcard
mkdir WhatsAppBot
cd WhatsAppBot
```

### 4. Install Bot (Metode Aman)
```bash
# Clone repository (ganti dengan URL repo Anda)
git clone https://github.com/[username]/whatsapp-bot.git
cd whatsapp-bot

# Persiapan pip
python -m pip install --upgrade pip
pip install wheel setuptools

# Install dependencies satu per satu (dengan versi yang tepat)
pip install yowsup2==2.5.4
pip install pycrypto==2.6.1
pip install python-dateutil==2.7.5
pip install protobuf==3.6.1

# Jika ada error, coba ini
pip install --no-deps yowsup2
```

### 3. Install Bot dan Dependencies

```bash
# 1. Install package yang dibutuhkan untuk Python 3.8
python3.8 -m pip install --upgrade pip
pip install wheel setuptools

# 2. Install requirements (cara aman)
pip install --no-cache-dir yowsup2==2.5.4
pip install --no-cache-dir pycrypto==2.6.1
pip install --no-cache-dir python-dateutil==2.7.5
pip install --no-cache-dir protobuf==3.6.1

# Alternatif: Install semua sekaligus
pip install -r requirements.txt
```

### 4. Cek Instalasi
```bash
# Pastikan Python versi 3.8
python --version  # Harus tampil Python 3.8.x

# Cek pip dan package
pip list  # Harus ada yowsup2==2.5.4, pycrypto==2.6.1, dll
```

### 5. Troubleshooting Umum

#### Error saat pip install:
```bash
# Hapus cache pip
pip cache purge
rm -rf ~/.cache/pip

# Install ulang
pip install --no-cache-dir -r requirements.txt
```

#### Error "No module found":
```bash
# Install ulang semua package
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

#### Error Permission:
```bash
# Pastikan storage diizinkan
termux-setup-storage

# Coba dengan sudo (jika ada)
pkg install tsu -y
sudo pip install -r requirements.txt
```

### 6. Masalah Umum & Solusi

#### A. Error "ModuleNotFoundError"
```bash
# Solusi 1: Install ulang pip
pkg install python-pip -y
python -m pip install --upgrade pip

# Solusi 2: Install package satu per satu
pip install yowsup2
pip install pycrypto
```

#### B. Error "Permission Denied"
```bash
# Solusi 1: Setup storage ulang
termux-setup-storage
# Tekan ALLOW di popup

# Solusi 2: Fix permission folder
chmod +x /data/data/com.termux/files/usr/bin/*
```

#### C. Error "Connection Failed"
1. Pastikan format nomor benar (+62xxx)
2. Periksa koneksi internet
3. Tunggu 5 menit, coba lagi
4. Hapus credentials.json, setup ulang

#### D. Error PIP di Termux
```bash
# 1. Fix Repository
pkg clean
rm -rf $PREFIX/var/cache/*
echo "deb https://packages-cf.termux.org/apt/termux-main stable main" > $PREFIX/etc/apt/sources.list
pkg update -y

# 2. Install ulang Python 3.8 + PIP
pkg remove python -y
pkg install python3.8 -y
pkg install python3.8-pip -y

# 3. Jika masih error, install manual:
cd ~
curl https://bootstrap.pypa.io/get-pip.py --output get-pip.py
python3 get-pip.py --no-cache-dir

# 4. Test pip dan path:
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc
pip3 --version

# 5. Jika 'command not found':
ln -s $PREFIX/bin/pip3 $PREFIX/bin/pip
hash -r
```

#### E. Error saat pip install package
```bash
# 1. Fix dependencies
pkg install build-essential binutils pkg-config -y
pkg install python-dev openssl libffi-dev -y

# 2. Clear pip cache
pip cache purge
pip3 cache purge
rm -rf ~/.cache/pip

# 3. Install dengan opsi tambahan
pip install --no-cache-dir --no-deps --ignore-installed package_name

# 4. Jika masih error, coba:
LDFLAGS="-L/system/lib/" CFLAGS="-I/data/data/com.termux/files/usr/include/" pip install package_name
```

### 7. Masalah PIP di Termux

#### Masalah 1: pip: command not found
```bash
# Solusi lengkap:
pkg clean
rm -rf $PREFIX/var/cache/*
pkg update -y
pkg remove python -y
pkg install python3.8 -y
curl https://bootstrap.pypa.io/pip/3.8/get-pip.py --output get-pip.py
python3.8 get-pip.py --no-cache-dir
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

#### Masalah 2: Could not install packages due to an OSError
```bash
# Fix permission
chmod 700 -R ~/.local/lib/python*
chmod 700 -R /data/data/com.termux/files/usr/lib/python*

# Install ulang dengan flag khusus
pip install --user --no-cache-dir package_name
```

#### Masalah 3: Error building wheel
```bash
# Install build tools
pkg install build-essential -y
pkg install cmake make -y
pkg install python-dev -y

# Set environment variables
export CFLAGS="-I/data/data/com.termux/files/usr/include"
export LDFLAGS="-L/data/data/com.termux/files/usr/lib"
export CXXFLAGS="-I/data/data/com.termux/files/usr/include"
```

#### Masalah 4: SSL Certificate Error
```bash
# Fix certificate
pkg install openssl-tool -y
pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"
```

### 8. Kompatibilitas
- ✅ Android 7 sampai 14
- ✅ Termux dari F-Droid (Recommended)
- ✅ Termux versi lama
- ✅ Tidak perlu root
- ❌ Termux dari Play Store (Deprecated)

### 3. Install Bot (Metode Tanpa Root)
```bash
# Download requirements satu per satu (lebih aman)
pip install requests==2.25.1
pip install Pillow==8.4.0
pip install python-dotenv==0.19.2
pip install pycryptodome==3.10.1
pip install yowsup-cli==0.4.4

# Clone repository
git clone https://github.com/[username]/bottermux.git
cd bottermux

# Salin file konfigurasi
cp -r * ~/storage/shared/WhatsAppBot/
cd ~/storage/shared/WhatsAppBot
```

### 4. Jalankan Bot
```bash
# Jalankan bot
python bot.py
```

## 🚀 Cara Menggunakan Bot

### Pertama Kali Pakai:
1. Jalankan bot: `python bot.py`
2. Masukkan nomor WhatsApp yang akan dijadikan bot
   - Format: +62812XXXXX (pakai kode negara)
3. Tunggu SMS verifikasi
4. Masukkan kode verifikasi
5. Bot akan menyimpan kredensial otomatis

### Kirim Pesan:
1. Jalankan bot: `python bot.py`
2. Ketik `send` untuk kirim pesan
3. Masukkan nomor tujuan: +62812XXXXX
4. Ketik pesan yang ingin dikirim
5. Bot akan mengirim pesan ke nomor tujuan

### Perintah Bot:
- `send` : Kirim pesan WhatsApp
- `help` : Tampilkan bantuan
- `exit` : Keluar dari program

## ⚙️ Perintah Bot
- `help` : Tampilkan bantuan
- `apod` : Kirim foto astronomi NASA hari ini
- `exit` : Keluar dari program

## ❗ Troubleshooting

### 1. Error "ModuleNotFoundError"
Jalankan perintah ini satu per satu:
```bash
# Hapus instalasi yang ada
pip uninstall -y requests Pillow python-dotenv cryptography yowsup-cli pycryptodome
rm -rf ~/.local/lib/python*/site-packages/*

# Install ulang dengan pip
python -m pip install --upgrade pip
pip install --no-cache-dir requests==2.28.2
pip install --no-cache-dir Pillow==9.5.0
pip install --no-cache-dir python-dotenv==0.21.1
pip install --no-cache-dir pycryptodome==3.17.0
pip install --no-cache-dir yowsup-cli==0.4.4

# 2. Upgrade pip dan install tools dasar
python -m pip install --upgrade pip
pip install wheel setuptools

# 3. Install requirements satu per satu (versi spesifik untuk Python 3.8)
pip install requests==2.25.1
pip install Pillow==8.4.0
pip install python-dotenv==0.19.2
pip install cryptography==3.4.7
pip install yowsup2==2.5.4

# 4. Jika masih error, coba ini
pip install --no-cache-dir -r requirements.txt
```

Jika masih ada error "ModuleNotFoundError", jalankan:
```bash
# Hapus dan install ulang semua package
pip uninstall -y -r requirements.txt
pip cache purge
pip install -r requirements.txt
```

### 2. Error Kompilasi
Jika ada error "unable to compile", jalankan:
```bash
pkg install clang -y
pkg install make -y
pip install -r requirements.txt
```

### 3. Error Permission
Jika ada error permission, jalankan:
```bash
termux-setup-storage
```
Lalu izinkan akses storage saat diminta.

### 4. Bot Tidak Bisa Konek
- Pastikan format nomor benar (+62xxx)
- Coba hapus file `credentials.json`
- Jalankan ulang proses registrasi

## 📝 Catatan Penting
- Bot menggunakan DEMO_KEY NASA API
- Untuk penggunaan lebih baik:
  1. Daftar di https://api.nasa.gov/
  2. Dapatkan API key gratis
  3. Ganti `DEMO_KEY` di `bot.py` dengan API key Anda

## 🤝 Kontribusi
- Report bug: Buat issue di GitHub
- Tambah fitur: Kirim pull request
- Pertanyaan: Buat issue dengan label "question"

### Troubleshooting Python 3.8

#### A. Jika Python 3.8 tidak terpasang
```bash
# Hapus Python yang ada
pkg remove python -y

# Install Python 3.8 secara spesifik
pkg install python3.8 -y
pkg install python3.8-pip -y

# Set sebagai default
ln -sf /data/data/com.termux/files/usr/bin/python3.8 /data/data/com.termux/files/usr/bin/python
```

#### B. Jika pip error di Python 3.8
```bash
# Reinstall pip untuk Python 3.8
python3.8 -m ensurepip --default-pip
python3.8 -m pip install --upgrade pip

# Jika masih error, install manual
curl -L https://bootstrap.pypa.io/get-pip.py > get-pip.py
python3.9 get-pip.py --no-cache-dir
```

#### C. Package tidak kompatibel dengan Python 3.8
```bash
# Install versi spesifik yang support Python 3.8
pip install --no-cache-dir yowsup2==2.5.4
pip install --no-cache-dir pycrypto==2.6.1
pip install --no-cache-dir python-dateutil==2.7.5
pip install --no-cache-dir protobuf==3.6.1
```
