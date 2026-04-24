#!/usr/bin/env python3
"""
Static site builder for causalmap.app
Reads markdown files with YAML front matter from content/, outputs HTML to dist/.
"""

import os
import sys
import re
import shutil
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

def render_hero(section, cfg):
    headline = section.get("headline", "")
    subhead = md(section.get("subhead", ""))
    cta_text = section.get("cta_text", "")
    cta_url = section.get("cta_url", "#")
    cta_html = f'<a class="btn-cta" href="{cta_url}">{cta_text}</a>' if cta_text else ""
    return f'''<section class="hero">
  <div class="container">
    <h1>{headline}</h1>
    <div class="hero-sub">{subhead}</div>
    {cta_html}
  </div>
</section>'''

def render_hero_light(section, cfg):
    headline = section.get("headline", "")
    subhead = md(section.get("subhead", ""))
    return f'''<section class="hero-light">
  <div class="container">
    <h1>{headline}</h1>
    {f'<div class="hero-sub">{subhead}</div>' if subhead else ''}
  </div>
</section>'''

def render_features(section, cfg):
    cols = section.get("columns", [])
    cards = ""
    for col in cols:
        cards += f'''<div class="feature-card">
      <h3>{col.get("title","")}</h3>
      {md(col.get("text",""))}
    </div>\n'''
    return f'''<section class="features">
  <div class="container">
    <div class="features-grid">{cards}</div>
  </div>
</section>'''

def render_video(section, cfg):
    url = section.get("url", "")
    vid_id = ""
    if "vimeo.com" in url:
        vid_id = url.rstrip("/").split("/")[-1]
        embed = f'https://player.vimeo.com/video/{vid_id}'
    elif "youtube.com" in url or "youtu.be" in url:
        m = re.search(r'(?:v=|youtu\.be/)([^&?]+)', url)
        vid_id = m.group(1) if m else ""
        embed = f'https://www.youtube.com/embed/{vid_id}'
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

SECTION_RENDERERS = {
    "hero": render_hero,
    "hero-light": render_hero_light,
    "features": render_features,
    "video": render_video,
    "two-col": render_two_col,
    "steps": render_steps,
    "trust-strip": render_trust_strip,
    "logos": render_logos,
    "testimonials": render_testimonials,
    "cta-banner": render_cta_banner,
    "team": render_team,
}

def make_links_relative(html, page_path):
    """Convert absolute internal links to relative paths for file:// preview."""
    import re
    page_depth = page_path.strip("/").count("/") + (0 if page_path == "/" else 1)
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

    return re.sub(r'(href|src)="(/[^"]*)"', lambda m: replace_href(m), html)

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

    return f'''<nav class="navbar">
  <div class="container nav-inner">
    <a href="/" class="nav-logo">{logo}</a>
    <div class="nav-links">
{links}    </div>
    <a class="btn-cta nav-cta" href="{app_url}">Try it free</a>
  </div>
</nav>
<div class="accent-stripe"></div>'''

def build_footer(cfg):
    return '''<footer>
  <div class="container footer-inner">
    <div class="footer-links">
      <a href="/terms-and-conditions">Terms</a>
      <a href="/privacy-policy">Privacy</a>
      <a href="/sla">SLA</a>
      <a href="/ethical-principles">Ethical Principles</a>
      <a href="https://forms.gle/JrK2AE6NTsGzUvWe8">Newsletter</a>
    </div>
    <div class="footer-social">
      <a href="https://www.linkedin.com/company/causalmap">LinkedIn</a>
      <a href="mailto:hello@causalmap.app">Email</a>
      <a href="https://www.youtube.com/watch?v=YskPTmWfADw&list=PLSCKdSxlLlfGfcab5njcT57xzU0hOURc-">YouTube</a>
      <a href="https://github.com/stevepowell99/">GitHub</a>
    </div>
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
    cm_bg = colors.get("body_bg", "#fcfcfc")
    cm_text = colors.get("text", "#222")
    return f''':root {{
  --cm-ink: {cm_ink};
  --cm-pink: {cm_pink};
  --cm-green: {cm_green};
  --cm-teal: {cm_teal};
  --cm-bg: {cm_bg};
  --cm-text: {cm_text};
  --cm-light: #f4f6f8;
  --cm-border: #e2e6ea;
  --radius: 8px;
  --cm-green-light: {rgba(cm_green, 0.08)};
  --cm-teal-light: {rgba(cm_teal, 0.10)};
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

a { transition: color 0.15s; }

.container { max-width: 960px; margin: 0 auto; padding: 0 1.5rem; }

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
  padding: 0.6rem 0;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.nav-inner { display: flex; align-items: center; gap: 1.5rem; }
.nav-logo {
  text-decoration: none; margin-right: auto; display: flex; align-items: center;
}
.nav-logo-img { height: 56px; width: auto; }
.nav-links { display: flex; align-items: center; gap: 1.25rem; }
.nav-links > a { color: rgba(255,255,255,0.85); text-decoration: none; font-size: 0.92rem; transition: color 0.15s; padding: 0.5rem 0; }
.nav-links a:hover { color: #fff; }
.nav-cta { margin-left: 0.5rem; }

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
  color: #fff;
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
  color: #fff;
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
.hero-light h1 { font-size: 2.86rem; font-weight: 700; margin-bottom: 0.75rem; color: var(--cm-ink); }
.hero-light .hero-sub { font-size: 1.05rem; color: #666; max-width: none; margin: 0; opacity: 1; }

/* ---- Features grid ---- */
.features { padding: 4rem 0; background: var(--cm-light); }
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 2rem; }
.feature-card {
  background: #fff;
  border: 1px solid var(--cm-border);
  border-top: 3px solid var(--cm-green);
  border-radius: var(--radius);
  padding: 2rem;
  transition: transform 0.15s, box-shadow 0.15s;
}
.feature-card:nth-child(2) { border-top-color: var(--cm-teal); }
.feature-card:nth-child(3) { border-top-color: var(--cm-pink); }
.feature-card:nth-child(4) { border-top-color: var(--cm-green); }
.feature-card:nth-child(5) { border-top-color: var(--cm-teal); }
.feature-card:nth-child(6) { border-top-color: var(--cm-pink); }
.feature-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.06); }
.feature-card h3 { font-size: 1.1rem; margin-bottom: 0.5rem; color: var(--cm-ink); font-weight: 600; }
.feature-card p { font-size: 0.95rem; color: #555; }
.feature-card a, .step-item a, .two-col a, .hero a, .hero-light-inner a { color: var(--cm-ink); text-decoration: underline; text-decoration-color: var(--cm-teal); text-underline-offset: 2px; }
.feature-card a:hover, .step-item a:hover, .two-col a:hover, .hero a:hover, .hero-light-inner a:hover { color: var(--cm-teal); }

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
.two-col a { color: var(--cm-ink); text-decoration: underline; text-underline-offset: 2px; }
.two-col a:hover { color: var(--cm-teal); }

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
.team-card .team-role { font-size: 0.85rem; color: var(--cm-green); font-weight: 600; margin-bottom: 0.5rem; }
.team-card p { font-size: 0.9rem; color: #555; line-height: 1.55; }
.team-link { font-size: 0.8rem; color: var(--cm-teal); text-decoration: none; font-weight: 400; }
.team-link:hover { color: var(--cm-green); }

/* ---- Prose ---- */
.prose-section { padding: 3.5rem 0; }
.prose-section h2 {
  font-size: 1.4rem; margin: 2rem 0 0.75rem; color: var(--cm-ink); font-weight: 600;
  padding-bottom: 0.4rem;
  border-bottom: 2px solid var(--cm-green);
  display: inline-block;
}
.prose-section h3 { font-size: 1.15rem; margin: 1.5rem 0 0.5rem; color: var(--cm-ink); font-weight: 600; }
.prose-section p { margin-bottom: 1rem; }
.prose-section ul, .prose-section ol { margin: 0 0 1rem 1.5rem; }
.prose-section li { margin-bottom: 0.35rem; }
.prose-section li::marker { color: var(--cm-teal); }
.prose-section a { color: var(--cm-ink); text-decoration: underline; text-underline-offset: 2px; }
.prose-section a:hover { color: var(--cm-teal); }
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
.prose-section td.check { color: var(--cm-green); font-weight: 700; font-size: 1.1rem; text-align: center; }

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
.footer-copy { color: rgba(255,255,255,0.5); font-size: 0.8rem; }

/* ---- Responsive ---- */
@media (max-width: 768px) {
  html { font-size: 16px; }
  .hero h1 { font-size: 2.4rem; }
  .hero { padding: 3rem 0 2.5rem; }
  .hero-light h1 { font-size: 2rem; }
  .nav-logo-img { height: 44px; }
  .two-col-grid { grid-template-columns: 1fr; }
  .team-grid { grid-template-columns: 1fr; }
  .nav-links { display: none; }
  .features { padding: 2.5rem 0; }
  .steps-grid { grid-template-columns: 1fr; }
}
'''

def page_template(title, nav_html, content_html, footer_html, cfg, meta_desc=""):
    site_name = cfg.get("site_name", "Causal Map")
    desc = meta_desc or "Causal mapping software for qualitative research and evaluation"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{desc}">
  <title>{title} | {site_name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>{build_css(cfg)}</style>
</head>
<body>
{nav_html}
<main>
{content_html}
</main>
{footer_html}
</body>
</html>'''

def redirect_template(title, redirect):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0;url={redirect}">
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{redirect}">
  <title>{title}</title>
  <script>window.location.replace({redirect!r});</script>
</head>
<body>
  <p>Redirecting to <a href="{redirect}">{redirect}</a>...</p>
</body>
</html>'''

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
    for mdfile in sorted(input_dir.glob("*.md")):
        page = parse_page(mdfile)
        page["_file"] = mdfile.name
        pages.append(page)

    nav_html = build_nav(pages, cfg)
    footer_html = build_footer(cfg)
    redirect_rules = []

    for page in pages:
        title = page.get("title", "Untitled")
        meta_desc = page.get("description", "")
        path = page.get("path", "/" + page["_file"].replace(".md", ""))
        redirect = page.get("redirect")
        if redirect:
            html = redirect_template(title, redirect)
            redirect_rules.extend(redirect_rules_for(path, redirect))
        else:
            content_html = render_sections(page, cfg)
            html = page_template(title, nav_html, content_html, footer_html, cfg, meta_desc)
            html = make_links_relative(html, path)
        if path == "/":
            out_file = output_dir / "index.html"
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

    print(f"\nBuilt {len(pages)} pages to {output_dir.relative_to(SCRIPT_DIR)}/")

if __name__ == "__main__":
    build()
