# personal-dashboard

Local-first personal dashboard (MVP starts with calendar/events) for Bartek.

## Run (dev)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 3210
```

Open: `http://<server-ip>:3210`

## Security basics
- Keep secrets in `.env` (never commit it)
- Use `.env.example` as template
- Set `PERSONAL_DASHBOARD_API_TOKEN` for write endpoint auth (`X-API-Token` header)
- Local DB/log files are gitignored

Bridge notes: `docs/OPENCLAW_BRIDGE.md`

## Run (docker)
```bash
docker compose up -d --build
```

Health:
```bash
curl http://127.0.0.1:3210/health
```

## systemd user service (auto-start)
Service file: `deploy/systemd/personal-dashboard.service`

Install as user service:
```bash
mkdir -p ~/.config/systemd/user
cp deploy/systemd/personal-dashboard.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now personal-dashboard.service
```

Manage:
```bash
systemctl --user status personal-dashboard.service
systemctl --user restart personal-dashboard.service
journalctl --user -u personal-dashboard.service -n 100 --no-pager
```
