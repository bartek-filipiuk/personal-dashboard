# OpenClaw Bridge Notes (Phase 3)

## Write auth
All write endpoints require header:

- `X-API-Token: <PERSONAL_DASHBOARD_API_TOKEN>`

Protected endpoints:
- `POST /api/events`
- `PUT /api/events/{event_id}`
- `DELETE /api/events/{event_id}`
- `POST /api/events/quick-add`

Read endpoints are open:
- `GET /health`
- `GET /api/events`
- `GET /api/events/{event_id}`

## Quick-add grammar
Accepted quick-add payload:

```json
{ "text": "Dentysta jutro 14:00" }
```

Supported forms:
1. `<title> jutro HH:MM`
2. `<title> YYYY-MM-DD HH:MM`
3. `<title> YYYY-MM-DDTHH:MM`

Examples:
- `Dentysta jutro 14:00`
- `Siłownia 2026-02-24 18:30`
- `Call 2026-02-24T09:00`

## OpenClaw wrapper flow
1. Receive user intent text.
2. Send `POST /api/events/quick-add` with JSON `{ "text": "..." }`.
3. Add `X-API-Token` header from secret store.
4. If status `201`, return created event summary.
5. If status `400`, return parser/validation error and ask user to rephrase.
6. If status `401`, report invalid token/config issue.
