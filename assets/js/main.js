/* ── Language switching ──────────────────── */
  const supportedLangs = ['es', 'en'];

  function cleanAnalyticsLabel(value) {
    return String(value || '')
      .toLowerCase()
      .replace(/^www\./, '')
      .replace(/\.(pdf|html?)$/i, '')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '')
      .slice(0, 100);
  }

  function trackEvent(path, title) {
    if (!window.goatcounter || typeof window.goatcounter.count !== 'function') return;

    window.goatcounter.count({
      path,
      title: title || path,
      event: true
    });
  }

  function analyticsEventName(link) {
    const href = link.getAttribute('href');
    let url;
    let filename;

    if (!href || href.charAt(0) === '#' || href.startsWith('mailto:')) return null;

    try {
      url = new URL(href, window.location.href);
    } catch (error) {
      return null;
    }

    filename = url.pathname.split('/').pop() || '';

    if (/\.pdf$/i.test(url.pathname)) {
      return `download-pdf-${cleanAnalyticsLabel(filename || url.pathname)}`;
    }

    if (url.hostname !== window.location.hostname) {
      return `outbound-${cleanAnalyticsLabel(url.hostname)}`;
    }

    return null;
  }

  function setLang(lang, options = {}) {
    if (!supportedLangs.includes(lang)) lang = 'es';
    document.documentElement.lang = lang;
    localStorage.setItem('redesLang', lang);

    document.querySelectorAll('[data-lang]').forEach(node => {
      const active = node.dataset.lang === lang;
      node.hidden = !active;
      node.setAttribute('aria-hidden', active ? 'false' : 'true');
    });

    document.querySelectorAll('[data-aria-label-es][data-aria-label-en]').forEach(node => {
      node.setAttribute('aria-label', node.dataset[`ariaLabel${lang.toUpperCase()}`]);
    });

    document.querySelectorAll('[data-alt-es][data-alt-en]').forEach(node => {
      node.setAttribute('alt', node.dataset[`alt${lang.toUpperCase()}`]);
    });

    document.querySelectorAll('[data-lang-switch]').forEach(btn => {
      const active = btn.dataset.langSwitch === lang;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-pressed', active);
    });

    if (options.track) {
      trackEvent(`language-${lang}`, `Language switched to ${lang.toUpperCase()}`);
    }
  }

  document.querySelectorAll('[data-lang-switch]').forEach(btn => {
    btn.addEventListener('click', () => setLang(btn.dataset.langSwitch, { track: true }));
  });

  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    const eventName = link ? analyticsEventName(link) : null;

    if (eventName) {
      trackEvent(eventName, link.textContent.trim().replace(/\s+/g, ' ').slice(0, 120));
    }
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
  const contactTopic = queryParams.get('topic');
  const contactSubject = document.getElementById('asunto');
  const formsubmitSubject = document.getElementById('formsubmit-subject');
  const topicSubjects = {
    'policy-briefing': {
      es: 'Solicitud de briefing de políticas',
      en: 'Policy briefing request'
    },
    training: {
      es: 'Solicitud de formación',
      en: 'Training session request'
    },
    collaboration: {
      es: 'Propuesta de colaboración',
      en: 'Collaboration proposal'
    },
    media: {
      es: 'Consulta de medios',
      en: 'Media enquiry'
    }
  };

  if (contactStatus && queryParams.get('sent') === '1') {
    contactStatus.hidden = false;
    trackEvent('contact-form-sent', 'Contact form sent');
    history.replaceState(null, '', window.location.pathname);
  }

  if (contactSubject && topicSubjects[contactTopic]) {
    const topic = topicSubjects[contactTopic];
    contactSubject.value = `${topic.es} / ${topic.en}`;
    if (formsubmitSubject) {
      formsubmitSubject.value = `${topic.es} - REDES-IA`;
    }
    document.querySelector(`.contact-purpose-card[href*="topic=${contactTopic}"]`)?.classList.add('is-selected');
    trackEvent(`contact-topic-${contactTopic}`, topic.en);
  }

  document.getElementById('contact-form')?.addEventListener('submit', () => {
    trackEvent('contact-form-submit', 'Contact form submit');
  });

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
