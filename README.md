# causalmap-site-prototype

Static site prototype for **causalmap.app**, replacing the previous Notion + bullet.io setup.

## How it works

A Python script (`build.py`) reads markdown files from `content/`, renders them to HTML, and writes the output to `dist/`. Each markdown file uses YAML front matter to define the page path, navigation order, and layout sections. The prose body (below the second `---`) is rendered as standard markdown.

There is no external static site generator. Everything is in `build.py`: section renderers, CSS, navigation builder, and the build loop.

## Structure

```
causalmap-site-prototype/
  build.py        Site generator (single script, ~650 lines)
  config.yml      Brand colours, input/output dirs
  content/        Markdown source files + assets/
    home.md         Homepage (path: /)
    product.md      Causal Map app page, with dropdown nav to Consultancy and QualiaInterviews
    pricing.md      Subscription tiers, feature table, pricing table, discounts
    consultancy.md  Consultancy services
    causal-mapping.md  "What is causal mapping?" explainer
    about.md        About us + team, with dropdown nav to causal-mapping
    resources.md    Links to Guide, case studies, bibliography, videos
    contact.md      Contact form / details
    search.md       Search page (client-side search over built page content)
    qualiainterviews.md  Redirect stub to qualiainterviews.com
    ethical-principles.md, privacy-policy.md, sla.md, terms-and-conditions.md  Legal pages
    assets/         Logo files (logo-white.png, logo-dark.png) and team photos
  dist/           Generated HTML site (output)
```

## Content format

Each `.md` file has YAML front matter controlling the page layout:

```yaml
---
title: Page Title
path: /page-path
nav_order: 2          # position in top nav (omit to exclude from nav)
nav_label: Nav Text   # label shown in nav bar
nav_children:         # optional dropdown menu
  - label: Sub-item
    path: /sub-path
description: Meta description for SEO.
sections:
  - type: hero
    headline: Main heading
    subhead: Supporting text (rendered as markdown)
    cta_text: Button label
    cta_url: https://...
  - type: features
    columns:
      - title: Card title
        text: Card body (rendered as markdown)
  - type: prose       # signals that the markdown body below should be rendered
---

Markdown body goes here (only rendered if a `prose` section is listed).
```

## Section types

The build script supports these section types:

- **hero**: dark background, large headline, subhead, CTA button
- **hero-light**: light background variant
- **features**: grid of cards (2 or 3 columns)
- **steps**: numbered workflow steps
- **video**: Vimeo or YouTube embed
- **two-col**: two-column layout with title and markdown body per column
- **trust-strip**: "Trusted by" organisation list
- **testimonials**: quote cards
- **team**: team member cards with photos
- **cta-banner**: call-to-action strip
- **search**: client-side search page with indexed site content
- **prose**: renders the markdown body below the front matter
- **logos**: logo images

## Brand colours

Brand colours are defined in `config.yml` and exposed in the generated CSS as the `:root` variables `--cm-ink`, `--cm-pink`, `--cm-green`, `--cm-teal`, `--cm-bg`, and `--cm-text`.

## Building

```bash
python build.py
```

Requires Python 3 with `pyyaml` and `markdown`:

```bash
pip install pyyaml markdown
```

Output goes to `dist/`. Open `dist/index.html` in a browser to preview.

## Navigation

Top-level nav items are defined by `nav_order` in front matter. Dropdown menus use `nav_children`. The nav bar shows the logo (from `content/assets/logo-white.png`), top-level items, and a sitewide search form that submits to `/search`.

## Links and cross-references

Internal links in markdown content use absolute paths (`/pricing`, `/causal-mapping`) which are converted to relative paths by `make_links_relative()` so the site works both from a web server and from `file://`.

Several pages link to specific Garden pages (garden.causalmap.app) using short-URL anchors defined by `((anchor))` tags in the Garden's markdown filenames (e.g. `((main-outcomes))`, `((comparing-groups))`).

## Design decisions

- All content containers are 960px max-width for consistent alignment.
- Feature cards and steps render their text as markdown, so inline links work.
- Links inside cards and sections use ink-coloured text with teal underlines (not browser-default blue).
- Hero and hero-light headings are left-aligned, not centred.
- Pricing page uses green checkmarks in feature comparison tables.
- Visual accents (coloured card borders, gradient stripes, green h2 underlines) use the brand palette.
- `<td>Yes</td>` in tables is automatically replaced with a teal checkmark.
- Redirect pages (e.g. QualiaInterviews) use `redirect` in front matter to generate a meta-refresh page.

## Deployment

For Netlify, track the parent repo, not just `dist/`. Set the publish directory to `dist/`. That keeps the source files (`content/`, `build.py`, `config.yml`) versioned properly while Netlify serves only the generated site.
