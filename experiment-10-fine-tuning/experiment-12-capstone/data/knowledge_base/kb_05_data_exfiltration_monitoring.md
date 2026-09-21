# Data Exfiltration Monitoring & DLP Safeguards

## Overview
Data exfiltration occurs when unauthorized actors transfer sensitive enterprise data (PII, IP, financial records, API keys) outside organizational control boundaries. Exfiltration channels include cloud storage uploads, encrypted SSH/SFTP tunnels, DNS tunneling, and webmail attachments.

## Detection Indicators
- Anomaly alerts for outbound network traffic volume significantly exceeding historical baseline per workstation.
- DNS query log analysis showing high-frequency sub-domain requests consistent with DNS tunneling.
- DLP (Data Loss Prevention) triggers on outbound emails or web uploads matching regex patterns for social security numbers, credit card numbers, or proprietary keywords.
- Unapproved cloud synchronization tool execution (e.g., mega.nz, rclone, cloudflared).

## Defensive Mitigation Playbook
1. Block unauthorized outbound destination IP addresses, DNS domains, and storage provider ranges.
2. Revoke cloud storage OAuth permissions and temporary access tokens for affected accounts.
3. Enable strict Data Loss Prevention (DLP) blocking policies on email gateways and web proxies.
4. Quarantine affected host systems and preserve memory dumps for forensic analysis.
5. Notify data privacy compliance officers if confirmed PII exposure meets regulatory reporting thresholds.

## MITRE ATT&CK Mapping
- T1048.003: Exfiltration Over Alternative Protocol
- T1567: Exfiltration Over Web Service
- T1071.004: Application Layer Protocol — DNS
