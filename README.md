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
- Local DB/log files are gitignored

## Run (docker)
```bash
docker compose up -d --build
```

Health:
```bash
curl http://127.0.0.1:3210/health
```
