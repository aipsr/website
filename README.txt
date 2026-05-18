REDES-IA hybrid website draft

Build workflow:
- Edit shared chrome in _includes/:
  - head.html
  - main-nav.html
  - main-footer.html
  - workshop-nav.html
  - workshop-footer.html
  - logo.svg.html
- Edit page titles, descriptions and active nav state in scripts/build_site.py.
- Run `python3 scripts/build_site.py` after changing shared chrome.
- The root .html files remain deployable static files; the script refreshes the managed `build:` blocks and regenerates `robots.txt` and `sitemap.xml`.

This package contains:
- index.html: revised single-file website using the agreed hybrid direction.
- images/members/optimized/: member portrait assets referenced by the HTML.
- netlify.toml: portable Netlify configuration for static deployment.

Design direction applied:
- Option 4 refined palette: teal #047F78, terracotta #C85F42, dark base #242B2E, soft neutral #F4F1F0.
- Serif/sans pairing: Source Serif 4 for major headings; Inter for navigation, body, cards, buttons and UI.
- Muted, warmer hero treatment preserving the team-photo concept.
- More restrained institutional cards, metrics, badges and section hierarchy.
- Revised inline logo mark combining institutional and network/AI motifs.

Note: the hero image is still referenced from the hosted URL in the original HTML. If you want a fully self-contained deploy, replace that URL with a local file path and add the image to this package.
