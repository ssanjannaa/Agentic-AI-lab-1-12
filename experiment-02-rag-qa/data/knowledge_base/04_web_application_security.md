# Web Application Security

## Overview
Web application security focuses on building and securing web applications, APIs, and microservices against malicious attacks targeting application-layer logic and user data.

## OWASP Top 10 Vulnerabilities
1. **SQL Injection (SQLi):** Occurs when untrusted user input is concatenated directly into database query strings, allowing attackers to manipulate SQL execution, bypass authentication, or exfiltrate full database contents.
2. **Cross-Site Scripting (XSS):** Occurs when web applications inject untrusted data into web pages without proper encoding or sanitization, allowing malicious client-side JavaScript execution in victim browsers.
3. **Cross-Site Request Forgery (CSRF):** Tricks authenticated users into executing unwanted actions on web applications in which they are currently logged in.
4. **Broken Access Control:** Failures in enforcing authorization limits, allowing unauthorized users to view, modify, or delete administrative resources.

## Defense and Mitigation Techniques
- **Parameterized Queries:** Use prepared statements and parameterized inputs for all database queries to prevent SQL injection completely.
- **Context-Aware Output Encoding:** HTML, attribute, and JavaScript encoding to mitigate XSS vulnerabilities.
- **Web Application Firewalls (WAF):** Filter and inspect incoming HTTP/HTTPS traffic to block common web attacks (SQLi, XSS, bot scraping).
- **Content Security Policy (CSP):** Implement strict HTTP response headers restricting script execution sources.
