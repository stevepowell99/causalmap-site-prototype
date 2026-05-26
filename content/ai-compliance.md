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

- Data is processed using a variety of LLM APIs. As of November 2025, exclusively Google Vertex APIs.
- Each model use is recorded internally.
- For Google Vertex AI:
    - <span class="hl hl-green">Data is not used to train models.</span>
    - <span class="hl hl-yellow">Zero long-term retention: a maximum of 24 hours in-memory cache</span> of data.
    - Data stays in the user's chosen region: europe-west1, europe-west2 or Virginia (us-east5).
    - For users who select a European region, data storage and processing are GDPR compliant.
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
