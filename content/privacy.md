---
title: Privacy Policy
path: /privacy-policy
description: How we handle your data and privacy.
sections:
  - type: prose
---

<!-- NOT CANONICAL for storage, security, backups or our controller/processor role.
     Master copy is README-unified.md in the qualia-edit-multi repo, published at
     manage.qualiainterviews.com/help#compliance. Change that first, then this.
     The controller/processor wording was corrected on 26 August 2026 and now matches the
     master. See memory reference_controller_or_processor. -->


## Privacy Policy

<p class="print-link"><a href="#" onclick="window.print(); return false;">Print or save as PDF</a></p>

Causal Map Ltd is committed to protecting the privacy of our users. This policy explains how we collect, use, store and protect personal data in compliance with the General Data Protection Regulation (GDPR), the EU AI Act and other applicable regulations.

Causal Map is an online-only service: there is nothing to download or install.

Related policies: [Information Security Policy](/information-security), [AI Compliance](/ai-compliance), [Terms and Conditions](/terms-and-conditions) (including the [SLA](/terms-and-conditions#sla)), [Ethical Principles](/ethical-principles).

### Summary

- **<span class="hl hl-green">Your data belongs to you.</span>** We do not sell or share your data with third parties.
- **We use <span class="hl hl-yellow">industry-standard security</span>**, including encryption at rest and in transit. See the [Information Security Policy](/information-security) for detail.
- **You can export or delete your data at any time** from your account.
- **AI compliance:** We comply with UK AI Bill and GDPR requirements on automated decision-making. <span class="hl hl-pink">AI features are optional</span> and always subject to human review. **Full GDPR protection of AI processing depends on the client selecting an EU or UK region.** See [AI Compliance](/ai-compliance).
- **Research participants:** If your data contains research participant information, you must obtain consent before uploading. We provide privacy-by-default settings for sensitive data.

### Data controller and data processor

Which role we hold depends on the data, so there are two answers.

- **Your account data**, meaning your name, work email address, usage and billing: Causal Map Ltd is the **data controller**. We decide why we hold it, which is to run, support and bill for the service.
- **The research data you collect or upload** through QualiaInterviews or the Causal Map app: **you are the data controller** and Causal Map Ltd is the **data processor**. You decide what the research is for, who takes part and what they are asked. We process it on your instructions.

Where we are engaged as consultants and design the research ourselves, we act as a data controller in our own right, or jointly with you. That is set out in the engagement contract rather than here.

Our Data Protection Officer is Steve Powell, contactable at [hello@causalmap.app](mailto:hello@causalmap.app).

### Data collection and processing

We collect and process data necessary to operate Causal Map:

- From clients (users and subscribers): user account information, usage data, essential cookies, name and email address.
- Research data provided by clients, for which clients are the data controllers.

Data processing is conducted in compliance with the GDPR and other applicable regulations.

#### Client responsibilities

As data controllers, clients must ensure:

- Data was collected with appropriate consent or legal basis.
- They have permission to use data from previous research projects.
- They provide details of initial data collection and methodology.
- They document legitimate interests for data use.

#### Client data protection principles

**1. Lawful, fair and transparent processing.** All data processing must meet at least one condition: subject consent, contract performance, legal obligation, vital interests protection, public interest, or legitimate interests.

**2. Purpose limitation.** Data is processed only for specified research purposes. Further processing for research or statistical purposes is permitted if compatible.

<h3 id="sub-processors">Sub-processors</h3>

We use the following sub-processors to operate Causal Map. They may handle personal data on our behalf, under contract. Technical security controls are described in the [Information Security Policy](/information-security); AI region choices and their GDPR implications are described in [AI Compliance](/ai-compliance).

| Service | Purpose | Location | Retention |
|---|---|---|---|
| Supabase | Auth, Postgres, Storage, Realtime, Edge Functions | AWS eu-west-2 (London) | Held until user deletes |
| Google Vertex AI | AI inference (Gemini) | europe-west1, europe-west2 or us-east5 | None; up to 24 h in-memory |
| Google Cloud Functions | AI routing (`process_chunk`) | us-central1 (Iowa) | None; audit logs only |
| Dashscope (Alibaba) | Optional AI inference (Qwen) | Singapore or US | None (in-memory) |
| OpenAI | Optional AI inference (GPT-5) | OpenAI infrastructure | OpenAI policy |
| Railway | PDF text extraction | Railway infrastructure | None; files discarded |
| Netlify | Static webapp hosting | Netlify infrastructure | Static assets only |
| Loops.so | Email marketing and welcome flow | Loops infrastructure | Loops policy |
| Lemon Squeezy | Subscriptions, checkout, customer portal | Lemon Squeezy infrastructure | Lemon Squeezy policy |
| Slack | Admin support notifications via webhook | Slack infrastructure | Slack policy |

### Data retention and deletion

- Personal data is not kept longer than necessary.
- Data can be erased on request.
- Causal Map Ltd will not usually collect, store, host or process personal data of its clients' research subjects. Where this is necessary, it will occur only for the specific purpose(s) informed to data subjects. Data will be pseudonymised at the point of data collection using a unique identifier that is not connected to the subject's real-world identity, using techniques such as coding or hashing (Article 89, GDPR). All information that enables the reversal of pseudonymisation, and thereby re-identification, will only be held for a limited period, after which all data will be fully anonymised by destruction of all key lists.

#### Anonymity

At Causal Map we work with anonymous data. It can be hard for clients to ensure data is free from personally identifying information, especially with large volumes of text such as interview transcripts. For this case we provide an offline AI tool that runs locally without internet access and removes such information before text is uploaded. See [AI Compliance](/ai-compliance) for detail.

### International data transfers

Causal Map Ltd regularly transfers personal data to countries outside the UK ("transfer" includes making available remotely). Transfers to a country outside the UK take place only where one or more of the following applies:

- The transfer is to a country, territory, or specific sector (or international organisation) for which the UK Information Commissioner's Office has determined an adequate level of protection.
- The transfer is to a country or international organisation that provides appropriate safeguards through a legally binding agreement between public authorities, binding corporate rules, standard data protection clauses adopted by the ICO, compliance with an approved code of conduct, certification under an approved mechanism, contractual clauses authorised by the competent supervisory authority, or provisions in administrative arrangements between public authorities authorised by the competent supervisory authority.
- The transfer is necessary for the performance of a contract between the data subject and Causal Map Ltd, or for pre-contractual steps at the request of the data subject.
- The transfer is necessary for important public-interest reasons.
- The transfer is necessary for the conduct of legal claims.
- The transfer is necessary to protect the vital interests of the data subject or other individuals where the data subject is physically or legally unable to give consent.
- The transfer is made from a register that, under UK law, is intended to provide information to the public and is open for public access or to those who can show a legitimate interest.

### Client rights

Clients have the right to:

- Access their personal data.
- Request rectification or erasure of their data.
- Object to data processing.
- Data portability.
- Withdraw consent at any time.

To exercise these rights, contact the Data Protection Officer at [hello@causalmap.app](mailto:hello@causalmap.app).

### Data breach notification

In the event of a data breach, we will notify the relevant authorities and affected users in accordance with applicable laws.

### Changes to this policy

We reserve the right to update this policy. Users will be notified of significant changes.

### Acceptable use

Services provided by us may only be used for lawful purposes. Any material or conduct that in our judgment violates this policy may result in suspension or termination of the services or removal of the user's account, with or without notice.

Prohibited uses include, but are not limited to:

- Phishing or engaging in identity theft.
- Distributing malicious code.
- Distributing pornography or adult-related content.
- Promoting or facilitating violence or terrorist activities.
- Infringing on intellectual property rights.

By using Causal Map, you agree to the terms of this privacy policy. Full terms are in the [Terms and Conditions](/terms-and-conditions).

### Contact

For privacy-related enquiries:

- Data Protection Officer: Steve Powell
- Email: [hello@causalmap.app](mailto:hello@causalmap.app)
- Website: [https://www.causalmap.app](https://www.causalmap.app/)

We reserve the right to change this policy at any given time, in which case we will notify users.
