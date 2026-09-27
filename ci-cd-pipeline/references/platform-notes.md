# CI/CD Platform Configuration Reference

> Companion reference for `ci-cd-pipeline`.
> Production-ready syntax patterns, caching strategies, matrix configurations, and deployment guardrails for GitHub Actions, GitLab CI, and CircleCI.

---

## 1. GitHub Actions (`.github/workflows/ci.yml`)

### 1.1 Fast-Fail & Parallel Job Topology
Structure pipelines to fail on fast checks (lint, types) before executing expensive test suites:

```yaml
name: CI Pipeline

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  # Fast-fail stage: runs in parallel, completes in < 60 seconds
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm exec tsc --noEmit

  # Heavy test stage: runs only if lint and typecheck pass
  test:
    needs: [lint, typecheck]
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [20, 22]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm test:ci

  # Build stage: persists immutable artifact
  build:
    needs: [test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm build
      - uses: actions/upload-artifact@v4
        with:
          name: app-dist
          path: dist/
          retention-days: 7
```

### 1.2 Environment Protection & Scoped Secrets
Deployments must target declared GitHub Environments with manual approval gates:
```yaml
  deploy-production:
    needs: [build]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.example.com
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app-dist
          path: dist/
      - name: Deploy to Cloud
        env:
          PROD_API_KEY: ${{ secrets.PROD_API_KEY }} # Scoped strictly to production environment
        run: ./scripts/deploy.sh
```

---

## 2. GitLab CI (`.gitlab-ci.yml`)

### 2.1 Multi-Stage Pipeline with Lockfile Caching
```yaml
stages:
  - validate
  - test
  - build
  - deploy

default:
  image: node:20-alpine
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
    policy: pull-push

lint:
  stage: validate
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run lint

unit-tests:
  stage: test
  needs: [lint]
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run test:coverage
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

build-artifact:
  stage: build
  needs: [unit-tests]
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 3 days

deploy-staging:
  stage: deploy
  environment:
    name: staging
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
  script:
    - ./scripts/deploy-staging.sh

deploy-production:
  stage: deploy
  environment:
    name: production
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual # Requires manual click to release
  script:
    - ./scripts/deploy-production.sh
```

---

## 3. CircleCI (`.circleci/config.yml`)

### 3.1 Checksum Caching & Workflow Orchestration
```yaml
version: 2.1

executors:
  node-executor:
    docker:
      - image: cimg/node:20.11

jobs:
  lint-and-typecheck:
    executor: node-executor
    steps:
      - checkout
      - restore_cache:
          keys:
            - v1-deps-{{ checksum "package-lock.json" }}
            - v1-deps-
      - run: npm ci
      - save_cache:
          key: v1-deps-{{ checksum "package-lock.json" }}
          paths:
            - ~/.npm
      - run: npm run lint
      - run: npx tsc --noEmit

  test:
    executor: node-executor
    steps:
      - checkout
      - restore_cache:
          keys:
            - v1-deps-{{ checksum "package-lock.json" }}
      - run: npm ci
      - run: npm test

workflows:
  build-test-deploy:
    jobs:
      - lint-and-typecheck
      - test:
          requires:
            - lint-and-typecheck
```

---

## 4. Platform Comparison & Best Practice Matrix

| Dimension | GitHub Actions | GitLab CI | CircleCI |
|---|---|---|---|
| **Pipeline File** | `.github/workflows/*.yml` | `.gitlab-ci.yml` | `.circleci/config.yml` |
| **Fail-Fast Directive** | `concurrency: cancel-in-progress` | `interruptible: true` | `auto-cancel: true` |
| **Dependency Caching** | Built-in to `setup-*` actions or `actions/cache` | `cache:key:files` | `restore_cache` + `save_cache` |
| **Artifact Handoff** | `upload-artifact` / `download-artifact` | `artifacts:paths` | `persist_to_workspace` |
| **Secret Scoping** | Repository / Environment Secrets | Protected / Masked Variables | Organization Contexts |
| **Required Checks** | Branch Protection / Rulesets | Merge Checks ("Pipelines must succeed") | GitHub status check integration |
