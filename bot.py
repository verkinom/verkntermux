#!/usr/bin/env python3.8
import sys

# Pastikan menggunakan Python 3.8
if sys.version_info[0] != 3 or sys.version_info[1] != 8:
    print("\n❌ Error: Bot ini khusus untuk Python versi 3.8")
    print("🔍 Versi Python Anda:", ".".join(map(str, sys.version_info[:3])))
    print("\n📥 Install Python 3.8 di Termux dengan perintah:")
    print("1. pkg update && pkg upgrade")
    print("2. pkg install python3.8")
    print("3. ln -sf /data/data/com.termux/files/usr/bin/python3.8 /data/data/com.termux/files/usr/bin/python")
    sys.exit(1)

import os
import json
import time
from yowsup.registration import WARegRequest
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YowStackBuilder
from yowsup.registration import WARegRequest
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages import YowMessagesProtocolLayer
from yowsup.layers import YowLayerEvent
from yowsup.stacks import YowStack, YowStackBuilder

class WhatsappBot:
    def __init__(self):
        self.bot_name = "VerkinomBot"
        self.creator = "Verkinom"
        self.version = "1.0.0"
        self.phone = None
        self.password = None
        self.stack = None
        self.credentials_file = "credentials.json"
        self.connected = False
        
    def setup(self):
        """Setup awal bot dan registrasi nomor"""
        print(f"\n{self.bot_name} v{self.version}")
        print(f"Dibuat oleh: {self.creator}")
        print("=" * 40)
        print("\n🚀 Memulai proses registrasi bot...")
        
        try:
            # Cek apakah sudah ada kredensial tersimpan
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    creds = json.load(f)
                    self.phone = creds.get('phone')
                    self.password = creds.get('password')
                print("\n✅ Kredensial ditemukan!")
                return self.connect()

            # Minta nomor telepon
            self.phone = input("\n📱 Masukkan nomor WhatsApp yang akan dijadikan bot (contoh: +628123456789): ").strip()
            if not self.phone.startswith('+'):
                self.phone = '+' + self.phone

            # Minta kode registrasi
            req = WARegRequest(self.phone, debug=True)
            result = req.request_code()
            
            if result:
                print("\n📲 Kode verifikasi telah dikirim via SMS")
                code = input("✍️  Masukkan kode verifikasi: ").strip()
                
                # Verifikasi kode
                reg = WARegRequest(self.phone, code)
                result = reg.register()
                
                if result:
                    self.password = result['login']
                    # Simpan kredensial
                    with open(self.credentials_file, 'w') as f:
                        json.dump({
                            'phone': self.phone,
                            'password': self.password
                        }, f)
                    print("\n✅ Registrasi berhasil!")
            
            # Tandai bot siap digunakan
            self.connected = True
            return True
            
        except Exception as e:
            print(f"\n❌ Terjadi kesalahan: {str(e)}")
            return False
            
    def connect(self):
        """Koneksi ke WhatsApp menggunakan kredensial"""
        try:
            if not self.phone or not self.password:
                print("\n❌ Kredensial tidak ditemukan")
                return False

            stackBuilder = YowStackBuilder()
            self.stack = stackBuilder\
                .pushDefaultLayers()\
                .build()

            self.stack.setCredentials((self.phone, self.password))
            self.connected = True
            print("\n✅ Berhasil terhubung ke WhatsApp!")
            return True
            
        except Exception as e:
            print(f"\n❌ Gagal terhubung: {str(e)}")
            return False
            
    def send_message(self, to_number, message):
        """Kirim pesan menggunakan stack yowsup"""
        try:
            if not self.ensure_connected():
                return False

            to_number = self._validate_phone(to_number)
            if not self.is_valid_phone_number(to_number):
                print("\n❌ Format nomor telepon tidak valid")
                return False

            # Kirim pesan
            self.stack.broadcastEvent(
                YowLayerEvent(
                    YowMessagesProtocolLayer.EVENT_SEND_MESSAGE,
                    message=message,
                    to=to_number
                )
            )
            
            print("\n✅ Pesan berhasil dikirim!")
            return True
        except Exception as e:
            print(f"\n❌ Gagal mengirim pesan: {str(e)}")
            if "auth" in str(e).lower():
                print("🔄 Mencoba login ulang...")
                if self.retry_connection():
                    return self.send_message(to_number, message)
            return False    # Hapus fungsi send_photo karena kita hanya butuh kirim teks
            
    def close(self):
        """Tutup koneksi bot"""
        if self.stack:
            self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))
            self.connected = False

    def _validate_phone(self, phone):
        """Validasi format nomor telepon"""
        if not isinstance(phone, str):
            return None
        phone = phone.strip()
        # Hapus spasi dan karakter khusus
        phone = ''.join(c for c in phone if c.isdigit() or c == '+')
        # Pastikan format +62
        if not phone.startswith('+'):
            phone = '+' + phone
        if phone.startswith('+0'):
            phone = '+62' + phone[2:]
        return phone

    def _save_credentials(self):
        """Simpan kredensial ke file"""
        if self.phone and self.password:
            with open(self.credentials_file, 'w') as f:
                json.dump({
                    'phone': self.phone,
                    'password': self.password
                }, f)
            return True
        return False

    def _load_credentials(self):
        """Muat kredensial dari file"""
        try:
            if os.path.exists(self.credentials_file):
                with open(self.credentials_file, 'r') as f:
                    creds = json.load(f)
                    self.phone = creds.get('phone')
                    self.password = creds.get('password')
                return True
            return False
        except Exception:
            return False

    def retry_connection(self, max_retries=3):
        """Mencoba menghubungkan ulang dengan beberapa percobaan"""
        for attempt in range(max_retries):
            print(f"\n🔄 Mencoba menghubungkan ulang (percobaan ke-{attempt + 1}/{max_retries})...")
            if self.connect():
                return True
                time.sleep(2 ** attempt)  # Jeda eksponensial
        return False

    def ensure_connected(self):
        """Memastikan bot terhubung sebelum kirim pesan"""
        if not hasattr(self, 'connected') or not self.connected:
            print("\n❌ Bot belum terhubung. Mencoba menghubungkan ulang...")
            return self.retry_connection()
        if not self.stack:
            print("\n❌ Koneksi terputus. Mencoba menghubungkan ulang...")
            return self.connect()
        return True

    def is_valid_phone_number(self, phone):
        """Periksa format nomor telepon"""
        if not phone:
            return False
        phone = self._validate_phone(phone)
        # Validasi dasar: dimulai dengan +, diikuti 10-15 angka
        import re
        return bool(re.match(r'^\+[1-9]\d{10,14}$', phone))

# Bot ini hanya fokus pada fitur pengiriman pesan teks saja

def main():
    """Program utama WhatsApp Bot"""
    try:
        print("\n" + "="*50)
        print("🤖 WhatsApp Bot Termux")
        print("="*50)
        
        # Inisialisasi bot
        bot = WhatsappBot()
        
        # Setup dan registrasi bot
        print("\n📱 Memulai setup bot...")
        if not bot.setup():
            print("\n❌ Gagal setup bot:")
            print("1. Pastikan format nomor benar (+62xxx)")
            print("2. Pastikan bisa menerima SMS")
            print("3. Coba hapus credentials.json jika ada")
            return

        # Hubungkan bot ke WhatsApp
        print("\n🔄 Menghubungkan ke WhatsApp...")
        if not bot.connect():
            print("\n❌ Gagal terhubung ke WhatsApp:")
            print("1. Periksa koneksi internet")
            print("2. Pastikan nomor belum dipakai di HP lain")
            print("3. Coba restart Termux dan jalankan ulang")
            return

        print("\n✅ Bot berhasil terhubung!")
        print("\n📝 Perintah yang tersedia:")
        print("┌─────────────────────────────────")
        print("│ send : Kirim pesan WhatsApp")
        print("│ help : Tampilkan bantuan")
        print("│ exit : Keluar dari program")
        print("└─────────────────────────────────")

        while True:
            try:
                command = input("\n🤖 Masukkan perintah: ").lower().strip()
                
                if command == "help":
                    print("\n📚 Bantuan WhatsApp Bot:")
                    print("1. Ketik 'send' untuk mengirim pesan")
                    print("2. Masukkan nomor tujuan dengan format +62xxx")
                    print("3. Ketik pesan yang ingin dikirim")
                    print("4. Ketik 'exit' untuk keluar")
                elif command == "send":
                    print("\n📱 Format nomor: +62812xxxxx")
                    print("Contoh: +628123456789 atau 08123456789")
                    to_number = input("👉 Masukkan nomor tujuan: ").strip()
                    
                    if not bot.is_valid_phone_number(to_number):
                        print("\n❌ Format nomor tidak valid!")
                        print("Tips: Gunakan format +62xxx atau 08xxx")
                        continue
                        
                    print("\n✍️ Ketik pesanmu (Enter untuk kirim):")
                    message = input("👉 ").strip()
                    
                    if not message:
                        print("\n❌ Pesan tidak boleh kosong!")
                        continue
                    
                    print("\n📤 Mengirim pesan...")
                    if bot.send_message(to_number, message):
                        print("\n✅ Pesan berhasil dikirim ke " + to_number)
                    else:
                        print("\n❌ Gagal mengirim pesan!")
                        print("Tips:")
                        print("1. Periksa koneksi internet")
                        print("2. Pastikan nomor tujuan benar")
                        print("3. Coba kirim ulang setelah beberapa detik")
                        
                elif command == "exit":
                    print("\n👋 Terima kasih telah menggunakan VerkinomBot!")
                    break
                    
                else:
                    print("\n❌ Perintah tidak dikenal. Ketik 'help' untuk bantuan.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Program dihentikan oleh pengguna.")
                break
            except Exception as e:
                print(f"\n❌ Terjadi kesalahan: {str(e)}")
                print("Silakan coba lagi atau ketik 'exit' untuk keluar.")

    except Exception as e:
        print(f"\n❌ Terjadi kesalahan fatal: {str(e)}")
    finally:
        if 'bot' in locals():
            bot.close()
        print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
