# phishing-detector
program to detect phishing attempts

demo link: https://phishing-detector-80290sc21-wsaronam1.vercel.app/


![CI / Security](https://github.com/wsaronam/phishing-detector/actions/workflows/security.yml/badge.svg)

## Security pipeline

Every push and pull request runs an automated CI/CD pipeline (GitHub Actions):

| Check | Tool | What it catches |
|---|---|---|
| Unit tests | Pytest | Broken detection logic (34 tests) |
| Static analysis (SAST) | Bandit | Insecure Python code patterns |
| Dependency scan | pip-audit, npm audit | Packages with known CVEs |
| Secrets detection | Gitleaks | API keys or passwords in git history |
| Container scan | Trivy | Vulnerabilities in the Docker image |

Dependabot opens weekly update PRs, and the pipeline also re-runs every Monday to catch newly disclosed CVEs.

**Security decisions**
- Workflows use least-privilege permissions (`contents: read` by default).
- Trivy runs from a pinned CLI image instead of `aquasecurity/trivy-action`, whose version tags were hijacked in a March 2026 supply-chain attack (CVE-2026-33634).

**What it caught:** the first run flagged 4 high-severity vulnerabilities in frontend dependencies (including axios) and 9 broken unit tests, all fixed before merging.