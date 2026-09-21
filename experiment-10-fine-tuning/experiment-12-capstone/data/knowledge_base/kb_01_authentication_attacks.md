# Enterprise Authentication Attacks & Defensive Mitigations

## Overview
Authentication attacks target enterprise identity boundaries through brute force, credential stuffing, password spraying, and session hijacking. Detectable anomalies include high volumes of failed login attempts, login spikes outside normal business hours, concurrent sessions across disparate geographic IP ranges, and legacy protocol usage (e.g., NTLM, basic auth).

## Key Indicators of Compromise (IOCs)
- Event ID 4625 (Failed Logon) spikes in Windows Event Logs.
- Multiple failed authentications targeting distinct accounts from a single IP address (Password Spraying).
- Successful authentication immediately following 10+ failed attempts (Brute Force Success).
- Anomalous ASN/Geolocated IP logins without registered travel approval.

## Defensive Containment Playbook
1. Enforce Multi-Factor Authentication (MFA) with FIDO2 / webauthn hardware keys or push-notification matching.
2. Implement automated IP rate-limiting and temporary account lockout policies (e.g., 5 attempts in 15 minutes).
3. Revoke existing user refresh tokens and active OAuth sessions for affected accounts.
4. Block malicious external IP addresses at the perimeter firewall / WAF level.
5. Require password reset over a secure out-of-band channel.

## MITRE ATT&CK Mapping
- T1110.001: Brute Force — Password Guessing
- T1110.003: Brute Force — Password Spraying
- T1078: Valid Accounts
