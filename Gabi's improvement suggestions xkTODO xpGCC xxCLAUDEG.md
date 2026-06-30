# Gabi's improvement suggestions

Here I'll add my comments/suggestions for improving the CM website. I'll split them by website page

# Product

https://causalmap.netlify.app/product/ 

In the box titled 'Manual and AI coding', add a link to the case studies section in the Garden to provide examples for the users: https://garden.causalmap.app/case-studies/

# Consultancy 

https://causalmap.netlify.app/pricing/

Add a section on costs for transparency. Something like the text below, but you can edit it to fit with the new website format.

### Costs

We believe in full transparency around costs, so you can make informed decisions about investing in causal insight for your organisation.

We anticipate that a simple causal mapping project will take a **minimum of 2 days’** billable time spread out over a week or two, not including additional iterations of the research design and any additional reporting. Our standard consulting rate is £695 + VAT per day.

These rates are negotiable for particularly interesting use cases and for clients from the global South.

Email us at [hello@causalmap.app](mailto:hello@causalmap.app) to talk about the consultancy services.



# Pricing

In the description of the 'App subscriptions', add a link to causal map app (https://app.causalmap.app/) to the excerpt highlighted "sig up in the app"ning

![image-20260424104255158](C:\Users\gabic\AppData\Roaming\Typora\typora-user-images\image-20260424104255158.png)

### AI add-ons

In this section, add that users can purchase the addons directly from the app and the prices for each plan with an AI add-on are these: 



Monthly prices

![image-20260424104814022](C:\Users\gabic\AppData\Roaming\Typora\typora-user-images\image-20260424104814022.png)



Annual prices

![image-20260424104840218](C:\Users\gabic\AppData\Roaming\Typora\typora-user-images\image-20260424104840218.png)



# Get in touch

https://causalmap.netlify.app/contact/ 

### Other ways to connect

In the 'WhatsApp support group' line, add the link to the whatsapp group: https://chat.whatsapp.com/KwWn0lfpHuR0qJKtkuGZUA

Also add a new row for newsletters: 

Email newsletter: where we share News, case studies, app tips, events etc about the Causal Map world: https://docs.google.com/forms/d/e/1FAIpQLSenw-0xaNccM2L8ujkw7rL7JhYtpamqS9LW8TIps3LOG6GyaA/viewform 

Causal mapping, evaluation, AI LinkedIn newsletter: Thoughts pieces from our work on causal mapping in evaluation, with a dash of AI: https://www.linkedin.com/newsletters/causal-mapping-evaluation-ai-7201488452201185280/

---

# Status check & further suggestions (Claude, 30 June 2026)

Checked against the live site (causalmap.app) and the current content files — they match, so the prototype is live.

## Status of the suggestions above

- **Product / Garden case studies link** — not done. The "Manual and AI coding" section on `/product` still has no link to the Garden case studies.
- **Consultancy costs section** — not done. This doc points to `/pricing`, but the day-rate content (minimum 2 days, £695+VAT/day) reads as consultancy info, and `/consultancy` currently has no pricing or cost indication at all — that's likely the better home for it now that consultancy has its own page.
- **Pricing → link "signing up in the app"** — partly there. `/pricing` already links to app.causalmap.app one line below that phrase, just not on the phrase itself. Low priority.
- **AI add-ons pricing table** — done. `/pricing` now has full monthly/annual tables with "with AI" rows for every tier. Could still add a line saying add-ons can be bought directly from the app.
- **Contact page (WhatsApp + newsletters)** — not done. "Other ways to connect" only lists Documentation, LinkedIn, and YouTube — no WhatsApp group, no newsletter signup, no LinkedIn newsletter. (The email newsletter form is linked sitewide in the footer, so it's not entirely missing from the site, just not on this page.)

## A few more things spotted in this pass

- **`/subscriptions` is live and out of date.** It's a real, indexable page (not a redirect, unlike `/subscriptions-cm4` and `/subscriptions-cm4-old`, which both redirect here) and it still describes the AI add-on as a flat "+£18/month" instead of the per-tier pricing now on `/pricing`. The two pages contradict each other — worth redirecting `/subscriptions` to `/pricing` too.
- **James Copestake's photo on `/about` is hotlinked from an old Notion CDN URL**, not stored in `content/assets/` like the other three team photos. Worth downloading and hosting it locally so it can't break if that URL is retired.
- **The LinkedIn newsletter isn't linked anywhere on the site**, including the footer (only the LinkedIn company page is). Worth a link from Contact or Resources to help it grow.
