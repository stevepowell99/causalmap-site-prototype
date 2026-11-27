---
title: AI Compliance
path: /ai-compliance
description: How Causal Map handles AI features, providers, regions, and automated decision-making.
sections:
  - type: prose
---

<!-- Facts about the Causal Map app come from the causal-map-extension code (branch dev), never
     from a Qualia document: regions and models in webapp/js/config.js and coding-run-plan.js,
     Cloud Functions in webapp/env-config.js, credits in webapp/js/capabilities.js and the
     get_user_ai_credits_status migration, AI logging in the ai_logs table. Checked 27 November 2026. -->

## AI Compliance (Data Protection and Privacy)

<p class="print-link"><a href="#" onclick="window.print(); return false;">Print or save as PDF</a></p>

Causal Map app, developed by Causal Map Ltd, is committed to protecting the privacy of our users. This page covers how AI features are operated. It is in addition to the general provisions in the [Privacy Policy](/privacy-policy), in compliance with GDPR, EU AI Act and other applicable regulations.

Causal Map is an online-only service: there is nothing to download or install.

### Who can use AI

Every plan, Free included, comes with a monthly allowance of AI credits, and the AI versions of the paid plans give more (see [Pricing](/pricing)). AI runs only for users who have switched it on: new users are asked at sign-up, and anyone can switch it off in Account settings, which stops every AI feature, MapCat (the in-app assistant) included.

### Where AI processing takes place

Project data is stored in London (Supabase, AWS eu-west-2), whichever AI region a project uses. Each project has an **AI Processing Region**, set under Project → Edit project; new projects are set to Europe. The region decides which models the app offers and where they run.

| AI Processing Region | Models | Where the models run | Google Cloud Functions that pass on AI requests |
|---|---|---|---|
| Europe (EU, EEA and UK) | Gemini (Google) and Claude (Anthropic), both served by Google Vertex AI | Google Vertex AI in EU locations: the EU multi-region and europe-west1 (Belgium) | europe-west1 (Belgium) |
| United States | Gemini and Claude, served by Google Vertex AI | Google Vertex AI in US locations | us-central1 (Iowa) |
| Global | As United States, plus GPT (OpenAI) and Qwen (Alibaba) for AI coding | As United States; GPT on OpenAI's infrastructure; Qwen on Alibaba Cloud's DashScope, in Singapore or the US | us-central1 (Iowa) |

- For a Europe or United States project, the app offers only the models that run in that territory, and refuses any request that would be processed elsewhere: in the browser, and again on our server for AI coding runs.
- For a Europe project, AI processing takes place in the EU. The app does not offer AI processing in the UK itself.
- Some AI requests reach Google through our backend functions on Supabase rather than through Google Cloud Functions. Supabase runs these functions in its region nearest the person using the app, so for someone working outside Europe, a request for a Europe project passes through a Supabase server outside Europe on its way to the EU.
- The connector that lets Claude, ChatGPT and other AI chat apps read your projects does not make any AI request of its own. What it returns goes to the company behind your chat app, under your agreement with them, and the project's AI Processing Region does not apply to it.

**Google Vertex AI** (Gemini, and Anthropic's Claude models served on Vertex AI):

- <span class="hl hl-green">Data is not used to train models.</span>
- <span class="hl hl-yellow">Zero long-term retention: a maximum of 24 hours in-memory cache</span>, and prompt logging for abuse monitoring can be turned off under invoiced billing.

**Optional providers, Global projects only:**

- **Dashscope (Alibaba Qwen)**: Qwen Flash, Plus or Max, served from Singapore or the US. Alibaba does not retain data; processing is in-memory only.
- **OpenAI (GPT)**: used only when chosen as the model for AI coding. OpenAI's own retention policy applies.

> **GDPR and data residency.** Full GDPR protection for AI processing needs the project's AI Processing Region to be Europe. With United States or Global, AI processing takes place outside the UK and EU (with Global, possibly in Singapore too) and falls outside the territorial protections of UK GDPR, though contractual safeguards still apply. Choose your region with this in mind.

- Clients are asked not to upload data containing personally identifying information. Where this is hard to guarantee, remove it before upload with an anonymisation tool that runs offline on your own computer, and have a person check the result.
- Causal Map Ltd adheres to established qualitative research protocols to limit the AI's freedom in making evaluative judgments, aiming for transparency and accuracy in the AI's interpretation of causal claims.
- Ethical considerations include attention to the types of data processed and ensuring the AI's analysis reflects respondent views without systematic bias or undue influence.

### Optional, and checked by the user

- <span class="hl hl-pink">AI features are optional.</span> Users can code entirely by hand if they prefer.
- AI coding saves the links it codes straight into the project: there is no step to approve each link before it is saved. Links created by AI coding are marked as AI-coded, and the user can review, edit or delete them like any other link.
- MapCat, the in-app assistant, asks the user to confirm before it changes a project's data or starts a coding run.
- AI Answers and map vignettes show their output without changing the project, unless the user asks AI Answers to create or change columns.
- AI output is not guaranteed to be accurate. Users are responsible for reviewing, editing and validating all AI output.

### Automated decision-making

Causal Map does not make solely automated decisions with legal or similarly significant effects on data subjects. AI output is coded material in the user's own project, which the user checks, edits and interprets, in line with GDPR Article 22.

### User activity monitoring and audit logs

- Every AI request is recorded in our database, in London, with its prompt and response, the model, the region, the number of tokens and the cost. These records are kept until the user's account is deleted. The project's owner and collaborators can read them, as can any signed-in user where the project is public, and our administrators. Records for a deleted project stay readable by our administrators only.
- Sign-in is handled by Supabase Auth, which keeps its own logs.
- New registrations, sign-ins, new projects and AI coding runs are emailed to the company's administrators.
- Actions such as opening, creating, importing into and exporting a project are recorded in our database.

### Related policies

- [Privacy Policy](/privacy-policy)
- [Information Security Policy](/information-security)
- [Ethical Principles](/ethical-principles)
- [Terms and Conditions](/terms-and-conditions)

### Contact

For questions about AI features and compliance, contact our Data Protection Officer Steve Powell at [hello@causalmap.app](mailto:hello@causalmap.app).
