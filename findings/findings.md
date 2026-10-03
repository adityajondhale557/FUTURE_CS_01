# Vulnerability Assessment Findings

| ID | Finding | ZAP Risk | Confidence | Validation Status |
|---|---|---|---|---|
| F01 | Content Security Policy (CSP) Header Not Set | Medium | High | Manually validated |
| F02 | Cross-Domain Misconfiguration | Medium | Medium | Manually validated |
| F03 | Missing Anti-clickjacking Header | Medium | Medium | Endpoint-specific; manually reviewed |
| F04 | Session ID in URL Rewrite | Medium | High | Partially validated; URL exposure not confirmed |
| F05 | Private IP Disclosure | Low | Medium | Observed; lab-environment limitation |
| F06 | Timestamp Disclosure - Unix | Low | Low | Observed; impact not established |
| F07 | X-Content-Type-Options Header Missing | Low | Medium | Endpoint-specific; manually reviewed |
| F08 | Information Disclosure - Suspicious Comments | Informational | Low | Observed; sensitive disclosure not established |
| F09 | Modern Web Application | Informational | Medium | Informational; not a vulnerability |

## Scope

Target: OWASP Juice Shop running locally at `http://127.0.0.1:3000`

Testing environment: Local authorized laboratory environment.

## Important Reporting Notes

- ZAP alerts are treated as scanner observations and were manually reviewed where possible.
- F03 and F07 should not be described as site-wide missing security headers because the root response contains the relevant headers.
- F04 should not be described as confirmed session-ID exposure in the URL because the captured evidence only shows `sid` in the Socket.IO response body.
- F05 is environment-specific because the assessment was performed against a local laboratory instance.
- F06 and F08 have insufficient evidence to establish meaningful security impact.
- F09 is an informational scanner observation and is not a vulnerability.
