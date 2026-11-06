/** Deploy from redes-ia@ibei.org, executing as owner, accessible to anyone.
 * Set RECAPTCHA_SECRET in Script Properties. Never put the secret in the website.
 */
const CONTACT_EMAIL = 'redes-ia@ibei.org';
const COPY = {
  es: { subject: 'Hemos recibido tu mensaje | REDES-IA', body: 'Gracias por contactar con REDES-IA. Hemos recibido tu mensaje y nos pondremos en contacto contigo a la mayor brevedad.', success: 'Gracias. Hemos recibido tu mensaje.', error: 'No hemos podido confirmar el envío. Inténtalo de nuevo o escribe a redes-ia@ibei.org.', back: 'Volver al formulario' },
  ca: { subject: 'Hem rebut el teu missatge | REDES-IA', body: 'Gràcies per contactar amb REDES-IA. Hem rebut el teu missatge i ens posarem en contacte amb tu tan aviat com sigui possible.', success: 'Gràcies. Hem rebut el teu missatge.', error: 'No hem pogut confirmar l’enviament. Torna-ho a provar o escriu a redes-ia@ibei.org.', back: 'Tornar al formulari' },
  en: { subject: 'We have received your message | REDES-IA', body: 'Thank you for contacting REDES-IA. We have received your message and will get back to you as soon as possible.', success: 'Thank you. We have received your message.', error: 'We could not confirm delivery. Please try again or email redes-ia@ibei.org.', back: 'Back to the form' }
};

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]));
}

function resultPage(lang, sent) {
  const text = COPY[lang];
  return HtmlService.createHtmlOutput('<!doctype html><html lang="' + lang + '"><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>REDES-IA</title></head><body style="font:18px/1.6 system-ui,sans-serif;color:#242b2e;background:#f4f1f0;padding:3rem 1rem"><main style="max-width:38rem;margin:auto"><h1>REDES-IA</h1><p>' + escapeHtml(sent ? text.success : text.error) + '</p><p><a target="_top" style="color:#047f78" href="https://redes-ia.org/contacto.html?lang=' + lang + '">' + escapeHtml(text.back) + '</a></p></main></body></html>').setTitle('REDES-IA').addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function doGet() { return resultPage('es', false); }

/** Owner-only editor check: sends test confirmations to our own mailbox. */
function testDelivery() {
  if (Session.getEffectiveUser().getEmail().toLowerCase() !== CONTACT_EMAIL) throw new Error('Wrong sending account');
  ['es', 'ca', 'en'].forEach(lang => MailApp.sendEmail({ to: CONTACT_EMAIL, replyTo: CONTACT_EMAIL, name: 'REDES-IA', subject: '[PRUEBA ' + lang.toUpperCase() + '] ' + COPY[lang].subject, body: COPY[lang].body + '\n\nREDES-IA\nhttps://redes-ia.org/' }));
  console.log('Three test confirmations sent to the REDES-IA mailbox.');
}

function doPost(event) {
  const p = event && event.parameter || {};
  const lang = Object.prototype.hasOwnProperty.call(COPY, p.idioma) ? p.idioma : 'es';
  let lock;
  try {
    if (Session.getEffectiveUser().getEmail().toLowerCase() !== CONTACT_EMAIL) throw new Error('Wrong sending account');
    if (p._honey || !p.nombre || !p.mensaje || !p.email) return resultPage(lang, false);
    if (p.nombre.length > 150 || p.mensaje.length > 10000 || (p.asunto || '').length > 200) return resultPage(lang, false);
    if (p.email.length > 254 || !/^[^\s@,;<>]+@[^\s@,;<>]+\.[^\s@,;<>]+$/.test(p.email)) return resultPage(lang, false);
    const secret = PropertiesService.getScriptProperties().getProperty('RECAPTCHA_SECRET');
    const token = p['g-recaptcha-response'];
    if (!secret || !token || token.length > 8192) return resultPage(lang, false);
    const verification = UrlFetchApp.fetch('https://www.google.com/recaptcha/api/siteverify', { method: 'post', payload: { secret: secret, response: token } });
    const captcha = JSON.parse(verification.getContentText());
    if (!captcha.success || !['redes-ia.org', 'www.redes-ia.org'].includes(captcha.hostname)) return resultPage(lang, false);
    lock = LockService.getScriptLock();
    if (!lock.tryLock(10000)) return resultPage(lang, false);
    const cache = CacheService.getScriptCache();
    const key = Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, p.email.toLowerCase()));
    const day = Utilities.formatDate(new Date(), 'UTC', 'yyyy-MM-dd');
    const properties = PropertiesService.getScriptProperties();
    const counter = JSON.parse(properties.getProperty('CONTACT_DAY_COUNT') || '{}');
    const total = counter.day === day ? Number(counter.count || 0) : 0;
    if (cache.get('recent:' + key) || total >= 100 || MailApp.getRemainingDailyQuota() < 2) return resultPage(lang, false);
    // Reserve before sending, so concurrent submissions cannot bypass limits.
    cache.put('recent:' + key, '1', 60);
    properties.setProperty('CONTACT_DAY_COUNT', JSON.stringify({ day: day, count: total + 1 }));
    MailApp.sendEmail({
      to: CONTACT_EMAIL,
      replyTo: p.email,
      name: 'REDES-IA · Formulario web',
      subject: 'Consulta web REDES-IA' + (p.asunto ? ': ' + p.asunto.replace(/[\r\n]/g, ' ') : ''),
      body: 'Nombre: ' + p.nombre + '\nEmail: ' + p.email + '\nIdioma: ' + lang + '\nAsunto: ' + (p.asunto || '') + '\n\n' + p.mensaje
    });
    MailApp.sendEmail({ to: p.email, replyTo: CONTACT_EMAIL, name: 'REDES-IA', subject: COPY[lang].subject, body: COPY[lang].body + '\n\nREDES-IA\nhttps://redes-ia.org/' });
    return resultPage(lang, true);
  } catch (error) {
    // Do not log names, addresses, message contents, or CAPTCHA tokens.
    console.error('Contact form delivery failed');
    return resultPage(lang, false);
  } finally {
    if (lock && lock.hasLock()) lock.releaseLock();
  }
}
