# Known Supply-Chain Attack Patterns & Real-World Case Studies

> Companion reference for `package-security-vetting`.
> Contains defensive threat modeling, indicators of compromise (IOCs), and historical industry case studies. **No exploit payloads are included.**

---

## 1. Typosquatting

### Mechanism
Attackers register package names with deceptive typographical similarities to popular, high-traffic libraries (e.g., swapping hyphens for underscores, minor character omissions, or prefixing with `python3-` or `node-`). Unsuspecting developers or automated agents accidentally install the misspelled name, executing the malware during install or execution.

### Historical Incidents
1. **`crossenv` vs `cross-env` (npm, 2017):**
   - *Target:* The popular utility `cross-env` (for cross-platform environment variables).
   - *The Attack:* The typosquatted package `crossenv` collected machine environment variables (including AWS keys, npm tokens, and passwords) in a `package.json` install script and exfiltrated them via HTTP POST to a remote endpoint.
2. **PyPI Typosquatting Campaigns (PyPI, 2022–2024):**
   - *Target:* Packages like `reqeusts`, `python3-dateutil`, `colorama-v2`.
   - *The Attack:* Dropped obfuscated Discord token stealers and browser credential extractors in the `setup.py` build execution phase.

### Defensive Checks
- Verify package download statistics: genuine utilities typically have millions of downloads; typosquats often have under 5,000.
- Check the official documentation repository URL (GitHub, GitLab) directly from the project's official homepage, not registry search rankings.

---

## 2. Dependency Confusion (Substitution Attack)

### Mechanism
Many enterprises host private, un-scoped internal packages (e.g., `corp-auth`, `analytics-internal`) on private registries (Artifactory, Nexus, GitHub Packages). If a build tool is configured with both an internal and a public registry without strict scoping, an external attacker can register the exact same package name on the public registry (npm, PyPI, RubyGems) with an artificially high version number (e.g., `v99.0.0`). The package manager prioritizes the higher version from the public registry.

### Historical Incidents
1. **Alex Birsan Multi-Corporate Research (2021):**
   - *The Incident:* Researcher Alex Birsan identified internal package names leaked in public `package.json` files and GitHub repositories of Apple, Microsoft, PayPal, Shopify, and Tesla.
   - *Result:* Registered identical package names on public npm, PyPI, and RubyGems. Automated build servers pulled the public packages instead of private internal builds, achieving arbitrary code execution in corporate build pipelines.

### Defensive Checks
- Always **scope internal packages** (e.g., `@mycompany/auth` instead of bare `auth`).
- Configure package managers to only look for scoped namespaces in the internal repository.
- Reserve / claim placeholders for internal package names on public registries if un-scoped.

---

## 3. Maintainer Account Takeover & Social Engineering

### Mechanism
Legitimate, widely-trusted packages with millions of weekly downloads are often maintained by single individuals or volunteer open-source developers. Threat actors acquire access via:
- Compromising un-muffled credentials or leaked API tokens on developer machines.
- Credential stuffing against maintainer registry accounts lacking Two-Factor Authentication (2FA).
- Social engineering: volunteering sustained maintenance contributions over months, earning repository commit rights, and quietly slipping in a backdoor.

### Historical Incidents
1. **`event-stream` / `flatmap-stream` (npm, 2018):**
   - *The Incident:* The original creator of `event-stream` handed over repository ownership to a volunteer contributor ("right9ctrl") who had offered to maintain the dormant library.
   - *The Attack:* The new maintainer added a dependency `flatmap-stream` containing encrypted payload logic specifically targeting the Copay bitcoin wallet application to harvest private wallet seeds.
2. **`xz-utils` Backdoor (Linux / C, 2024 - CVE-2024-3094):**
   - *The Incident:* A persona ("Jia Tan") spent years contributing benign patches to `xz` compression utilities, gaining co-maintainer trust, before injecting a sophisticated multi-stage backdoor into release tarballs targeting OpenSSH authentication on Linux distributions.

### Defensive Checks
- Monitor maintainer changes and sudden ownership transfers on critical dependencies.
- Inspect binary differences between published registry tarballs and Git release tags.
- Pin cryptographic checksums in lockfiles.

---

## 4. Malicious Lifecycle / Postinstall Scripts

### Mechanism
Package registries often allow packages to run automated shell commands during installation (e.g., npm `preinstall`/`postinstall`, Python `setup.py`, Composer scripts). While intended for compiling native C/C++ bindings, malicious packages abuse these hooks to run network requests, download secondary droppers, or read local SSH keys before any application code even runs.

### Historical Incidents
1. **`ua-parser-js` Account Takeover (npm, 2021):**
   - *The Incident:* The developer's npm account was compromised. Versions `0.7.29`, `0.8.0`, and `1.0.1` were published with a modified `package.json` containing a `preinstall` script that downloaded and executed a cryptocurrency miner and password-stealing trojan (`danabot`).
2. **`colors` and `faker` Protestware (npm, 2022):**
   - *The Incident:* Maintainer Marak intentionally updated `colors.js` to an infinite loop printing zalgo text and corrupted `faker.js`, breaking tens of thousands of dependent production builds globally.

### Defensive Checks
- Audit dependencies using flags like `--ignore-scripts` (npm/pnpm) and `--no-scripts` (Composer).
- Use sandbox environments or containerized CI runners with restricted network access during dependency resolution.
- Never run package manager commands with `sudo` or `root` permissions.

---

## 5. Summary Threat Matrix for Agents

| Threat Vector | Red Flag / Indicator | Primary Mitigation |
|---|---|---|
| **Typosquatting** | New author, low downloads, misspellings | Compare against official docs, check registry age |
| **Dependency Confusion** | Un-scoped internal package names | Enforce `@org/` scopes, private registry isolation |
| **Account Takeover** | Sudden unexpected major release on dormant package | Pin lockfile hashes, review diffs before updating |
| **Malicious Scripts** | `postinstall` / `setup.py` running curl or base64 | Use `--ignore-scripts`, inspect install scripts |
| **Protestware** | Deliberate logic bombs by frustrated authors | Review release diffs, avoid unpinned `latest` ranges |
