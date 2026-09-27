---
name: docker-and-containers
description: >
  Language-agnostic framework for writing, reviewing, optimizing, and securing Dockerfiles,
  container images, and Docker Compose configurations. Triggers whenever an agent is asked to
  "write a Dockerfile", "containerize this app", "review this Dockerfile", "why is my image so big?",
  "docker-compose setup", or "optimize Docker build". Enforces minimal base images, multi-stage builds,
  layer caching order, non-root user execution, HEALTHCHECK declarations, and vulnerability scanning with Trivy.
metadata:
  author: yash
  version: "1.0"
  scope: "docker, containers, dockerfile, compose, container-security, multi-stage"
allowed-tools: Read Write Bash
---

# Docker & Container Engineering Standards

A language-agnostic operational standard for authoring, evaluating, and securing Dockerfiles, container images, and local multi-service container environments.

> **Sibling Standards:**
> - For managing environment variables and avoiding baking secrets into images, see [`secrets-and-config-management`](file:///Users/apple/Projects/yash/skills/secrets-and-config-management/SKILL.md).
> - For integrating container vulnerability scans and image caching into CI, see [`ci-cd-pipeline`](file:///Users/apple/Projects/yash/skills/ci-cd-pipeline/SKILL.md).

---

## 1. Base Image Selection & Pinning

- [ ] **1.1 Prefer Minimal Official Images:**
  - Avoid full general-purpose OS images (`ubuntu:latest`, `debian:latest`, `node:20`).
  - Use minimal variants (`alpine`, `slim`, or Google `distroless` for compiled binaries) to minimize attack surface and reduce image transfer times.
- [ ] **1.2 Pin Explicit Versions:**
  - 🚫 **Never use `:latest`** in production Dockerfiles.
  - Pin exact versions (e.g. `node:20.18-alpine3.20` or `python:3.12-slim-bookworm`). For immutable reproducibility, pin the SHA-256 image digest.
- [ ] **1.3 Actively Maintained Repositories:**
  - Ensure the base image receives regular CVE security patches from verified publishers.

---

## 2. Multi-Stage Build Architecture

- [ ] **2.1 Decouple Build Tools from Runtime:**
  - Every compiled or transpiled application (TypeScript, Go, Rust, Java, Python virtualenvs) must use multi-stage builds.
  - Compilers, SDKs, devDependencies, and test runners remain in the `builder` stage and are **never copied into the final production image**.
- [ ] **2.2 Copy Only Built Artifacts:**
  - Use `COPY --from=builder` to extract only production binaries, static bundles, or pruned production dependencies.

---

## 3. Layer Caching & Build Context Efficiency

- [ ] **3.1 Order Instructions by Change Frequency:**
  - Place slow, infrequently-changing steps at the top; frequently-changing code at the bottom:
    ```dockerfile
    # 1. System packages & tools (rarely changes)
    RUN apk add --no-cache dumb-init

    # 2. Dependency manifests & installation (changes weekly/monthly)
    COPY package.json pnpm-lock.yaml ./
    RUN pnpm install --frozen-lockfile

    # 3. Source code copy & compilation (changes on every commit)
    COPY . .
    RUN pnpm build
    ```
- [ ] **3.2 Combine Consecutive RUN Commands:**
  - Group package manager updates, installs, and cache cleanups into a single `RUN` command to prevent bloated intermediate layers:
    ```dockerfile
    RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
     && rm -rf /var/lib/apt/lists/*
    ```
- [ ] **3.3 Mandatory `.dockerignore`:**
  - Every repository must have a `.dockerignore` file excluding `.git`, `node_modules`, `.env*`, build outputs, and test artifacts from the Docker build context.

---

## 4. Container Security & Isolation

- [ ] **4.1 Non-Root User Execution:**
  - 🚫 **Never run production processes as `root`!**
  - Switch to a dedicated non-root user before the final `ENTRYPOINT` or `CMD` (e.g. `USER node` in Node, `USER 10001` in Python, `USER nonroot:nonroot` in Distroless).
- [ ] **4.2 Zero Baked Secrets:**
  - Never use `ENV` or `ARG` to pass production secrets during `docker build`. Secrets embedded in build arguments persist permanently in image layer metadata.
  - Inject secrets at container startup via runtime environment variables or a secrets manager.
- [ ] **4.3 Automated Vulnerability Scanning:**
  - Audit images for CVEs using Trivy, Grype, or Docker Scout in CI (see [`references/scanning-tools.md`](file:///Users/apple/Projects/yash/skills/docker-and-containers/references/scanning-tools.md)).
- [ ] **4.4 Explicit Resource Constraints:**
  - Always define CPU and memory limits (`mem_limit`, `cpus`) in orchestration configs to prevent runaway processes from starving host nodes.

---

## 5. Runtime Lifecycle & Signals

- [ ] **5.1 Proper Signal Handling (Graceful Shutdown):**
  - Use an init system (like `dumb-init` or `tini`) or format `ENTRYPOINT` in exec form (`ENTRYPOINT ["node", "server.js"]`) so the process runs as PID 1 and receives `SIGTERM` signals for graceful termination.
  - Avoid shell form (`CMD npm start`), which wraps the process in `/bin/sh` and swallows shutdown signals, forcing a slow `SIGKILL` timeout.
- [ ] **5.2 Declare a Healthcheck:**
  - Define an explicit `HEALTHCHECK` directive so orchestrators and Docker Desktop can monitor application availability.

---

## 6. Docker Compose Standards (Local Development)

- [ ] **6.1 Development Scoping:**
  - Use Docker Compose primarily for local multi-container developer environments (e.g. app + PostgreSQL + Redis), not as a raw production deployment mechanism.
- [ ] **6.2 Named Volumes for Persistence:**
  - Use explicit named volumes for database storage (`db_data:/var/lib/postgresql/data`) to prevent data loss on container recreation.
- [ ] **6.3 Layered Overrides:**
  - Use a base `docker-compose.yml` with layered `docker-compose.override.yml` files rather than duplicating entire service configurations.

---

## Detailed References

- [`references/dockerfile-examples.md`](file:///Users/apple/Projects/yash/skills/docker-and-containers/references/dockerfile-examples.md): Production-ready multi-stage Dockerfiles and `.dockerignore` templates for **Node.js (pnpm + Alpine)**, **Python (uv + Slim)**, and **Go (Static Binary + Distroless)**.
- [`references/scanning-tools.md`](file:///Users/apple/Projects/yash/skills/docker-and-containers/references/scanning-tools.md): Setup, CLI usage, and CI integration guides for **Trivy**, **Grype**, and **Docker Scout**.
