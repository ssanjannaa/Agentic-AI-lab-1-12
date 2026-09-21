# Authentication and Access Control

## Authentication vs Authorization
- **Authentication (AuthN):** Verifying the identity of a user, device, or system (answering "Who are you?").
- **Authorization (AuthZ):** Determining what permissions and resources an authenticated identity is permitted to access (answering "What are you allowed to do?").

## Multi-Factor Authentication (MFA)
Multi-Factor Authentication requires users to provide two or more verification factors from distinct categories before gaining access:
1. **Something You Know:** Password, PIN, or passphrase.
2. **Something You Have:** Hardware token, TOTP authenticator app, or SMS code.
3. **Something You Are:** Biometric data (fingerprint, facial recognition, iris scan).

## Access Control Models
1. **Role-Based Access Control (RBAC):** Assigning permissions to specific job roles (e.g., Administrator, Manager, Student) rather than individual users.
2. **Attribute-Based Access Control (ABAC):** Evaluating dynamic rules based on user attributes, environmental factors (time, location), and resource sensitivity.
3. **Zero Trust Architecture (ZTA):** A security philosophy based on the strict principle: *"Never Trust, Always Verify"*. Every access request is continuously authenticated, authorized, and encrypted regardless of network location.
