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
    const focusableSelector = 'a[href], button:not([disabled])';
    const getMobileFocusable = () => Array.from(mobileNav.querySelectorAll(focusableSelector));

    function closeMenu() {
      mobileNav.classList.remove('open');
      mobileNav.setAttribute('aria-hidden', 'true');
      menuBtn.setAttribute('aria-expanded', 'false');
    }

    function openMenu() {
      mobileNav.classList.add('open');
      mobileNav.setAttribute('aria-hidden', 'false');
      menuBtn.setAttribute('aria-expanded', 'true');
      getMobileFocusable()[0]?.focus();
    }

    menuBtn.addEventListener('click', () => {
      mobileNav.classList.contains('open') ? closeMenu() : openMenu();
    });

    document.querySelectorAll('.mobile-nav-link').forEach(link => {
      link.addEventListener('click', closeMenu);
    });

    document.addEventListener('keydown', event => {
      if (!mobileNav.classList.contains('open')) return;

      if (event.key === 'Escape') {
        closeMenu();
        menuBtn.focus();
        return;
      }

      if (event.key !== 'Tab') return;

      const focusable = getMobileFocusable();
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
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
  const requestedLang = queryParams.get('lang');
  const savedLang = localStorage.getItem('redesLang');
  const browserLang = navigator.language?.toLowerCase().startsWith('en') ? 'en' : 'es';
  setLang(
    supportedLangs.includes(requestedLang) ? requestedLang :
    supportedLangs.includes(savedLang) ? savedLang :
    browserLang
  );

  if (window.location.hash === '#analisis') {
    history.replaceState(null, '', '#politicas');
    document.getElementById('politicas')?.scrollIntoView();
  }
