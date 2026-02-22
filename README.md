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
