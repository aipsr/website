REDES-IA contact form

The static contact page submits to a Google Apps Script web app owned by
redes-ia@ibei.org. It emails the enquiry to that mailbox and sends a fixed
confirmation to the visitor in the selected language (es, ca or en).

Source: Code.gs in this directory.
Apps Script project:
https://script.google.com/home/projects/1OCMqNm2F0eyDyUvKu5MbZ5LcQ6T3lAwLEgiocYkUOEfF8G1HA3xlTh2g/edit

The web app executes as redes-ia@ibei.org and permits anonymous requests.
Requests require a valid reCAPTCHA for redes-ia.org, validated server-side.
RECAPTCHA_SECRET is stored only in Apps Script properties, never in GitHub.
The source also checks field sizes, recipient syntax, a honeypot, sending quota,
and a maximum of 100 enquiries per UTC day, with one per sender per minute.

To change the email text, edit COPY in Code.gs and copy the source into the
Apps Script project. Save, then update the existing deployment to a NEW version
through Deploy > Manage deployments. Preserve its URL. A GitHub push alone does
not update Apps Script. testDelivery sends the three confirmations to the
REDES-IA mailbox from the Apps Script editor and is not a public endpoint.

The form endpoint is configured in contacto.html. Client validation and the
language field are handled by assets/js/contact-form.js. The shared head and
scripts/build_site.py preserve the contact page's Google-specific CSP settings.
