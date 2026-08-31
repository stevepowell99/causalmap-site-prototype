#!/usr/bin/env python3
"""
Static site builder for causalmap.app
Reads markdown files with YAML front matter from content/, outputs HTML to dist/.
"""

import os
import sys
import re
import shutil
import json
import html as html_lib
import yaml
import markdown
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_PATH = SCRIPT_DIR / "config.yml"

def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)

def parse_page(filepath):
    text = filepath.read_text(encoding="utf-8")
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm) or {}
        meta["body"] = body.strip()
    else:
        meta = {"body": text.strip()}
    return meta

def md(text):
    return markdown.markdown(text, extensions=["extra", "tables", "smarty"])

_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

def inline_html(text):
    """Frontmatter subheads often include raw <span class=\"hl\"> markup."""
    text = (text or "").strip()
    if not text:
        return ""
    if "<" in text and ">" in text:
        def _link(m):
            label, url = m.group(1), m.group(2)
            return (
                f'<a href="{html_lib.escape(url, quote=True)}">'
                f"{html_lib.escape(label)}</a>"
            )
        return _MD_LINK.sub(_link, text)
    return md(text)

def render_fa_icon(icon, class_name):
    icon = html_lib.escape((icon or "").strip(), quote=True)
    if not icon:
        return ""
    return f'<span class="{class_name}" aria-hidden="true"><i class="{icon}"></i></span>'

def render_hero(section, cfg):
    headline = section.get("headline", "")
    subhead = inline_html(section.get("subhead", ""))
    cta_text = section.get("cta_text", "")
    cta_url = section.get("cta_url", "#")
    cta_html = f'<a class="btn-cta" href="{cta_url}">{cta_text}</a>' if cta_text else ""
    return f'''<section class="hero">
  <div class="container">
    <h1>{headline}</h1>
    <div class="hero-sub" data-hl-cycle>{subhead}</div>
    {cta_html}
  </div>
</section>'''

def render_hero_light(section, cfg):
    headline = section.get("headline", "")
    subhead = inline_html(section.get("subhead", ""))
    pillars = section.get("pillars")
    pills_block = ""
    if pillars:
        pills_inner = render_stand_pillar_articles(pillars, cfg)
        pills_block = f'''
  <div class="hero-light-pills">
    <div class="stand-pills-grid">
{pills_inner}    </div>
  </div>'''
    mod = " hero-light--with-pills" if pillars else ""
    return f'''<section class="hero-light{mod}">
  <div class="container">
    <h1>{headline}</h1>
    {f'<div class="hero-sub" data-hl-cycle>{subhead}</div>' if subhead else ''}
    {pills_block}
  </div>
</section>'''


def render_stand_pillar_articles(pillars, cfg):
    """Rounded stand cards (UKES etc.): badge title, optional intro/bullets, links. Used inside hero-light only."""
    app_url = cfg.get("app_url", "https://app.causalmap.app")
    parts = []
    for i, p in enumerate(pillars):
        heading = html_lib.escape(p.get("heading", ""))
        page_url = (p.get("page_url") or "").strip()
        page_label = html_lib.escape(p.get("page_label", "Learn more"))
        secondary_url = (p.get("secondary_url") or "").strip()
        sec_label_raw = p.get("secondary_label", "")
        if i == 0 and sec_label_raw and not secondary_url:
            secondary_url = app_url.rstrip("/") + "/"
        items = p.get("items") or []
        intro = p.get("intro", "")
        extra_links = p.get("links") or []

        bullets = ""
        for it in items:
            bullets += f'<li><span class="stand-pill-check" aria-hidden="true">&#10003;</span> {html_lib.escape(it)}</li>'
        list_html = f'<ul class="stand-pill-list">{bullets}</ul>' if bullets else ""
        intro_html = f'<div class="stand-pill-intro">{md(intro)}</div>' if intro else ""

        action_bits = []
        if page_url:
            action_bits.append(f'<a class="stand-pill-action" href="{page_url}">{page_label}</a>')
        if secondary_url and sec_label_raw:
            action_bits.append(
                f'<a class="stand-pill-action" href="{secondary_url}">{html_lib.escape(sec_label_raw)}</a>'
            )
        for L in extra_links:
            u = (L.get("url") or "").strip()
            lab = html_lib.escape(L.get("label", u))
            if u:
                action_bits.append(f'<a class="stand-pill-action" href="{u}">{lab}</a>')
        actions_html = f'<div class="stand-pill-actions">{"".join(action_bits)}</div>' if action_bits else ""

        parts.append(
            f'''<article class="stand-pill">
      <p class="stand-pill-badge-wrap"><span class="stand-pill-badge">{heading}</span></p>
      {intro_html}
      {list_html}
      {actions_html}
    </article>\n'''
        )
    return "".join(parts)

def feature_doc_url(col, cfg):
    """Link to Causal Map Guide page (garden.causalmap.app/anchor/)."""
    if col.get("doc_url"):
        return col["doc_url"]
    anchor = (col.get("help_anchor") or "").strip().lstrip("#")
    if not anchor:
        return ""
    base = (cfg.get("help_url") or "https://garden.causalmap.app").rstrip("/")
    return f"{base}/{anchor}/"

def render_features(section, cfg):
    cols = section.get("columns", [])
    heading = section.get("heading", "")
    # Card titles sit one level below a section heading when present; without one
    # they follow the page h1 directly, so they must be h2 to avoid skipping a level.
    card_tag = "h3" if heading else "h2"
    cards = ""
    for col in cols:
        icon_html = render_fa_icon(col.get("icon"), "feature-icon")
        title = col.get("title", "")
        doc_url = feature_doc_url(col, cfg)
        title_html = f"<{card_tag}>{title}</{card_tag}>"
        link_html = ""
        if doc_url:
            link_html = (
                f'<a class="feature-card-link" href="{doc_url}" '
                f'target="_blank" rel="noopener noreferrer" '
                f'aria-label="{html_lib.escape(title)} — documentation"></a>'
            )
        cards += f'''<div class="feature-card">
      {link_html}
      {icon_html}
      {title_html}
      {inline_html(col.get("text", ""))}
    </div>\n'''
    h = f'<h2 class="features-heading">{heading}</h2>' if heading else ""
    return f'''<section class="features">
  <div class="container">
    {h}
    <div class="features-grid" data-hl-cycle>{cards}</div>
  </div>
</section>'''

def render_callout(section, cfg):
    icon_html = render_fa_icon(section.get("icon"), "callout-icon")
    title = section.get("title", "")
    text = inline_html(section.get("text", ""))
    return f'''<section class="callout-section">
  <div class="container">
    <div class="callout-card">
      {icon_html}
      <div data-hl-cycle>
        <h2>{title}</h2>
        {text}
      </div>
    </div>
  </div>
</section>'''

def render_video(section, cfg):
    url = section.get("url", "")
    vid_id = ""
    if "vimeo.com" in url:
        vid_id = url.rstrip("/").split("/")[-1]
        # dnt=1 stops Vimeo setting tracking cookies / loading analytics.
        embed = f'https://player.vimeo.com/video/{vid_id}?dnt=1'
    elif "youtube.com" in url or "youtu.be" in url:
        m = re.search(r'(?:v=|youtu\.be/)([^&?]+)', url)
        vid_id = m.group(1) if m else ""
        # youtube-nocookie defers cookies until the visitor plays the video.
        embed = f'https://www.youtube-nocookie.com/embed/{vid_id}'
    else:
        embed = url
    return f'''<section class="video-section">
  <div class="container">
    <div class="video-wrap">
      <iframe src="{embed}" frameborder="0" allowfullscreen loading="lazy"></iframe>
    </div>
  </div>
</section>'''

def render_two_col(section, cfg):
    lt = section.get("left_title", "")
    lb = md(section.get("left_body", ""))
    rt = section.get("right_title", "")
    rb = md(section.get("right_body", ""))
    return f'''<section class="two-col">
  <div class="container">
    <div class="two-col-grid">
      <div>
        <h2>{lt}</h2>
        {lb}
      </div>
      <div>
        <h2>{rt}</h2>
        {rb}
      </div>
    </div>
  </div>
</section>'''

def render_steps(section, cfg):
    items = section.get("items", [])
    cards = ""
    for i, item in enumerate(items, 1):
        cards += f'''<div class="step-item">
      <div class="step-number">{i}</div>
      <h3>{item.get("title","")}</h3>
      {md(item.get("text",""))}
    </div>\n'''
    return f'''<section class="steps">
  <div class="container">
    <div class="steps-grid">{cards}</div>
  </div>
</section>'''

def render_trust_strip(section, cfg):
    heading = section.get("heading", "")
    orgs = section.get("organisations", "")
    return f'''<section class="trust-strip">
  <div class="container">
    <p><strong>{heading}</strong> {orgs}</p>
  </div>
</section>'''

def render_logos(section, cfg):
    heading = section.get("heading", "")
    image = section.get("image", "")
    return f'''<section class="logos-section">
  <div class="container">
    <h3>{heading}</h3>
    <img src="/{image}" alt="{heading}" loading="lazy">
  </div>
</section>'''

def render_testimonials(section, cfg):
    heading = section.get("heading", "")
    items = section.get("items", [])
    cards = ""
    for item in items:
        name = item.get("name", "")
        quote = item.get("quote", "")
        cards += f'''<div class="testimonial-card">
      <blockquote>{quote}</blockquote>
      <p class="testimonial-name">{name}</p>
    </div>\n'''
    h = f"<h2>{heading}</h2>" if heading else ""
    return f'''<section class="testimonials">
  <div class="container">
    {h}
    <div class="testimonials-grid">{cards}</div>
  </div>
</section>'''

def render_cta_banner(section, cfg):
    text = section.get("text", "")
    url = section.get("url", "#")
    btn = section.get("button_text", "Learn more")
    return f'''<section class="cta-banner">
  <div class="container">
    <span>{text}</span>
    <a class="btn-cta" href="{url}">{btn}</a>
  </div>
</section>'''

def render_prose(section, cfg, body_html):
    return f'''<section class="prose-section">
  <div class="container">
    {body_html}
  </div>
</section>'''

def render_team(section, cfg):
    heading = section.get("heading", "")
    members = section.get("members", [])
    cards = ""
    for m in members:
        img = ""
        if m.get("image"):
            img = f'<img src="{m["image"]}" alt="{m.get("name","")}" loading="lazy">'
        links = ""
        if m.get("linkedin"):
            links = f' <a href="{m["linkedin"]}" class="team-link">LinkedIn</a>'
        cards += f'''<div class="team-card">
      {img}
      <h3>{m.get("name","")}{links}</h3>
      <p class="team-role">{m.get("role","")}</p>
      <p>{m.get("bio","")}</p>
    </div>\n'''
    h = f"<h2>{heading}</h2>" if heading else ""
    return f'''<section class="team-section">
  <div class="container">
    {h}
    <div class="team-grid">{cards}</div>
  </div>
</section>'''

def render_search(section, cfg):
    heading = section.get("heading", "Search the site")
    intro = md(section.get("intro", "Find pages, methods, pricing, case studies, and policies across the site."))
    return f'''<section class="search-section">
  <div class="container">
    <div id="site-search-root" class="search-shell">
      <h1>{heading}</h1>
      <div class="search-intro">{intro}</div>
      <form class="search-page-form" action="/search" method="get" data-search-form>
        <label class="sr-only" for="search-page-input">Search the site</label>
        <input
          id="search-page-input"
          class="search-input"
          type="search"
          name="q"
          placeholder="Search"
          autocomplete="off"
          data-search-input
        >
        <button type="submit" class="search-submit">Search</button>
      </form>
      <p class="search-status" data-search-status>Search page titles and content.</p>
      <div class="search-results" data-search-results></div>
    </div>
  </div>
</section>'''

SECTION_RENDERERS = {
    "hero": render_hero,
    "hero-light": render_hero_light,
    "features": render_features,
    "callout": render_callout,
    "video": render_video,
    "two-col": render_two_col,
    "steps": render_steps,
    "trust-strip": render_trust_strip,
    "logos": render_logos,
    "testimonials": render_testimonials,
    "cta-banner": render_cta_banner,
    "team": render_team,
    "search": render_search,
}

def output_depth(page_path):
    """Directory depth of the generated page for file:// relative links."""
    stripped = page_path.strip("/")
    if not stripped:
        return 0
    if "." in stripped.split("/")[-1]:
        parent = stripped.rsplit("/", 1)[0] if "/" in stripped else ""
        return parent.count("/") + 1 if parent else 0
    return stripped.count("/") + 1

def make_links_relative(html, page_path):
    """Convert absolute internal URLs to relative paths for file:// preview."""
    import re
    page_depth = output_depth(page_path)
    prefix = "../" * page_depth if page_depth > 0 else "./"

    def replace_href(m):
        attr = m.group(1)
        path = m.group(2)
        if path.startswith("/") and not path.startswith("//"):
            fragment = ""
            if "#" in path:
                path, fragment = path.split("#", 1)
                fragment = "#" + fragment
            stripped = path.lstrip("/")
            if stripped == "":
                rel = prefix.rstrip("/") + "/index.html"
                if rel.startswith("/"):
                    rel = "./index.html"
            elif "." in stripped.split("/")[-1]:
                rel = prefix + stripped
            else:
                rel = prefix + stripped + "/index.html"
            return f'{attr}="{rel}{fragment}"'
        return m.group(0)

    return re.sub(r'(href|src|action)="(/[^"]*)"', lambda m: replace_href(m), html)

def add_external_link_attrs(html):
    """Open external site links in a new tab."""
    def replace_anchor(match):
        tag = match.group(0)
        href = match.group(1)
        if not (href.startswith("http://") or href.startswith("https://") or href.startswith("//")):
            return tag
        if 'target=' in tag:
            return tag
        return tag[:-1] + ' target="_blank" rel="noopener noreferrer">'

    return re.sub(r'<a\b[^>]*href="([^"]+)"[^>]*>', replace_anchor, html)

def tag_app_links(html, cfg):
    """Append UTM params to links pointing to the app host, so corporate-site signups are
    attributed. Configured once via `app_utm` in config.yml; links already carrying utm_source
    are left untouched."""
    import re
    from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

    utm = {k: v for k, v in (cfg.get("app_utm") or {}).items() if v}
    if not utm:
        return html
    app_host = urlsplit(cfg.get("app_url", "https://app.causalmap.app")).netloc.lower()
    if not app_host:
        return html

    def add_utm(href):
        parts = urlsplit(href)
        if parts.netloc.lower() != app_host:
            return href
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        if "utm_source" in query:
            return href
        query.update(utm)
        path = parts.path or "/"
        return urlunsplit((parts.scheme, parts.netloc, path, urlencode(query), parts.fragment))

    return re.sub(r'(href|src|action)="(https?://[^"]+)"', lambda m: f'{m.group(1)}="{add_utm(m.group(2))}"', html)

def normalize_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()

def html_to_plain_text(html):
    text = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return normalize_whitespace(html_lib.unescape(text))

def relative_site_path(target_path, from_path):
    from_depth = output_depth(from_path)
    prefix = "../" * from_depth if from_depth > 0 else "./"
    stripped = target_path.lstrip("/")
    if stripped == "":
        return prefix.rstrip("/") + "/index.html"
    if "." in stripped.split("/")[-1]:
        return prefix + stripped
    return prefix + stripped + "/index.html"

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

def build_search_index(pages):
    docs = []
    for page in pages:
        if page.get("redirect"):
            continue
        path = page["_path"]
        if path == "/search":
            continue
        docs.append({
            "title": page.get("title", "Untitled"),
            "path": path,
            "href": relative_site_path(path, "/search"),
            "description": normalize_whitespace(page.get("description", "")),
            "content": html_to_plain_text(page.get("_content_html", "")),
        })
    return docs

def build_search_script(search_index):
    search_json = json.dumps(search_index, ensure_ascii=False).replace("<", "\\u003c").replace("</", "<\\/")
    return f'''<script>
(function () {{
  const root = document.getElementById("site-search-root");
  if (!root) return;

  const searchIndex = {search_json};
  const form = root.querySelector("[data-search-form]");
  const input = root.querySelector("[data-search-input]");
  const status = root.querySelector("[data-search-status]");
  const results = root.querySelector("[data-search-results]");
  const params = new URLSearchParams(window.location.search);
  const initialQuery = (params.get("q") || "").trim();

  function tokenize(text) {{
    return [...new Set((text.toLowerCase().match(/[a-z0-9]+/g) || []))];
  }}

  function scoreDoc(doc, terms) {{
    const title = doc.title.toLowerCase();
    const description = doc.description.toLowerCase();
    const content = doc.content.toLowerCase();
    let score = 0;

    for (const term of terms) {{
      if (title.includes(term)) score += 12;
      if (description.includes(term)) score += 6;
      if (content.includes(term)) score += 2;
    }}

    return score;
  }}

  function buildSnippet(doc, terms) {{
    const source = doc.content || doc.description;
    if (!source) return "";

    const lower = source.toLowerCase();
    let start = 0;
    for (const term of terms) {{
      const index = lower.indexOf(term);
      if (index !== -1) {{
        start = Math.max(0, index - 80);
        break;
      }}
    }}

    const end = Math.min(source.length, start + 190);
    const snippet = source.slice(start, end).trim();
    const prefix = start > 0 ? "..." : "";
    const suffix = end < source.length ? "..." : "";
    return prefix + snippet + suffix;
  }}

  function renderResults(query) {{
    results.replaceChildren();
    const terms = tokenize(query);

    if (!terms.length) {{
      status.textContent = "Search page titles and content.";
      return;
    }}

    const matches = searchIndex
      .map((doc) => ({{ doc, score: scoreDoc(doc, terms) }}))
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score || a.doc.title.localeCompare(b.doc.title))
      .slice(0, 20);

    status.textContent = matches.length
      ? `${{matches.length}} result${{matches.length === 1 ? "" : "s"}} for "${{query}}"`
      : `No results for "${{query}}"`;

    for (const match of matches) {{
      const card = document.createElement("article");
      card.className = "search-result-card";

      const heading = document.createElement("h2");
      const link = document.createElement("a");
      link.href = match.doc.href;
      link.textContent = match.doc.title;
      heading.appendChild(link);
      card.appendChild(heading);

      if (match.doc.description) {{
        const description = document.createElement("p");
        description.className = "search-result-desc";
        description.textContent = match.doc.description;
        card.appendChild(description);
      }}

      const snippetText = buildSnippet(match.doc, terms);
      if (snippetText) {{
        const snippet = document.createElement("p");
        snippet.className = "search-result-snippet";
        snippet.textContent = snippetText;
        card.appendChild(snippet);
      }}

      results.appendChild(card);
    }}
  }}

  function submitSearch(event) {{
    event.preventDefault();
    const query = input.value.trim();
    const nextUrl = new URL(window.location.href);

    if (query) {{
      nextUrl.searchParams.set("q", query);
    }} else {{
      nextUrl.searchParams.delete("q");
    }}

    window.history.replaceState({{}}, "", nextUrl);
    renderResults(query);
  }}

  form.addEventListener("submit", submitSearch);
  input.value = initialQuery;
  if (initialQuery) renderResults(initialQuery);
}})();
</script>'''

def build_analytics_html(cfg):
    # Each tracker is injected only when its own key is configured, so a site
    # can run either, both or neither.
    analytics = cfg.get("analytics", {}) or {}
    tags = []

    umami_id = (analytics.get("umami_id") or "").strip()
    if umami_id:
        umami_script = (analytics.get("umami_script") or "https://cloud.umami.is/script.js").strip()
        tags.append(
            f'<script defer src="{umami_script}" '
            f'data-website-id="{umami_id}"></script>'
        )

    # GoatCounter is the one that records whether a hit was a bot, which Umami
    # does not; the value is the full count URL from the GoatCounter snippet.
    goatcounter = (analytics.get("goatcounter") or "").strip()
    if goatcounter:
        tags.append(
            f'<script data-goatcounter="{goatcounter}" '
            f'async src="//gc.zgo.at/count.js"></script>'
        )

    return "\n  ".join(tags)

def render_sections(page, cfg):
    sections = page.get("sections", [])
    body_html = md(page.get("body", ""))
    has_prose = any(s.get("type") == "prose" for s in sections)
    parts = []
    for s in sections:
        stype = s.get("type", "")
        if stype == "prose":
            parts.append(render_prose(s, cfg, body_html))
        elif stype in SECTION_RENDERERS:
            parts.append(SECTION_RENDERERS[stype](s, cfg))
    if not has_prose and body_html.strip():
        parts.append(render_prose({}, cfg, body_html))
    result = "\n<hr class=\"section-divider\">\n".join(parts)
    result = result.replace("<td>Yes</td>", '<td class="check">&#10003;</td>')
    return result

def build_logo_img():
    """Use the actual Causal Map logo PNG (white version for dark navbar)."""
    return '<img class="nav-logo-img" src="/assets/logo-white.png" alt="Causal Map">'

def build_nav(pages, cfg):
    nav_pages = sorted(
        [p for p in pages if p.get("nav_order") is not None],
        key=lambda p: p["nav_order"]
    )
    links = ""
    for p in nav_pages:
        label = p.get("nav_label", p.get("title", ""))
        path = p.get("path", "/")
        children = p.get("nav_children", [])
        if children:
            sub = ""
            for ch in children:
                sub += f'<a href="{ch["path"]}">{ch["label"]}</a>\n'
            links += f'''    <div class="nav-dropdown">
      <a href="{path}" class="nav-dropdown-trigger">{label}</a>
      <div class="nav-dropdown-menu">{sub}</div>
    </div>\n'''
        else:
            links += f'    <a href="{path}">{label}</a>\n'

    app_url = cfg.get("app_url", "https://app.causalmap.app")
    logo = build_logo_img()
    search_form = '''    <form class="site-search-form" action="/search" method="get" role="search">
      <label class="sr-only" for="nav-search-input">Search the site</label>
      <input
        id="nav-search-input"
        class="search-input"
        type="search"
        name="q"
        placeholder="Search"
        autocomplete="off"
      >
      <button type="submit" class="search-submit" aria-label="Submit search">&#8594;</button>
    </form>
'''

    return f'''<nav class="navbar">
  <div class="container nav-inner">
    <a href="/" class="nav-logo">{logo}</a>
    <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav-links">
      <span></span><span></span><span></span>
    </button>
    <div class="nav-links" id="nav-links">
{links}    </div>
{search_form}    <a class="btn-cta nav-cta" href="{app_url}">Try it free</a>
  </div>
</nav>
<div class="accent-stripe"></div>'''

def build_footer(cfg):
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
    <p class="footer-legal">Causal Map Ltd, registered in England and Wales, company no. 12926630. Registered office: 39 Apsley Road, Bath BA1 3LP, United Kingdom. VAT no. GB 399950030.</p>
    <p class="footer-copy">This work is licensed under CC BY-NC 4.0</p>
  </div>
</footer>'''

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip().lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgba(hex_color, alpha):
    r, g, b = hex_to_rgb(hex_color)
    return f"rgba({r}, {g}, {b}, {alpha})"

def build_css(cfg):
    colors = cfg.get("colors", {})
    cm_ink = colors.get("accent_ink", "#1f1f36")
    cm_pink = colors.get("accent_pink", "#ff8fb8")
    cm_green = colors.get("accent_primary", "#00ffaf")
    cm_teal = colors.get("accent_secondary", "#6dc4c8")
    cm_yellow = colors.get("highlight_yellow", "#f7ed73")
    cm_bg = colors.get("body_bg", "#fcfcfc")
    cm_text = colors.get("text", "#222")
    return f''':root {{
  --cm-ink: {cm_ink};
  --cm-pink: {cm_pink};
  --cm-green: {cm_green};
  --cm-teal: {cm_teal};
  --cm-yellow: {cm_yellow};
  --cm-bg: {cm_bg};
  --cm-text: {cm_text};
  --cm-light: #f4f6f8;
  --cm-border: #e2e6ea;
  --radius: 8px;
  --cm-green-light: {rgba(cm_green, 0.08)};
  --cm-teal-light: {rgba(cm_teal, 0.10)};
  --cm-yellow-light: {rgba(cm_yellow, 0.75)};
  --cm-pink-light: {rgba(cm_pink, 0.45)};
}}

{CSS_BODY}'''

CSS_BODY = '''
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { font-size: 17px; scroll-behavior: smooth; }
body {
  font-family: "Inter", system-ui, -apple-system, sans-serif;
  color: var(--cm-text);
  background: var(--cm-bg);
  line-height: 1.6;
}

a {
  color: var(--cm-ink);
  text-decoration: underline;
  text-decoration-color: var(--cm-teal);
  text-underline-offset: 2px;
  transition: color 0.15s;
}
a:hover { color: var(--cm-teal); }

.container { max-width: 1040px; margin: 0 auto; padding: 0 1.5rem; }

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* ---- Inline highlights (inset shadow = reliable marker on inline spans) ---- */
.hl {
  padding: 0 0.1em;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
/* Static markers only (no hl-reveal); cycling phrases use rules below */
.hl-yellow:not(.hl-reveal) { box-shadow: inset 0 -0.42em 0 0 var(--cm-yellow-light); }
.hl-pink:not(.hl-reveal) { box-shadow: inset 0 -0.42em 0 0 var(--cm-pink-light); }
.hl-green:not(.hl-reveal) { box-shadow: inset 0 -0.42em 0 0 var(--cm-green-light); }
/* Cycling marker: box-shadow fade (3s in, hold, 3s out via JS) */
.hl.hl-reveal { transition: box-shadow 3s ease; }
.hl.hl-reveal.hl-yellow { box-shadow: inset 0 -0.42em 0 0 rgba(240, 215, 107, 0); }
.hl.hl-reveal.hl-pink { box-shadow: inset 0 -0.42em 0 0 rgba(255, 190, 200, 0); }
.hl.hl-reveal.hl-green { box-shadow: inset 0 -0.42em 0 0 rgba(43, 169, 156, 0); }
.hl.hl-reveal.hl-active.hl-yellow { box-shadow: inset 0 -0.42em 0 0 rgba(240, 215, 107, 0.85); }
.hl.hl-reveal.hl-active.hl-pink { box-shadow: inset 0 -0.42em 0 0 rgba(255, 190, 200, 0.8); }
.hl.hl-reveal.hl-active.hl-green { box-shadow: inset 0 -0.42em 0 0 rgba(43, 169, 156, 0.45); }
.hero .hl.hl-reveal.hl-active.hl-yellow { box-shadow: inset 0 -0.42em 0 0 rgba(240, 215, 107, 0.9); }
.hero .hl.hl-reveal.hl-active.hl-pink { box-shadow: inset 0 -0.42em 0 0 rgba(255, 190, 200, 0.85); }
.hero .hl.hl-reveal.hl-active.hl-green { box-shadow: inset 0 -0.42em 0 0 rgba(140, 230, 215, 0.9); }
.callout-card .hl.hl-reveal.hl-active.hl-green { box-shadow: inset 0 -0.42em 0 0 rgba(43, 169, 156, 0.5); }

/* ---- Heading reveal ---- */
.scroll-reveal {
  opacity: 0;
  transform: translateY(22px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.scroll-reveal.in-view {
  opacity: 1;
  transform: translateY(0);
}

/* ---- Section divider ---- */
.section-divider {
  height: 2px; border: none; margin: 0;
  background: linear-gradient(90deg, var(--cm-green), var(--cm-teal));
  opacity: 0.3;
}

/* ---- Navbar ---- */
.navbar {
  background: var(--cm-ink);
  color: #fff;
  position: sticky; top: 0; z-index: 100;
  padding: 1.35rem 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.nav-inner { display: flex; align-items: center; gap: 1rem; flex-wrap: nowrap; }
.nav-logo {
  text-decoration: none; margin-right: auto; display: flex; align-items: center;
}
.nav-logo-img { height: 73px; width: auto; }
.nav-links { display: flex; align-items: center; gap: 1rem; }
.nav-links > a { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.92rem; transition: color 0.15s; padding: 0.5rem 0; }
.nav-links a:hover { color: #fff; }
.nav-cta { margin-left: 0.25rem; }
/* Hamburger toggle (hidden on desktop) */
.nav-toggle {
  display: none;
  background: transparent; border: 0; cursor: pointer;
  width: 2.5rem; height: 2.5rem; padding: 0;
  flex-direction: column; justify-content: center; align-items: center; gap: 5px;
}
.nav-toggle span {
  display: block; width: 1.5rem; height: 2px; background: #fff; border-radius: 2px;
  transition: transform 0.2s, opacity 0.2s;
}
.nav-toggle[aria-expanded="true"] span:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.nav-toggle[aria-expanded="true"] span:nth-child(2) { opacity: 0; }
.nav-toggle[aria-expanded="true"] span:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }
.site-search-form,
.search-page-form {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.site-search-form {
  flex: 0 1 15rem;
  opacity: 0.55;
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.site-search-form:hover,
.site-search-form:focus-within {
  opacity: 1;
}
.search-input {
  width: 100%;
  min-width: 0;
  border: 1px solid var(--cm-border);
  border-radius: 999px;
  padding: 0.7rem 0.95rem;
  font: inherit;
  color: var(--cm-ink);
  background: #fff;
}
.search-input:focus {
  outline: 2px solid var(--cm-teal);
  outline-offset: 1px;
}
.site-search-form .search-input {
  border-color: rgba(255,255,255,0.16);
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.72);
  padding: 0.56rem 0.85rem;
  transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease, box-shadow 0.18s ease;
}
.site-search-form .search-input::placeholder {
  color: rgba(255,255,255,0.74);
}
.site-search-form:hover .search-input,
.site-search-form:focus-within .search-input {
  border-color: rgba(255,255,255,0.34);
  background: rgba(255,255,255,0.13);
  color: #fff;
}
.search-submit {
  border: 0;
  border-radius: 999px;
  padding: 0.7rem 1rem;
  background: var(--cm-green);
  color: var(--cm-ink);
  font: inherit;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}
.search-submit:hover {
  background: var(--cm-teal);
}
.site-search-form .search-submit {
  width: 2.35rem;
  min-width: 2.35rem;
  padding: 0.56rem 0;
  background: rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.72);
  text-align: center;
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transition: background 0.18s ease, color 0.18s ease, opacity 0.18s ease;
}
.site-search-form .search-input:not(:placeholder-shown) + .search-submit {
  opacity: 1;
  visibility: visible;
  pointer-events: auto;
}
.site-search-form:hover .search-submit,
.site-search-form:focus-within .search-submit {
  background: rgba(255,255,255,0.18);
  color: #fff;
}

/* ---- Nav dropdown ---- */
.nav-dropdown { position: relative; display: flex; align-items: center; }
.nav-dropdown-trigger { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.92rem; transition: color 0.15s; cursor: pointer; padding: 0.5rem 0; }
.nav-dropdown-trigger:hover { color: #fff; }
.nav-dropdown-menu {
  display: none; position: absolute; top: 100%; left: -0.75rem;
  background: var(--cm-ink); border-radius: 0 0 var(--radius) var(--radius);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  min-width: 200px; padding: 0.5rem 0; z-index: 200;
}
.nav-dropdown:hover .nav-dropdown-menu { display: block; }
.nav-dropdown-menu a {
  display: block; padding: 0.5rem 1.25rem;
  color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.9rem;
  transition: background 0.12s, color 0.12s; white-space: nowrap;
}
.nav-dropdown-menu a:hover { background: rgba(255,255,255,0.08); color: #fff; }

/* ---- Accent stripe ---- */
.accent-stripe {
  height: 3px;
  background: linear-gradient(90deg, var(--cm-green), var(--cm-teal), var(--cm-pink));
}

/* ---- Buttons ---- */
.btn-cta {
  display: inline-block;
  background: var(--cm-pink);
  color: var(--cm-ink);
  padding: 0.6rem 1.6rem;
  border-radius: 11px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: transform 0.15s, box-shadow 0.15s;
  cursor: pointer;
  border: none;
}
.btn-cta:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(255,143,184,0.3); }
.btn-secondary {
  display: inline-block;
  background: var(--cm-green);
  color: var(--cm-ink);
  padding: 0.6rem 1.6rem;
  border-radius: 11px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: transform 0.15s, box-shadow 0.15s;
  cursor: pointer;
  border: none;
}
.btn-secondary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(121,187,147,0.3); }

/* ---- Hero ---- */
.hero {
  background: linear-gradient(135deg, var(--cm-ink) 0%, #2d2d52 100%);
  background-image:
    linear-gradient(135deg, var(--cm-ink) 0%, #2d2d52 100%),
    linear-gradient(0deg, transparent 24%, rgba(121, 187, 147, 0.03) 25%, rgba(121, 187, 147, 0.03) 26%, transparent 27%, transparent 74%, rgba(121, 187, 147, 0.03) 75%, rgba(121, 187, 147, 0.03) 76%, transparent 77%, transparent),
    linear-gradient(90deg, transparent 24%, rgba(121, 187, 147, 0.03) 25%, rgba(121, 187, 147, 0.03) 26%, transparent 27%, transparent 74%, rgba(121, 187, 147, 0.03) 75%, rgba(121, 187, 147, 0.03) 76%, transparent 77%, transparent);
  background-size: 100% 100%, 50px 50px, 50px 50px;
  color: #fff;
  padding: 5rem 0 4.5rem;
  text-align: center;
}
.hero h1 { font-size: 3.9rem; font-weight: 800; margin-bottom: 1rem; line-height: 1.15; }
.hero-sub { font-size: 1.15rem; opacity: 0.88; max-width: 600px; margin: 0 auto 2rem; }
.hero-sub p { margin: 0; }

/* ---- Hero Light ---- */
.hero-light {
  background: linear-gradient(135deg, rgba(121,187,147,0.04) 0%, rgba(144,195,198,0.04) 100%);
  padding: 3.5rem 0 3rem;
  border-bottom: 2px solid transparent;
  border-image: linear-gradient(90deg, var(--cm-green), var(--cm-teal)) 1;
}
.hero-light--with-pills {
  background: #fff;
  border-image: none;
  border-bottom: 1px solid var(--cm-border);
  padding-bottom: 3.25rem;
}
.hero-light h1 { font-size: 2.86rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--cm-ink); }
.hero-light .hero-sub { font-size: 1.05rem; color: #666; max-width: none; margin: 0; opacity: 1; }
.hero-light .hero-sub p { margin: 0 0 0.5rem; }
.hero-light .hero-sub p:last-child { margin-bottom: 0; }

/* Stand follow-up pills (inside hero-light, white cards) */
.hero-light-pills { margin-top: 2.25rem; }
.stand-pills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.25rem;
  align-items: stretch;
}
.stand-pill {
  background: #fff;
  border: 1px solid var(--cm-border);
  border-radius: 28px;
  padding: 1.5rem 1.35rem 1.4rem;
  box-shadow: 0 6px 24px rgba(31, 31, 54, 0.07);
}
.stand-pill-badge-wrap {
  margin: 0 0 1rem;
  line-height: 1.3;
}
.stand-pill-badge {
  display: inline-block;
  border-radius: 999px;
  padding: 0.4rem 1rem 0.42rem;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.04em;
  background: var(--cm-light);
  color: var(--cm-ink);
  border: 1px solid var(--cm-border);
}
.stand-pill-intro { font-size: 0.95rem; color: #444; line-height: 1.55; margin-bottom: 0.85rem; }
.stand-pill-intro p { margin: 0 0 0.5rem; }
.stand-pill-intro p:last-child { margin-bottom: 0; }
.stand-pill-intro a { color: var(--cm-ink); }
.stand-pill-list {
  list-style: none;
  margin: 0 0 1rem;
  padding: 0;
  font-size: 0.92rem;
  color: #444;
}
.stand-pill-list li {
  display: flex;
  gap: 0.45rem;
  align-items: flex-start;
  margin-bottom: 0.45rem;
}
.stand-pill-check {
  color: var(--cm-teal);
  font-weight: 800;
  flex-shrink: 0;
}
.stand-pill-actions {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  margin-top: 0.25rem;
}
.stand-pill-action {
  display: block;
  text-align: center;
  padding: 0.55rem 1rem;
  font-size: 0.88rem;
  font-weight: 600;
  border-radius: 999px;
  border: 2px solid var(--cm-teal);
  color: var(--cm-ink);
  background: #fff;
  text-decoration: none;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.stand-pill-action:hover {
  background: var(--cm-teal-light);
  color: var(--cm-ink);
  border-color: var(--cm-teal);
}

/* ---- Features grid ---- */
.features { padding: 4rem 0; background: var(--cm-light); }
.features + .features { padding-top: 2rem; }
.features-heading {
  margin: 0 0 2rem;
  color: var(--cm-ink);
  font-weight: 600;
  font-size: 1.65rem;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid var(--cm-green);
  display: inline-block;
}
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 2rem; }
.feature-card {
  position: relative;
  background: #fff;
  border: 1px solid var(--cm-border);
  border-top: 3px solid var(--cm-green);
  border-radius: var(--radius);
  padding: 2rem;
  transition: transform 0.15s, box-shadow 0.15s;
}
.feature-card-link {
  position: absolute;
  inset: 0;
  z-index: 1;
  border-radius: inherit;
}
.feature-card-link:focus-visible {
  outline: 2px solid var(--cm-teal);
  outline-offset: 2px;
}
.feature-card:has(.feature-card-link) { cursor: pointer; }
.feature-card:has(.feature-card-link) p a { position: relative; z-index: 2; }
.feature-card:nth-child(2) { border-top-color: var(--cm-teal); }
.feature-card:nth-child(3) { border-top-color: var(--cm-pink); }
.feature-card:nth-child(4) { border-top-color: var(--cm-green); }
.feature-card:nth-child(5) { border-top-color: var(--cm-teal); }
.feature-card:nth-child(6) { border-top-color: var(--cm-pink); }
.feature-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.06); }
.feature-icon {
  display: inline-flex;
  width: 3rem;
  height: 3rem;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.1rem;
  border-radius: 999px;
  background: var(--cm-ink);
  color: #fff;
  font-size: 1.25rem;
  box-shadow: 0 0 0 8px var(--cm-teal-light);
}
.feature-card h3, .feature-card h2 { font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--cm-ink); font-weight: 600; }
.feature-card:has(.feature-card-link):hover h3,
.feature-card:has(.feature-card-link):hover h2 { color: var(--cm-teal); }
.feature-card p { font-size: 0.95rem; color: #555; }

/* ---- Callout ---- */
.callout-section { padding: 2.25rem 0; background: var(--cm-light); }
.callout-card {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  max-width: 820px;
  margin: 0 auto;
  padding: 1.35rem 1.55rem;
  border: 1px solid rgba(43,169,156,0.25);
  border-radius: 22px;
  background: #fff;
  box-shadow: 0 8px 28px rgba(31, 31, 54, 0.07);
}
.callout-icon {
  display: inline-flex;
  width: 3.4rem;
  height: 3.4rem;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 999px;
  background: var(--cm-teal-light);
  color: var(--cm-ink);
  font-size: 1.4rem;
}
.callout-card h2 {
  margin-bottom: 0.25rem;
  color: var(--cm-ink);
  font-size: 1.2rem;
}
.callout-card p { margin: 0; color: #555; }
/* ---- Video ---- */
.video-section { padding: 3.5rem 0; }
.video-wrap {
  position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;
  border-radius: var(--radius); box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.video-wrap iframe {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
}

/* ---- Two-col ---- */
.two-col { padding: 4rem 0; }
.two-col-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; }
.two-col-grid > div {
  padding: 1.5rem; border-radius: var(--radius);
  background: var(--cm-light); border-left: 3px solid var(--cm-green);
}
.two-col-grid > div:nth-child(2) { border-left-color: var(--cm-teal); }
.two-col h2 { font-size: 1.35rem; margin-bottom: 0.75rem; color: var(--cm-ink); font-weight: 600; }
.two-col p, .two-col li { font-size: 0.95rem; }
/* ---- Steps ---- */
.steps { padding: 4rem 0; background: var(--cm-light); }
.steps-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem;
  position: relative;
}
.steps-grid::before {
  content: ""; position: absolute; top: 1.8rem; left: 10%; right: 10%;
  height: 2px; background: repeating-linear-gradient(90deg, var(--cm-green) 0, var(--cm-green) 8px, transparent 8px, transparent 16px);
  z-index: 0;
}
.step-item { text-align: center; position: relative; z-index: 1; }
.step-number {
  font-size: 2.5rem; font-weight: 800; color: var(--cm-green);
  margin-bottom: 0.5rem;
  background: var(--cm-light); display: inline-block; padding: 0 0.5rem;
}
.step-item h3 { font-size: 1rem; margin-bottom: 0.5rem; color: var(--cm-ink); font-weight: 600; }
.step-item p { font-size: 0.9rem; color: #555; }

/* ---- Trust strip ---- */
.trust-strip {
  padding: 2.5rem 0;
  background: linear-gradient(135deg, rgba(121,187,147,0.06) 0%, rgba(144,195,198,0.06) 100%);
  border-top: 1px solid var(--cm-border); border-bottom: 1px solid var(--cm-border);
}
.trust-strip p { font-size: 0.95rem; color: #555; }
.trust-strip strong { color: var(--cm-ink); }

/* ---- Logos ---- */
.logos-section { padding: 3rem 0; text-align: center; }
.logos-section h3 { font-size: 1rem; color: #666; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 600; }
.logos-section img { max-width: 100%; }

/* ---- Testimonials ---- */
.testimonials { padding: 4rem 0; background: var(--cm-light); }
.testimonials h2 { margin-bottom: 2rem; color: var(--cm-ink); font-weight: 600; }
.testimonials-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; }
.testimonial-card {
  background: #fff;
  border: 1px solid var(--cm-border);
  border-left: 4px solid var(--cm-teal);
  border-radius: var(--radius);
  padding: 2rem;
  transition: transform 0.15s, box-shadow 0.15s;
}
.testimonial-card:nth-child(2) { border-left-color: var(--cm-green); }
.testimonial-card:nth-child(3) { border-left-color: var(--cm-pink); }
.testimonial-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.06); }
.testimonial-card blockquote {
  font-size: 0.95rem; font-style: italic; color: #444;
  margin: 0 0 1rem; line-height: 1.65;
}
.testimonial-card .testimonial-name { font-weight: 600; color: var(--cm-ink); font-size: 0.9rem; }

/* ---- CTA banner ---- */
.cta-banner {
  background: linear-gradient(135deg, var(--cm-ink) 0%, #2d2d52 100%);
  color: #fff;
  padding: 2.5rem 0;
  text-align: center;
}
.cta-banner .container { display: flex; align-items: center; justify-content: center; gap: 1.5rem; flex-wrap: wrap; }
.cta-banner span { font-size: 1.1rem; }

/* ---- Team ---- */
.team-section { padding: 4rem 0; }
.team-section h2 { margin-bottom: 2.5rem; color: var(--cm-ink); font-weight: 600; padding-bottom: 0.4rem; border-bottom: 2px solid var(--cm-green); display: inline-block; }
.team-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 2.5rem; }
.team-card { text-align: left; }
.team-card img {
  width: 160px; height: 160px; border-radius: 50%; object-fit: cover;
  margin-bottom: 1rem; border: 3px solid var(--cm-border);
  transition: border-color 0.2s, box-shadow 0.2s;
}
.team-card:hover img { border-color: var(--cm-green); box-shadow: 0 0 0 4px rgba(121,187,147,0.15); }
.team-card h3 { font-size: 1.1rem; color: var(--cm-ink); margin-bottom: 0.25rem; }
.team-card .team-role { font-size: 0.85rem; color: var(--cm-teal); font-weight: 600; margin-bottom: 0.5rem; }
.team-card p { font-size: 0.9rem; color: #555; line-height: 1.55; }
.team-link { font-size: 0.8rem; color: var(--cm-teal); text-decoration: none; font-weight: 400; }
.team-link:hover { color: var(--cm-green); }

/* ---- Search ---- */
.search-section { padding: 3.5rem 0; }
.search-shell {
  max-width: 760px;
}
.search-shell h1 {
  font-size: 2.3rem;
  line-height: 1.15;
  color: var(--cm-ink);
  margin-bottom: 0.75rem;
}
.search-intro {
  color: #555;
  margin-bottom: 1.5rem;
}
.search-intro p { margin-bottom: 0; }
.search-page-form {
  margin-bottom: 1rem;
}
.search-status {
  color: #555;
  margin-bottom: 1.25rem;
}
.search-results {
  display: grid;
  gap: 1rem;
}
.search-result-card {
  background: #fff;
  border: 1px solid var(--cm-border);
  border-left: 4px solid var(--cm-green);
  border-radius: var(--radius);
  padding: 1.2rem 1.25rem;
}
.search-result-card h2 {
  font-size: 1.15rem;
  margin-bottom: 0.35rem;
}
.search-result-card h2 a {
  text-decoration: none;
}
.search-result-desc {
  color: var(--cm-ink);
  font-weight: 600;
  margin-bottom: 0.35rem;
}
.search-result-snippet {
  color: #555;
  margin-bottom: 0;
}
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

/* ---- Prose ---- */
.prose-section { padding: 3.5rem 0; }
.prose-section h2 {
  font-size: 1.4rem; margin: 2rem 0 0.75rem; color: var(--cm-ink); font-weight: 600;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid var(--cm-green);
  display: inline-block;
}
.prose-section h2 a,
.prose-section h3 a {
  color: inherit;
  text-decoration: none;
}
.prose-section h2 a:hover,
.prose-section h3 a:hover { color: var(--cm-teal); }
.prose-section h3 { font-size: 1.15rem; margin: 1.5rem 0 0.5rem; color: var(--cm-ink); font-weight: 600; }
.prose-section p { margin-bottom: 1rem; }
.prose-section ul, .prose-section ol { margin: 0 0 1rem 1.5rem; }
.prose-section ol.ukes-programme-list > li { margin-bottom: 1.15rem; }
.prose-section ol.ukes-programme-list > li:last-child { margin-bottom: 0; }
.prose-section ol.ukes-programme-list p { margin-bottom: 0.5rem; }
.prose-section ol.ukes-programme-list p:last-child { margin-bottom: 0; }
.prose-section li { margin-bottom: 0.35rem; }
.prose-section li::marker { color: var(--cm-teal); }
.prose-section strong { color: var(--cm-ink); font-weight: 600; }

/* Prose callout */
.prose-section blockquote {
  border-left: 4px solid var(--cm-teal);
  background: var(--cm-teal-light);
  padding: 1rem 1.25rem; margin: 1.5rem 0;
  border-radius: 0 var(--radius) var(--radius) 0;
  font-size: 0.95rem;
}
.prose-section blockquote p { margin-bottom: 0; }

/* Prose tables */
.prose-section table {
  width: 100%; border-collapse: collapse; margin: 1.5rem 0;
  font-size: 0.92rem; border-radius: var(--radius); overflow: hidden;
}
.prose-section th, .prose-section td {
  border: 1px solid var(--cm-border); padding: 0.6rem 0.8rem; text-align: left;
}
.prose-section th {
  background: linear-gradient(135deg, rgba(121,187,147,0.12), rgba(144,195,198,0.12));
  font-weight: 600; color: var(--cm-ink);
}
.prose-section tr:nth-child(even) td { background: #fafbfc; }
.prose-section td:first-child { font-weight: 500; color: var(--cm-ink); }
.prose-section td.check {
  color: #0f6b4e;
  font-weight: 800;
  font-size: 1.2rem;
  text-align: center;
  text-shadow: 0 0 0.01px currentColor;
}

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

/* ---- Footer ---- */
footer {
  background: var(--cm-ink);
  color: rgba(255,255,255,0.8);
  padding: 2.5rem 0;
  font-size: 0.88rem;
  margin-top: 3rem;
  border-top: 3px solid var(--cm-green);
}
.footer-inner { text-align: center; }
.footer-links { display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; margin-bottom: 1rem; }
.footer-links a { color: rgba(255,255,255,0.8); text-decoration: none; transition: color 0.15s; }
.footer-links a:hover { color: #fff; }
.footer-social { display: flex; justify-content: center; gap: 1.25rem; margin-bottom: 1rem; }
.footer-social a { color: var(--cm-pink); text-decoration: none; transition: opacity 0.15s; }
.footer-social a:hover { opacity: 0.88; }
.footer-legal { color: rgba(255,255,255,0.55); font-size: 0.78rem; max-width: 640px; margin: 0 auto 0.5rem; line-height: 1.5; }
.footer-copy { color: rgba(255,255,255,0.5); font-size: 0.8rem; }

/* ---- Responsive ---- */
@media (max-width: 768px) {
  html { font-size: 16px; }
  .hero h1 { font-size: 2.4rem; }
  .hero { padding: 3rem 0 2.5rem; }
  .hero-light h1 { font-size: 2rem; }
  .nav-logo-img { height: 57px; }
  .nav-inner { flex-wrap: wrap; }
  .two-col-grid { grid-template-columns: 1fr; }
  .team-grid { grid-template-columns: 1fr; }
  .nav-toggle { display: flex; order: 2; margin-left: auto; }
  .nav-cta { order: 3; }
  .nav-links {
    display: none; order: 4; width: 100%; flex-basis: 100%;
    flex-direction: column; align-items: stretch; gap: 0;
    padding: 0.5rem 0 0.25rem;
  }
  .nav-links.open { display: flex; }
  .nav-links > a,
  .nav-dropdown-trigger { padding: 0.75rem 0.25rem; border-bottom: 1px solid rgba(255,255,255,0.08); }
  .nav-dropdown { display: block; }
  .nav-dropdown-menu {
    display: block; position: static; box-shadow: none; padding: 0 0 0.25rem 1rem;
    background: transparent; border-radius: 0; min-width: 0;
  }
  .nav-dropdown-menu a { padding: 0.45rem 0.25rem; }
  .site-search-form { order: 5; width: 100%; flex-basis: 100%; }
  .search-page-form,
  .site-search-form { flex-wrap: wrap; }
  .search-page-form .search-submit { width: 100%; }
  .site-search-form .search-submit { width: 2.35rem; }
  .features { padding: 2.5rem 0; }
  .steps-grid { grid-template-columns: 1fr; }
  .stand-pills-grid { grid-template-columns: 1fr; }
}
@media (prefers-reduced-motion: reduce) {
  .scroll-reveal {
    opacity: 1;
    transform: none;
    transition: none;
  }
  .hl.hl-reveal { transition: none; }
  .hl.hl-reveal.hl-active.hl-yellow { box-shadow: inset 0 -0.42em 0 0 rgba(240, 215, 107, 0.85); }
  .hl.hl-reveal.hl-active.hl-pink { box-shadow: inset 0 -0.42em 0 0 rgba(255, 190, 200, 0.8); }
  .hl.hl-reveal.hl-active.hl-green { box-shadow: inset 0 -0.42em 0 0 rgba(43, 169, 156, 0.45); }
}

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

/* ---- Print-only banner (shown only when printing) ---- */
.print-banner { display: none; }

/* ---- Print stylesheet ---- */
@media print {
  @page {
    margin: 20mm 18mm 22mm;
    @bottom-center { content: counter(page) " / " counter(pages); font-family: Georgia, serif; font-size: 9pt; color: #555; }
    @bottom-left { content: "causalmap.app"; font-family: Georgia, serif; font-size: 9pt; color: #555; }
  }
  * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
  html, body { background: #fff !important; color: #000 !important; }
  body { font-family: Georgia, "Times New Roman", serif !important; font-size: 10.5pt !important; line-height: 1.5 !important; }

  /* Hide all site chrome */
  nav, .site-nav, .nav-inner, .nav-toggle, .site-search-form, .nav-logo, .nav-cta,
  footer, .footer-inner, .footer-links, .footer-social, .footer-copy,
  .accent-stripe, .print-link, .no-print,
  .scroll-reveal, button.nav-toggle { display: none !important; }

  /* Reveal the print banner */
  .print-banner {
    display: block !important;
    border-bottom: 1.5pt solid #000;
    padding-bottom: 6pt;
    margin-bottom: 14pt;
  }
  .print-banner .brand { font-weight: 700; font-size: 13pt; color: #000; letter-spacing: 0.2pt; }
  .print-banner .url { float: right; font-size: 9.5pt; color: #555; }

  /* Layout reset */
  main { display: block !important; }
  .container { max-width: 100% !important; padding: 0 !important; margin: 0 !important; width: 100% !important; }
  section, .prose-section, .hero, .hero-light {
    padding: 0 !important; margin: 0 0 0.5rem !important;
    background: #fff !important; color: #000 !important; box-shadow: none !important;
  }

  /* Headings */
  .prose-section h1, .prose-section h2 {
    font-family: Georgia, serif !important;
    font-size: 18pt !important;
    font-weight: 700 !important;
    border: 0 !important;
    color: #000 !important;
    padding: 0 0 4pt !important;
    margin: 0 0 8pt !important;
  }
  .prose-section h2:not(:first-of-type) { margin-top: 18pt !important; padding-top: 4pt !important; border-top: 0.5pt solid #888 !important; }
  .prose-section h3 { font-size: 12.5pt !important; font-weight: 700 !important; margin: 10pt 0 4pt !important; color: #000 !important; }
  .prose-section h4 { font-size: 11pt !important; font-weight: 700 !important; font-style: italic; margin: 8pt 0 3pt !important; color: #000 !important; }
  h1, h2, h3, h4 { page-break-after: avoid !important; break-after: avoid !important; }
  h2 + p, h2 + ul, h3 + p, h3 + ul, h4 + p, h4 + ul { page-break-before: avoid !important; }

  /* Body text */
  p { margin: 0 0 6pt !important; orphans: 3; widows: 3; }
  ul, ol { margin: 0 0 8pt 18pt !important; padding: 0 !important; }
  li { margin-bottom: 2pt !important; page-break-inside: avoid !important; }
  blockquote {
    border-left: 2pt solid #000 !important; background: transparent !important;
    padding: 2pt 0 2pt 10pt !important; margin: 8pt 0 !important;
    font-style: italic; color: #000 !important;
  }
  blockquote p { margin: 0 !important; }

  /* Tables */
  table { width: 100% !important; border-collapse: collapse !important; margin: 8pt 0 !important; font-size: 9.5pt !important; page-break-inside: auto !important; }
  th, td { border: 0.5pt solid #888 !important; padding: 4pt 6pt !important; text-align: left !important; vertical-align: top !important; background: #fff !important; color: #000 !important; }
  th { background: #eee !important; font-weight: 700 !important; }
  tr { page-break-inside: avoid !important; }

  /* Highlights become bold plain text */
  .hl, span[class*="hl-"] {
    background: transparent !important; box-shadow: none !important;
    color: #000 !important; font-weight: 700 !important; padding: 0 !important;
  }

  /* Links */
  a, a:link, a:visited { color: #000 !important; text-decoration: underline !important; }
  a[href^="http"]:not([href*="causalmap.app"])::after,
  a[href^="https://www.notion"]::after { content: " (" attr(href) ")"; font-size: 0.82em; color: #555; word-break: break-all; }
  a[href^="mailto:"]::after, a[href^="#"]::after, a[href^="/"]::after, a[href^="../"]::after { content: "" !important; }
}
'''

def page_template(title, nav_html, content_html, footer_html, cfg, meta_desc="", search_index=None):
    site_name = cfg.get("site_name", "Causal Map")
    desc = meta_desc or "Causal mapping software for qualitative research and evaluation"
    search_script = build_search_script(search_index) if search_index is not None else ""
    analytics_html = build_analytics_html(cfg)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{desc}">
  <link rel="icon" href="/assets/favicon.ico" sizes="any">
  <title>{title} | {site_name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
  {analytics_html}
  <style>{build_css(cfg)}</style>
</head>
<body>
{nav_html}
<main>
<div class="print-banner"><span class="brand">Causal Map</span><span class="url">causalmap.app</span></div>
{content_html}
</main>
{footer_html}
<script>
(function () {{
  const toggle = document.querySelector(".nav-toggle");
  const links = document.getElementById("nav-links");
  if (toggle && links) {{
    toggle.addEventListener("click", () => {{
      const open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }});
  }}
}})();
(function () {{
  const headings = document.querySelectorAll("main h1, main h2, main h3");
  if (!headings.length) return;

  headings.forEach((heading) => heading.classList.add("scroll-reveal"));

  if (!("IntersectionObserver" in window)) {{
    headings.forEach((heading) => heading.classList.add("in-view"));
    return;
  }}

  const observer = new IntersectionObserver((entries) => {{
    entries.forEach((entry) => {{
      if (entry.isIntersecting) {{
        entry.target.classList.add("in-view");
      }} else {{
        entry.target.classList.remove("in-view");
      }}
    }});
  }}, {{ threshold: 0.2, rootMargin: "0px 0px -12% 0px" }});

  headings.forEach((heading) => observer.observe(heading));
}})();
function cycleHighlightGroup(root) {{
  const holdMs = 2500;
  const fadeMs = 3000;
  let timer = null;
  let inView = false;
  const cards = root.querySelectorAll(".feature-card");
  const cardData = cards.length
    ? Array.from(cards)
        .map((card) => ({{ phrases: Array.from(card.querySelectorAll(".hl-reveal")) }}))
        .filter((c) => c.phrases.length)
    : [];
  const phrases = cardData.length
    ? cardData.flatMap((c) => c.phrases)
    : Array.from(root.querySelectorAll(".hl-reveal"));
  if (!phrases.length) return;

  function shuffle(arr) {{
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {{
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }}
    return a;
  }}
  function clearPhrases() {{
    phrases.forEach((p) => p.classList.remove("hl-active"));
  }}
  function activeCount(total) {{
    const jitter = Math.random() < 0.5 ? 0 : (Math.random() < 0.5 ? -1 : 1);
    return Math.max(1, Math.round(total / 3 + jitter));
  }}
  function nextDelay() {{
    return holdMs + fadeMs * 2 + Math.floor(Math.random() * 3000);
  }}
  function pick() {{
    if (cardData.length === 1 && phrases.length === 1) {{
      phrases[0].classList.add("hl-active");
      return;
    }}
    clearPhrases();
    void root.offsetHeight;
    if (cardData.length) {{
      const n = activeCount(cardData.length);
      shuffle(cardData).slice(0, n).forEach((c) => {{
        const ps = c.phrases;
        ps[Math.floor(Math.random() * ps.length)].classList.add("hl-active");
      }});
    }} else if (phrases.length === 1) {{
      phrases[0].classList.add("hl-active");
    }} else {{
      shuffle(phrases).slice(0, activeCount(phrases.length)).forEach((p) => p.classList.add("hl-active"));
    }}
  }}
  function stop() {{
    if (timer) clearTimeout(timer);
    timer = null;
  }}
  function schedule() {{
    stop();
    timer = setTimeout(function tick() {{
      pick();
      timer = setTimeout(tick, nextDelay());
    }}, nextDelay());
  }}
  function bump() {{
    stop();
    pick();
    schedule();
  }}
  function onLeave() {{
    stop();
    clearPhrases();
  }}

  if (!("IntersectionObserver" in window)) {{
    bump();
    return;
  }}
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach((entry) => {{
      if (entry.isIntersecting) {{
        if (!inView) {{
          inView = true;
          bump();
        }}
      }} else if (inView) {{
        inView = false;
        onLeave();
      }}
    }});
  }}, {{ threshold: 0.2, rootMargin: "0px 0px -12% 0px" }});
  observer.observe(root);
}}
function cycleHighlights() {{
  document.querySelectorAll("[data-hl-cycle]").forEach(cycleHighlightGroup);
}}
if (document.readyState === "loading") {{
  document.addEventListener("DOMContentLoaded", cycleHighlights);
}} else {{
  cycleHighlights();
}}
</script>
{search_script}
</body>
</html>'''

def redirect_template(title, redirect):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0;url={redirect}">
  <meta name="robots" content="noindex">
  <link rel="icon" href="/assets/favicon.ico" sizes="any">
  <link rel="canonical" href="{redirect}">
  <title>{title}</title>
  <script>window.location.replace({redirect!r});</script>
</head>
<body>
  <p>Redirecting to <a href="{redirect}">{redirect}</a>...</p>
</body>
</html>'''

def site_url_for(base, path):
    """Absolute canonical URL for a page path. Directory paths get a trailing slash."""
    base = base.rstrip("/")
    stripped = path.strip("/")
    if not stripped:
        return base + "/"
    if "." in stripped.split("/")[-1]:
        return f"{base}/{stripped}"
    return f"{base}/{stripped}/"

def build_sitemap_xml(pages, base):
    """XML sitemap of indexable pages (skips redirects and the 404 page)."""
    urls = []
    for page in sorted(pages, key=lambda p: p["_path"]):
        if page.get("redirect"):
            continue
        path = page["_path"]
        if path == "/404.html":
            continue
        loc = html_lib.escape(site_url_for(base, path), quote=True)
        date = str(page.get("date") or "").strip()
        lastmod = f"\n    <lastmod>{date}</lastmod>" if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date) else ""
        urls.append(f"  <url>\n    <loc>{loc}</loc>{lastmod}\n  </url>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )

def build_robots_txt(base):
    return (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {base.rstrip('/')}/sitemap.xml\n"
    )

def redirect_rules_for(path, redirect):
    src = path.rstrip("/") or "/"
    if src == "/":
        return []
    return [
        f"{src} {redirect} 301",
        f"{src}/ {redirect} 301",
    ]

def build():
    cfg = load_config()
    input_dir = SCRIPT_DIR / cfg.get("input_dir", "content")
    output_dir = SCRIPT_DIR / cfg.get("output_dir", "dist")

    if output_dir.exists():
        shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    pages = []
    md_files = sorted(p for p in input_dir.rglob("*.md") if "assets" not in p.parts)
    for mdfile in md_files:
        page = parse_page(mdfile)
        page["_file"] = str(mdfile.relative_to(input_dir)).replace("\\", "/")
        page["_path"] = page.get("path", "/" + mdfile.stem)
        if not page.get("redirect"):
            page["_content_html"] = render_sections(page, cfg)
        pages.append(page)

    # Tag chips on tagged pages + collect tag membership for index pages
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

    search_index = build_search_index(pages)
    nav_html = build_nav(pages, cfg)
    footer_html = build_footer(cfg)
    redirect_rules = []

    for page in pages:
        title = page.get("title", "Untitled")
        meta_desc = page.get("description", "")
        path = page["_path"]
        redirect = page.get("redirect")
        if redirect:
            html = redirect_template(title, redirect)
            redirect_rules.extend(redirect_rules_for(path, redirect))
        else:
            content_html = page["_content_html"]
            html = page_template(
                title,
                nav_html,
                content_html,
                footer_html,
                cfg,
                meta_desc,
                search_index if path == "/search" else None,
            )
            html = make_links_relative(html, path)
        html = add_external_link_attrs(html)
        html = tag_app_links(html, cfg)
        if path == "/":
            out_file = output_dir / "index.html"
        elif "." in path.strip("/").split("/")[-1]:
            out_file = output_dir / path.strip("/")
            out_file.parent.mkdir(parents=True, exist_ok=True)
        else:
            out_dir = output_dir / path.strip("/")
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / "index.html"

        out_file.write_text(html, encoding="utf-8")
        print(f"  {path} -> {out_file.relative_to(SCRIPT_DIR)}")

    # Copy assets
    assets_src = input_dir / "assets"
    if assets_src.exists():
        shutil.copytree(assets_src, output_dir / "assets", dirs_exist_ok=True)
        print("  assets/ copied")

    if redirect_rules:
        redirects_path = output_dir / "_redirects"
        redirects_path.write_text("\n".join(redirect_rules) + "\n", encoding="utf-8")
        print("  _redirects written")

    base_url = cfg.get("site_url", "https://causalmap.app")
    (output_dir / "sitemap.xml").write_text(build_sitemap_xml(pages, base_url), encoding="utf-8")
    (output_dir / "robots.txt").write_text(build_robots_txt(base_url), encoding="utf-8")
    print("  sitemap.xml + robots.txt written")

    print(f"\nBuilt {len(pages)} pages to {output_dir.relative_to(SCRIPT_DIR)}/")

if __name__ == "__main__":
    build()
