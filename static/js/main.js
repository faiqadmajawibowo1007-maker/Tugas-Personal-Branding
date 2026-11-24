document.documentElement.classList.add('js-ready');

document.addEventListener('DOMContentLoaded', () => {

  initNavbarAndScroll();
  initPhotoFlipper();
  initScrollAnimations();
  initTiltEffect();
  initJourneyTabs();
  initProjectFiltering();
  initProjectModal();
  initSkillBars();
  initContactActions();
  initAudioEffects();
});

function initBackgroundCanvas() {
  return;
  const canvas = document.getElementById('canvas-bg');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let width, height;
  let particles = [];
  const particleCount = window.innerWidth < 768 ? 35 : 75;
  const connectDistance = window.innerWidth < 768 ? 90 : 130;
  let mouse = { x: null, y: null, radius: 150 };

  function resize() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener('resize', resize);

  window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
  });

  class Particle {
    constructor() {
      this.x = Math.random() * width;
      this.y = Math.random() * height;
      this.vx = (Math.random() - 0.5) * 0.6;
      this.vy = (Math.random() - 0.5) * 0.6;
      this.size = Math.random() * 2 + 1;
      this.baseColor = Math.random() > 0.4 ? '0, 242, 254' : '30, 91, 198';
      this.alpha = Math.random() * 0.5 + 0.2;
    }

    update() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.x < 0 || this.x > width) this.vx *= -1;
      if (this.y < 0 || this.y > height) this.vy *= -1;

      if (mouse.x !== null && mouse.y !== null) {
        let dx = mouse.x - this.x;
        let dy = mouse.y - this.y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < mouse.radius) {
          let force = (mouse.radius - dist) / mouse.radius;
          this.x -= (dx / dist) * force * 1.5;
          this.y -= (dy / dist) * force * 1.5;
        }
      }
    }

    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${this.baseColor}, ${this.alpha})`;
      ctx.shadowBlur = 8;
      ctx.shadowColor = `rgba(${this.baseColor}, 0.8)`;
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }

  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }

  function render() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        let dx = particles[i].x - particles[j].x;
        let dy = particles[i].y - particles[j].y;
        let dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < connectDistance) {
          let opacity = (1 - dist / connectDistance) * 0.25;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(0, 242, 254, ${opacity})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    if (mouse.x !== null && mouse.y !== null) {
      for (let i = 0; i < particles.length; i++) {
        let dx = mouse.x - particles[i].x;
        let dy = mouse.y - particles[i].y;
        let dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < connectDistance * 1.2) {
          let opacity = (1 - dist / (connectDistance * 1.2)) * 0.45;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(mouse.x, mouse.y);
          ctx.strokeStyle = `rgba(0, 242, 254, ${opacity})`;
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }
    }

    particles.forEach(p => {
      p.update();
      p.draw();
    });

    requestAnimationFrame(render);
  }

  render();
}

function initCustomCursor() {
  return;
  const dot = document.querySelector('.custom-cursor-dot');
  const ring = document.querySelector('.custom-cursor-ring');
  if (!dot || !ring) return;

  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;
  let ringX = mouseX;
  let ringY = mouseY;

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    dot.style.transform = `translate3d(${mouseX}px, ${mouseY}px, 0) translate(-50%, -50%)`;
  });

  function animateRing() {
    ringX += (mouseX - ringX) * 0.16;
    ringY += (mouseY - ringY) * 0.16;
    ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0) translate(-50%, -50%)`;
    requestAnimationFrame(animateRing);
  }
  animateRing();

  const hoverTargets = 'a, button, .project-card, .tab-btn, .filter-btn, .software-card, .contact-channel-item, .bento-card';
  document.querySelectorAll(hoverTargets).forEach(el => {
    el.addEventListener('mouseenter', () => document.body.classList.add('cursor-hover'));
    el.addEventListener('mouseleave', () => document.body.classList.remove('cursor-hover'));
  });
}

function initNavbarAndScroll() {
  const navbar = document.querySelector('.navbar');
  const progressBar = document.querySelector('.scroll-progress-bar');
  const backToTopBtn = document.querySelector('.back-to-top');
  const navItems = document.querySelectorAll('.nav-item');
  const sections = document.querySelectorAll('section[id]');
  const mobileMenuBtn = document.querySelector('#mobileMenuBtn') || document.querySelector('.mobile-menu-btn');
  const mobileDrawer = document.querySelector('#mobileDrawer');
  const mobileBackdrop = document.querySelector('#mobileBackdrop');
  const drawerCloseBtn = document.querySelector('#drawerCloseBtn');
  const drawerLinks = document.querySelectorAll('.drawer-link, .drawer-btn-cta');

  function openDrawer() {
    if (mobileDrawer) mobileDrawer.classList.add('open');
    if (mobileBackdrop) mobileBackdrop.classList.add('open');
    if (mobileMenuBtn) mobileMenuBtn.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeDrawer() {
    if (mobileDrawer) mobileDrawer.classList.remove('open');
    if (mobileBackdrop) mobileBackdrop.classList.remove('open');
    if (mobileMenuBtn) mobileMenuBtn.classList.remove('active');
    document.body.style.overflow = '';
  }

  if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (mobileDrawer && mobileDrawer.classList.contains('open')) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });
  }

  if (drawerCloseBtn) {
    drawerCloseBtn.addEventListener('click', closeDrawer);
  }

  if (mobileBackdrop) {
    mobileBackdrop.addEventListener('click', closeDrawer);
  }

  drawerLinks.forEach(link => {
    link.addEventListener('click', () => {
      closeDrawer();
    });
  });

  document.querySelectorAll('.nav-item a').forEach(a => {
    a.addEventListener('click', () => {
      closeDrawer();
    });
  });

  window.addEventListener('scroll', () => {
    const scrollY = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = docHeight > 0 ? (scrollY / docHeight) * 100 : 0;

    if (progressBar) {
      progressBar.style.width = `${progress}%`;
    }

    if (navbar) {
      if (scrollY > 40) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }

    if (backToTopBtn) {
      if (scrollY > 500) {
        backToTopBtn.classList.add('visible');
      } else {
        backToTopBtn.classList.remove('visible');
      }
    }

    let currentId = '';
    sections.forEach(sec => {
      const top = sec.offsetTop - 140;
      const height = sec.offsetHeight;
      if (scrollY >= top && scrollY < top + height) {
        currentId = sec.getAttribute('id');
      }
    });

    if (navbar) {
      if (currentId === 'journey' || currentId === 'contact') {
        navbar.classList.add('nav-on-dark');
        navbar.classList.remove('nav-on-light');
      } else {
        navbar.classList.add('nav-on-light');
        navbar.classList.remove('nav-on-dark');
      }
    }

    navItems.forEach(item => {
      item.classList.remove('active');
      const href = item.querySelector('a')?.getAttribute('href');
      if (href === `#${currentId}`) {
        item.classList.add('active');
      }
    });

    document.querySelectorAll('.drawer-link').forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  window.dispatchEvent(new Event('scroll'));
}

function initTiltEffect() {
  const card = document.querySelector('.tilt-card-wrapper');
  if (!card) return;

  const cardFrame = card.querySelector('.glow-frame');
  const badges = card.querySelectorAll('.floating-badge');

  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const rotateX = ((y - centerY) / centerY) * -12;
    const rotateY = ((x - centerX) / centerX) * 12;

    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;

    badges.forEach((badge, idx) => {
      const depth = idx === 0 ? 30 : -25;
      badge.style.transform = `translateZ(${depth}px) translateY(${rotateX * 0.8}px) translateX(${rotateY * 0.8}px)`;
    });
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
    badges.forEach((badge) => {
      badge.style.transform = '';
    });
  });
}

function initJourneyTabs() {
  const tabs = document.querySelectorAll('.tab-btn');
  const views = document.querySelectorAll('.timeline-view');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetId = tab.dataset.target;
      tabs.forEach(t => t.classList.remove('active'));
      views.forEach(v => v.classList.remove('active'));

      tab.classList.add('active');
      const targetView = document.getElementById(targetId);
      if (targetView) targetView.classList.add('active');
    });
  });
}

function initProjectFiltering() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const cards = document.querySelectorAll('.project-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;

      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      cards.forEach(card => {
        const category = card.dataset.category;
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
          card.style.animation = 'fadeIn 0.4s ease forwards';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

const projectDetails = {
  'songgoriti': {
    title: 'Songgoriti yang Tak Lagi Suci',
    category: 'Video Editing & Documentary',
    image: '/static/assets/project_video_songgoriti.jpg',
    client: 'Creative Documentary / Independent Film',
    year: '2025',
    link: 'https://youtu.be/op1KOrBpuGU?si=GshyVsbx8vNh7ZMP',
    tools: 'Adobe Premiere Pro, After Effects, Drone 4K',
    desc: 'Karya sinematografi dokumenter investigatif dan visual storytelling mendalam mengenai dinamika sosial, budaya, dan transformasi kawasan Songgoriti, Kota Batu. Mengombinasikan visual sinematik aerial drone dengan narasi wawancara yang kuat dan color grading bertema misterius bernuansa sinematik.'
  },
  'surga-bahari': {
    title: 'Surga Bahari Asa Dibalik Lara yang Melanda',
    category: 'Video Editing & Cinematography',
    image: '/static/assets/project_video_pujon.jpg',
    client: 'Sinematografi Dokumenter Bahari',
    year: '2023',
    link: 'https://www.youtube.com/watch?v=ati4_mgcoMs',
    tools: 'Premiere Pro, Drone Pilot, Color Grading LUTs',
    desc: 'Karya video dokumenter sinematografi pesisir bahari yang menampilkan bentang keindahan alam laut sekaligus potret keteguhan perjuangan masyarakat di balik tantangan kehidupan pesisir.'
  },
  'profil-sma': {
    title: 'VIDEO PROFIL SMA PROGRESIF BUMI SHALAWAT 2024',
    category: 'Video Editing & Institutional Branding',
    image: '/static/assets/project_video_spiritual.jpg',
    client: 'SMA Progresif Bumi Shalawat',
    year: '2024',
    link: 'https://www.youtube.com/watch?v=4o0sfJnrX54',
    tools: 'Premiere Pro, Audition, After Effects',
    desc: 'Video profil institusional resmi yang merepresentasikan filosofi pendidikan pesantren modern: memadukan kemantapan spiritual santri dengan kecemerlangan intelektual sains dan teknologi.'
  },
  'campus-motion': {
    title: 'CAMPUS EXPO 2026 Opening & Motion Graphic',
    category: 'Motion Graphic & Kinetic Typography',
    image: '/static/assets/project_motion_campusexpo_full.png',
    client: 'Campus Expo SMA Progresif Bumi Shalawat',
    year: '2025 - 2026',
    link: 'https://www.instagram.com/iambshce',
    tools: 'After Effects, Illustrator, Cinema 4D Elements',
    desc: 'Desain visual utama dan animasi motion graphic bumper panggung spektakuler bertajuk "Temukan Arahmu, Taklukan Tahtamu" untuk perhelatan akbar Campus Expo 2026.'
  },
  'haul-motion': {
    title: 'Haul & Harlah Bumi Shalawat 2024',
    category: 'Motion Graphic & Event Visuals',
    image: '/static/assets/project_motion_haul_full.png',
    client: 'Yayasan Pondok Pesantren Bumi Shalawat',
    year: '2024',
    link: 'https://www.youtube.com/watch?v=6V7hBdw_kpk',
    tools: 'After Effects, Illustrator, Particle VFX',
    desc: 'Visual motion display panggung LED dan materi publikasi digital untuk peringatan Haul & Harlah 2024 Pesantren Progresif Bumi Shalawat dengan elemen islami kontemporer bercahaya emas.'
  },
  'pengaosan-alumni': {
    title: 'Pengaosan Rutin Alumni bersama Gus Aria Muhammad dan IAMBSH',
    category: 'Motion Graphic & Documentation',
    image: '/static/assets/project_motion_alumni.jpg',
    client: 'Ikatan Alumni Santri & Majelis Pengaosan',
    year: '2023',
    link: 'https://www.youtube.com/watch?v=YuQVN3Ic9g8',
    tools: 'After Effects, Premiere Pro, Photoshop',
    desc: 'Dokumentasi sinematik dan motion video panggung untuk acara pengaosan rutin ikatan alumni santri bersama Gus Aria Muhammad dan IAMBSH.'
  },
  'campus-ae-pr': {
    title: 'Proses Editing After Effects & Premiere Pro Campus Expo',
    category: 'Motion Graphic & Post-Production',
    image: '/static/assets/project_campusexpo_ae_pr.png',
    client: 'Campus Expo Production Team',
    year: '2025',
    link: 'https://www.instagram.com/iambshce',
    tools: 'Adobe After Effects, Adobe Premiere Pro',
    desc: 'Dokumentasi alur kerja teknis compositing bumper banner Campex di After Effects dan timeline sequence arrangement di Premiere Pro yang presisi.'
  },
  'social-emub-feeds': {
    title: 'Koleksi Desain Feed Instagram EM UB 2025',
    category: 'Social Media Design',
    image: '/static/assets/project_social_emub2025_feeds.png',
    client: 'Kementerian Komunikasi dan Informasi EM UB 2025',
    year: '2025',
    link: 'https://www.instagram.com/em_ubofficial',
    tools: 'Adobe Illustrator, Figma, Photoshop',
    desc: 'Rangkaian karya desain visual feed Instagram resmi EM UB 2025 oleh Faiq AW, mencakup #Diary Satcita dan Ribuan Memori Tips & Trick Survive Akhir Bulan dengan engagement tinggi.'
  },
  'social-emub-figma': {
    title: 'Design Bulanan Feeds IG EM UB Bulan Oktober 2025',
    category: 'Social Media Design',
    image: '/static/assets/project_social_emub_oktober_figma.png',
    client: 'Kedirjenan Media Kreatif EM UB',
    year: '2025',
    link: 'https://www.instagram.com/em_ubofficial',
    tools: 'Figma, Design System, Illustrator',
    desc: 'Perancangan arsitektur visual feed media sosial EM UB bulan Oktober 2025 di Figma: standarisasi layout, aset siap pakai, dan template modul divisi kementerian.'
  },
  'uiux-website-emub': {
    title: 'UI/UX Website EM UB 2026',
    category: 'App & Web UI/UX',
    image: '/static/assets/project_app_2.jpg',
    client: 'Kedirjenan Pendayagunaan Teknologi EM UB 2026',
    year: '2026',
    link: 'https://em.ub.ac.id',
    tools: 'Figma, Design System, Wireframing, Prototyping',
    desc: 'Perancangan antarmuka pengguna (UI) dan alur pengalaman pengguna (UX) Website Resmi Eksekutif Mahasiswa Universitas Brawijaya 2026.'
  },
  'portal-website-emub': {
    title: 'Portal Resmi Website EM UB (Eksekutif Mahasiswa UB 2026)',
    category: 'Website EM UB',
    image: '/static/assets/project_web_1.jpg',
    client: 'Kedirjenan Pendayagunaan Teknologi EM UB',
    year: '2025 - 2026',
    link: 'https://em.ub.ac.id',
    tools: 'Figma, Modern Web Technologies, Responsive Frameworks',
    desc: 'Pengembangan dan perancangan Website Resmi Eksekutif Mahasiswa Universitas Brawijaya (em.ub.ac.id) sebagai portal terpadu informasi dan advokasi mahasiswa UB.'
  }
};

function initProjectModal() {
  const modal = document.querySelector('.project-modal');
  const modalCloseBtn = document.querySelector('.modal-close-btn');
  const cards = document.querySelectorAll('.project-card');

  if (!modal) return;

  const modalImg = modal.querySelector('.modal-img');
  const modalBadge = modal.querySelector('.modal-category-badge');
  const modalTitle = modal.querySelector('.modal-title');
  const modalDesc = modal.querySelector('.modal-description');
  const modalClient = modal.querySelector('#modal-client');
  const modalYear = modal.querySelector('#modal-year');
  const modalTools = modal.querySelector('#modal-tools');
  const modalLinkBtn = modal.querySelector('#modal-link-btn');

  cards.forEach(card => {

    const directBtn = card.querySelector('.project-direct-btn');
    if (directBtn) {
      directBtn.addEventListener('click', (e) => {
        e.stopPropagation();
      });
    }

    const thumbWrapper = card.querySelector('.project-thumbnail-wrapper');
    const titleElem = card.querySelector('.project-title');

    const openDetails = () => {
      const id = card.dataset.id;
      const data = projectDetails[id];
      if (!data) return;

      modalImg.src = data.image;
      modalImg.alt = data.title;
      modalBadge.textContent = data.category;
      modalTitle.textContent = data.title;
      modalDesc.textContent = data.desc;
      if (modalClient) modalClient.textContent = data.client;
      if (modalYear) modalYear.textContent = data.year;
      if (modalTools) modalTools.textContent = data.tools;

      if (modalLinkBtn) {
        if (data.link) {
          modalLinkBtn.href = data.link;
          modalLinkBtn.style.display = 'inline-flex';
          modalLinkBtn.innerHTML = `<span>Buka Link Proyek / Tonton</span> <i class="fa-solid fa-arrow-up-right-from-square"></i>`;
        } else {
          modalLinkBtn.style.display = 'none';
        }
      }

      modal.classList.add('open');
      document.body.style.overflow = 'hidden';
    };

    if (thumbWrapper) thumbWrapper.addEventListener('click', openDetails);
    if (titleElem) titleElem.addEventListener('click', openDetails);
  });

  function closeModal() {
    modal.classList.remove('open');
    document.body.style.overflow = '';
  }

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }

  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });

  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) {
      closeModal();
    }
  });
}

function initSkillBars() {
  const skillSection = document.querySelector('.skills-section');
  const fills = document.querySelectorAll('.skill-progress-fill');

  if (!skillSection || fills.length === 0) return;

  let animated = false;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !animated) {
        fills.forEach(fill => {
          const target = fill.dataset.percent;
          fill.style.width = `${target}%`;
        });
        animated = true;
      }
    });
  }, { threshold: 0.25 });

  observer.observe(skillSection);
}

function initContactActions() {
  const toast = document.querySelector('.toast-notice');
  const toastMsg = document.querySelector('.toast-msg');

  function showToast(message) {
    if (!toast) return;
    if (toastMsg) toastMsg.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 2800);
  }

  document.querySelectorAll('.action-btn-copy').forEach(btn => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.dataset.copy;
      if (!textToCopy) return;

      navigator.clipboard.writeText(textToCopy).then(() => {
        showToast(`Tersalin ke papan klip: ${textToCopy}`);
      }).catch(() => {

        const textarea = document.createElement('textarea');
        textarea.value = textToCopy;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast(`Tersalin ke papan klip: ${textToCopy}`);
      });
    });
  });

  const sendBtn = document.querySelector('.btn-send-wa');
  const msgInput = document.querySelector('.input-quick-msg');

  if (sendBtn && msgInput) {
    const handleSend = () => {
      const msg = msgInput.value.trim();
      const defaultText = 'Halo Faiq AW, saya melihat portofolio Anda dan tertarik untuk berdiskusi/berkolaborasi!';
      const text = msg.length > 0 ? encodeURIComponent(msg) : encodeURIComponent(defaultText);
      const url = `https://wa.me/6281358476770?text=${text}`;
      window.open(url, '_blank');
    };

    sendBtn.addEventListener('click', handleSend);
    msgInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleSend();
    });
  }

  const scanQrBtn = document.querySelector('#btn-scan-qr');
  const qrFrame = document.querySelector('.qr-card-frame');

  if (scanQrBtn && qrFrame) {
    scanQrBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetUrl = scanQrBtn.getAttribute('href');
      
      qrFrame.classList.add('scanning-active');
      showToast('Memindai QR Barcode Portfolio...');

      setTimeout(() => {
        qrFrame.classList.remove('scanning-active');
        if (targetUrl) {
          window.open(targetUrl, '_blank');
        }
      }, 750);
    });
  }
}

function initAudioEffects() {
  let audioCtx = null;
  let soundEnabled = false;

  const audioBtn = document.querySelector('.audio-toggle-btn');
  const icon = audioBtn?.querySelector('i');

  function playTone(freq, duration, type = 'sine', gainVal = 0.04) {
    if (!soundEnabled) return;
    try {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }

      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = type;
      osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
      gain.gain.setValueAtTime(gainVal, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start();
      osc.stop(audioCtx.currentTime + duration);
    } catch (e) {

    }
  }

  if (audioBtn) {
    audioBtn.addEventListener('click', () => {
      soundEnabled = !soundEnabled;
      if (soundEnabled) {
        if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        audioCtx.resume();
        playTone(660, 0.12, 'sine', 0.05);
        if (icon) icon.className = 'fa-solid fa-volume-high';
        audioBtn.style.color = 'var(--accent-cyan)';
        audioBtn.style.borderColor = 'var(--accent-cyan)';
      } else {
        if (icon) icon.className = 'fa-solid fa-volume-xmark';
        audioBtn.style.color = '';
        audioBtn.style.borderColor = '';
      }
    });
  }

  const clickables = document.querySelectorAll('button, .project-card, .tab-btn, .filter-btn, .nav-item a');
  clickables.forEach(el => {
    el.addEventListener('mouseenter', () => {
      if (soundEnabled) playTone(440, 0.05, 'triangle', 0.02);
    });
    el.addEventListener('click', () => {
      if (soundEnabled) playTone(880, 0.08, 'sine', 0.05);
    });
  });
}

function initScrollAnimations() {

  const sections = document.querySelectorAll('.scroll-fade-section');
  if (sections.length > 0) {
    function checkSections() {
      sections.forEach(sec => {
        const rect = sec.getBoundingClientRect();
        if (rect.top < window.innerHeight * 0.9 && rect.bottom > 0) {
          sec.classList.add('is-visible');
        }
      });
    }

    const sectionObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    }, {
      threshold: 0.05,
      rootMargin: '0px 0px -40px 0px'
    });

    sections.forEach(sec => sectionObserver.observe(sec));
    window.addEventListener('scroll', checkSections, { passive: true });
    checkSections();
  }

  const targetSelectors = [
    '.section-header',
    '.bento-card',
    '.timeline-card',
    '.project-card',
    '.software-card',
    '.skills-box',
    '.contact-left-card',
    '.contact-right-card'
  ];

  const elements = document.querySelectorAll(targetSelectors.join(', '));
  elements.forEach((el, index) => {
    el.classList.add('reveal-on-scroll');
    const staggerIndex = (index % 5) + 1;
    el.classList.add(`stagger-${staggerIndex}`);
  });

  const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-revealed');
      }
    });
  }, {
    threshold: 0.05,
    rootMargin: '0px 0px -40px 0px'
  });

  elements.forEach(el => cardObserver.observe(el));
}

function initPhotoFlipper() {
  const flipperCard = document.getElementById('flipperCard');
  const showcaseSec = document.getElementById('profile');
  if (!flipperCard || !showcaseSec) return;

  let flipped = false;

  function checkFlip() {
    const rect = showcaseSec.getBoundingClientRect();
    const winH = window.innerHeight;

    if (rect.top < winH * 0.7 && rect.bottom > winH * 0.2) {
      if (!flipped) {
        flipperCard.classList.add('is-flipped');
        flipped = true;
      }
    } else if (rect.top >= winH * 0.85) {

      if (flipped) {
        flipperCard.classList.remove('is-flipped');
        flipped = false;
      }
    }
  }

  flipperCard.addEventListener('click', () => {
    flipperCard.classList.toggle('is-flipped');
    flipped = flipperCard.classList.contains('is-flipped');
  });

  window.addEventListener('scroll', checkFlip, { passive: true });
  window.addEventListener('resize', checkFlip, { passive: true });
  checkFlip();
}
