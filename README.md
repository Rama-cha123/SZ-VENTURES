# SZ Ventures

> A venture studio operating at the intersection of technology, hospitality, sustainability, and advanced manufacturing — building category-defining companies.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyour-org%2Fsz-ventures)
[![Netlify Status](https://api.netlify.com/api/v1/badges/YOUR_BADGE_ID/deploy-status)](https://app.netlify.com/sites/YOUR_SITE_NAME/deploys)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Local Development](#local-development)
- [Deployment](#deployment)
  - [Vercel (Recommended — One-Click)](#vercel-recommended--one-click)
  - [Netlify](#netlify)
  - [GitHub Pages](#github-pages)
  - [Docker / Self-Hosted](#docker--self-hosted)
- [CI/CD Pipeline](#cicd-pipeline)
- [Environment Variables](#environment-variables)
- [Project Structure](#project-structure)
- [Performance & SEO](#performance--seo)

---

## Project Overview

SZ Ventures is a pure-static website — zero build step, zero runtime dependencies. Every page is a hand-authored HTML file served with a curated set of vendored JS/CSS libraries bundled locally. This makes it:

- **Instantly deployable** to any CDN or static host.
- **Framework-agnostic** — no Node, no Python, no compilation.
- **Blazing fast** — all assets are served from edge CDN nodes.

---

## Tech Stack

| Layer     | Technology                                        |
|-----------|---------------------------------------------------|
| Structure | Semantic HTML5                                    |
| Styling   | Vanilla CSS + custom design tokens                |
| Behaviour | Vanilla JS (ES2017+)                              |
| Libraries | AOS · Lenis · Tippy.js · Swup · Odometer · Popper |
| Hosting   | Vercel / Netlify / GitHub Pages / Docker          |
| CI/CD     | GitHub Actions                                    |

---

## Local Development

No build step is required. Simply serve the project root over HTTP:

### Option A — Python (zero install)
```bash
# Python 3
python -m http.server 8000
# Open → http://localhost:8000
```

### Option B — Node (npx serve)
```bash
npx serve .
# Open → http://localhost:3000
```

### Option C — VS Code Live Server Extension
Install the [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension, right-click `index.html` → **Open with Live Server**.

> **Why a server?** Swup page transitions and some browser security policies require an HTTP origin — opening `index.html` directly via `file://` may not work correctly.

---

## Deployment

### Vercel (Recommended — One-Click)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyour-org%2Fsz-ventures)

**Manual steps:**

1. Push this repo to GitHub.
2. Go to [vercel.com](https://vercel.com) → **New Project** → import your repo.
3. Vercel auto-detects the static site — **no configuration needed** (the `vercel.json` handles everything).
4. Click **Deploy**. Your site is live in ~30 seconds.

**Clean URLs** (`/portfolio` instead of `/portfolio.html`) are pre-configured in `vercel.json`.

---

### Netlify

1. Push this repo to GitHub.
2. Go to [netlify.com](https://netlify.com) → **Add new site** → **Import an existing project**.
3. Select the repo. Leave the build command **blank** and set the publish directory to **`.`** (dot).
4. Click **Deploy site**.

The `netlify.toml` file handles pretty URLs, asset caching, security headers, and CSS/JS minification automatically.

---

### GitHub Pages

1. Push to GitHub.
2. Go to **Settings → Pages**.
3. Source: **Deploy from a branch** → select `main` / `master`, folder `/` (root).
4. Save. GitHub Pages will serve the site at `https://your-org.github.io/sz-ventures/`.

> **Note:** GitHub Pages does not support clean URLs (`.html` extension is required in links) unless you use a custom domain + `_redirects` file workaround.

---

### Docker / Self-Hosted

A production-hardened Nginx Docker image is included.

```bash
# Build the image
docker build -t sz-ventures:latest .

# Run locally (port 8080 → container port 80)
docker run -p 8080:80 sz-ventures:latest

# Open → http://localhost:8080
```

**Push to a registry (e.g. Docker Hub):**
```bash
docker tag sz-ventures:latest your-dockerhub-username/sz-ventures:latest
docker push your-dockerhub-username/sz-ventures:latest
```

**Docker Compose (optional):**
```yaml
version: "3.9"
services:
  web:
    image: sz-ventures:latest
    ports:
      - "80:80"
    restart: unless-stopped
```

---

## CI/CD Pipeline

The `.github/workflows/deploy.yml` pipeline runs on every push to `main`/`master` and every pull request:

| Job             | Trigger          | What it does                                    |
|-----------------|------------------|-------------------------------------------------|
| **lint**        | All events       | Validates HTML files exist; checks asset paths  |
| **security**    | All events       | Scans for hardcoded secrets / committed .env    |
| **deploy-vercel** | Push to `main` | Deploys to production on Vercel                 |
| **deploy-preview** | Pull request  | Deploys preview & comments URL on the PR        |

### Required GitHub Secrets

Navigate to **Settings → Secrets and variables → Actions** and add:

| Secret name         | Where to find it                                                    |
|---------------------|---------------------------------------------------------------------|
| `VERCEL_TOKEN`      | [vercel.com/account/tokens](https://vercel.com/account/tokens)      |
| `VERCEL_ORG_ID`     | Run `vercel link` locally → check `.vercel/project.json`           |
| `VERCEL_PROJECT_ID` | Run `vercel link` locally → check `.vercel/project.json`           |

---

## Environment Variables

This is a pure-static site with **no server-side code**, so there are no runtime environment variables. All configuration is baked into HTML/CSS/JS at authoring time.

If you add a backend (e.g. a contact form API), follow this pattern:

- Store secrets in the hosting platform's environment variable UI (Vercel / Netlify dashboard).
- Never commit `.env` files — they are covered by `.gitignore`.

---

## Project Structure

```
sz-ventures/
├── index.html                  # Home page
├── portfolio.html
├── philosophy.html
├── achievements.html
├── contact.html
├── snapops.html                # Portfolio company pages
├── bowl-sip.html
├── terramuse.html
├── mirai.html
├── sz-manufacturing.html
├── team.html
├── insights.html
├── careers.html
├── press.html
├── privacy.html
├── terms.html
├── cookies.html
├── style.css                   # Global glass-morphism utilities
├── main.js                     # Global interaction layer
├── robots.txt
├── sitemap.xml
├── assets/
│   ├── img/
│   │   ├── favicon.svg
│   │   └── og-image.svg
│   ├── js/
│   │   ├── app.js              # Shared UI behaviours (nav, reveal, counters)
│   │   ├── enhance.js          # Library initialisers (AOS, Lenis, Tippy, Odometer)
│   │   ├── libs.bundle.js      # Concatenated vendor JS (one HTTP request)
│   │   └── libs/               # Individual library source (reference)
│   └── styles/
│       ├── tokens.css          # Design tokens (colours, spacing, type)
│       ├── base.css            # Reset + global defaults
│       ├── layout.css          # Page-level layouts
│       ├── components.css      # Reusable component styles
│       ├── libs.bundle.css     # Concatenated vendor CSS (one HTTP request)
│       └── libs/               # Individual library CSS (reference)
├── vercel.json                 # Vercel: clean URLs, headers, caching
├── netlify.toml                # Netlify: processing, headers, redirects
├── Dockerfile                  # Self-hosted: Nginx Alpine production image
├── nginx.conf                  # Nginx server block config
└── .github/
    └── workflows/
        └── deploy.yml          # GitHub Actions CI/CD pipeline
```

---

## Performance & SEO

- **Canonical URLs** — each page declares `<link rel="canonical">`.
- **Open Graph / Twitter Cards** — meta tags on every page.
- **robots.txt** — allows all crawlers, points to sitemap.
- **sitemap.xml** — covers all 17 public pages with correct priorities.
- **Gzip** — enabled in Docker/Nginx; Vercel/Netlify apply it automatically.
- **Immutable caching** — `Cache-Control: max-age=31536000, immutable` for all assets.
- **Security headers** — `X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`, `Permissions-Policy` on every response.
- **Prefers-reduced-motion** — all animations are skipped for users who opt out.
- **Google Fonts** — loaded with `preconnect` for minimal render-blocking impact.

---

## License

© SZ Ventures. All rights reserved.
