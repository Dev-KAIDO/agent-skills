---
name: deployment-comprehensive
description: Complete deployment skill — Vercel, Netlify, Cloudflare, Render, Expo/App Store, CI/CD pipelines (GitHub Actions, EAS), environment management, blue-green/canary deployment, rollback, and monitoring. Use for ANY deployment or hosting task.
---

# Deployment Comprehensive — Complete Skill

## Overview

**Single skill for all deployment work.** Merges `vercel-deploy`, `netlify-deploy`, `cloudflare-deploy`, `render-deploy`, `expo-deployment`, `expo-cicd-workflows`, `github-actions`, `engineering-devops-automator`, `expo-deployment`, and `sdlc-devops`.

---

## 1. Platform Selection (اختيار المنصة)

### 1.1 Decision Matrix
| Platform | Best For | Pricing |
|----------|----------|---------|
| **Vercel** | Next.js, React, static sites | Free tier + usage |
| **Netlify** | Static sites, JAMstack, forms | Free tier + usage |
| **Cloudflare Pages** | Edge performance, Workers | Free tier + usage |
| **Cloudflare Workers** | Serverless API, edge compute | 100K req/day free |
| **Render** | Full-stack apps, databases | Free tier + $7/mo |
| **AWS** | Enterprise, full control | Pay-as-you-go |
| **Railway** | Simple full-stack | $5/mo usage |
| **Fly.io** | Docker containers, global | Free tier + usage |
| **VPS (DigitalOcean)** | Full control, databases | $6/mo+ |

### 1.2 Decision Tree
```
Static site / SSG?          → Vercel or Netlify or Cloudflare Pages
Next.js app?                → Vercel (first-class support)
Full-stack with database?   → Render or Railway or VPS
Serverless API?             → Cloudflare Workers or Vercel Functions
Docker container?           → Fly.io or Railway or AWS
Enterprise / compliance?    → AWS or Azure or GCP
Mobile app (Expo)?          → EAS (Expo Application Services)
```

---

## 2. Vercel (فيرسيل)

### 2.1 Deployment
```bash
# Install CLI
npm i -g vercel

# Deploy (preview)
vercel

# Deploy (production)
vercel --prod

# Link project
vercel link

# Environment variables
vercel env add DATABASE_URL production
vercel env pull .env.local  # Pull to local
```

### 2.2 Configuration
```json
// vercel.json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "regions": ["iad1"],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/api/(.*)", "destination": "/api" }
  ]
}
```

### 2.3 Features
- Automatic HTTPS and CDN
- Preview deployments for PRs
- Serverless functions (API routes)
- Edge middleware
- Analytics and speed insights
- Custom domains with automatic SSL

---

## 3. Netlify (نتل-افي)

### 3.1 Deployment
```bash
# Install CLI
npm i -g netlify-cli

# Login
netlify login

# Link site
netlify link --git-remote-url https://github.com/user/repo

# Deploy (preview)
netlify deploy

# Deploy (production)
netlify deploy --prod

# Environment variables (set in dashboard)
# Site settings → Environment variables
```

### 3.2 Configuration
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[build.environment]
  NODE_VERSION = "20"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
```

---

## 4. Cloudflare (كلاود فلير)

### 4.1 Workers (Serverless)
```bash
# Create worker
npx wrangler init my-worker

# Deploy
npx wrangler deploy

# Check auth
npx wrangler whoami
```

```javascript
// worker.js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    
    if (url.pathname === "/api/hello") {
      return Response.json({ message: "Hello from Workers!" });
    }
    
    return env.ASSETS.fetch(request);
  },
};
```

### 4.2 Pages (Static + Functions)
```bash
# Deploy to Pages
npx wrangler pages deploy dist
```

### 4.3 Cloudflare Products
| Product | Use |
|---------|-----|
| **Workers** | Serverless functions |
| **Pages** | Static hosting + functions |
| **KV** | Key-value storage |
| **D1** | SQL database (SQLite) |
| **R2** | Object storage (S3-compatible) |
| **Queues** | Message queue |
| **Vectorize** | Vector database |
| **AI** | ML inference |
| **WAF** | Web application firewall |
| **Turnstile** | CAPTCHA alternative |

### 4.4 Advanced Building Blocks (كتل متقدمة)
| Need | Product | When |
|------|---------|------|
| Stateful, per-entity coordination (durable state, WebSockets, rate limiting per user) | **Durable Objects** | Single-threaded actor per ID; strong consistency |
| Multi-step, long-running, resumable business processes | **Workflows** | Retries per step, durable execution, survives restarts |
| Scheduled jobs (cron) | **Cron Triggers** | `scheduled` handler on a Worker; no separate scheduler |
| Running containers | **Containers** | Long-lived compute that doesn't fit Worker limits |
| Multi-tenant SaaS serving custom domains per customer | **Workers for Platforms** | Isolated per-customer configs/secret stores |
| One-off edge logic without a deploy | **Snippets** | Quick request/response modification |
| **Workers for Platforms vs Durable Objects:** WFP = per-tenant code/config isolation; DO = per-entity state/coordination |

**Cron example:**
```javascript
export default {
  async scheduled(event, env, ctx) {
    await env.DB.prepare("UPDATE jobs SET status='due' WHERE run_at <= ?")
      .bind(Date.now()).run();
  },
};
```

### 4.5 CI Authentication (مصادقة CI)
```bash
# In CI — never commit tokens; inject as env var
CLOUDFLARE_API_TOKEN=... npx wrangler deploy
# Scoped API token (not Global API Key): Edit Cloudflare Workers, Pages, and appropriate resources
```
- ✅ Use a **scoped API token** with least privilege; rotate regularly
- ✅ Reference docs for every product live in this skill's `references/` folder (e.g. `references/durable-objects/`, `references/workflows/`, `references/cron-triggers/`)

---

## 5. Render (رِندر)

### 5.1 Blueprint (render.yaml)
```yaml
# render.yaml
services:
  - type: web
    name: my-app
    runtime: node
    buildCommand: npm install && npm run build
    startCommand: npm start
    envVars:
      - key: DATABASE_URL
        sync: false
    healthCheckPath: /health
    scaling:
      minInstances: 1
      maxInstances: 3

databases:
  - name: my-db
    plan: free
    databaseName: myapp
```

### 5.2 Deployment
```bash
# Connect repo in dashboard, then:
# Every push to main = production deploy
# Every PR = preview deploy
```

---

## 6. Expo / Mobile (تطبيقات المحمول)

### 6.1 EAS Build
```bash
# Install EAS CLI
npm i -g eas-cli

# Login
eas login

# Configure
eas build:configure

# Build for development
eas build --platform ios --profile development

# Build for production
eas build --platform all --profile production
```

### 6.2 EAS Update (OTA)
```bash
# Push OTA update
eas update --branch production --message "Bug fix"

# Check update health
eas update:list
eas channel:insights production
```

### 6.3 EAS Workflows (CI/CD)
Workflows live in `.eas/workflows/*.yml`. They are **NOT** GitHub Actions — no `runs-on`, no `uses:` steps. They use Expo's **pre-packaged job types** driven by the live schema.

```yaml
# .eas/workflows/build-and-submit.yml
name: Build and Submit
on:
  push:
    branches: [main]

jobs:
  build_ios:
    type: build
    params:
      platform: ios
      profile: production
      distribution: store
      output: build_ios

  build_android:
    type: build
    params:
      platform: android
      profile: production
      distribution: store
      output: build_android

  submit:
    type: submit
    after: [build_ios, build_android]
    params:
      track: production
```
**Structure:** `name` · `on` (≥1 trigger) · `jobs` (required) · `defaults` · `concurrency`.
**Expressions:** `${{ }}` with contexts `github.*`, `inputs.*`, `needs.*`, `jobs.*`, `steps.*`, `workflow.*`.

⚠️ **Schema-first discipline (critical):**
- Fetch `https://api.expo.dev/v2/workflows/schema` before generating/editing — it is the source of truth for job types, params, triggers, runners, and enums
- Do **not** rely on memorized values; the schema evolves
- Validate after editing: `node scripts/validate.js <workflow.yml>` (fetches latest schema, checks structure)
- Answer "what options exist?" by reading the schema, never from memory

### 6.4 Store Submission (نشر المتاجر)
```bash
eas build --platform ios --profile production
eas submit --platform ios --latest        # TestFlight / App Store
eas submit --platform android --latest    # Play Store
```
- **TestFlight:** upload via `eas submit`, add internal/external testers, build must pass App Store review guidelines
- **Play Store:** requires signing key (managed by EAS), staged rollout recommended (10% → 100%)
- **ASO / metadata:** app name, subtitle, keywords, screenshots per device class, description with real value props
- **iOS review:** expect rejections for privacy declarations, login-without-logout, and incomplete demo accounts
- **Channels:** use `eas update` channels per environment (production/preview/development)

---

## 7. GitHub Actions (CI/CD)

### 7.1 CI Pipeline
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v4

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - run: npm run deploy
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

### 7.2 Secrets
```bash
# Add secrets in repo settings
# Settings → Secrets and variables → Actions

# Use in workflow
env:
  API_KEY: ${{ secrets.API_KEY }}
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

### 7.3 React Native Cloud Builds (بناء سحابي لتطبيقات RN)
Run iOS **simulator** / Android **emulator** builds in cloud CI (no local Xcode/SDK needed):
- iOS artifact: `.app.tar.gz` (simulator bootable bundle) · Android artifact: `.apk` (emulator variant, usually `Debug`)
- Structure: composite actions for build steps, wired into a workflow that uploads artifacts with `actions/upload-artifact@v4`, capturing `artifact-name` / `artifact-id` outputs
- **Artifact retrieval:**
```bash
gh run download <run-id> -n <artifact-name> -D ./artifacts
# or REST:
gh api repos/<owner>/<repo>/actions/runs/<run-id>/artifacts
gh api repos/<owner>/<repo>/actions/artifacts/<artifact-id>/zip > artifact.zip
```
- ✅ Pin artifact names — unpinned names make `gh run download -n` brittle
- ✅ Set retention days explicitly; publish artifact metadata to the job summary
- Full composite-action + workflow templates: `references/gha-ios-composite-action.md`, `gha-android-composite-action.md`, `gha-workflow-and-downloads.md`

---

## 8. Environment Management (إدارة البيئات)

### 8.1 Environment Strategy
```
Development  → local, .env.local
Staging      → staging.example.com (pre-production)
Production   → example.com (live)
```

### 8.2 Environment Variables
```bash
# .env (NEVER commit)
DATABASE_URL=postgresql://...
JWT_SECRET=...
NEXT_PUBLIC_API_URL=https://api.example.com

# NEXT_PUBLIC_ prefix = exposed to browser (careful!)
# No prefix = server-side only (safer)
```

### 8.3 Environment Checklist
- [ ] Different secrets for each environment
- [ ] No production secrets in staging/development
- [ ] Secrets rotated regularly
- [ ] Environment variables documented
- [ ] `.env` in `.gitignore`

---

## 9. Deployment Strategies (استراتيجيات النشر)

### 9.1 Blue-Green
```
Blue (v1) ← live traffic
Green (v2) ← new version

1. Deploy Green
2. Test Green
3. Switch traffic to Green
4. Blue becomes standby (rollback target)
```

### 9.2 Canary
```
1. Deploy to 1% of users
2. Monitor metrics (errors, latency)
3. If OK → increase to 10%, 50%, 100%
4. If errors → roll back immediately
```

### 9.3 Rollback
```bash
# Vercel
vercel rollback

# GitHub Actions
git revert <deploy-commit>
git push origin main  # triggers redeploy

# Docker
docker rollback  # if using Docker

# Database migrations: ALWAYS forward-only
# Never rollback schema changes (add, don't remove)
```

---

## 10. Pre-Deploy Checklist (قبل النشر)

- [ ] All tests pass (unit, integration, e2e)
- [ ] Security scan passed
- [ ] Environment variables set for target environment
- [ ] Database migrations tested
- [ ] Rollback plan documented
- [ ] Monitoring and alerts configured
- [ ] DNS settings verified
- [ ] SSL certificates valid
- [ ] CDN cache purged (if applicable)
- [ ] Backup created before deploy
- [ ] Team notified of deployment
- [ ] Health check endpoint verified post-deploy

---

## 11. Post-Deploy Verification (بعد النشر)

```bash
# Check status
curl -f https://example.com/health

# Verify SSL
curl -I https://example.com | grep "HTTP/2 200"

# Check DNS
nslookup example.com

# Monitor errors
# Check Sentry/Dashboard for new errors

# Performance check
# Lighthouse, Core Web Vitals
```

---

## Bundled Tools & References (الأدوات والمراجع المرفقة)

**Scripts:**
| Script | Purpose |
|--------|---------|
| `scripts/fetch.js` | Fetch EAS workflow schema/docs with ETag caching |
| `scripts/validate.js` | Validate `.eas/workflows/*.yml` against the live schema |
| `scripts/deploy.sh` | Generic deploy helper |
| `scripts/package.json` | Node deps for the above (`npm install --prefix scripts`) |

**References (high value):**
- **Cloudflare:** `references/<product>/` — 64 product folders (durable-objects, workflows, cron-triggers, containers, workers-for-platforms, snippets, d1, kv, r2, queues, ai, wrangler, terraform, …)
- **Mobile stores:** `references/testflight.md`, `ios-app-store.md`, `play-store.md`, `app-store-metadata.md`
- **GitHub Actions RN:** `references/gha-ios-composite-action.md`, `gha-android-composite-action.md`, `gha-workflow-and-downloads.md`
- **EAS:** `references/channel-insights-schema.md`, `update-insights-schema.md`
- **Platform configs:** `references/netlify-toml.md`, `configuration-guide.md`, `service-types.md`

---

## Verification Checklist (قائمة التحقق)قائمة التحقق)

- [ ] Site loads correctly at production URL
- [ ] HTTPS working (SSL valid)
- [ ] All pages/routes accessible
- [ ] API endpoints responding
- [ ] Database connections working
- [ ] Environment variables loaded correctly
- [ ] No console errors in production
- [ ] Performance within thresholds (LCP < 2.5s)
- [ ] Error monitoring active (Sentry, etc.)
- [ ] Analytics tracking working
- [ ] Backup automation running
- [ ] Rollback tested and functional
