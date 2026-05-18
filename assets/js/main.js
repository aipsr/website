/* ── Language switching ──────────────────── */
  const supportedLangs = ['es', 'en'];

  function setLang(lang) {
    if (!supportedLangs.includes(lang)) lang = 'es';
    document.documentElement.lang = lang;
    localStorage.setItem('redesLang', lang);

    document.querySelectorAll('[data-lang-switch]').forEach(btn => {
      const active = btn.dataset.langSwitch === lang;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-pressed', active);
    });
  }

  document.querySelectorAll('[data-lang-switch]').forEach(btn => {
    btn.addEventListener('click', () => setLang(btn.dataset.langSwitch));
  });

  /* ── Mobile menu ─────────────────────────── */
  const menuBtn   = document.getElementById('mobile-menu-btn');
  const mobileNav = document.getElementById('mobile-nav');

  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', () => {
      const open = mobileNav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open);
    });

    document.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', () => {
        mobileNav.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', false);
      });
    });
  }

  /* ── Contact form ────────────────────────── */
  const contactStatus = document.getElementById('contact-form-status');
  const queryParams = new URLSearchParams(window.location.search);

  if (contactStatus && queryParams.get('sent') === '1') {
    contactStatus.hidden = false;
    history.replaceState(null, '', window.location.pathname);
  }

  /* ── Init ────────────────────────────────── */
  const savedLang = localStorage.getItem('redesLang');
  const browserLang = navigator.language?.toLowerCase().startsWith('en') ? 'en' : 'es';
  setLang(supportedLangs.includes(savedLang) ? savedLang : browserLang);

  if (window.location.hash === '#analisis') {
    history.replaceState(null, '', '#politicas');
    document.getElementById('politicas')?.scrollIntoView();
  }
