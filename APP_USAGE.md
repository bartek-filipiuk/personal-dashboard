# Personal Dashboard — Instrukcja (MVP)

## Gdzie to działa
- URL: `http://116.203.94.11:3210`
- Katalog projektu: `/home/vince/projects/personal-dashboard`
- Healthcheck: `http://116.203.94.11:3210/health`

## Co jest teraz
- Bootstrap aplikacji FastAPI + widok kalendarza FullCalendar
- Deployment przez Docker Compose

## Jak uruchomić / zrestartować
```bash
cd /home/vince/projects/personal-dashboard

docker compose up -d --build      # start / rebuild

docker compose ps                 # status

docker compose logs -f            # logi

docker compose restart            # restart
```

## Jak zatrzymać
```bash
docker compose down
```

## Co będzie po nocnym buildzie
- CRUD eventów (dodaj/edytuj/usuń)
- SQLite lokalnie (bez Supabase)
- Quick-add tekstowy (np. "Dentysta jutro 14:00")
- Podpięcie kalendarza do API
- Token na endpointy zapisu

## Jak używać (docelowo po etapie nocnym)
1. Otwórz URL aplikacji
2. Kliknij w dzień lub przycisk dodawania eventu
3. Wpisz tytuł i czas
4. Zapisz — event pojawi się w kalendarzu
5. Edycja/usuwanie z poziomu eventu

## Integracja z OpenClaw (następny krok)
- komenda tekstowa w Discordzie (np. `dodaj event: dentysta jutro 14:00`)
- OpenClaw wywołuje API `POST /api/quick-add`
- dostajesz potwierdzenie w kanale
