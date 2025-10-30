# RocksMusic

# RocksMusic — Fixed Deployable Build

This is an auto-repaired build with standardized packaging for **Heroku**, **Railway**, and **VPS/Docker**.

## Quick Start
```bash
cp .env.example .env
# fill API_ID, API_HASH, BOT_TOKEN
docker compose up --build -d
```

## Heroku
- `runtime.txt` pinned to Python 3.11.9
- `Procfile` exposes `web` (FastAPI) and `worker` (bot).

## Railway
- `railway.json` included (Nixpacks) or use Dockerfile.

## Entrypoint
- `launcher.py` defers imports to avoid circular import/runtime crashes.
- Health endpoint at `/health` via `web/app.py`.

## Requirements
Generated `requirements.txt` consolidates detected libraries.


## Kurigram / Pyrogram (dev) Stack
This build preloads a compatibility adapter for Kurigram and pins deps for Heroku/Railway/VPS.

### Install Kurimuzon Pyrogram (dev) manually (optional)
```bash
pip install --force-reinstall https://github.com/KurimuzonAkuma/pyrogram/archive/refs/heads/dev.zip
```
> Note: fixed `--force-reinstall` (typo in original instructions).


## Hybrid Runtime
- Auto-detects Heroku vs VPS and prints environment mode.
- Error guard + safe send fallback + helpers included.
- Engine fallback (Pyrogram ⇆ Kurigram) preloaded by launcher.
