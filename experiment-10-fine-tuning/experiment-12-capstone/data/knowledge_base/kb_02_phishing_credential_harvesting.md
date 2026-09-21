# Email Phishing & Credential Harvesting Remediation

## Overview
Phishing campaigns leverage deceptive emails, typosquatted domain names, urgent lure language, and malicious attachments or links to harvest employee credentials or deploy initial-access payloads. Modern adversary-in-the-middle (AiTM) phishing proxies bypass legacy MFA by relaying session cookies.

## Detection Indicators
- Inbound emails with mismatched SPF/DKIM/DMARC authentication checks.
- Typosquatted sender domains (e.g., `micros0ft-support.com` instead of `microsoft.com`).
- High-volume email campaigns containing shortened URLs or newly registered domains (< 14 days old).
- User submission of suspicious links to the internal Security Operations Center (SOC) report button.

## Defensive Containment Playbook
1. Purge matching phishing emails from all employee mailboxes using automated Email Security Gateway (ESG) search-and-purge commands.
2. Block malicious URL domains and IP indicators at perimeter DNS resolvers and Secure Web Gateways (SWG).
3. Reset credentials for any user who interacted with the phishing link or submitted credentials.
4. Terminate active web sessions and enforce FIDO2-compliant (phishing-resistant) MFA.
5. Isolate affected endpoints if attachment execution or macro enablement occurred.

## MITRE ATT&CK Mapping
- T1566.001: Phishing — Spearphishing Attachment
- T1566.002: Phishing — Spearphishing Link
- T1539: Steal Web Session Cookie
