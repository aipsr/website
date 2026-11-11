#!/usr/bin/env python3
"""Dependency-free checks for the generated static site."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.references: list[str] = []
        self.title_count = 0
        self.h1_count = 0
        self.has_lang = False
        self.images_without_alt = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "html" and values.get("lang", "").strip():
            self.has_lang = True
        if tag == "title":
            self.title_count += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "img" and "alt" not in values:
            self.images_without_alt += 1
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate_ids.add(element_id)
            self.ids.add(element_id)
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.references.append(values[attribute])


def local_target(page: Path, reference: str) -> Path | None:
    reference = reference.strip()
    if not reference or reference.startswith(("#", "//")):
        return None
    if "{{" in reference or "{%" in reference:
        return None
    split = urlsplit(reference)
    if split.scheme in {"http", "https", "mailto", "tel", "data", "javascript"}:
        return None
    raw_path = unquote(split.path)
    if not raw_path:
        return None
    target = ROOT / raw_path.lstrip("/") if raw_path.startswith("/") else page.parent / raw_path
    if raw_path.endswith("/"):
        target = target / "index.html"
    return target.resolve()


def main() -> int:
    failures: list[str] = []
    pages = sorted(ROOT.glob("*.html"))
    if not pages:
        failures.append("No root HTML pages found")

    for page in pages:
        parser = PageParser()
        try:
            parser.feed(page.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            failures.append(f"{page.name}: cannot read as UTF-8 ({exc})")
            continue
        if not parser.has_lang:
            failures.append(f"{page.name}: <html> has no lang attribute")
        if parser.title_count != 1:
            failures.append(f"{page.name}: expected one <title>, found {parser.title_count}")
        if parser.h1_count != 1:
            failures.append(f"{page.name}: expected one <h1>, found {parser.h1_count}")
        if parser.images_without_alt:
            failures.append(f"{page.name}: {parser.images_without_alt} image(s) lack alt")
        for duplicate in sorted(parser.duplicate_ids):
            failures.append(f"{page.name}: duplicate id #{duplicate}")
        for reference in parser.references:
            target = local_target(page, reference)
            if target is not None and not target.exists():
                failures.append(f"{page.name}: missing local target {reference}")

    if failures:
        print("Site checks failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"OK: checked {len(pages)} HTML pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
