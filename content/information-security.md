---
title: Information Security Policy
path: /information-security
description: How Causal Map classifies data, controls access, and secures the app.
sections:
  - type: prose
---

## Information Security Policy

<p class="print-link"><a href="#" onclick="window.print(); return false;">Print or save as PDF</a></p>

### 1. Purpose

Causal Map Ltd restricts access to confidential and sensitive data to protect it from being lost or compromised, to avoid adverse impact on customers, penalties for non-compliance, and damage to our reputation. At the same time we ensure users can access data as required to work effectively.

This policy cannot eliminate all malicious data theft. Its primary objective is to raise user awareness and avoid accidental loss, and it sets out requirements for data-breach prevention.

### 2. Scope

#### Data classification

- **Public:** data that is not personal or sensitive, accessible by anyone.
- **Internal:** data not intended for public disclosure but with low security requirements. For example, data in the Causal Map folder at Google Workspace.
- **Confidential:** data that could create moderate risk if disclosed to an unauthorised user. For example, data in the Causal Map Management folder at Google Workspace, or data in the Public section at Notion.
- **Restricted:** the highest level of sensitive data, which could put the company at severe risk if disclosed. In particular, client data including their data in the Causal Map app and associated files.

**In scope.** This policy applies to all customer data, personal data and other company data classified as sensitive. It applies to every server, database and IT system that handles such data, including any device regularly used for email, web access or other work-related tasks. Every user who interacts with company IT services is subject to this policy.

**Out of scope.** Information classified as Public is not subject to this policy. Other data can be excluded by company management based on specific business needs, for example where protecting the data is too costly or complex.

### 3. Policy for internal and contracted users

#### 3.1 Principles

Causal Map Ltd provides employees and contracted third parties (the "users") with access to the information they need to carry out their responsibilities as effectively as possible.

#### 3.2 General

- Each user is identified by a unique user ID so that individuals can be held accountable for their actions.
- Shared identities are permitted only where suitable, such as training accounts or service accounts (for example, help@causalmap.app).
- Each user shall read this policy and the login and logoff guidelines, and confirm they understand the conditions of access.
- Records of user access may be used as evidence in security incident investigations.
- Access is granted on the principle of least privilege: each program and user is granted the fewest privileges necessary to complete their tasks.

#### 3.3 Access control authorisation

Access to company IT resources and services is given through a unique user account based on an email address and complex password.

#### 3.4 Network access

For Google Workspace, Notion, the Causal Map app and similar systems, employees and contractors are given network access in accordance with business access-control procedures and the least-privilege principle.

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

### 4. App security controls

#### Data storage and security

- Causal Map is a serverless application. The Postgres database, authentication, storage, realtime and Edge Functions are provided by Supabase, with the database pooler hosted in AWS eu-west-2 (London).
- Static web assets are hosted on Netlify (`app.causalmap.app`).
- The PDF processor service runs on Railway and does not store uploaded PDFs; files are extracted to text and discarded.
- Cloudflare CDN serves a PDF.js worker; no user data is stored at Cloudflare.
- Data is encrypted at rest and at the database layer, and in transit via TLS over HTTPS.
- Row-Level Security policies are enforced at Supabase.
- Daily backups of the database are made automatically.

For the list of sub-processors that handle personal data, see [Sub-processors](/privacy-policy#sub-processors) on the Privacy Policy page. For AI processing details, including the choice of EU, UK or US regions and what that means for GDPR, see [AI Compliance](/ai-compliance).

#### Data protection measures

- All emails to and from clients containing personal data are encrypted at rest and in transit.
- Clients' personal data is securely deleted when no longer needed.
- Access to clients' personal data is restricted to authorised personnel only.

#### App authentication

Authentication is handled by Supabase.

- Users can authenticate with email and password, or through a Google account.
- Two-factor authentication is available on request.
- Strong passwords and regular password resets are recommended.

#### Role-based access

There are two levels of access: Admin and User.

**Admin access:**

- Granted to three accounts at Supabase, controlled only by the domain admin.
- Admins can see metadata and significant events for all users.
- Admins can view and, if necessary, delete client data, but will not do so without the client's explicit permission.

**User access:**

- Users on the corresponding plan can assign and revoke view, copy or edit rights for other users.
- Users can view, copy or edit files to which they have the appropriate permission.
- Users can create new files over which they then have edit permission.

#### User activity monitoring and audit logs

- Log on and log off are monitored via Supabase Auth.
- Highly significant events such as new user registration and file creation are logged in a system SQL database and emailed to the Data Protection Officer.
- Significant events such as log on and file load are recorded in a system SQL database.

### 5. Reporting requirements

- Daily incident reports are produced and handled by the IT Director in the event of an incident.
- High-priority incidents are immediately reported to the IT Director (Steve Powell).

### 6. Definitions

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
