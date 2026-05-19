#!/usr/bin/env python3
"""Render shared head, nav, and footer partials into the static HTML pages.

The site intentionally stays deployable as plain static HTML. This script only
keeps repeated chrome centralized in _includes/.
"""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INCLUDES = ROOT / "_includes"
SITE_URL = "https://redes-ia.org"
DEFAULT_DESCRIPTION = (
    "Red de investigadores en ciencias sociales que analiza la inteligencia "
    "artificial y propone soluciones de política pública."
)
DEFAULT_DESCRIPTION_EN = (
    "A social science research network that analyses artificial intelligence "
    "and proposes public policy solutions."
)
DEFAULT_OG_TITLE = "REDES-IA — Políticas públicas para la transición a la IA"
DEFAULT_OG_IMAGE = "images/hero/optimized/hero-team-working.jpg"

NAV = [
    ("index", "index.html", "Inicio", "Main"),
    ("miembros", "miembros.html", "Miembros", "Members"),
    ("actividades", "actividades.html", "Actividades", "Activities"),
    ("politicas", "politicas.html", "Políticas", "Policies"),
    ("formacion", "formacion.html", "Formación", "Training"),
    ("medios", "medios.html", "En medios", "In the media"),
    ("contacto", "contacto.html", "Contacto", "Contact"),
]

PAGES = {
    "index.html": {
        "layout": "main",
        "active": "index",
        "title": "REDES-IA — Políticas públicas para la transición a la IA",
        "description": "REDES-IA conecta investigación en ciencias sociales, instituciones y sociedad civil para orientar políticas públicas sobre la transición a la inteligencia artificial.",
        "description_en": "REDES-IA connects social science research, institutions and civil society to inform public policy on the transition to artificial intelligence.",
    },
    "miembros.html": {
        "layout": "main",
        "active": "miembros",
        "title": "Miembros — REDES-IA",
        "description": "Conoce al equipo de investigadores y colaboradores de REDES-IA que estudian las implicaciones sociales, económicas y políticas de la inteligencia artificial.",
        "description_en": "Meet the REDES-IA researchers and collaborators studying the social, economic and political implications of artificial intelligence.",
    },
    "actividades.html": {
        "layout": "main",
        "active": "actividades",
        "title": "Actividades — REDES-IA",
        "description": "Seminarios, talleres y jornadas de REDES-IA sobre inteligencia artificial, ciencias sociales, gobernanza, economía política y políticas públicas.",
        "description_en": "REDES-IA seminars, workshops and conferences on artificial intelligence, social science, governance, political economy and public policy.",
    },
    "politicas.html": {
        "layout": "main",
        "active": "politicas",
        "title": "Políticas — REDES-IA",
        "description": "Policy briefs y recomendaciones de REDES-IA para instituciones y responsables políticos sobre la transición a la inteligencia artificial.",
        "description_en": "REDES-IA policy briefs and recommendations for institutions and policymakers on the transition to artificial intelligence.",
    },
    "formacion.html": {
        "layout": "main",
        "active": "formacion",
        "title": "Formación — REDES-IA",
        "description": "Formaciones de REDES-IA sobre impacto de la inteligencia artificial, economía, políticas públicas y herramientas de IA para ciencias sociales.",
        "description_en": "REDES-IA training on the impact of artificial intelligence, economics, public policy and AI tools for social science.",
    },
    "medios.html": {
        "layout": "main",
        "active": "medios",
        "title": "En los medios — REDES-IA",
        "description": "Artículos y contribuciones públicas de REDES-IA sobre inteligencia artificial, automatización, empleo, desigualdad y políticas tecnológicas.",
        "description_en": "Public articles and contributions from REDES-IA on artificial intelligence, automation, employment, inequality and technology policy.",
    },
    "contacto.html": {
        "layout": "main",
        "active": "contacto",
        "title": "Contacto — REDES-IA",
        "description": "Contacta con REDES-IA para colaboraciones, actividades, formaciones o consultas sobre investigación y políticas públicas de inteligencia artificial.",
        "description_en": "Contact REDES-IA for collaborations, activities, training or enquiries about artificial intelligence research and public policy.",
    },
    "formacion-herramientas-ia.html": {
        "layout": "main",
        "active": "formacion",
        "title": "Ten Ways to Use Agentic AI in Academic Research — REDES-IA",
        "description": "Diez usos concretos de la IA agéntica en investigación académica y ciencias sociales, desde síntesis de literatura hasta código, documentación y docencia.",
        "description_en": "Ten concrete uses of agentic AI in academic research and social science workflows, from literature synthesis to code, documentation and teaching.",
        "og_title": "Ten Ways to Use Agentic AI in Academic Research — REDES-IA",
        "og_description": "Ten concrete uses of agentic AI in academic research and social science workflows.",
    },
    "workshop-1-llms.html": {
        "layout": "workshop",
        "title": "Workshop sobre LLMs y análisis de textos políticos | REDES-IA",
        "description": "Programa del workshop sobre grandes modelos de lenguaje y análisis de textos políticos.",
        "description_en": "Programme for the workshop on large language models and political text analysis.",
    },
    "workshop-2-ai.html": {
        "layout": "workshop",
        "title": "Workshop on AI & Politics | REDES-IA",
        "description": "Programa del workshop sobre IA y política, opinión pública, economía política y comunicación política.",
        "description_en": "Programme for the workshop on AI and politics, public opinion, political economy and political communication.",
    },
    "workshop-3-politics-of-ai.html": {
        "layout": "workshop",
        "title": "Workshop 2: Politics of AI | REDES-IA",
        "description": "Programa del workshop The Politics of AI: Actors, Policy, Geopolitics, and Resistances.",
        "description_en": "Programme for The Politics of AI workshop: actors, policy, geopolitics and resistances.",
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
    description_en = meta.get("description_en", DEFAULT_DESCRIPTION_EN)
    canonical_url = canonical_for(meta["filename"])
    alternate_en_url = f"{canonical_url}?lang=en"
    context = {
        "title": html.escape(meta["title"], quote=True),
        "description": html.escape(description, quote=True),
        "description_es": html.escape(description, quote=True),
        "description_en": html.escape(description_en, quote=True),
        "og_title": html.escape(meta.get("og_title", meta["title"]), quote=True),
        "og_description": html.escape(meta.get("og_description", description), quote=True),
        "og_image": html.escape(absolute_url(meta.get("og_image", DEFAULT_OG_IMAGE)), quote=True),
        "canonical_url": html.escape(canonical_url, quote=True),
        "alternate_es_url": html.escape(canonical_url, quote=True),
        "alternate_en_url": html.escape(alternate_en_url, quote=True),
        "stylesheets": stylesheets,
    }
    return managed("head", render_template(read_include("head.html"), context))


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
    for key, href, es, en in NAV:
        current = ' aria-current="page"' if key == active else ""
        nav_items.append(
            f'<li><a href="{href}"{current}><span data-lang="es">{es}</span>'
            f'<span data-lang="en">{en}</span></a></li>'
        )
        mobile_items.append(
            f'<li><a class="mobile-nav-link" href="{href}"><span data-lang="es">{es}</span>'
            f'<span data-lang="en">{en}</span></a></li>'
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


def build_page(filename: str, meta: dict[str, str]) -> None:
    path = ROOT / filename
    meta = {**meta, "filename": filename}
    content = path.read_text(encoding="utf-8")
    content = replace_head(content, render_head(meta))
    nav = render_workshop_nav() if meta["layout"] == "workshop" else render_main_nav(meta["active"])
    content = replace_nav(content, meta, nav)
    content = replace_footer(content, meta["layout"], render_footer(meta["layout"]))
    path.write_text(content, encoding="utf-8")


def write_seo_files() -> None:
    sitemap_urls = [
        "  <url>\n"
        f"    <loc>{canonical_for(filename)}</loc>\n"
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
