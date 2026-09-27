# Production Multi-Stage Dockerfile Examples

> Companion reference for `docker-and-containers`.
> Production-tested, multi-stage, layer-cached, and non-root Dockerfile examples for Node.js, Python, and Go.

---

## 1. Node.js Multi-Stage Dockerfile (pnpm + Alpine)

```dockerfile
# ----------------------------------------------------
# Stage 1: Dependencies Cache
# ----------------------------------------------------
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Enable pnpm via Corepack
RUN corepack enable && corepack prepare pnpm@latest --activate

# Copy dependency manifests first to leverage layer cache
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile --prod=false

# ----------------------------------------------------
# Stage 2: Application Builder
# ----------------------------------------------------
FROM node:20-alpine AS builder
WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Run build (transpile TypeScript / bundle frontend)
RUN pnpm build && pnpm prune --prod

# ----------------------------------------------------
# Stage 3: Minimal Production Runtime
# ----------------------------------------------------
FROM node:20-alpine AS runner
WORKDIR /app

# Install dumb-init to properly handle PID 1 signals (SIGTERM/SIGINT)
RUN apk add --no-cache dumb-init

ENV NODE_ENV=production
ENV PORT=3000

# Use pre-existing non-root 'node' user
USER node

# Copy only production dependencies and compiled artifacts
COPY --chown=node:node --from=builder /app/node_modules ./node_modules
COPY --chown=node:node --from=builder /app/dist ./dist
COPY --chown=node:node --from=builder /app/package.json ./package.json

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "dist/server.js"]
```

---

## 2. Python Multi-Stage Dockerfile (`uv` + Distroless or Slim)

```dockerfile
# ----------------------------------------------------
# Stage 1: Build virtual environment with uv
# ----------------------------------------------------
FROM python:3.12-slim AS builder
WORKDIR /app

# Install uv for blazing-fast locked package installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install dependencies before copying source code
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# Copy source code and install project
COPY . .
RUN uv sync --frozen --no-dev

# ----------------------------------------------------
# Stage 2: Minimal Runtime
# ----------------------------------------------------
FROM python:3.12-slim AS runner
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

# Create dedicated non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup -u 10001 appuser

# Copy virtualenv and app from builder
COPY --chown=appuser:appgroup --from=builder /app/.venv /app/.venv
COPY --chown=appuser:appgroup --from=builder /app/src /app/src

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 3. Go Multi-Stage Dockerfile (Static Binary + Distroless)

```dockerfile
# ----------------------------------------------------
# Stage 1: Build Static Go Binary
# ----------------------------------------------------
FROM golang:1.22-alpine AS builder
WORKDIR /app

RUN apk add --no-cache git ca-certificates

# Cache dependencies
COPY go.mod go.sum ./
RUN go mod download && go mod verify

COPY . .

# Compile fully static binary (no CGO, stripped symbols for minimal size)
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /bin/server ./cmd/server

# ----------------------------------------------------
# Stage 2: Ultra-Minimal Distroless Container (Zero Shell)
# ----------------------------------------------------
FROM gcr.io/distroless/static-debian12:nonroot
WORKDIR /

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /bin/server /server

# Distroless runs as user 65532:65532 (nonroot) by default
USER nonroot:nonroot

EXPOSE 8080

ENTRYPOINT ["/server"]
```

---

## 4. Standard `.dockerignore` Template

Place this file in the root directory alongside every Dockerfile to prevent cache invalidation and secret leaks:

```gitignore
.git
.github
.gitignore
.dockerignore
node_modules
npm-debug.log
.pnpm-store
__pycache__
*.pyc
.pytest_cache
.venv
target
dist
build
.env
.env.*
!.env.example
*.pem
*.key
.DS_Store
Thumbs.db
.idea
.vscode
coverage
test
tests
docs
README.md
```
