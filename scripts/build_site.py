#!/usr/bin/env python3
"""Render shared head, nav, and footer partials into the static HTML pages.

The site intentionally stays deployable as plain static HTML. This script only
keeps repeated chrome centralized in _includes/.
"""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INCLUDES = ROOT / "_includes"
SITE_URL = "https://redes-ia.org"
DEFAULT_DESCRIPTION = (
    "Red de investigadores en ciencias sociales que analiza la inteligencia "
    "artificial y propone soluciones de política pública."
)
DEFAULT_DESCRIPTION_CA = (
    "Xarxa d'investigadors en ciències socials que analitza la intel·ligència "
    "artificial i proposa solucions de política pública."
)
DEFAULT_DESCRIPTION_EN = (
    "A social science research network that analyses artificial intelligence "
    "and proposes public policy solutions."
)
DEFAULT_OG_TITLE = "REDES-IA — Políticas públicas para la transición a la IA"
DEFAULT_OG_IMAGE = "images/hero/optimized/hero-team-working.jpg"
DEFAULT_OG_IMAGE_ALT = "Red de investigación REDES-IA sobre inteligencia artificial y políticas públicas"

NAV = [
    ("index", "index.html", "Inicio", "Inici", "Main"),
    ("miembros", "miembros.html", "Quiénes somos", "Qui som", "About us"),
    ("actividades", "actividades.html", "Actividades", "Activitats", "Activities"),
    ("politicas", "politicas.html", "Políticas", "Polítiques", "Policies"),
    ("formacion", "formacion.html", "Formación", "Formació", "Training"),
    ("medios", "medios.html", "En medios", "Als mitjans", "In the media"),
    ("contacto", "contacto.html", "Contacto", "Contacte", "Contact"),
]

PAGES = {
    "index.html": {
        "layout": "main",
        "active": "index",
        "title": "REDES-IA — Políticas públicas para la transición a la IA",
        "description": "REDES-IA conecta investigación en ciencias sociales, instituciones y sociedad civil para orientar políticas públicas sobre la transición a la inteligencia artificial.",
        "description_ca": "REDES-IA connecta la recerca en ciències socials, institucions i societat civil per orientar polítiques públiques sobre la transició a la intel·ligència artificial.",
        "description_en": "REDES-IA connects social science research, institutions and civil society to inform public policy on the transition to artificial intelligence.",
    },
    "miembros.html": {
        "layout": "main",
        "active": "miembros",
        "title": "Quiénes somos — REDES-IA",
        "description": "Conoce REDES-IA, una red de investigación que analiza las implicaciones sociales, económicas y políticas de la inteligencia artificial y propone respuestas de política pública.",
        "description_ca": "Coneix REDES-IA, una xarxa de recerca que analitza les implicacions socials, econòmiques i polítiques de la intel·ligència artificial i proposa respostes de política pública.",
        "description_en": "Meet REDES-IA, a research network that analyses the social, economic and political implications of artificial intelligence and develops public policy responses.",
    },
    "actividades.html": {
        "layout": "main",
        "active": "actividades",
        "title": "Actividades — REDES-IA",
        "description": "Seminarios, talleres y jornadas de REDES-IA sobre inteligencia artificial, ciencias sociales, gobernanza, economía política y políticas públicas.",
        "description_ca": "Seminaris, tallers i jornades de REDES-IA sobre intel·ligència artificial, ciències socials, governança, economia política i polítiques públiques.",
        "description_en": "REDES-IA seminars, workshops and conferences on artificial intelligence, social science, governance, political economy and public policy.",
    },
    "politicas.html": {
        "layout": "main",
        "active": "politicas",
        "title": "Políticas — REDES-IA",
        "description": "Policy briefs y recomendaciones de REDES-IA para instituciones y responsables políticos sobre la transición a la inteligencia artificial.",
        "description_ca": "Documents de política pública i recomanacions de REDES-IA per a institucions i responsables polítics sobre la transició a la intel·ligència artificial.",
        "description_en": "REDES-IA policy briefs and recommendations for institutions and policymakers on the transition to artificial intelligence.",
    },
    "formacion.html": {
        "layout": "main",
        "active": "formacion",
        "title": "Formación — REDES-IA",
        "description": "Formaciones de REDES-IA sobre impacto de la inteligencia artificial, economía, políticas públicas y herramientas de IA para ciencias sociales.",
        "description_ca": "Formacions de REDES-IA sobre l'impacte de la intel·ligència artificial, economia, polítiques públiques i eines d'IA per a les ciències socials.",
        "description_en": "REDES-IA training on the impact of artificial intelligence, economics, public policy and AI tools for social science.",
    },
    "medios.html": {
        "layout": "main",
        "active": "medios",
        "title": "En los medios — REDES-IA",
        "description": "Artículos y contribuciones públicas de REDES-IA sobre inteligencia artificial, automatización, empleo, desigualdad y políticas tecnológicas.",
        "description_ca": "Articles i contribucions públiques de REDES-IA sobre intel·ligència artificial, automatització, ocupació, desigualtat i polítiques tecnològiques.",
        "description_en": "Public articles and contributions from REDES-IA on artificial intelligence, automation, employment, inequality and technology policy.",
    },
    "contacto.html": {
        "layout": "main",
        "active": "contacto",
        "title": "Contacto — REDES-IA",
        "description": "Contacta con REDES-IA para colaboraciones, actividades, formaciones o consultas sobre investigación y políticas públicas de inteligencia artificial.",
        "description_ca": "Contacta amb REDES-IA per a col·laboracions, activitats, formacions o consultes sobre recerca i polítiques públiques d'intel·ligència artificial.",
        "description_en": "Contact REDES-IA for collaborations, activities, training or enquiries about artificial intelligence research and public policy.",
    },
    "formacion-herramientas-ia.html": {
        "layout": "main",
        "active": "formacion",
        "title": "Diez formas de usar IA agéntica en la investigación académica — REDES-IA",
        "description": "Diez usos concretos de la IA agéntica en investigación académica y ciencias sociales, desde síntesis de literatura hasta código, documentación y docencia.",
        "description_ca": "Deu usos concrets de la IA agèntica en la recerca acadèmica i les ciències socials, des de la síntesi de literatura fins al codi, la documentació i la docència.",
        "description_en": "Ten concrete uses of agentic AI in academic research and social science workflows, from literature synthesis to code, documentation and teaching.",
        "og_title": "Diez formas de usar IA agéntica en la investigación académica — REDES-IA",
        "og_description": "Diez usos concretos de la IA agéntica en investigación académica y ciencias sociales.",
    },
    "formacion-impacto-ia.html": {
        "layout": "main",
        "active": "formacion",
        "title": "Impacto de la IA en el mercado laboral — REDES-IA",
        "description": "Formación de REDES-IA sobre el impacto de la inteligencia artificial en el mercado laboral, la distribución de la riqueza y las respuestas de política pública.",
        "description_ca": "Formació de REDES-IA sobre l'impacte de la intel·ligència artificial en el mercat laboral, la distribució de la riquesa i les respostes de política pública.",
        "description_en": "REDES-IA training on the impact of artificial intelligence on the labour market, wealth distribution and public policy responses.",
        "og_title": "Impacto de la IA en el mercado laboral — REDES-IA",
        "og_description": "Consecuencias y posibles vías de acción ante el impacto de la IA en el mercado laboral.",
    },
    "workshop-1-llms.html": {
        "layout": "workshop",
        "title": "Workshop sobre LLMs y análisis de textos políticos | REDES-IA",
        "description": "Programa del workshop sobre grandes modelos de lenguaje y análisis de textos políticos.",
        "description_ca": "Programa del workshop sobre grans models de llenguatge i anàlisi de textos polítics.",
        "description_en": "Programme for the workshop on large language models and political text analysis.",
        "event_name": "Workshop sobre LLMs y análisis de textos políticos",
        "event_start": "2024-01-21",
        "event_location": "Barcelona",
    },
    "workshop-2-ai.html": {
        "layout": "workshop",
        "title": "Workshop sobre IA y política | REDES-IA",
        "description": "Programa del workshop sobre IA y política, opinión pública, economía política y comunicación política.",
        "description_ca": "Programa del workshop sobre IA i política, opinió pública, economia política i comunicació política.",
        "description_en": "Programme for the workshop on AI and politics, public opinion, political economy and political communication.",
        "event_name": "Workshop sobre IA y política",
        "event_start": "2024-12-03",
        "event_location": "Facultat de Dret, Universitat de Barcelona",
    },
    "workshop-3-politics-of-ai.html": {
        "layout": "workshop",
        "title": "Workshop 2: Política de la IA | REDES-IA",
        "description": "Programa del workshop The Politics of AI: Actors, Policy, Geopolitics, and Resistances.",
        "description_ca": "Programa del workshop The Politics of AI: Actors, Policy, Geopolitics, and Resistances.",
        "description_en": "Programme for The Politics of AI workshop: actors, policy, geopolitics and resistances.",
        "event_name": "The Politics of AI: Actors, Policy, Geopolitics, and Resistances",
        "event_start": "2025-10-02",
        "event_end": "2025-10-03",
        "event_location": "Barcelona",
    },
}


def read_include(name: str) -> str:
    return (INCLUDES / name).read_text(encoding="utf-8").strip()


def render_template(template: str, context: dict[str, str]) -> str:
    rendered = template
    for key, value in context.items():
        rendered = rendered.replace("{{ " + key + " }}", value)
    return rendered


def managed(name: str, body: str) -> str:
    return f"<!-- build:{name} -->\n{body}\n<!-- /build:{name} -->"


def replace_managed(content: str, name: str, replacement: str) -> str | None:
    pattern = re.compile(
        rf"<!-- build:{re.escape(name)} -->[\s\S]*?<!-- /build:{re.escape(name)} -->"
    )
    if pattern.search(content):
        return pattern.sub(replacement, content, count=1)
    return None


def render_head(meta: dict[str, str]) -> str:
    layout = meta["layout"]
    stylesheet = "assets/css/workshop.css" if layout == "workshop" else "assets/css/styles.css"
    stylesheets = f'<link rel="stylesheet" href="{stylesheet}">'
    description = meta.get("description", DEFAULT_DESCRIPTION)
    description_ca = meta.get("description_ca", DEFAULT_DESCRIPTION_CA)
    description_en = meta.get("description_en", DEFAULT_DESCRIPTION_EN)
    canonical_url = canonical_for(meta["filename"])
    alternate_ca_url = f"{canonical_url}?lang=ca"
    alternate_en_url = f"{canonical_url}?lang=en"
    og_description = meta.get("og_description", description)
    context = {
        "title": html.escape(meta["title"], quote=True),
        "description": html.escape(description, quote=True),
        "description_es": html.escape(description, quote=True),
        "description_ca": html.escape(description_ca, quote=True),
        "description_en": html.escape(description_en, quote=True),
        "og_title": html.escape(meta.get("og_title", meta["title"]), quote=True),
        "og_description": html.escape(og_description, quote=True),
        "og_image": html.escape(absolute_url(meta.get("og_image", DEFAULT_OG_IMAGE)), quote=True),
        "og_image_alt": html.escape(meta.get("og_image_alt", DEFAULT_OG_IMAGE_ALT), quote=True),
        "canonical_url": html.escape(canonical_url, quote=True),
        "alternate_es_url": html.escape(canonical_url, quote=True),
        "alternate_ca_url": html.escape(alternate_ca_url, quote=True),
        "alternate_en_url": html.escape(alternate_en_url, quote=True),
        "stylesheets": stylesheets,
        "structured_data": render_structured_data(meta, canonical_url, description),
    }
    return managed("head", render_template(read_include("head.html"), context))


def render_structured_data(meta: dict[str, str], canonical_url: str, description: str) -> str:
    filename = meta["filename"]
    data: list[dict[str, object]] = [
        organization_schema(),
        breadcrumb_schema(filename, meta["title"], canonical_url),
    ]

    if filename == "index.html":
        data.append(website_schema())

    if meta["layout"] == "workshop":
        data.append(event_schema(meta, canonical_url, description))

    return "\n  ".join(
        '<script type="application/ld+json">'
        + json.dumps(item, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
        for item in data
    )


def organization_schema() -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{SITE_URL}/#organization",
        "name": "REDES-IA",
        "url": f"{SITE_URL}/",
        "logo": absolute_url("images/logo/png/redes-ia-icon.png"),
        "description": DEFAULT_DESCRIPTION,
        "email": "mailto:redes.aipsr@gmail.com",
        "sameAs": [],
    }


def website_schema() -> dict[str, object]:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE_URL}/#website",
        "name": "REDES-IA",
        "url": f"{SITE_URL}/",
        "publisher": {"@id": f"{SITE_URL}/#organization"},
        "inLanguage": ["es", "ca", "en"],
    }


def breadcrumb_schema(filename: str, title: str, canonical_url: str) -> dict[str, object]:
    items: list[dict[str, object]] = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Inicio",
            "item": f"{SITE_URL}/",
        }
    ]

    if filename != "index.html":
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": title.split("—")[0].split("|")[0].strip(),
                "item": canonical_url,
            }
        )

    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def event_schema(meta: dict[str, str], canonical_url: str, description: str) -> dict[str, object]:
    event: dict[str, object] = {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": meta.get("event_name", meta["title"]),
        "description": description,
        "url": canonical_url,
        "startDate": meta["event_start"],
        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
        "eventStatus": "https://schema.org/EventScheduled",
        "organizer": {"@id": f"{SITE_URL}/#organization"},
        "location": {
            "@type": "Place",
            "name": meta.get("event_location", "Barcelona"),
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Barcelona",
                "addressCountry": "ES",
            },
        },
    }

    if "event_end" in meta:
        event["endDate"] = meta["event_end"]

    return event


def absolute_url(path: str) -> str:
    if path.startswith(("http://", "https://")):
        return path
    return f"{SITE_URL}/{path.lstrip('/')}"


def canonical_for(filename: str) -> str:
    path = "" if filename == "index.html" else filename
    return f"{SITE_URL}/{path}"


def render_main_nav(active: str) -> str:
    logo_svg = read_include("logo.svg.html")
    nav_items = []
    mobile_items = []
    for key, href, es, ca, en in NAV:
        current = ' aria-current="page"' if key == active else ""
        nav_items.append(
            f'<li><a href="{href}"{current}><span data-lang="es" aria-hidden="false">{es}</span>'
            f'<span data-lang="ca" hidden aria-hidden="true">{ca}</span>'
            f'<span data-lang="en" hidden aria-hidden="true">{en}</span></a></li>'
        )
        mobile_items.append(
            f'<li><a class="mobile-nav-link" href="{href}"><span data-lang="es" aria-hidden="false">{es}</span>'
            f'<span data-lang="ca" hidden aria-hidden="true">{ca}</span>'
            f'<span data-lang="en" hidden aria-hidden="true">{en}</span></a></li>'
        )
    return managed(
        "nav",
        render_template(
            read_include("main-nav.html"),
            {
                "logo_svg": logo_svg,
                "nav_items": "\n      ".join(nav_items),
                "mobile_nav_items": "\n    ".join(mobile_items),
            },
        ),
    )


def render_workshop_nav() -> str:
    return managed(
        "nav",
        render_template(read_include("workshop-nav.html"), {"logo_svg": read_include("logo.svg.html")}),
    )


def render_footer(layout: str) -> str:
    include = "workshop-footer.html" if layout == "workshop" else "main-footer.html"
    return managed(
        "footer",
        render_template(read_include(include), {"logo_svg": read_include("logo.svg.html")}),
    )


def replace_head(content: str, head: str) -> str:
    updated = replace_managed(content, "head", head)
    if updated is not None:
        return updated
    return re.sub(r"<head>[\s\S]*?</head>", f"<head>\n{head}\n</head>", content, count=1)


def replace_nav(content: str, meta: dict[str, str], nav: str) -> str:
    updated = replace_managed(content, "nav", nav)
    if updated is not None:
        return updated

    start = content.find('<nav class="site-nav"')
    if start == -1:
        raise ValueError("Could not find site nav")

    if meta["layout"] == "workshop":
        end = content.find("</nav>", start)
        if end == -1:
            raise ValueError("Could not find workshop nav end")
        end += len("</nav>")
    else:
        end_candidates = [
            content.find("\n\n\n<!--", start),
            content.find("\n\n<section", start),
        ]
        end_candidates = [idx for idx in end_candidates if idx != -1]
        if not end_candidates:
            raise ValueError("Could not find main nav end")
        end = min(end_candidates)

    return content[:start] + nav + content[end:]


def replace_footer(content: str, layout: str, footer: str) -> str:
    updated = replace_managed(content, "footer", footer)
    if updated is not None:
        return updated
    klass = "footer" if layout == "workshop" else "site-footer"
    pattern = re.compile(rf"<footer class=\"{klass}\">[\s\S]*?</footer>")
    if not pattern.search(content):
        raise ValueError(f"Could not find {klass} footer")
    return pattern.sub(footer, content, count=1)


def set_default_language_state(content: str) -> str:
    """Ship the static HTML with Spanish visible and other languages hidden."""

    def normalize(match: re.Match[str]) -> str:
        tag = match.group(0)
        lang = match.group(1)
        tag = re.sub(r"\s+hidden\b", "", tag)
        tag = re.sub(r'\s+aria-hidden="[^"]*"', "", tag)
        if lang == "es":
            return tag.replace(">", ' aria-hidden="false">')
        return tag.replace(">", ' hidden aria-hidden="true">')

    return re.sub(r'<span data-lang="(es|ca|en)"[^>]*>', normalize, content)


def build_page(filename: str, meta: dict[str, str]) -> None:
    path = ROOT / filename
    meta = {**meta, "filename": filename}
    content = path.read_text(encoding="utf-8")
    content = replace_head(content, render_head(meta))
    nav = render_workshop_nav() if meta["layout"] == "workshop" else render_main_nav(meta["active"])
    content = replace_nav(content, meta, nav)
    content = replace_footer(content, meta["layout"], render_footer(meta["layout"]))
    content = set_default_language_state(content)
    path.write_text(content, encoding="utf-8")


def write_seo_files() -> None:
    today = date.today().isoformat()
    sitemap_urls = [
        "  <url>\n"
        f"    <loc>{canonical_for(filename)}</loc>\n"
        f"    <lastmod>{today}</lastmod>\n"
        "  </url>"
        for filename in PAGES
    ]
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(sitemap_urls)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")

    robots = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")


def main() -> None:
    for filename, meta in PAGES.items():
        build_page(filename, meta)
    write_seo_files()
    print(f"Rendered {len(PAGES)} pages.")


if __name__ == "__main__":
    main()
