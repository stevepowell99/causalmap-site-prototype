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

## Workflow

- The generator is sitegen ([stevepowell99/sitegen](https://github.com/stevepowell99/sitegen), public; on Steve's machine `C:\dev\sitegen`), shared with qualiainterviews.com and pinned in `requirements.txt`. `build.py` holds only this site's footer, tag pages and CSS values. Change shared behaviour in sitegen, release a new tag, then bump the pin here, per sitegen's README.
- Content lives in `content/`.
- Generated output goes to `dist/`.
- Keep README updates concise when setup, structure, behaviour, workflows or dependencies change.

Global guidance: `C:\Users\Zoom\.claude\CLAUDE.md`
