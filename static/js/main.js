// ================================================================
// PREMIUM PORTFOLIO — MAIN JAVASCRIPT
// Vikramaraj M — All Interactive Features
// ================================================================

document.addEventListener('DOMContentLoaded', function() {
  
  // ── LOADING SCREEN ────────────────────────────────────────────
  const loadingScreen = document.getElementById('loading-screen');
  if (loadingScreen && !sessionStorage.getItem('visited')) {
    setTimeout(() => {
      loadingScreen.classList.add('hidden');
      sessionStorage.setItem('visited', 'true');
    }, 1800);
  } else if (loadingScreen) {
    loadingScreen.style.display = 'none';
  }
  
  // ── SCROLL PROGRESS BAR ───────────────────────────────────────
  const scrollProgress = document.getElementById('scroll-progress');
  if (scrollProgress) {
    window.addEventListener('scroll', () => {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const progress = (scrollTop / scrollHeight) * 100;
      scrollProgress.style.width = progress + '%';
    });
  }
  
  // ── NAVBAR SCROLL EFFECT ──────────────────────────────────────
  const navbar = document.querySelector('.navbar-custom');
  if (navbar) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 80) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    });
  }
  
  // ── ACTIVE NAV LINK ON SCROLL ─────────────────────────────────
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link-custom');
  
  function highlightNav() {
    const scrollY = window.pageYOffset;
    
    sections.forEach(section => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop - 100;
      const sectionId = section.getAttribute('id');
      
      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
          }
        });
      }
    });
  }
  
  window.addEventListener('scroll', highlightNav);
  
  // ── DARK/LIGHT MODE TOGGLE ────────────────────────────────────
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;
  
  // Load saved theme
  const savedTheme = localStorage.getItem('theme') || 'dark';
  html.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);
  
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = html.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }
  
  function updateThemeIcon(theme) {
    if (themeToggle) {
      const icon = themeToggle.querySelector('i');
      if (icon) {
        icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
      }
    }
  }

  
  // ── TYPEWRITER EFFECT (HERO ROLE) ─────────────────────────────
  const roleElement = document.querySelector('.hero-role');
  if (roleElement) {
    const roles = [
      'Data Engineer',
      'ML Enthusiast',
      'Python Developer',
      'BI Developer'
    ];
    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    
    function typeWriter() {
      const currentRole = roles[roleIndex];
      
      if (isDeleting) {
        roleElement.textContent = currentRole.substring(0, charIndex - 1);
        charIndex--;
      } else {
        roleElement.textContent = currentRole.substring(0, charIndex + 1);
        charIndex++;
      }
      
      let typeSpeed = isDeleting ? 50 : 100;
      
      if (!isDeleting && charIndex === currentRole.length) {
        typeSpeed = 2000; // Pause at end
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
        typeSpeed = 500; // Pause before next word
      }
      
      setTimeout(typeWriter, typeSpeed);
    }
    
    typeWriter();
  }
  
  // ── COUNT-UP ANIMATION (STATS) ────────────────────────────────
  const statNumbers = document.querySelectorAll('.stat-num');
  
  function animateCount(element) {
    const target = element.textContent;
    const numMatch = target.match(/\d+/);
    if (!numMatch) return;
    
    const targetNum = parseInt(numMatch[0]);
    const suffix = target.replace(/\d+/, '');
    const duration = 2000;
    const increment = targetNum / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
      current += increment;
      if (current >= targetNum) {
        element.textContent = targetNum + suffix;
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current) + suffix;
      }
    }, 16);
  }
  
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
        animateCount(entry.target);
        entry.target.classList.add('counted');
      }
    });
  }, { threshold: 0.5 });
  
  statNumbers.forEach(stat => statsObserver.observe(stat));
  
  // ── SKILL BAR ANIMATION ───────────────────────────────────────
  const skillFills = document.querySelectorAll('.skill-fill');
  
  const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const width = entry.target.getAttribute('data-width');
        entry.target.style.width = width + '%';
      }
    });
  }, { threshold: 0.3 });
  
  skillFills.forEach(fill => skillObserver.observe(fill));
  
  // ── SKILL TABS FILTER ─────────────────────────────────────────
  const skillTabs = document.querySelectorAll('.skill-tab');
  const skillCategories = document.querySelectorAll('.skill-category');
  
  skillTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const filter = tab.getAttribute('data-filter');
      
      // Update active tab
      skillTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      
      // Filter categories
      skillCategories.forEach(cat => {
        if (filter === 'all' || cat.getAttribute('data-category') === filter) {
          cat.style.display = 'block';
          cat.classList.add('fade-in');
        } else {
          cat.style.display = 'none';
        }
      });
    });
  });
  
  // ── PROJECT FILTER ────────────────────────────────────────────
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');
  
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.getAttribute('data-filter');
      
      // Update active button
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      // Filter projects
      projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.classList.remove('hidden');
          card.style.animation = 'fadeIn 0.5s ease';
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });

  
  // ── CERTIFICATION MODAL ───────────────────────────────────────
  const certCards = document.querySelectorAll('.cert-card');
  const modalOverlay = document.getElementById('cert-modal');
  const modalClose = document.querySelector('.modal-close');
  
  certCards.forEach(card => {
    card.addEventListener('click', (e) => {
      // Don't open topics modal if clicking the thumbnail (opens fullscreen instead)
      if (e.target.closest('.cert-thumb-wrapper')) return;

      const certName     = card.getAttribute('data-cert-name');
      const certPlatform = card.getAttribute('data-cert-platform');
      const topics       = JSON.parse(card.getAttribute('data-topics') || '[]');
      const imageUrl     = card.getAttribute('data-image') || '';
      
      // Update modal content
      document.getElementById('modal-cert-name').textContent     = certName;
      document.getElementById('modal-cert-platform').textContent = certPlatform;
      
      // Show/hide certificate image
      const imgWrap = document.getElementById('modal-cert-image-wrap');
      const imgEl   = document.getElementById('modal-cert-image');
      if (imageUrl) {
        imgEl.src = imageUrl;
        imgWrap.style.display = 'block';
      } else {
        imgWrap.style.display = 'none';
        imgEl.src = '';
      }

      const topicList = document.getElementById('modal-topics');
      topicList.innerHTML = '';
      
      if (topics.length > 0) {
        document.getElementById('modal-topics-section').style.display = 'block';
        topics.forEach((topic, index) => {
          const li = document.createElement('li');
          li.className = 'topic-item';
          li.innerHTML = `
            <span class="topic-number">${index + 1}</span>
            <span>${topic}</span>
          `;
          topicList.appendChild(li);
        });
      } else {
        document.getElementById('modal-topics-section').style.display = imageUrl ? 'none' : 'block';
        topicList.innerHTML = '<li class="topic-item"><span class="text-soft">No topics listed</span></li>';
      }
      
      // Show modal
      modalOverlay.classList.add('active');
    });

    // Thumbnail click → fullscreen
    const thumb = card.querySelector('.cert-thumb-wrapper');
    if (thumb) {
      thumb.addEventListener('click', (e) => {
        e.stopPropagation();
        const imageUrl = card.getAttribute('data-image') || '';
        if (imageUrl) openCertFullscreen(imageUrl);
      });
    }
  });
  
  // Close modal
  if (modalClose) {
    modalClose.addEventListener('click', () => {
      modalOverlay.classList.remove('active');
    });
  }
  
  if (modalOverlay) {
    modalOverlay.addEventListener('click', (e) => {
      if (e.target === modalOverlay) {
        modalOverlay.classList.remove('active');
      }
    });
  }

  // ── FULLSCREEN CERTIFICATE VIEWER ─────────────────────────────
  window.openCertFullscreen = function(src) {
    const overlay = document.getElementById('cert-fullscreen');
    const img     = document.getElementById('cert-fullscreen-img');
    img.src = src;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  window.closeCertFullscreen = function() {
    const overlay = document.getElementById('cert-fullscreen');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  };

  // Close fullscreen on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeCertFullscreen();
      if (modalOverlay) modalOverlay.classList.remove('active');
    }
  });
  
  // ── BACK TO TOP BUTTON ────────────────────────────────────────
  const backToTop = document.getElementById('back-to-top');
  
  if (backToTop) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        backToTop.classList.add('visible');
      } else {
        backToTop.classList.remove('visible');
      }
    });
    
    backToTop.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
  
  // ── SMOOTH SCROLL FOR ANCHOR LINKS ────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#' && href !== '#!') {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });
  
  // ── PARTICLES.JS INITIALIZATION ───────────────────────────────
  if (typeof particlesJS !== 'undefined') {
    particlesJS('particles-js', {
      particles: {
        number: {
          value: 80,
          density: {
            enable: true,
            value_area: 800
          }
        },
        color: {
          value: '#58A6FF'
        },
        shape: {
          type: 'circle'
        },
        opacity: {
          value: 0.5,
          random: false
        },
        size: {
          value: 3,
          random: true
        },
        line_linked: {
          enable: true,
          distance: 150,
          color: '#58A6FF',
          opacity: 0.2,
          width: 1
        },
        move: {
          enable: true,
          speed: 2,
          direction: 'none',
          random: false,
          straight: false,
          out_mode: 'out',
          bounce: false
        }
      },
      interactivity: {
        detect_on: 'canvas',
        events: {
          onhover: {
            enable: true,
            mode: 'grab'
          },
          onclick: {
            enable: true,
            mode: 'push'
          },
          resize: true
        },
        modes: {
          grab: {
            distance: 140,
            line_linked: {
              opacity: 0.5
            }
          },
          push: {
            particles_nb: 4
          }
        }
      },
      retina_detect: true
    });
  }
  
  // ── AOS (ANIMATE ON SCROLL) INITIALIZATION ────────────────────
  if (typeof AOS !== 'undefined') {
    AOS.init({
      duration: 800,
      easing: 'ease-in-out',
      once: true,
      offset: 100
    });
  }
  
});

// ================================================================
// END OF MAIN.JS
// ================================================================
