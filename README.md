# CareLoopAI - Clinic Chatbot

<p align="center">
  <img width="250" height="250" alt="careloop-ai" src="https://github.com/user-attachments/assets/4f45d36a-0302-4bdd-a3a4-636ec13e0030" />
</p>


CareLoopAI adalah chatbot berbasis Rasa (Python) yang dirancang untuk klinik kecil. Sistem ini tidak hanya melakukan triase awal, tetapi juga menciptakan "perulangan perawatan" otomatis - pasien menerima rencana pengobatan yang direvisi setiap hari berdasarkan gejala yang mereka foto atau ceritakan, mengurangi kunjungan ulang yang tidak perlu.

## Fitur Utama

- **Triage Otomatis**: Penilaian awal kondisi pasien berdasarkan gejala yang dilaporkan
- **Rencana Pengobatan Dinamis**: Pembuatan dan revisi rencana pengobatan harian
- **Pelacakan Gejala**: Pemantauan perkembangan gejala dari hari ke hari
- **Analisis Foto Gejala**: Kemampuan untuk menganalisis foto gejala pasien (simulasi)
- **Pengurangan Kunjungan Ulang**: Mengurangi kebutuhan kunjungan ulang yang tidak perlu
- **Penjadwalan Janji**: Sistem penjadwalan kunjungan ke klinik

## Struktur Proyek

```
CareLoopAI/
├── actions/                 # Custom actions untuk Rasa
├── data/                    # Data training
│   ├── nlu/                 # Data NLU (Natural Language Understanding)
│   ├── stories/             # Cerita percakapan
│   └── rules/               # Aturan percakapan
├── models/                  # Model yang dilatih (akan dibuat saat training)
├── config.yml               # Konfigurasi pipeline dan policies
├── domain.yml               # Definisi domain chatbot
├── requirements.txt         # Daftar dependensi
├── README.md                # Dokumentasi
├── careloopai_clinic.py     # Sistem inti CareLoopAI
├── cli_chatbot.py           # Interface command-line
├── clinic_chatbot.html      # Interface web
├── image_processor.py       # Modul pemrosesan gambar
├── patient_data_manager.py  # Manajemen data pasien
└── setup.py                 # Script setup
```

## Instalasi

1. Clone repository ini:
   ```
   git clone <repository-url>
   cd CareLoopAI
   ```

2. Instal dependensi:
   ```
   pip install -r requirements.txt
   ```

3. Jalankan script setup:
   ```
   python setup.py
   ```

## Penggunaan

### Command Line Interface
Jalankan chatbot melalui terminal:
```
python cli_chatbot.py
```

### Web Interface
Buka file `clinic_chatbot.html` di browser Anda.

### Rasa Chatbot (jika Rasa terinstal)
1. Train model:
   ```
   rasa train
   ```

2. Jalankan chatbot:
   ```
   rasa shell
   ```

## Arsitektur Sistem

### 1. Core Components
- **Patient Data Manager**: Mengelola data pasien, riwayat gejala, dan rencana pengobatan
- **Image Processor**: Menganalisis foto gejala (simulasi dalam implementasi ini)
- **Treatment Planner**: Membuat dan merevisi rencana pengobatan harian

### 2. Rasa Components
- **NLU (Natural Language Understanding)**: Memahami maksud pengguna
- **Dialog Management**: Mengelola alur percakapan
- **Custom Actions**: Aksi khusus untuk fungsionalitas aplikasi

### 3. Interfaces
- **CLI Interface**: Antarmuka berbasis command-line
- **Web Interface**: Antarmuka berbasis web responsif
- **Rasa Shell**: Antarmuka bawaan Rasa

## Cara Kerja

1. **Registrasi Pasien**: Pasien mendaftarkan diri dengan nama dan informasi dasar
2. **Pelaporan Gejala**: Pasien melaporkan gejala awal (teks atau foto)
3. **Triage Awal**: Sistem melakukan penilaian awal dan membuat rencana pengobatan
4. **Checkin Harian**: Pasien melakukan checkin harian untuk update kondisi
5. **Revisi Pengobatan**: Sistem merevisi rencana pengobatan berdasarkan perkembangan
6. **Pengurangan Kunjungan**: Sistem menentukan apakah kunjungan ulang diperlukan

## Pengembangan Lebih Lanjut

Beberapa area untuk pengembangan masa depan:
- Integrasi model machine learning untuk analisis gejala yang lebih akurat
- Koneksi ke sistem rekam medis elektronik
- Notifikasi otomatis melalui SMS/email
- API REST untuk integrasi dengan sistem lain
- Dashboard admin untuk tenaga medis

## Lisensi

Proyek ini dilisensikan di bawah lisensi MIT - lihat file [LICENSE](LICENSE) untuk detailnya.
