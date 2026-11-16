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
- **In the Causal Map app you can export or delete your data at any time** from your account. In Qualia Workshops, whoever owns a workshop can delete it at any time, with everything people wrote and added in it.
- **AI compliance:** We comply with UK AI Bill and GDPR requirements on automated decision-making. <span class="hl hl-pink">AI features are optional</span> and always subject to human review. **Full GDPR protection of AI processing depends on the client selecting an EU or UK region.** See [AI Compliance](/ai-compliance).
- **Research participants:** If your data contains research participant information, you must obtain consent before uploading. We provide privacy-by-default settings for sensitive data.

### Data controller and data processor

Which role we hold depends on the data, so there are two answers.

- **Your account data**, meaning your name, work email address, usage and billing: Causal Map Ltd is the **data controller**. We decide why we hold it, which is to run, support and bill for the service.
- **The research data you collect or upload** through QualiaInterviews, Qualia Workshops or the Causal Map app: **you are the data controller** and Causal Map Ltd is the **data processor**. You decide what the research is for, who takes part and what they are asked. We process it on your instructions.

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

We use the following sub-processors to operate Causal Map. They may handle personal data on our behalf, under contract. Technical security controls are described in the [Information Security Policy](/information-security); AI region choices and their GDPR implications are described in [AI Compliance](/ai-compliance). QualiaInterviews runs on different infrastructure, and its sub-processors, hosting regions and security controls are in the Compliance section of the [QualiaInterviews help](https://manage.qualiainterviews.com/help#compliance) and on [qualiainterviews.com/privacy](https://qualiainterviews.com/privacy). Qualia Workshops also runs on infrastructure of its own, listed [below the table](#qualia-workshops).

| Service | Purpose | Location | Retention |
|---|---|---|---|
| Supabase | Auth, Postgres, Storage, Realtime, Edge Functions | AWS eu-west-2 (London) | Held until user deletes |
| Google Vertex AI | AI inference (Gemini) | europe-west1, europe-west2 or us-east5 | None; up to 24 h in-memory |
| Google Cloud Functions | AI routing (`process_chunk`) | us-central1 (Iowa) | None; audit logs only |
| Dashscope (Alibaba) | Optional AI inference (Qwen) | Singapore or US | None (in-memory) |
| OpenAI | Optional AI inference (GPT-5) | OpenAI infrastructure | OpenAI policy |
| Lyceum | AI inference for Rubicon, in testing (DeepSeek V4.1 Flash, GLM 5.3 Flash) | EU: Paris (Scaleway) and Finland (OVHcloud) | Prompts and outputs deleted after each request, except where needed for abuse detection or security; metadata (timestamps, token counts, model IDs) kept 30 days |
| Railway | PDF text extraction | Railway infrastructure | None; files discarded |
| Netlify | Static webapp hosting | Netlify infrastructure | Static assets only |
| Loops.so | Email marketing and welcome flow | Loops infrastructure | Loops policy |
| Lemon Squeezy | Subscriptions, checkout, customer portal | Lemon Squeezy infrastructure | Lemon Squeezy policy |
| Slack | Admin support notifications via webhook | Slack infrastructure | Slack policy |

<h4 id="qualia-workshops">Qualia Workshops</h4>

Qualia Workshops is our app for workshops, in which people join from their own devices with a code. Someone taking part gives a name of their choosing and does not need an account; the person running the workshop signs in with Google or with a link sent by email. What people write and add in a workshop, and the files uploaded to it, are stored and processed in the EU. Someone taking part can delete a message they wrote, and whoever owns a workshop can delete the whole workshop, with its uploaded files.

| Service | Purpose | Location | Retention |
|---|---|---|---|
| Supabase | Auth, Postgres, Storage, Realtime, Edge Functions | AWS eu-central-1 (Frankfurt) | Held until the workshop's owner deletes it, or on request |
| Google Vertex AI | AI inference (Gemini) | EU multi-region | Google Cloud terms for Vertex AI |
| Google Workspace | Sending sign-in links by email | Google infrastructure | Google Workspace terms |
| Netlify | Static webapp hosting | Netlify infrastructure | Static assets only |
| GoatCounter | Counts of page visits | GoatCounter infrastructure | GoatCounter policy |

<h4 id="rubicon-plugin">The Rubicon plugin for Claude</h4>

The Rubicon plugin runs in the evaluator's own Claude, on their own Claude plan. Their documents, questions and answers go to Anthropic under the terms of that plan, and never to Causal Map. The plugin comes in two versions. `rubicon-private` sends us nothing. `rubicon` sends us one request in a conversation, after a report is handed over; Claude says first what it is about to send, and the evaluator can deny it. The request carries only these values, each worked out by fixed rules from the run's own files:

- the plugin's version, and the model family (Opus, Fable, Sonnet, Haiku or other);
- what was handed over: a report, a revision or a combined report;
- a random code that the run keeps among its own files, the same for the run's report and each of its revisions, so that they can be counted as one run; it appears in no report, Word copy or zip the evaluator shares, so a row cannot be matched to a report;
- the number of documents, in bands (1, 2-5, 6-10, 11-25, 26-50, 51-100, 101-250, over 250);
- about how many words the documents hold, in bands (under 5,000, 5,000-20,000, 20,000-50,000, 50,000-150,000, 150,000-500,000, over 500,000);
- the number of questions, and whether they were taken one by itself, together, one at a time, or after a shared reading;
- the number of steps of each kind in the run's workflow (sampling, coding, grouping, profiling, tabulating, judging, claims and writing);
- the number of passages coded, in bands (0, 1-10, 11-50, 51-200, 201-1,000, 1,001-5,000, over 5,000);
- the second reading: none, a check of the coding, or a second coding;
- the minutes from the run's first agreement to the hand-over, in bands (under 10, 10-30, 30-60, 60-120, 120-240, 240-480, over 480);
- the share of the answer's sentences found tied to the coded passages, in bands (under 50%, 50-79%, 80-89%, 90-99%, 100%).

It never carries a question, a document or folder name, a passage, a code or label, the time of day, or anything about the person or their computer. The request goes to a small relay we run on Google Cloud Run in Belgium (europe-west1), which reads only these values and passes them on to our database as one row, with the date; a request holding any other value adds nothing. Google Cloud is set to store no log of the relay's requests, so the IP address a request comes from is not kept, and our database, on Supabase, listed above, sees only Google's address: the person's IP address never reaches Causal Map.

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
