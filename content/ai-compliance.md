---
title: AI Compliance
path: /ai-compliance
description: How Causal Map handles AI features, providers, regions, and automated decision-making.
sections:
  - type: prose
---

## AI Compliance (Data Protection and Privacy)

<p class="print-link"><a href="#" onclick="window.print(); return false;">Print or save as PDF</a></p>

Causal Map app, developed by Causal Map Ltd, is committed to protecting the privacy of our users. This page covers how AI features are operated. It is in addition to the general provisions in the [Privacy Policy](/privacy-policy), in compliance with GDPR, EU AI Act and other applicable regulations.

Causal Map is an online-only service: there is nothing to download or install.

### AI processing for Causal Map 4

Causal Map 4 does not have AI enabled by default. AI is enabled only for users who sign up to specific AI plans.

**Primary AI provider: Google Vertex AI** (Gemini models).

- **Regions for AI processing:** europe-west1 (Belgium), europe-west2 (UK) or us-east5 (Virginia), chosen per workspace.
- <span class="hl hl-green">Data is not used to train models.</span>
- <span class="hl hl-yellow">Zero long-term retention: a maximum of 24 hours in-memory cache</span>, and prompt logging for abuse monitoring can be turned off under invoiced billing.

**AI coding service path.** AI requests are routed through a Google Cloud Function (`process_chunk`, project `cm-translation-426218`, region us-central1 / Iowa). The function does not store user data; it forwards prompts to the chosen AI provider and writes only audit logs to a `ai_logs` table in Supabase.

**Optional alternative providers** (selected per plan or model):

- **Dashscope (Alibaba Qwen)** — Qwen Flash, Plus or Max, served from Singapore or the US. Alibaba does not retain data; processing is in-memory only.
- **OpenAI (GPT-5)** — used only when explicitly selected. OpenAI's own retention policy applies.

Each model use is recorded internally for audit purposes.

> **GDPR and data residency.** Full GDPR compliance for AI processing depends on the client selecting an EU or UK region (europe-west1 or europe-west2). If a US region or a non-EU alternative provider (OpenAI in the US, Dashscope) is used, AI processing leaves the UK or EU and falls outside the territorial protections of UK GDPR, though contractual safeguards still apply. Choose your region with this in mind.

- Clients are asked not to upload data containing personally identifying information. Where this is hard to guarantee, see the offline anonymisation tool described in the [Privacy Policy](/privacy-policy).
- Causal Map Ltd adheres to established qualitative research protocols to limit the AI's freedom in making evaluative judgments, aiming for transparency and accuracy in the AI's interpretation of causal claims.
- Ethical considerations include attention to the types of data processed and ensuring the AI's analysis reflects respondent views without systematic bias or undue influence.

### Optional and human-reviewed

- <span class="hl hl-pink">AI features are optional.</span> Users can code entirely manually if they prefer.
- All AI suggestions require human review and approval before they are saved.
- AI suggests; it does not decide.
- AI suggestions are not guaranteed to be accurate. Users are responsible for reviewing, editing and validating all AI output.

### Automated decision-making

Causal Map does not make solely automated decisions with legal or similarly significant effects on data subjects. AI output is treated as advisory and always passes through user review, in line with GDPR Article 22.

### User activity monitoring and audit logs

- Log on and log off are monitored via the app's authentication provider.
- Highly significant events such as new user registration and file creation are logged in a system SQL database and emailed to the Data Protection Officer.
- Significant events such as log on and file load are recorded in a system SQL database.

### Related policies

- [Privacy Policy](/privacy-policy)
- [Information Security Policy](/information-security)
- [Ethical Principles](/ethical-principles)
- [Terms and Conditions](/terms-and-conditions)

### Contact

For questions about AI features and compliance, contact our Data Protection Officer Steve Powell at [hello@causalmap.app](mailto:hello@causalmap.app).
