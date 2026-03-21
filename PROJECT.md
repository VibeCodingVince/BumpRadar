# BumpRadar — PROJECT.md

## Overview
- **App:** Pregnancy ingredient safety checker — AI-powered
- **Domain:** https://bumpradar.app
- **Repo:** VibeCodingVince/pregnancy-safety-radar
- **Stack:** FastAPI + SQLite + GPT-4o-mini + vanilla frontend
- **Server:** This VPS (systemd service `bumpredar`, nginx reverse proxy)

## Status
- MVP launched March 18, 2026 — ALL 7 AGENTS COMPLETE
- Agents: Orchestrator, SafetyClassifier, ProductScanner (Open Food Facts), OCR (OpenAI Vision), Research, QA, Builder
- DB: 141 ingredients, 157+ aliases, zero gaps
- Freemium: 3 free scans/day, premium upsell at $4.99/mo (Stripe TBD)
- Frontend: 3-tab UI (Paste/Barcode/Photo), scan counter, camera support
- Admin API: /admin/research, /admin/qa, /admin/stats

## Competitors
- SafeMom.ai, PregSafe.ai, MamaScan.app, MamaSkin.app, Little Bean App, SkinSAFE
- BumpRadar advantages: no download (browser-based), covers food AND skincare, barcode scanning, partner/husband angle untapped

## Monetization
- Freemium rate limiting: 3 free scans/day per IP
- Premium: $4.99/mo (Stripe integration TBD)

## TikTok Marketing
- Using Larry skill for slideshow automation
- Self-hosted Postiz at https://postiz.bumpradar.app
- Image gen: FLUX.2 via Replicate API
- Text overlays: node-canvas
- TikTok Developer app review pending
- First post published March 19, 2026
- Config: `tiktok-marketing/config.json`
- Strategy: `tiktok-marketing/strategy.json`

## Key Files
- Backend service: `sudo systemctl status bumpredar`
- Nginx: `/etc/nginx/sites-available/bumpradar`
- SSL: `/etc/letsencrypt/live/bumpradar.app/`
- Logs: `sudo journalctl -u bumpredar`
- Backend env: `pregnancy-safety-radar/backend/.env`

## TODO
- Stripe payments integration
- TikTok developer app review video
- Generate more slideshow content
- Monitor first post performance
- Consider Kling AI for animated slideshows
