# Consolidate the newsletter sign-up forms

Owner: Gabriele. Raised 15 August 2026 while adding the LinkedIn newsletter links to the three sites. Also posted to `gabi-steve-claude1`.

We ask people to sign up through six different forms across the three sites, and four of them collect the same thing. Four are Wix forms, all still returning 200, so they are still taking addresses into an account we have otherwise left. Anyone who signs up through the Garden or the eval22 page is landing somewhere nobody reads.

## The four that collect "Causal Map news"

| Form | Where it appears |
|------|------------------|
| `https://forms.gle/JrK2AE6NTsGzUvWe8` (Google) | causalmap.app `/contact`, and a CTA on the home page (`content/home.md`) |
| `https://forms.wix.com/f/6990334085528813568` (Wix) | Garden About page (`19aCMgarden/content/990 Finally/1140 About ((about)).md`) |
| `https://forms.wix.com/61ba16e1-ecce-4108-85c6-cafefe6b1b0d:309d5446-7e6e-4660-b8de-62c8ed6432b4` (Wix) | causalmap.app `/events/eval22` |
| `https://forms.wix.com/f/6992844431304950386` (Wix) | causalmap.app `/events/eval22`, a StorySurvey waiting list. StorySurvey became Qualia, so it collects for a product that no longer exists under that name |

## The two that are topic-specific

These are arguably fine as they are, but decide whether they still earn their place.

| Form | Where it appears |
|------|------------------|
| `https://docs.google.com/forms/d/e/1FAIpQLScuYBIfGGnq_0JZrnjjJzq8fGNIuNZOErauaROJ6l_ur8S9UA/viewform` | Outcome Harvesting with AI, causalmap.app `/events/coffee-break-oh` |
| `https://docs.google.com/forms/d/e/1FAIpQLSfNqtic4f1kPQBW3BH7hQf6aEuUa9TmGsYbHz3SIEHxTfN_-g/viewform` | The Qualia newsletter, qualiainterviews.com `/contact` and that site's footer (`config.yml`) |

## What to decide

1. Which single form is the one we keep for Causal Map news. The Google one is the obvious candidate, since it is already on the main site in two places.
2. Whether anything useful is sitting in the three Wix forms' responses. Export them before retiring the forms.
3. Whether the LinkedIn newsletters now replace the email list altogether, in which case the sign-up prompts become newsletter links.

## Then

- Point the Garden About page at the surviving form, or at the LinkedIn newsletters.
- Strip both sign-ups from `/events/eval22`. It is a 2022 event write-up and neither form belongs on it.
- Leave the Qualia form alone unless step 3 says otherwise. It is a different audience.

Ask Claude to make the edits once the decisions are made. All three sites publish on push, so each change is live within a couple of minutes.
