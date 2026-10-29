# JobTrack

JobTrack is a SaaS job application tracker, built as a learning project for full-stack development.

## Stack

- Backend: Django + Django REST Framework
- Database: PostgreSQL
- Later: a Spring Boot service for stats
- Later: a Nuxt frontend

## Environment

- Windows, PowerShell.
- Each command runs in a fresh shell, so never rely on activating the venv. Always run Python as `.\venv\Scripts\python.exe` (for example, `.\venv\Scripts\python.exe manage.py migrate` and `.\venv\Scripts\python.exe -m pip install ...`).
- Always use `python -m pip install` (not bare `pip install`) when installing packages.

## Secrets

- Secrets live in `.env`, which must never be committed.
- Never print or commit the contents of `.env`.

## App structure

- `accounts` — has a custom User model. `AUTH_USER_MODEL = "accounts.User"`.
- `applications` — has the `Application` model and an `ApplicationViewSet`.

## Security rule

- Users must only ever see their own applications. Any query, view, or serializer touching `Application` must filter by the requesting user.

## Working style

- I'm learning: explain each change in simple English, one step at a time.
- Tell me which file you changed and why.
- After each step works, remind me to commit to Git.
