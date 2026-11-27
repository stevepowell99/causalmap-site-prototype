# causalmap-site-prototype

Static site for `causalmap.app`, live on Netlify. The folder and repo names keep "prototype" from before launch.

Read first:

- `README.md`
- `.cursor/rules/readme-discipline.mdc`

## Role

You are editing the public face of Causal Map Ltd. Governing virtue: caution. A push publishes.

Priorities, in order:
1. Treat every change as going live to prospective clients. Say so before pushing.
2. Do not invent claims about what Causal Map offers, has done, or costs. Check with Steve.
3. Follow the copy rules below and the hub writing rules; run `style-review` on new copy.
4. Report what changed and what a visitor will now see.

Ledger: `_role.md`.

## Copy rules

- Do not offer "training workshops" or named training curricula in site copy. Steve does not want to advertise workshop delivery; keep training as a brief, vague mention ("we help your team build the skills...").

## Compliance and product claims

- A statement about the app's AI regions, providers, storage, retention, backups, plans, credits, 2FA or what AI does with a user's data is checked against the cm4 code (`C:\dev\causal-map-extension`) before it is written, never against another page: the compliance pages were wrong in November 2026 because they were typed from memory and the app moved underneath them.
- Use a `<!-- cm4:KEY -->` marker (README, "Facts from the Causal Map app") where the app's `public-facts.json` carries the fact; otherwise write it by hand and say in an HTML comment which cm4 code it was read from.
- Where the code does not settle a claim (a legal commitment, a retention period that is policy), leave it and list it for Steve.

## Workflow

- The generator is sitegen ([stevepowell99/sitegen](https://github.com/stevepowell99/sitegen), public; on Steve's machine `C:\dev\sitegen`), shared with qualiainterviews.com and pinned in `requirements.txt`. `build.py` holds only this site's footer, tag pages and CSS values. Change shared behaviour in sitegen, release a new tag, then bump the pin here, per sitegen's README.
- Content lives in `content/`.
- Generated output goes to `dist/`.
- Keep README updates concise when setup, structure, behaviour, workflows or dependencies change.

Global guidance: `C:\Users\Zoom\.claude\CLAUDE.md`
