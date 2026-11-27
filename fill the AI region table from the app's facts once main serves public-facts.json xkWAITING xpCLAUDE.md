# Fill the AI region table from the app's facts once main serves public-facts.json

- Waiting on: Steve merging causal-map-extension `dev` into `main`, which deploys `webapp/public-facts.json` (commit `5bc6f2953`, 27 November 2026) to https://app.causalmap.app/public-facts.json.
- Check: `curl -s https://app.causalmap.app/public-facts.json` returns JSON with `ai_regions`.
- Then:
    - `git apply _tmp/cm4-facts-markers.patch`: puts `cm4:` markers in place of the hand-typed AI region table (`content/ai-compliance.md`) and the Supabase, Vertex AI, Cloud Functions, DashScope and OpenAI cells (`content/privacy.md`)
    - `python build.py` (no `CM4_FACTS_FILE`), check it prints "cm4 facts from https://app.causalmap.app/... filled on /ai-compliance, /privacy-policy"
    - commit the two content files by path, push, and confirm the live pages show the table
- Until then the pages carry the same facts typed by hand, and `build.py` reads nothing, since no page has a marker. Pushing the markers before main serves the file stops every site build, other sessions' too.
- If the patch no longer applies (someone edited those rows), redo the markers by hand from the patch.
