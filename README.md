# Aplikasi Web Personal Branding - Python Flask

> **Tugas Individu Pemrograman Web dengan Flask**  
> **Mata Kuliah:** MAD61123 Pemrograman Lanjut   
> **Program Studi:** Sains Data  
> **Fakultas:** Sains dan Teknologi Maju (FSTeM)  
> **Universitas:** Universitas Brawijaya  
> **Nama Mahasiswa:** Faiq Admaja Wibowo  
> **NIM:** 255091107111004  

---

## Ringkasan Proyek

Aplikasi dibangun menggunakan micro-framework **Python Flask** dengan arsitektur multi-page, dan styling **CSS** modern (skema warna Brawijaya Deep Navy, Ocean Cobalt, Sky Cyan, dan Ice Blue).

---


##  Struktur Direktori Proyek

Personal Branding_Flask/
│
├── app.py                     # File utama aplikasi Python Flask (Routing, Logic, & Data)
├── messages.json              # Penyimpanan data pesan formulir kontak
├── requirements.txt           # Daftar dependensi modul Python (Flask, Werkzeug, Jinja2)
├── README.md                  # Dokumentasi teknis proyek
│
├── templates/                 # Folder template HTML (Jinja2 Template Engine)
│   ├── base.html              # Layout utama (Navbar, Footer, Flash Alerts, Modal, Scripts)
│   ├── home.html              # Halaman Beranda (Hero, Flipper Photo, Preview, Testimoni)
│   ├── about.html             # Halaman Tentang (Cerita, Purpose, Tab Organisasi & Pendidikan)
│   ├── services.html          # Halaman Layanan & Keahlian (6 Layanan, Alur Kerja, Skill Bar)
│   ├── portfolio.html         # Halaman Portofolio (Filterable Grid 11 Karya Proyek)
│   ├── project_detail.html    # Halaman Detail Proyek Dinamis (/portfolio/<id>)
│   ├── contact.html           # Halaman Kontak & Formulir Interaktif (POST Method)
│   └── 404.html               # Halaman Error 404 Kustom (Slide 13)
│
└── static/                    # Folder file statis (CSS, JS, Media)
    ├── css/
    │   └── style.css          # Stylesheet CSS utama & ekstensi multi-page
    ├── js/
    │   └── main.js            # Skrip JavaScript interaktivitas (Modal, Filter, Flip, Tabs)
    └── assets/                # Aset visual (Foto profil, thumbnail video, logo, QR code)
```

---

## Panduan Menjalankan Aplikasi

### 1. Prasyarat
Pastikan Python 3.9+ dan package manager pip telah terpasang.

### 2. Instalasi Dependensi
Buka Terminal / Command Prompt pada direktori proyek, lalu jalankan:
```bash
pip install -r requirements.txt
```

### 3. Menjalankan Server Flask
Jalankan file utama:
```bash
python app.py
```

Output pada terminal akan menampilkan:
Aplikasi Web Flask Personal Branding aktif di: http://127.0.0.1:5000


### 4. Membuka di Browser
Buka browser favorit Anda (Google Chrome, Edge, Firefox, dsb.) dan akses URL:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## Rincian Endpoint / URL

- `http://127.0.0.1:5000/` : Halaman Beranda
- `http://127.0.0.1:5000/about` : Profil, Cerita, Filosofi, Pengalaman Organisasi & Pendidikan
- `http://127.0.0.1:5000/services` : Layanan Profesional, Alur Kerja, & Software Mastery
- `http://127.0.0.1:5000/portfolio` : Galeri Portofolio & Bukti Kerja
- `http://127.0.0.1:5000/portfolio/<project_id>` : Studi Kasus Proyek Dinamis (contoh: `/portfolio/songgoriti`, `/portfolio/uiux-website-emub`)
- `http://127.0.0.1:5000/contact` : Formulir Kontak Interaktif (GET & POST)
