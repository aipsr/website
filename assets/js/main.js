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

  /* ── Contact form ────────────────────────── */
  const contactForm = document.getElementById('contact-form');

  contactForm?.addEventListener('submit', event => {
    event.preventDefault();

    const formData = new FormData(contactForm);
    const name = formData.get('nombre')?.toString().trim() || '';
    const email = formData.get('email')?.toString().trim() || '';
    const subject = formData.get('asunto')?.toString().trim() || 'Mensaje desde la web REDES-IA';
    const message = formData.get('mensaje')?.toString().trim() || '';

    const body = [
      `Nombre: ${name}`,
      `Email: ${email}`,
      '',
      message
    ].join('\n');

    const mailto = new URL('mailto:redes-aipsr@gmail.com');
    mailto.searchParams.set('subject', subject);
    mailto.searchParams.set('body', body);
    window.location.href = mailto.toString();
  });

  /* ── Init ────────────────────────────────── */
  const savedLang = localStorage.getItem('redesLang');
  const browserLang = navigator.language?.toLowerCase().startsWith('en') ? 'en' : 'es';
  setLang(supportedLangs.includes(savedLang) ? savedLang : browserLang);

  if (window.location.hash === '#analisis') {
    history.replaceState(null, '', '#politicas');
    document.getElementById('politicas')?.scrollIntoView();
  }