# Web Application Attack Surface Defense — SQL Injection & XSS

## Overview
Web application attacks attempt to exploit vulnerabilities in public-facing web servers. SQL Injection (SQLi) injects malicious SQL statements into database query inputs, allowing unauthorized data retrieval, table manipulation, or remote command execution. Cross-Site Scripting (XSS) injects malicious client-side scripts into web application parameters.

## Attack Indicators & Patterns
- HTTP Web Server logs containing SQL syntax keywords in query parameters (`UNION SELECT`, `OR 1=1--`, `INFORMATION_SCHEMA`, `SLEEP()`).
- Excessive 500 Internal Server Error codes triggered by database syntax errors.
- Unusually large HTTP response body sizes indicating database table dumping.
- Parameter inputs containing script tags (`<script>`, `onerror=alert()`, `javascript:`).

## Defensive Mitigation Playbook
1. Enforce Prepared Statements (Parameterized Queries) with ORM mapping across all database access layers.
2. Implement strict input validation, white-listing, and output encoding (HTML, JavaScript context encoding).
3. Update Web Application Firewall (WAF) rule signatures to block SQLi and XSS attack vectors at the perimeter.
4. Apply the Principle of Least Privilege to database connection accounts (restrict `DROP`, `ALTER`, or administrative privileges).
5. Deploy Content Security Policy (CSP) HTTP headers to block untrusted script execution.

## MITRE ATT&CK Mapping
- T1190: Exploit Public-Facing Application
- T1059: Command and Scripting Interpreter
- T1505: Server Software Component
