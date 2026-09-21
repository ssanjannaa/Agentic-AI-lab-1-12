# Security Monitoring and SIEM Operations

## Overview
Security monitoring is the continuous collection, correlation, and real-time analysis of security logs, network events, and system activities across an enterprise network infrastructure to detect threats and policy violations promptly.

## Security Information and Event Management (SIEM)
A SIEM system acts as the central intelligence engine for Security Operations Centers (SOC):
1. **Log Aggregation:** Collecting log files from firewalls, servers, domain controllers, endpoints, and cloud infrastructure into a unified central repository.
2. **Event Correlation:** Applying rule correlation logic and behavioral analysis to link disparate log events (e.g., failed logins followed by administrative privilege escalations).
3. **Alerting & Notification:** Generating real-time security alerts for SOC analysts when predefined threat patterns are triggered.

## Key Security Monitoring Metrics & Tools
- **Security Operations Center (SOC):** A centralized team of security analysts monitoring enterprise alerts 24/7/365.
- **Log Management Best Practices:** Ensure timestamps are synchronized using NTP (Network Time Protocol) across all network devices and protect logs from unauthorized alteration.
- **Threat Hunting:** Proactive human-led searches through telemetry logs to discover sophisticated attacks that bypassed automated SIEM detection rules.
