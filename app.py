import os
import json
import threading
import webbrowser
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = 'faiq-portfolio-secret-key-prolan-ub-2026'

MESSAGES_FILE = os.path.join(os.path.dirname(__file__), 'messages.json')

PERSONAL_INFO = {
    'name': 'Faiq Admaja Wibowo',
    'short_name': 'Faiq AW',
    'nim': '255091107111004',
    'faculty': 'Fakultas Sains, Teknologi, dan Matematika (FSTeM)',
    'university': 'Universitas Brawijaya',
    'major': 'Sains Data (Data Science)',
    'batch': '2025',
    'tagline': "SAINS DATA '25 • UNIVERSITAS BRAWIJAYA",
    'role_title': 'Creative Multimedia & UI/UX Specialist',
    'org_role': 'Staf Ahli Pendayagunaan Teknologi EM UB 2026',
    'hero_lead': 'Mahasiswa Sains Data Universitas Brawijaya & Staf Ahli EM UB 2026. Memadukan presisi komputasi analitis dengan estetika visual Creative Multimedia, Motion Graphics, dan perancangan UI/UX interaktif.',
    'email': 'faiqadmajaw1007@student.ub.ac.id',
    'whatsapp': '+62 813-5847-6770',
    'whatsapp_raw': '6281358476770',
    'linkedin': 'https://www.linkedin.com/in/faiq-admaja-w-bb3a98256',
    'instagram': 'https://www.instagram.com/faiqadmj',
    'instagram_handle': '@faiqadmj',
    'tiktok': 'https://www.tiktok.com/@thisisfaeeq',
    'tiktok_handle': '@thisisfaeeq',
    'gdrive_portfolio': 'https://drive.google.com/drive/folders/1yn4f8Lc5zWV57NYX529mxsbfoa6gn3Wm?usp=drive_link',
    'stats': [
        {'number': '6+', 'label': 'Tahun Kreatif'},
        {'number': '99+', 'label': 'Karya & Proyek'},
        {'number': '98%', 'label': 'Presisi & Estetika'},
        {'number': '100%', 'label': 'Dedikasi Organisasi'}
    ]
}

EXPERIENCE_DATA = [
    {
        'role': 'Wakil Ketua Pelaksana',
        'year': '2026',
        'organization': 'Grand Launching Company Profile & Website EM UB 2026',
        'badge': 'EM UB 2026',
        'points': [
            'Mendampingi ketua pelaksana dalam mengoordinasikan persiapan dan pelaksanaan kegiatan peluncuran akbar.',
            'Memantau progres pekerjaan panitia serta memastikan kesiapan kebutuhan acara sesuai linimasa ketat.',
            'Mengoordinasikan komunikasi lintas divisi (Acara, PDD, Humas, dan Perlengkapan) demi kelancaran kegiatan.'
        ],
        'tags': ['Vice Project Officer', 'Event Management', 'Website Launch', 'EM UB 2026']
    },
    {
        'role': 'Staf Ahli',
        'year': '2026 - Present',
        'organization': 'Kedirjenan Pendayagunaan Teknologi, Kementerian Komunikasi dan Informasi EM UB 2026',
        'badge': 'EM UB 2026',
        'points': [
            'Mendukung perancangan dan pelaksanaan program kerja yang berfokus pada pemanfaatan dan pengembangan teknologi terpadu.',
            'Berkolaborasi aktif dalam riset UI/UX dan arsitektur visual antarmuka Website Resmi EM UB (em.ub.ac.id).',
            'Berkontribusi mendorong inovasi digital, otomasi sistem kerja, dan tata kelola media digital di lingkungan kampus.'
        ],
        'tags': ['UI/UX & Web', 'Digital Solutions', 'Kominfo EM UB', 'Tech Innovation']
    },
    {
        'role': 'Project Lead Media & Motion Graphic',
        'year': '2025 - 2026',
        'organization': 'Campus Expo 2026 - Ikatan Alumni Santri',
        'badge': 'Event Media',
        'points': [
            'Memimpin perancangan bumper animasi panggung LED pembuka (opening video) bertema "Temukan Arahmu, Taklukan Tahtamu".',
            'Mengatur integrasi timeline compositing After Effects dan sequence Premiere Pro untuk visual display panggung.',
            'Menghasilkan identitas visual terpadu untuk konten promosi Instagram, booklet digital, dan merchandise expo.'
        ],
        'tags': ['Motion Design', 'After Effects', 'Stage LED Visuals', 'Creative Lead']
    },
    {
        'role': 'Koordinator Visual & Dokumentasi Media',
        'year': '2023 - 2024',
        'organization': 'Yayasan Pondok Pesantren Progresif Bumi Shalawat',
        'badge': 'Institutional Media',
        'points': [
            'Memproduksi video profil institusional resmi sekolah memadukan nilai keagamaan dan keunggulan sains modern.',
            'Membuat motion graphics display LED dan dokumentasi panggung pada perhelatan akbar Haul & Harlah Yayasan.',
            'Mengoperasikan aerial drone untuk dokumentasi sinematik lanskap kompleks pendidikan dan kegiatan santri.'
        ],
        'tags': ['Video Profil', 'Drone Pilot', 'Haul & Harlah', 'Cinematography']
    }
]

EDUCATION_DATA = [
    {
        'institution': 'Universitas Brawijaya',
        'degree': 'Sarjana (S1) - Program Studi Sains Data',
        'faculty': 'Fakultas Sains, Teknologi, dan Matematika (FSTeM)',
        'period': '2025 - Sekarang',
        'location': 'Malang, Jawa Timur',
        'points': [
            'Fokus studi pada analisis data komputasional, machine learning, visualisasi data, dan rekayasa perangkat lunak.',
            'Aktif sebagai pengurus organisasi kampus (Eksekutif Mahasiswa UB 2026).',
            'Mengintegrasikan ilmu sains data kuantitatif dengan kreativitas perancangan produk digital interaktif.'
        ]
    },
    {
        'institution': 'SMA Progresif Bumi Shalawat',
        'degree': 'Jurusan Matematika dan Ilmu Pengetahuan Alam (MIPA)',
        'period': '2021 - 2024',
        'location': 'Sidoarjo, Jawa Timur',
        'points': [
            'Aktif dalam klub multimedia, sinematografi, dan penelitian karya ilmiah remaja.',
            'Meraih predikat terbaik dalam produksi video dokumenter dan perancangan media komunikasi sekolah.'
        ]
    },
    {
        'institution': 'SMP Progresif Bumi Shalawat',
        'degree': 'Pendidikan Tingkat Menengah Pertama',
        'period': '2018 - 2021',
        'location': 'Sidoarjo, Jawa Timur',
        'points': [
            'Mengembangkan minat awal pada desain grafis digital, animasi komputer, dan logika pemrograman dasar.'
        ]
    }
]

SERVICES_DATA = [
    {
        'id': 'uiux',
        'icon': 'fa-solid fa-bezier-curve',
        'title': 'UI/UX & Product Design',
        'summary': 'Perancangan antarmuka pengguna interaktif, wireframing, high-fidelity design system di Figma berpusat pada kenyamanan pengguna (user-centered design).',
        'deliverables': ['Interactive Prototypes', 'Design Systems & Tokens', 'Wireframes & User Flows', 'Responsive Web & Mobile Layouts'],
        'tools': ['Figma', 'Adobe XD', 'FigJam', 'Whimsical']
    },
    {
        'id': 'video-editing',
        'icon': 'fa-solid fa-film',
        'title': 'Cinematic Video Editing',
        'summary': 'Produksi dan penyuntingan video sinematik dengan alur penceritaan naratif kuat, sound design dinamis, serta color grading berstandar profesional.',
        'deliverables': ['Video Dokumenter & Profil Institusi', 'Cinematic Aftermovies & Teaser', 'Color Grading (LUTs, Rec.709)', 'Audio Mixing & Sound FX'],
        'tools': ['Adobe Premiere Pro', 'DaVinci Resolve', 'Adobe Audition']
    },
    {
        'id': 'motion-graphic',
        'icon': 'fa-solid fa-wand-magic-sparkles',
        'title': 'Motion Graphics & Stage Visuals',
        'summary': 'Pembuatan animasi grafis bergerak, bumper opening panggung LED event skala besar, kinetic typography, dan efek visual 2D/3D kontemporer.',
        'deliverables': ['Opening Bumper Event & Panggung LED', 'Kinetic Typography & Titles', 'Logo Animation & Ident', 'Infographic Video Motion'],
        'tools': ['Adobe After Effects', 'Cinema 4D Elements', 'Adobe Illustrator']
    },
    {
        'id': 'drone-pilot',
        'icon': 'fa-solid fa-helicopter',
        'title': 'Aerial Drone Cinematography',
        'summary': 'Pengambilan gambar dan video udara bersolusi 4K dengan sudut sinematik untuk pemetaan lanskap kampus, dokumentasi pariwisata, dan event akbar.',
        'deliverables': ['4K High-Res Aerial Footages', 'Orbit, Reveal, & Bird-eye Shots', 'Landscape Mapping & Survey', 'Cinematic Real Estate / Venue'],
        'tools': ['DJI Drones 4K', 'LUTs Aerial Profiling', 'Premiere Pro Stabilizer']
    },
    {
        'id': 'data-science',
        'icon': 'fa-solid fa-chart-line',
        'title': 'Python & Data Analytics',
        'summary': 'Pemodelan data analitik menggunakan Python, eksplorasi data kuantitatif, otomasi pengolahan berkas, serta visualisasi data interaktif.',
        'deliverables': ['Exploratory Data Analysis (EDA)', 'Interactive Data Dashboards', 'Script Automation & Scraping', 'Statistical & Predictive Modeling'],
        'tools': ['Python', 'Pandas & NumPy', 'Matplotlib & Seaborn', 'Flask']
    },
    {
        'id': 'social-branding',
        'icon': 'fa-solid fa-palette',
        'title': 'Social Media Feeds & Event Branding',
        'summary': 'Perancangan arsitektur visual feed Instagram, poster promosi, infografis edukatif, serta materi identitas visual untuk organisasi dan kepanitiaan.',
        'deliverables': ['Instagram Feeds & Story Templates', 'Event Posters & Banner Spanduk', 'Digital Booklet & Media Kit', 'Social Media Branding Guidelines'],
        'tools': ['Adobe Photoshop', 'Adobe Illustrator', 'Figma']
    }
]

PROJECTS_DATA = {
    'songgoriti': {
        'id': 'songgoriti',
        'title': 'Songgoriti yang Tak Lagi Suci',
        'category': 'video',
        'category_name': 'Video Editing & Documentary',
        'image': 'assets/project_video_songgoriti.jpg',
        'client': 'Creative Documentary / Independent Film',
        'year': '2025',
        'link': 'https://youtu.be/op1KOrBpuGU?si=GshyVsbx8vNh7ZMP',
        'link_label': 'Tonton di YouTube',
        'tools': 'Adobe Premiere Pro, After Effects, Drone 4K',
        'summary': 'Karya sinematografi dokumenter investigatif mendalam yang mengungkap dinamika sosial dan transformasi kawasan Songgoriti Batu.',
        'desc': 'Karya sinematografi dokumenter investigatif dan visual storytelling mendalam mengenai dinamika sosial, budaya, dan transformasi kawasan Songgoriti, Kota Batu. Mengombinasikan visual sinematik aerial drone dengan narasi wawancara yang kuat dan color grading bertema misterius bernuansa sinematik.',
        'featured': True,
        'highlights': [
            'Color grading atmosferik gelap sinematik',
            'Aerial drone 4K lanskap pegunungan dan sudut urban Songgoriti',
            'Penyusunan alur wawancara jurnalistik dengan pacing dramatik'
        ]
    },
    'surga-bahari': {
        'id': 'surga-bahari',
        'title': 'Surga Bahari Asa Dibalik Lara yang Melanda',
        'category': 'video',
        'category_name': 'Video Editing & Cinematography',
        'image': 'assets/project_video_pujon.jpg',
        'client': 'Sinematografi Dokumenter Bahari',
        'year': '2023',
        'link': 'https://www.youtube.com/watch?v=ati4_mgcoMs',
        'link_label': 'Tonton di YouTube',
        'tools': 'Premiere Pro, Drone Pilot, Color Grading LUTs',
        'summary': 'Karya video dokumenter sinematografi pesisir bahari yang menampilkan bentang keindahan alam laut sekaligus potret keteguhan perjuangan masyarakat di balik tantangan kehidupan.',
        'desc': 'Karya video dokumenter sinematografi pesisir bahari yang menampilkan bentang keindahan alam laut sekaligus potret keteguhan perjuangan masyarakat di balik tantangan kehidupan pesisir.',
        'featured': True,
        'highlights': [
            'Komposisi visual Golden Hour pesisir pantai',
            'Drone bird-eye view perahu nelayan tradisional',
            'Soundscape natural deburan ombak dan audio storytelling'
        ]
    },
    'profil-sma': {
        'id': 'profil-sma',
        'title': 'VIDEO PROFIL SMA PROGRESIF BUMI SHALAWAT 2024',
        'category': 'video',
        'category_name': 'Video Editing & Institutional Branding',
        'image': 'assets/project_video_spiritual.jpg',
        'client': 'SMA Progresif Bumi Shalawat',
        'year': '2024',
        'link': 'https://www.youtube.com/watch?v=4o0sfJnrX54',
        'link_label': 'Tonton di YouTube',
        'tools': 'Premiere Pro, Audition, After Effects',
        'summary': 'Video profil institusional resmi yang merepresentasikan filosofi pendidikan pesantren modern: memadukan kemantapan spiritual santri dengan kecemerlangan intelektual sains dan teknologi.',
        'desc': 'Video profil institusional resmi yang merepresentasikan filosofi pendidikan pesantren modern: memadukan kemantapan spiritual santri dengan kecemerlangan intelektual sains dan teknologi.',
        'featured': False,
        'highlights': [
            'Branding institusional prestisius untuk penerimaan peserta didik baru',
            'Teknik transisi modern seamless match cut',
            'Voice-over rekaman jernih beriringan musik orkestra megah'
        ]
    },
    'campus-motion': {
        'id': 'campus-motion',
        'title': 'CAMPUS EXPO 2026 Opening & Motion Graphic',
        'category': 'motion',
        'category_name': 'Motion Graphic & Kinetic Typography',
        'image': 'assets/project_motion_campusexpo_full.png',
        'client': 'Campus Expo SMA Progresif Bumi Shalawat',
        'year': '2025 - 2026',
        'link': 'https://www.instagram.com/iambshce',
        'link_label': 'Lihat di Instagram',
        'tools': 'After Effects, Illustrator, Cinema 4D Elements',
        'summary': 'Desain visual utama dan animasi motion graphic bumper panggung spektakuler bertajuk "Temukan Arahmu, Taklukan Tahtamu" untuk perhelatan akbar Campus Expo 2026.',
        'desc': 'Desain visual utama dan animasi motion graphic bumper panggung spektakuler bertajuk "Temukan Arahmu, Taklukan Tahtamu" untuk perhelatan akbar Campus Expo 2026.',
        'featured': True,
        'highlights': [
            'Format video disesuaikan dengan rasio panggung LED panggung utama',
            'Kinetic typography dengan akselerasi kurva grafik halus',
            'Visual partikel kosmik dan sinkronisasi audio beat breakdown'
        ]
    },
    'haul-motion': {
        'id': 'haul-motion',
        'title': 'Haul & Harlah Bumi Shalawat 2024',
        'category': 'motion',
        'category_name': 'Motion Graphic & Event Visuals',
        'image': 'assets/project_motion_haul_full.png',
        'client': 'Yayasan Pondok Pesantren Bumi Shalawat',
        'year': '2024',
        'link': 'https://www.youtube.com/watch?v=6V7hBdw_kpk',
        'link_label': 'Tonton di YouTube',
        'tools': 'After Effects, Illustrator, Particle VFX',
        'summary': 'Visual motion display panggung LED dan materi publikasi digital untuk peringatan Haul & Harlah 2024 Pesantren Progresif Bumi Shalawat dengan elemen islami kontemporer bercahaya emas.',
        'desc': 'Visual motion display panggung LED dan materi publikasi digital untuk peringatan Haul & Harlah 2024 Pesantren Progresif Bumi Shalawat dengan elemen islami kontemporer bercahaya emas.',
        'featured': False,
        'highlights': [
            'Elemen kaligrafi dan ornamen geometris bergerak',
            'Efek ambient lighting hangat menyatu dengan tata panggung',
            'Looping seamless untuk latar belakang pembacaan shalawat'
        ]
    },
    'pengaosan-alumni': {
        'id': 'pengaosan-alumni',
        'title': 'Pengaosan Rutin Alumni bersama Gus Aria Muhammad dan IAMBSH',
        'category': 'motion',
        'category_name': 'Motion Graphic & Documentation',
        'image': 'assets/project_motion_alumni.jpg',
        'client': 'Ikatan Alumni Santri & Majelis Pengaosan',
        'year': '2023',
        'link': 'https://www.youtube.com/watch?v=YuQVN3Ic9g8',
        'link_label': 'Tonton di YouTube',
        'tools': 'After Effects, Premiere Pro, Photoshop',
        'summary': 'Dokumentasi sinematik dan motion video panggung untuk acara pengaosan rutin ikatan alumni santri bersama Gus Aria Muhammad dan IAMBSH.',
        'desc': 'Dokumentasi sinematik dan motion video panggung untuk acara pengaosan rutin ikatan alumni santri bersama Gus Aria Muhammad dan IAMBSH.',
        'featured': False,
        'highlights': [
            'Editing dokumentasi multi-kamera',
            'Intro motion bumper eksklusif ikatan alumni',
            'Audio enhancement ceramah yang jernih'
        ]
    },
    'campus-ae-pr': {
        'id': 'campus-ae-pr',
        'title': 'Proses Editing After Effects & Premiere Pro Campus Expo',
        'category': 'motion',
        'category_name': 'Motion Graphic & Post-Production',
        'image': 'assets/project_campusexpo_ae_pr.png',
        'client': 'Campus Expo Production Team',
        'year': '2025',
        'link': 'https://www.instagram.com/iambshce',
        'link_label': 'Lihat di Instagram',
        'tools': 'Adobe After Effects, Adobe Premiere Pro',
        'summary': 'Dokumentasi alur kerja teknis compositing bumper banner Campex di After Effects dan timeline sequence arrangement di Premiere Pro yang presisi.',
        'desc': 'Dokumentasi alur kerja teknis compositing bumper banner Campex di After Effects dan timeline sequence arrangement di Premiere Pro yang presisi.',
        'featured': False,
        'highlights': [
            'Dynamic Link antar software Adobe Creative Cloud',
            'Manajemen layer dan nesting composition terstruktur',
            'Color management LUTs konsisten dari konsep ke output render'
        ]
    },
    'social-emub-feeds': {
        'id': 'social-emub-feeds',
        'title': 'Koleksi Desain Feed Instagram EM UB 2025',
        'category': 'social',
        'category_name': 'Social Media Design',
        'image': 'assets/project_social_emub2025_feeds.png',
        'client': 'Kementerian Komunikasi dan Informasi EM UB 2025',
        'year': '2025',
        'link': 'https://www.instagram.com/em_ubofficial',
        'link_label': 'Kunjungi @em_ubofficial',
        'tools': 'Adobe Illustrator, Figma, Photoshop',
        'summary': 'Rangkaian karya desain visual feed Instagram resmi EM UB 2025 oleh Faiq AW, mencakup Diary Satcita dan Ribuan Memori Tips & Trick Survive Akhir Bulan.',
        'desc': 'Rangkaian karya desain visual feed Instagram resmi EM UB 2025 oleh Faiq AW, mencakup Diary Satcita dan Ribuan Memori Tips & Trick Survive Akhir Bulan dengan engagement tinggi.',
        'featured': True,
        'highlights': [
            'Engagement reach tinggi mencapai puluhan ribu impresi mahasiswa',
            'Tone and manner visual elegan, rapi, dan mudah dicerna',
            'Penggunaan ilustrasi mikro dan tipografi hierarkis'
        ]
    },
    'social-emub-figma': {
        'id': 'social-emub-figma',
        'title': 'Design Bulanan Feeds IG EM UB Bulan Oktober 2025',
        'category': 'social',
        'category_name': 'Social Media Design',
        'image': 'assets/project_social_emub_oktober_figma.png',
        'client': 'Kedirjenan Media Kreatif EM UB',
        'year': '2025',
        'link': 'https://www.instagram.com/em_ubofficial',
        'link_label': 'Kunjungi @em_ubofficial',
        'tools': 'Figma, Design System, Illustrator',
        'summary': 'Perancangan arsitektur visual feed media sosial EM UB bulan Oktober 2025 di Figma: standarisasi layout, aset siap pakai, dan template modul divisi kementerian.',
        'desc': 'Perancangan arsitektur visual feed media sosial EM UB bulan Oktober 2025 di Figma: standarisasi layout, aset siap pakai, dan template modul divisi kementerian.',
        'featured': False,
        'highlights': [
            'Komponen modular autolayout Figma',
            'Penyelarasan palet warna resmi Brawijaya',
            'Efisiensi produksi konten tim media sosial kampus'
        ]
    },
    'uiux-website-emub': {
        'id': 'uiux-website-emub',
        'title': 'UI/UX Website EM UB 2026',
        'category': 'website',
        'category_name': 'App & Web UI/UX',
        'image': 'assets/project_app_2.jpg',
        'client': 'Kedirjenan Pendayagunaan Teknologi EM UB 2026',
        'year': '2026',
        'link': 'https://em.ub.ac.id',
        'link_label': 'Kunjungi em.ub.ac.id',
        'tools': 'Figma, Design System, Wireframing, Prototyping',
        'summary': 'Perancangan antarmuka pengguna (UI) dan alur pengalaman pengguna (UX) Website Resmi Eksekutif Mahasiswa Universitas Brawijaya 2026.',
        'desc': 'Perancangan antarmuka pengguna (UI) dan alur pengalaman pengguna (UX) Website Resmi Eksekutif Mahasiswa Universitas Brawijaya 2026.',
        'featured': True,
        'highlights': [
            'Desain antarmuka responsif ramah perangkat mobile & desktop',
            'Arsitektur informasi advokasi, kementerian, dan database berita terpadu',
            'Interaksi mikro halus dan aksesibilitas kontras WCAG AAA'
        ]
    },
    'portal-website-emub': {
        'id': 'portal-website-emub',
        'title': 'Portal Resmi Website EM UB (Eksekutif Mahasiswa UB 2026)',
        'category': 'website',
        'category_name': 'Website EM UB',
        'image': 'assets/project_web_1.jpg',
        'client': 'Kedirjenan Pendayagunaan Teknologi EM UB',
        'year': '2025 - 2026',
        'link': 'https://em.ub.ac.id',
        'link_label': 'Buka Portal em.ub.ac.id',
        'tools': 'Figma, Modern Web Technologies, Responsive Frameworks',
        'summary': 'Pengembangan dan perancangan Website Resmi Eksekutif Mahasiswa Universitas Brawijaya (em.ub.ac.id) sebagai portal terpadu informasi dan advokasi mahasiswa UB.',
        'desc': 'Pengembangan dan perancangan Website Resmi Eksekutif Mahasiswa Universitas Brawijaya (em.ub.ac.id) sebagai portal terpadu informasi dan advokasi mahasiswa UB.',
        'featured': True,
        'highlights': [
            'Single gateway informasi kemahasiswaan Universitas Brawijaya',
            'Integrasi sistem informasi layanan publik dan aspirasi mahasiswa',
            'Penerapan clean code dan arsitektur web modern performa tinggi'
        ]
    }
}

TESTIMONIALS_DATA = [
    {
        'quote': 'Saya memiliki dedikasi luar biasa dalam merancang UI/UX website resmi em.ub.ac.id. Presisi visual dan pemahamannya terhadap kebutuhan mahasiswa menjadikan antarmuka portal sangat intuitif dan elegan.',
        'name': 'Rekan Kementerian Kominfo',
        'role': 'Eksekutif Mahasiswa Universitas Brawijaya 2026',
        'avatar': 'assets/faiq_almamater_ub.jpg'
    },
    {
        'quote': 'Motion graphic opening panggung dan bumper Campus Expo karya Faiq berhasil menciptakan euforia spektakuler di aula utama. Kecepatan kerja dan ide-ide kreatifnya patut diapresiasi tinggi!',
        'name': 'Ketua Pelaksana Campus Expo',
        'role': 'Ikatan Alumni Santri Bumi Shalawat',
        'avatar': 'assets/faiq_multirole_batik.jpg'
    },
    {
        'quote': 'Kombinasi langka antara logika analitis Sains Data dan kepekaan rasa seni sinematografi. Faiq membuktikan bahwa data dan visual dapat bersinergi melahirkan karya yang kuat dan berdampak.',
        'name': 'Koordinator Tim Media Kreatif',
        'role': 'Sains Data FSTeM Universitas Brawijaya',
        'avatar': 'assets/faiq_avatar.jpg'
    }
]

AWARDS_DATA = [
    {
        'title': 'Apresiasi Tim Pengembang Website Resmi EM UB',
        'issuer': 'Eksekutif Mahasiswa Universitas Brawijaya',
        'year': '2026',
        'desc': 'Penghargaan atas kontribusi perancangan UI/UX dan digitalisasi sistem portal terpadu em.ub.ac.id.'
    },
    {
        'title': 'Sertifikasi Kompetensi Python & Data Science Analytics',
        'issuer': 'Lembaga Pelatihan Nasional & Akademik',
        'year': '2025',
        'desc': 'Sertifikasi kompetensi analisis data, manipulasi dataset, dan pengembangan algoritma pemodelan Python.'
    },
    {
        'title': 'Karya Video Sinematik Terbaik - Dokumenter Investigatif',
        'issuer': 'Festival Karya Sinema Pelajar & Mahasiswa',
        'year': '2024',
        'desc': 'Apresiasi sinematografi dokumenter investigatif atas karya "Songgoriti yang Tak Lagi Suci".'
    }
]

MEDIA_COVERAGE_DATA = [
    {
        'title': 'Grand Launching Company Profile & Portal Terpadu Website EM UB 2026',
        'source': 'Portal Berita Kampus & Media Kominfo UB',
        'date': 'Februari 2026',
        'desc': 'Peluncuran akbar portal resmi em.ub.ac.id sebagai wajah baru digitalisasi organisasi mahasiswa Universitas Brawijaya.',
        'link': 'https://em.ub.ac.id'
    },
    {
        'title': 'Spektakuler! Campus Expo 2026 Memukau Ribuan Peserta dengan Visual Motion Modern',
        'source': 'Publikasi Media Pendidikan & Komunitas Santri',
        'date': 'Januari 2026',
        'desc': 'Sorotan visual motion stage panggung LED karya tim kreatif Faiq AW yang mengangkat tema "Temukan Arahmu, Taklukan Tahtamu".',
        'link': 'https://www.instagram.com/iambshce'
    }
]

def save_contact_message(data):
    messages = []
    if os.path.exists(MESSAGES_FILE):
        try:
            with open(MESSAGES_FILE, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        except Exception:
            messages = []
    
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages.append(data)
    
    try:
        with open(MESSAGES_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        pass

@app.route("/")
@app.route("/home")
def home():
    featured_projects = [p for p in PROJECTS_DATA.values() if p.get('featured', False)]
    return render_template(
        'home.html',
        page='home',
        profile=PERSONAL_INFO,
        services=SERVICES_DATA[:4],
        featured_projects=featured_projects,
        testimonials=TESTIMONIALS_DATA,
        awards=AWARDS_DATA,
        media=MEDIA_COVERAGE_DATA
    )

@app.route("/about")
def about():
    return render_template(
        'about.html',
        page='about',
        profile=PERSONAL_INFO,
        experiences=EXPERIENCE_DATA,
        educations=EDUCATION_DATA
    )

@app.route("/services")
@app.route("/expertise")
def services():
    return render_template(
        'services.html',
        page='services',
        profile=PERSONAL_INFO,
        services=SERVICES_DATA
    )

@app.route("/portfolio")
@app.route("/projects")
def portfolio():
    category_filter = request.args.get('category', 'all')
    if category_filter != 'all':
        projects_list = [p for p in PROJECTS_DATA.values() if p['category'] == category_filter]
    else:
        projects_list = list(PROJECTS_DATA.values())
        
    return render_template(
        'portfolio.html',
        page='portfolio',
        profile=PERSONAL_INFO,
        projects=projects_list,
        current_category=category_filter
    )

@app.route("/portfolio/<project_id>")
def project_detail(project_id):
    project = PROJECTS_DATA.get(project_id)
    if not project:
        abort(404)
        
    other_projects = [p for pid, p in PROJECTS_DATA.items() if pid != project_id][:3]
    
    return render_template(
        'project_detail.html',
        page='portfolio',
        profile=PERSONAL_INFO,
        project=project,
        other_projects=other_projects
    )

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        service = request.form.get("service", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Mohon lengkapi seluruh isian wajib pada formulir!", "error")
            return redirect(url_for('contact'))

        msg_payload = {
            'name': name,
            'email': email,
            'service': service or 'Diskusi Umum',
            'subject': subject or 'Pertanyaan Kolaborasi',
            'message': message
        }
        save_contact_message(msg_payload)

        flash(
            f"Terima kasih, {name}! Pesan Anda mengenai '{subject or 'Kolaborasi'}' telah berhasil terkirim. "
            f"Faiq akan segera membalas ke email ({email}) atau nomor kontak Anda.",
            "success"
        )
        return redirect(url_for('contact'))

    return render_template(
        'contact.html',
        page='contact',
        profile=PERSONAL_INFO
    )

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "Sahabat")
    email = request.form.get("email", "-")
    message = request.form.get("message", "-")
    
    save_contact_message({
        'name': name,
        'email': email,
        'service': 'Quick Form',
        'subject': 'Pesan dari Slide 16 Route',
        'message': message
    })
    
    flash(f"Halo, {name}! Formulir Anda berhasil diterima oleh server Flask.", "success")
    return redirect(url_for('contact'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', page='404', profile=PERSONAL_INFO), 404

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    print("Aplikasi Web Flask Personal Branding aktif di: http://127.0.0.1:5000")
    threading.Timer(1.2, open_browser).start()
    app.run(debug=True, host="127.0.0.1", port=5000)
