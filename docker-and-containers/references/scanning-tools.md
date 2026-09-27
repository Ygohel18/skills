# Container Vulnerability Scanning Tools Reference

> Companion reference for `docker-and-containers`.
> Setup, CLI commands, and CI integration guides for Trivy, Grype, and Docker Scout.

---

## 1. Trivy (Aqua Security) — Industry Standard

Trivy is a comprehensive, open-source vulnerability scanner that audits OS packages (Alpine, Debian, RedHat) and language-specific dependencies (npm, pip, Go modules) baked into container images.

### Local CLI Usage:
```bash
# Scan a local image and output human-readable table
trivy image my-app:latest

# Fail the command only if HIGH or CRITICAL vulnerabilities are found
trivy image --severity HIGH,CRITICAL --exit-code 1 my-app:latest

# Scan a local Dockerfile before building
trivy config Dockerfile
```

### GitHub Actions Integration:
```yaml
- name: Run Trivy Vulnerability Scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'my-app:${{ github.sha }}'
    format: 'sarif'
    output: 'trivy-results.sarif'
    severity: 'CRITICAL,HIGH'
    exit-code: '1' # Fails build if critical CVEs exist

- name: Upload Trivy Scan Results to GitHub Security Tab
  uses: github/codeql-action/upload-sarif@v3
  if: always()
  with:
    sarif_file: 'trivy-results.sarif'
```

### Triaging Known Vulnerabilities (`.trivyignore`):
If an upstream vendor CVE is acknowledged and cannot be remediated immediately, document it in `.trivyignore`:
```text
# Vendor patch pending; low risk in internal network
CVE-2024-12345
```

---

## 2. Grype (Anchore)

Grype is a fast vulnerability scanner specifically designed for developer workstations and CI environments.

### Local CLI Usage:
```bash
# Install Grype
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Scan container image
grype my-app:latest

# Fail build on CRITICAL vulnerabilities only
grype my-app:latest --fail-on critical
```

---

## 3. Docker Scout

Docker Scout is Docker's integrated vulnerability and supply-chain analysis tool built directly into Docker Desktop and Docker CLI.

### CLI Usage:
```bash
# Analyze vulnerabilities in an image
docker scout cves my-app:latest

# View actionable base image recommendations to reduce vulnerabilities
docker scout recommendations my-app:latest

# Compare two image tags to see CVE delta
docker scout compare --to my-app:v1.0.0 my-app:v1.0.1
```

---

## 4. Remediation Decision Hierarchy

When a vulnerability scanner flags a CVE in a container image:
1. **Update Base Image Tag:** 80% of container CVEs stem from outdated OS base images. Updating `node:20.10-alpine` $\rightarrow$ `node:20.18-alpine` often resolves hundreds of CVEs instantly.
2. **Switch to Distroless or Alpine:** Minimalist base images lack package managers (`apt`, `apk`), shells (`bash`), and utility binaries (`curl`, `tar`), eliminating entire classes of attack surface.
3. **Upgrade Language Dependencies:** Check language lockfiles via [`package-security-vetting`](file:///Users/apple/Projects/yash/skills/package-security-vetting/SKILL.md).
