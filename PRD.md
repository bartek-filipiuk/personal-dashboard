# PRD — Personal Dashboard (MVP: Calendar First)

## Goal
Build a local-first personal dashboard for Bartek, starting with calendar events and fast capture from text/voice later.

## Problem
Current reminders/tasks are scattered (Discord, notes, memory). Need one place to view schedule and quickly add personal events (e.g., dentist).

## Users
- Primary: Bartek (single user, self-hosted on VPS)

## MVP Scope (v1)
- Month/week calendar UI
- CRUD events
- Event fields: title, starts_at, ends_at (optional), category, notes
- Quick-add parser endpoint (text -> event draft)
- SQLite local storage
- Health endpoint

## Out of Scope (v1)
- Multi-user auth
- Google Calendar sync
- Mobile app
- Voice input direct from app (handled via OpenClaw bridge later)

## Success Criteria
- Add event in < 10s
- Calendar loads in < 1s for typical data
- Works on VPS without domain (IP:port)

## Example User Stories
- As Bartek, I can add: "Dentysta 2026-03-05 14:00" and see it on calendar.
- As Bartek, I can filter events by category.
- As Bartek, I can edit/remove wrong events.
