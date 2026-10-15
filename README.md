# Private Trading Dashboard — TradingView-Style AND Python FastAPI

A production-ready starter to run a **Private Trading dashboard** with a **TradingView-like chart UI**
and a **Python trading engine** behind a secure API + WebSocket bridge.

> **Heads-up on licensing:** This template includes an integration path for the **TradingView Charting Library** (TVCL),
> but **does not bundle it**. You must obtain access from TradingView and place the official `charting_library`
> directory under `web/public/charting_library/`. Until then, the app falls back to **Lightweight Charts** for development.

## Features

- React + TypeScript frontend, TradingView-like UI (TVCL-ready adapter + Lightweight Charts fallback)
- Secure backend: FastAPI (async), JWT (access + refresh), password hashing, role-based guards
- WebSocket streaming for live candles & signals
- UDF-compatible datafeed endpoints for TVCL (`/tv/udf/*`) + signals API (`/signals`)
- Strategy engine boundary keeps your formulas **server-side only**; only the rendered markers/series values are sent
- Order routing abstraction (`exec_providers/*`) to connect to real exchanges later (Binance, Deribit, Coinbase)
- Dockerized: `docker-compose` with Caddy reverse proxy, SSL-ready (Auto HTTPS in production with real domain)
- Private-only: locked behind auth; tokens stored in httpOnly cookies by default

## Quick Start (Dev, no Docker)

follow these steps:

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd web
pnpm i || yarn || npm i
cp .env.example .env
# If you have TVCL, place it in: web/public/charting_library/
npm run dev
```

Open: http://localhost:5173

Login with default user (dev only): `admin@example.com` / `changeme123`.

## Quick Start (Docker)

```bash
# root of repo
cp backend/.env.example backend/.env
cp web/.env.example web/.env
docker compose up --build
```

Open: https://localhost  (Caddy reverse-proxies to frontend + backend; self-signed locally).
To use real TLS in prod, point your domain DNS to the server and set `ACME_EMAIL` in `docker-compose.yml`.

## TradingView Charting Library (TVCL) Setup

1. Request access from TradingView and download the **Charting Library**.
2. Put the folder at: `web/public/charting_library/` (so you have `web/public/charting_library/bundles/…` etc).
3. In `web/src/tv/loader.ts`, the script will detect and load TVCL. If not found, it uses Lightweight Charts.
4. The backend implements key **UDF endpoints** under `/tv/udf/*`. Adjust them as needed to your data source.
5. Overlays/markers come from `/signals` and the WebSocket stream `/ws` with a `channel` param (e.g., `btcusdt@1m`).

## Security Notes

- Dev mode seeds a default admin user. **Change the password immediately** and disable seeding in production.
- Tokens are httpOnly cookies by default; you can switch to Authorization headers by toggling `AUTH_COOKIES` in `.env`.
- CORS is restricted to your frontend origin; configure it in `backend/app/core/config.py`.
- Never ship proprietary logic to the browser. Only send rendered values (markers, series points).

## Structure

```
backend/
  app/
    api/
    auth/
    core/
    exec_providers/
    models/
    services/
    strategy/
    tv/
    main.py
  requirements.txt
web/
  public/
  src/
    tv/
    components/
    pages/
    lib/
  index.html
docker-compose.yml
Caddyfile
```

## Disclaimer

This repository is provided **as-is** for educational purposes. Trading and execution carry risk.
Use at your own discretion and test thoroughly in paper/sandbox environments before connecting any real capital.
