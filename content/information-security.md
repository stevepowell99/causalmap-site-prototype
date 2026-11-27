---
title: Information Security Policy
path: /information-security
description: How Causal Map classifies data, controls access, secures the app, handles incidents and keeps its services running.
sections:
  - type: prose
---

<!-- Canonical for the company-wide policy: users, passwords, training, access reviews, incident
     management, continuity and disaster recovery. NOT CANONICAL for the QualiaInterviews facts:
     master copy is README-unified.md in the qualia-edit-multi repo, whose Data Breach Notification
     section links to #incidents here. "App security controls" covers the Causal Map app on Supabase,
     a different backend from Qualia on Railway, so do not copy Qualia's numbers across.
     Its Causal Map facts come from the causal-map-extension code: daily backups and the London
     region were read from the Supabase Management API on 27 November 2026. -->


## Information Security Policy

<p class="print-link"><a href="#" onclick="window.print(); return false;">Print or save as PDF</a></p>

Last reviewed: 27 November 2026.

### 1. Purpose

Causal Map Ltd restricts access to confidential and sensitive data to protect it from being lost or compromised, to avoid adverse impact on customers, penalties for non-compliance, and damage to our reputation. At the same time we ensure users can access data as required to work effectively.

This policy cannot eliminate all malicious data theft. Its primary objective is to raise user awareness and avoid accidental loss, and it sets out requirements for data-breach prevention.

### 2. Scope

#### Data classification

- **Public:** data that is not personal or sensitive, accessible by anyone.
- **Internal:** data not intended for public disclosure but with low security requirements. For example, data in the Causal Map folder at Google Workspace.
- **Confidential:** data that could create moderate risk if disclosed to an unauthorised user. For example, data in the Causal Map Management folder at Google Workspace.
- **Restricted:** the highest level of sensitive data, which could put the company at severe risk if disclosed. In particular, client data including their data in the Causal Map app and associated files.

**In scope.** This policy applies to all customer data, personal data and other company data classified as sensitive. It applies to every server, database and IT system that handles such data, including any device regularly used for email, web access or other work-related tasks. Every user who interacts with company IT services is subject to this policy.

**Out of scope.** Information classified as Public is not subject to this policy. Other data can be excluded by company management based on specific business needs, for example where protecting the data is too costly or complex.

### 3. Policy for internal and contracted users

#### 3.1 Principles

Causal Map Ltd provides employees and contracted third parties (the "users") with access to the information they need to carry out their responsibilities as effectively as possible.

#### 3.2 General

- Each user is identified by a unique user ID so that individuals can be held accountable for their actions.
- Shared identities are permitted only where suitable, such as training accounts or service accounts (for example, help@causalmap.app).
- Each user shall read this policy and confirm they understand the conditions of access.
- Records of user access may be used as evidence in security incident investigations.
- Access is granted on the principle of least privilege: each program and user is granted the fewest privileges necessary to complete their tasks.

#### 3.3 Access control authorisation

Access to company IT resources and services is given through a unique user account based on an email address and complex password.

#### 3.4 Network access

For Google Workspace, the Causal Map app, QualiaInterviews and similar systems, employees and contractors are given network access in accordance with business access-control procedures and the least-privilege principle.

#### 3.5 User responsibilities

- Lock screens whenever leaving a desk to reduce the risk of unauthorised access.
- Keep the workplace clear of sensitive or confidential information when away.
- Keep passwords confidential and do not share them.

#### 3.6 Application and information access

- Staff and contractors are granted access to the data and applications required for their job roles.
- Access to sensitive data and systems is granted only if there is a business need and approval from higher management.
- Sensitive systems are physically or logically isolated to restrict access to authorised personnel only.

#### 3.7 Access to confidential and restricted information

Access to data classified as Confidential or Restricted is limited to authorised persons whose job responsibilities require it, as determined by line management.

<h4 id="passwords">3.8 Passwords</h4>

- Every account has its own password, used for no other service, and long enough that it cannot be guessed.
- Passwords are kept in a password manager or in the company's encrypted key store, and never in code.
- Two-step verification is switched on for every company account that offers it and that holds customer data or gives access to production systems.

<h4 id="training">3.9 Training</h4>

Everyone given access to customer data, whether staff or contractor, reads this policy and the compliance documentation for the products they work on before access is granted, and again whenever either changes materially. Contractors who work on our code sign a non-disclosure agreement first.

<h4 id="access-reviews">3.10 Access reviews</h4>

Access to production systems and customer data (hosting and database accounts, cloud consoles, and the administrator accounts in each app) is limited to the directors and the named contractors who need it. The directors review that list each October, at the company's year end, and whenever someone joins or leaves, and remove a person's access when their work for us ends.

### 4. App security controls

#### Data storage and security

- Causal Map is a serverless application. The Postgres database, authentication, storage, realtime and Edge Functions are provided by Supabase, hosted in AWS eu-west-2 (London). Supabase runs the Edge Functions in its region nearest the user.
- Static web assets are hosted on Netlify (`app.causalmap.app`).
- The PDF processor service runs on Railway and does not store uploaded PDFs; files are extracted to text and discarded.
- Cloudflare CDN serves a PDF.js worker; no user data is stored at Cloudflare.
- Data is encrypted at rest and at the database layer, and in transit via TLS over HTTPS.
- Row-Level Security policies are enforced at Supabase.
- Daily backups of the database are made automatically.

For the list of sub-processors that handle personal data, see [Sub-processors](/privacy-policy#sub-processors) on the Privacy Policy page. For AI processing details, including each project's choice of AI Processing Region (Europe, United States or Global) and what that means for GDPR, see [AI Compliance](/ai-compliance).

#### Data protection measures

- All emails to and from clients containing personal data are encrypted at rest and in transit.
- Clients' personal data is securely deleted when no longer needed.
- Access to clients' personal data is restricted to authorised personnel only.

#### App authentication

Authentication is handled by Supabase.

- Users can authenticate with email and password, or through a Google account.
- Two-factor authentication is available.
- Strong passwords and regular password resets are recommended.

#### Role-based access

There are two levels of access: Admin and User.

**Admin access:**

- Granted to three accounts at Supabase, controlled only by the domain admin.
- Admins can see metadata and significant events for all users.
- Using the AI, admins cannot view, edit or delete clients' private data. They can do so programmatically but will not do that without the client's explicit permission.

**User access:**

- Users on the corresponding plan can assign and revoke view, copy or edit rights for other users on projects to which they have the appropriate permissions.
- Users can view, copy or edit files to which they have the appropriate permission.
- Users can create new files over which they then have edit permission.

#### User activity monitoring and audit logs

- Sign-in is handled by Supabase Auth, which keeps its own logs.
- New registrations, sign-ins, new projects and AI coding runs are emailed to the company's administrators.
- Actions such as opening, creating, importing into and exporting a project are recorded in our database, and every AI request is recorded with its prompt and response (see [AI Compliance](/ai-compliance)).

<h3 id="incidents">5. Incident management</h3>

An incident is any event that puts the confidentiality, integrity or availability of customer data or of our services at risk: a security breach or suspected breach, loss of data, or a significant outage. Steve Powell, director, is responsible for handling incidents. Report a suspected incident or vulnerability to [hello@causalmap.app](mailto:hello@causalmap.app).

- **Contain.** Stop the cause, for example by revoking credentials, rotating keys or taking a service offline.
- **Assess.** Establish what happened, which data and which customers are affected, and whether personal data is involved.
- **Notify.** Where personal data we process for a customer is affected, we tell that customer without undue delay, and within any time their data processing agreement sets, so they can meet their own duty to notify the Information Commissioner's Office (ICO). Where we are the controller, we notify the ICO within 72 hours where the law requires it, and tell the people affected where the risk to them is high. A notification says what happened, the kinds and rough numbers of people and records affected, the likely consequences, what we have done or will do about it, and who to contact.
- **Recover and record.** Restore the service and the data, then record the incident, its cause and what we changed to stop it happening again.

For outages of the Causal Map app, the restoration target and status updates are set out in the [SLA](/terms-and-conditions#sla).

<h3 id="continuity">6. Business continuity and disaster recovery</h3>

- **Hosting.** The products run on managed platforms (Supabase, Railway, Netlify and Google Cloud), which provide the hardware, its redundancy and infrastructure patching. No product depends on a company office or on any one person's computer.
- **Backups.** Databases are backed up automatically and encrypted at rest. The schedules are in each product's documentation: the [QualiaInterviews compliance documentation](https://manage.qualiainterviews.com/help#compliance) and, for the Causal Map app, the [SLA](/terms-and-conditions#sla).
- **Rebuilding.** The code for every product is held in Git on GitHub, with its build and deployment configuration and the name and source of every secret it needs (never the value), so each product can be rebuilt from its accounts on a new machine.
- **Secrets.** Credentials and recovery codes are kept in an encrypted key store, never in code or in documents that other services can read.
- **People.** A written continuity plan sets out how the other director would keep the company and its services running if Steve Powell were unavailable: access to the company's accounts, payments, customers, suppliers and code. It is reviewed each October and whenever a service is added or cancelled.

### 7. Definitions

- **Data owners** are employees or contractors with primary responsibility for maintaining information that they own.
- **Users** include everyone who has access to information resources: employees, trustees, contractors, consultants, temporary employees and volunteers.
- **Database:** an organised collection of data, generally stored and accessed electronically from a computer system.
- **Encryption:** the process of encoding information so that only authorised parties can access it.
- **Firewall:** a technology used for isolating one network from another. Firewalls can be standalone systems or included in other devices, such as routers or servers.
- **Server:** a computer program or device that provides functionality for other programs or devices, called clients.

We reserve the right to change this policy at any given time, in which case we will notify users.

### Related policies

- [Privacy Policy](/privacy-policy)
- [AI Compliance](/ai-compliance)
- [Terms and Conditions](/terms-and-conditions) (including the [SLA](/terms-and-conditions#sla))

### Contact

For security questions or to report a vulnerability, contact [hello@causalmap.app](mailto:hello@causalmap.app).
