# ⚠️ INFORMASI PENTING VERSI PYTHON ⚠️

## 🚫 DILARANG KERAS
- ❌ JANGAN Pakai Python 3.12
- ❌ JANGAN Pakai Python 3.11
- ❌ JANGAN Pakai Python 3.10
- ❌ JANGAN Pakai Python 3.9

## ✅ WAJIB PAKAI
- ✅ WAJIB Pakai Python 3.8.x
- ✅ Sudah ditest di Python 3.8.x
- ✅ Semua library kompatibel dengan 3.8.x

## 🔍 Cara Cek Versi Python
```bash
python --version
# HARUS menampilkan -> Python 3.8.x
```

## ❓ Mengapa Harus 3.8?
1. Library yowsup2 hanya stabil di Python 3.8
2. Protobuf dan dependencies lain lebih stabil di 3.8
3. Banyak error jika pakai versi Python yang lebih baru
4. Python 3.8 lebih ringan di Termux

## 📱 Untuk Pengguna Termux
```bash
# Install Python 3.8
pkg install python3.8 -y

# Set sebagai default
ln -sf $PREFIX/bin/python3.8 $PREFIX/bin/python
```
