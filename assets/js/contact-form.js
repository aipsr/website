(() => {
  const form = document.getElementById('contact-form');
  const captcha = document.getElementById('contact-captcha');
  const feedback = document.getElementById('contact-captcha-feedback');
  if (!form || !captcha) return;

  const languages = ['es', 'ca', 'en'];
  const language = () => languages.includes(document.documentElement.lang) ? document.documentElement.lang : 'es';
  let widget;
  window.onContactCaptchaLoad = () => {
    widget = window.grecaptcha.render(captcha, {
      sitekey: captcha.dataset.sitekey,
      size: captcha.clientWidth < 304 ? 'compact' : 'normal',
      callback: () => { feedback.hidden = true; }
    });
  };

  form.addEventListener('submit', event => {
    document.getElementById('contact-language').value = language();
    if (widget === undefined || !window.grecaptcha.getResponse(widget)) {
      event.preventDefault();
      feedback.hidden = false;
      feedback.scrollIntoView({ block: 'nearest' });
    }
  });

  const api = document.createElement('script');
  api.src = 'https://www.google.com/recaptcha/api.js?onload=onContactCaptchaLoad&render=explicit&hl=' + language();
  api.async = true;
  api.defer = true;
  document.head.appendChild(api);
})();
