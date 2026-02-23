# HANDOFF — Build Plan (Night Mode)

## Phase 0 — Foundation
- [x] Create repository scaffold
- [x] Write PRD
- [x] Write TECH_STACK
- [x] Set up Python env + dependencies (via Docker image build)
- [x] Implement DB models + migrations bootstrap

## Phase 1 — Core Calendar MVP
- [x] Implement events CRUD API
- [x] Implement quick-add parser (`"Dentysta jutro 14:00"` + ISO datetime)
- [x] Build calendar page (month/week) with FullCalendar
- [x] Connect frontend to API
- [x] Basic validation + error handling

## Phase 2 — Deploy on VPS (no domain)
- [ ] Create systemd user service
- [x] Run app on `0.0.0.0:3210` (Docker, restart unless-stopped)
- [x] Add startup/restart instructions in README
- [x] Smoke test from browser/health endpoint

## Phase 3 — OpenClaw Bridge
- [x] Add API token auth for write endpoints
- [x] Define OpenClaw command grammar for quick add
- [x] Add integration notes for custom skill/tool wrapper

## Definition of Done (MVP)
- [ ] Event can be added via web form
- [ ] Event can be added via text quick-add endpoint
- [ ] Event visible in calendar and editable/deletable
- [ ] App survives process restart (systemd)
- [ ] README has runbook for local ops

## Suggested Night Execution Order
1. Phase 0 remaining
2. Phase 1 core API + DB
3. Phase 1 UI hookup
4. Phase 2 deploy + smoke test
5. Update this file with completed checkboxes
