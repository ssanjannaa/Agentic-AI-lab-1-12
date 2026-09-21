# Firewalls and Network Defense

## What is a Firewall?
A firewall is a core network security device or software control that monitors and filters incoming and outgoing network traffic based on an organization's previously established security policies. It creates a protective barrier between trusted internal networks and untrusted external networks (such as the public internet).

## Types of Firewalls
1. **Packet Filtering Firewalls:** Inspect individual packet headers (IP address, protocol type, port numbers) against rule lists without maintaining connection state.
2. **Stateful Inspection Firewalls:** Track the active state of network connections (TCP handshakes, session states) to ensure incoming packets belong to legitimate established sessions.
3. **Next-Generation Firewalls (NGFW):** Combine traditional stateful inspection with deep packet inspection (DPI), integrated intrusion prevention (IPS), application-level control, and threat intelligence feeds.
4. **Web Application Firewalls (WAF):** Deployed specifically to inspect Layer-7 HTTP/HTTPS traffic targeting web applications.

## Network Defense Architecture
- **Demilitarized Zone (DMZ):** A perimeter network segment containing public-facing services (web servers, mail gateways) isolated from internal enterprise databases.
- **Intrusion Prevention Systems (IPS):** Active security appliances that inspect network streams and actively block or drop malicious traffic matching threat patterns in real time.
