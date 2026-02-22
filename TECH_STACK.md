# TECH_STACK — Personal Dashboard

## Chosen Stack
- Backend: FastAPI (Python 3.11+)
- DB: SQLite (local file: `data/personal_dashboard.db`)
- ORM: SQLAlchemy
- Frontend: Jinja templates + FullCalendar (CDN)
- Runtime: Uvicorn
- Process: systemd user service (planned in handoff)

## Why this stack
- Local-first, zero external dependencies
- Fast to iterate for solo product
- Easy to expose simple API for OpenClaw skill bridge
- SQLite is enough for single-user dashboard

## Planned API
- `GET /api/events`
- `POST /api/events`
- `PUT /api/events/{id}`
- `DELETE /api/events/{id}`
- `POST /api/quick-add` (NLP-lite parser for text commands)
- `GET /health`

## Future Integrations
- OpenClaw custom skill: `add_event` and `list_today`
- Optional STT pipeline for voice notes -> quick-add parser
