#!/usr/bin/env python3
"""
Pet Product Safety Analyzer - Setup dan Instruksi Menjalankan
Sistem Analisis Keamanan Produk Perawatan Hewan

Author: Claude AI Assistant
Version: 1.0
"""

import os
import sys
import subprocess
import platform

def print_header():
    print("=" * 60)
    print("🐾 PET PRODUCT SAFETY ANALYZER")
    print("   Sistem Analisis Keamanan Produk Perawatan Hewan")
    print("=" * 60)
    print()

def check_python_version():
    """Cek versi Python"""
    print("📋 Mengecek versi Python...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 atau lebih baru diperlukan!")
        print(f"   Versi saat ini: {sys.version}")
        return False
    else:
        print(f"✅ Python {sys.version.split()[0]} - OK")
        return True

def install_requirements():
    """Install dependencies dari requirements.txt"""
    print("\n📦 Menginstall dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies berhasil diinstall")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error menginstall dependencies")
        return False

def check_tesseract():
    """Cek apakah Tesseract OCR terinstall"""
    print("\n🔍 Mengecek Tesseract OCR...")
    try:
        subprocess.run(["tesseract", "--version"], capture_output=True, check=True)
        print("✅ Tesseract OCR ditemukan")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Tesseract OCR tidak ditemukan!")
        print_tesseract_installation_guide()
        return False

def print_tesseract_installation_guide():
    """Print panduan instalasi Tesseract"""
    system = platform.system().lower()
    
    print("\n📖 PANDUAN INSTALASI TESSERACT OCR:")
    print("-" * 40)
    
    if system == "windows":
        print("🪟 Windows:")
        print("1. Download dari: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install file .exe yang didownload")
        print("3. Tambahkan ke PATH atau update path di utils.py")
        print("   Contoh path: C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        
    elif system == "darwin":  # macOS
        print("🍎 macOS:")
        print("1. Install Homebrew jika belum ada: https://brew.sh/")
        print("2. Jalankan: brew install tesseract")
        
    elif system == "linux":
        print("🐧 Linux:")
        print("Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("CentOS/RHEL: sudo yum install tesseract")
        print("Fedora: sudo dnf install tesseract")
    
    print("\n4. Restart terminal setelah instalasi")
    print("5. Test dengan: tesseract --version")

def create_sample_folders():
    """Buat folder untuk contoh gambar"""
    print("\n📁 Membuat struktur folder...")
    folders = ["sample_images", "results", "temp"]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Folder '{folder}' dibuat")
        else:
            print(f"📁 Folder '{folder}' sudah ada")

def print_usage_instructions():
    """Print instruksi penggunaan"""
    print("\n" + "=" * 60)
    print("🚀 CARA MENJALANKAN APLIKASI")
    print("=" * 60)
    print()
    print("1. Pastikan semua requirements sudah terinstall")
    print("2. Jalankan aplikasi dengan command:")
    print("   streamlit run app.py")
    print()
    print("3. Aplikasi akan terbuka di browser pada:")
    print("   http://localhost:8501")
    print()
    print("4. Upload gambar produk perawatan hewan")
    print("5. Klik 'Analisis Produk' untuk memproses")
    print()
    print("📝 CATATAN PENTING:")
    print("- Pastikan gambar memiliki kualitas yang baik")
    print("- Teks pada label harus terlihat jelas")
    print("- Format yang didukung: JPG, PNG, JPEG")
    print("- Ukuran file maksimal: 200MB")
    print()

def print_file_structure():
    """Print struktur file project"""
    print("📂 STRUKTUR FILE PROJECT:")
    print("-" * 30)
    structure = """
pet-product-analyzer/
├── app.py                 # Aplikasi utama Streamlit
├── utils.py              # Fungsi pemrosesan dan analisis
├── requirements.txt      # Dependencies Python
├── ingredients_db.json   # Database bahan berbahaya/aman
├── setup_and_run.py     # Script setup ini
├── sample_images/       # Folder untuk contoh gambar
├── results/            # Folder untuk hasil analisis
└── temp/              # Folder temporary
"""
    print(structure)

def run_application():
    """Jalankan aplikasi Streamlit"""
    print("\n🚀 Menjalankan aplikasi...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplikasi dihentikan oleh user")
    except Exception as e:
        print(f"❌ Error menjalankan aplikasi: {e}")

def main():
    """Fungsi utama setup"""
    print_header()
    
    # Cek Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup gagal - tidak dapat menginstall dependencies")
        sys.exit(1)
    
    # Cek Tesseract
    tesseract_ok = check_tesseract()
    
    # Buat folder
    create_sample_folders()
    
    # Print struktur file
    print_file_structure()
    
    # Print instruksi
    print_usage_instructions()
    
    if tesseract_ok:
        # Tanya user apakah ingin langsung menjalankan
        print("🤔 Apakah Anda ingin menjalankan aplikasi sekarang? (y/n): ", end="")
        response = input().lower().strip()
        
        if response in ['y', 'yes', 'ya']:
            run_application()
        else:
            print("\n✅ Setup selesai!")
            print("Jalankan aplikasi kapan saja dengan: streamlit run app.py")
    else:
        print("\n⚠️  Setup hampir selesai!")
        print("Install Tesseract OCR terlebih dahulu, lalu jalankan:")
        print("python setup_and_run.py")

if __name__ == "__main__":
    main()
