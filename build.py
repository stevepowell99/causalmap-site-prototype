#!/usr/bin/env python3
"""Build causalmap.app: content/*.md to dist/, with the shared generator sitegen.

sitegen, pinned in requirements.txt, does the work. This file holds only what is
particular to this site: its footer, the tag chips and tag listing pages used by
the event write-ups, and the CSS values and blocks no other site uses.
"""

import html as html_lib
import re
from pathlib import Path

import sitegen
from sitegen import md, normalize_whitespace

ROOT = Path(__file__).parent


# ---- Tags: chips at the foot of each tagged page, and one listing page per tag ----

TAG_INDEX_BASE = "/events/tags"
_TAG_MONTHS = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

def slugify_tag(tag):
    return re.sub(r"[^a-z0-9]+", "-", str(tag).strip().lower()).strip("-")

def tag_display(tag):
    t = str(tag).replace("-", " ").strip()
    return (t[:1].upper() + t[1:]) if t else t

def page_tags(page):
    tags = page.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]
    return [str(t).strip() for t in tags if str(t).strip()]

def event_date_label(value):
    """'2025-05-21' -> 'May 2025'; '2022' -> '2022'."""
    if not value:
        return ""
    parts = str(value).split("-")
    year = parts[0]
    if len(parts) >= 2 and parts[1].isdigit():
        idx = int(parts[1])
        if 1 <= idx <= 12:
            return f"{_TAG_MONTHS[idx - 1]} {year}"
    return year

def render_tag_chips(tags):
    chips = "".join(
        f'<a class="tag-chip" href="{TAG_INDEX_BASE}/{slugify_tag(t)}">{html_lib.escape(tag_display(t))}</a>'
        for t in tags
    )
    return (f'<section class="tag-chips-section"><div class="container">'
            f'<div class="tag-chips">{chips}</div></div></section>')

def render_tag_index(tag, member_pages):
    """A listing page for one tag, reusing the search-result card styling.

    Cards are grouped under a heading per year. member_pages is expected to
    already be sorted by date descending, so years come out newest-first and
    each year's own cards stay in that same order.
    """
    intro = "Talks, workshops, posters and webinars where we have presented Causal Map and causal mapping."
    groups = []  # list of (year_label, cards_html)
    current_year = None
    cards = ""
    for p in member_pages:
        year = str(p.get("date") or "").split("-")[0] or "Undated"
        if year != current_year:
            if cards:
                groups.append((current_year, cards))
            current_year = year
            cards = ""
        label = event_date_label(p.get("date"))
        desc = normalize_whitespace(p.get("description", ""))
        cards += (
            '<article class="search-result-card">'
            f'<h2><a href="{p["_path"]}">{html_lib.escape(p.get("title", "Untitled"))}</a></h2>'
            + (f'<p class="search-result-desc">{html_lib.escape(label)}</p>' if label else "")
            + (f'<p class="search-result-snippet">{html_lib.escape(desc)}</p>' if desc else "")
            + "</article>"
        )
    if cards:
        groups.append((current_year, cards))

    groups_html = "".join(
        f'<h2 class="tag-year-heading">{html_lib.escape(year)}</h2>'
        f'<div class="search-results">{cards}</div>'
        for year, cards in groups
    )
    return (
        '<section class="hero-light"><div class="container">'
        f'<h1>{html_lib.escape(tag_display(tag))}</h1>'
        f'<div class="hero-sub">{md(intro)}</div>'
        "</div></section>"
        '<section class="search-section"><div class="container">'
        f'{groups_html}'
        "</div></section>"
    )

def add_tag_pages(pages, cfg):
    """Add tag chips to each tagged page, and a listing page per tag,
    e.g. /events/tags/academic-presentations."""
    tag_members = {}
    for page in pages:
        if page.get("redirect"):
            continue
        tags = page_tags(page)
        if not tags:
            continue
        for t in tags:
            tag_members.setdefault(slugify_tag(t), {"label": t, "pages": []})["pages"].append(page)
        page["_content_html"] += render_tag_chips(tags)

    # Synthetic tag index pages, e.g. /events/tags/academic-presentations
    for slug, info in sorted(tag_members.items()):
        members = sorted(info["pages"], key=lambda p: str(p.get("date") or ""), reverse=True)
        pages.append({
            "title": tag_display(info["label"]),
            "path": f"{TAG_INDEX_BASE}/{slug}",
            "_path": f"{TAG_INDEX_BASE}/{slug}",
            "description": f"Causal Map talks, workshops and webinars tagged {tag_display(info['label']).lower()}.",
            "_content_html": render_tag_index(info["label"], members),
        })


# ---- Footer ----

def footer(cfg):
    return '''<footer>
  <div class="container footer-inner">
    <div class="footer-links">
      <a href="/terms-and-conditions">Terms</a>
      <a href="/privacy-policy">Privacy</a>
      <a href="/information-security">Information Security</a>
      <a href="/ai-compliance">AI Compliance</a>
      <a href="/ethical-principles">Ethical Principles</a>
      <a href="https://forms.gle/JrK2AE6NTsGzUvWe8">Newsletter</a>
    </div>
    <div class="footer-social">
      <a href="https://www.linkedin.com/company/causalmap">LinkedIn</a>
      <a href="mailto:hello@causalmap.app">Email</a>
      <a href="https://www.youtube.com/watch?v=YskPTmWfADw&list=PLSCKdSxlLlfGfcab5njcT57xzU0hOURc-">YouTube</a>
      <a href="https://github.com/stevepowell99/">GitHub</a>
    </div>
    <a class="footer-badge" href="https://swidn.org.uk"><img src="/assets/swidn-member.png" alt="SWIDN member" width="96" height="36"></a>
    <p class="footer-legal">Causal Map Ltd, registered in England and Wales, company no. 12926630. Registered office: 39 Apsley Road, Bath BA1 3LP, United Kingdom. VAT no. GB 399950030.</p>
    <p class="footer-copy">This work is licensed under CC BY-NC 4.0</p>
  </div>
</footer>'''


# ---- CSS: this site's values and blocks for sitegen's shared stylesheet ----

CSS = {
    # Values every site sets (sitegen.css VALUES).
    'scroll_padding_top': '8rem',
    'nav_logo_height': '73px',
    'nav_logo_height_mobile': '57px',
    'nav_links': """\
.nav-links { display: flex; align-items: center; gap: 1rem; }
.nav-links > a { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.92rem; transition: color 0.15s; padding: 0.5rem 0; }""",
    'search_form_flex': '0 1 15rem',
    'button_text': 'var(--cm-ink)',
    'ink_deep': '#2d2d52',
    # Overrides of values sitegen works out from config.yml colours.
    'tint_a': '121,187,147',
    'tint_b': '144,195,198',
    'hero_grid_line': 'rgba(121, 187, 147, 0.03)',
    # CSS blocks only this site uses, by where they land in the cascade (sitegen.css SLOTS).
    'after_search': """\
.tag-year-heading {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--cm-ink);
  margin: 2.5rem 0 1rem;
  padding-bottom: 0.3rem;
  border-bottom: 2px solid var(--cm-green);
  display: inline-block;
}
.tag-year-heading:first-child {
  margin-top: 0;
}
""",
    'prose_lists': """\
.prose-section ol.ukes-programme-list > li { margin-bottom: 1.15rem; }
.prose-section ol.ukes-programme-list > li:last-child { margin-bottom: 0; }
.prose-section ol.ukes-programme-list p { margin-bottom: 0.5rem; }
.prose-section ol.ukes-programme-list p:last-child { margin-bottom: 0; }
""",
    'after_prose': """\
/* ---- Event post images ---- */
.prose-section img { max-width: 100%; height: auto; border-radius: var(--radius); margin: 1.25rem 0; display: block; }
.prose-section .img-row { display: flex; gap: 1rem; flex-wrap: wrap; margin: 1.25rem 0; }
.prose-section .img-row img { flex: 1 1 240px; min-width: 0; margin: 0; object-fit: cover; }

/* ---- Tags ---- */
.tag-chips-section { padding: 0 0 3rem; }
.tag-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.tag-chip {
  display: inline-block; padding: 0.3rem 0.85rem; border-radius: 999px;
  font-size: 0.8rem; font-weight: 600; text-decoration: none;
  background: var(--cm-light); color: var(--cm-ink); border: 1px solid var(--cm-border);
}
.tag-chip:hover { background: var(--cm-teal-light); color: var(--cm-ink); }

""",
    'before_footer_copy': """\
.footer-badge { display: inline-block; margin-bottom: 1rem; opacity: 0.75; transition: opacity 0.15s; }
.footer-badge:hover { opacity: 1; }
.footer-badge img { display: block; height: 36px; width: auto; border-radius: 3px; }
.footer-legal { color: rgba(255,255,255,0.55); font-size: 0.78rem; max-width: 640px; margin: 0 auto 0.5rem; line-height: 1.5; }
""",
    'before_print': """\
/* ---- Print / Save as PDF link ---- */
.print-link { margin: 0.25rem 0 2rem; }
.print-link a {
  display: inline-block;
  padding: 0.35rem 0.9rem;
  border: 1px solid var(--cm-teal);
  border-radius: 999px;
  color: var(--cm-ink) !important;
  background: #fff;
  font-size: 0.85rem;
  text-decoration: none !important;
}
.print-link a:hover { background: var(--cm-teal); color: #fff !important; }

""",
}


def build():
    sitegen.build(ROOT, footer=footer, css=CSS, extend_pages=add_tag_pages)


if __name__ == "__main__":
    build()
