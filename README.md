# Demo FastAPI App - Auto-Fix Bot Test Target

This is a throwaway FastAPI app for testing the autonomous auto-fixing DevOps Telegram bot.

## Seeded Bug

The `/api/users` POST endpoint contains a deliberate bug:
- Reads `os.environ["API_SECRET_KEY"]` without `.get()` or try/except
- This throws a `KeyError` at **request time** (not import time)
- The app deploys successfully but crashes when this specific route is hit

## Branches

- `main`: Represents "production" (bot never touches this)
- `dev`: Working branch where the bug exists (bot targets this for fixes)

## Local Testing

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit http://localhost:8000/docs for the interactive API docs.

## Triggering the Bug

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com"}'
```

This will produce a KeyError traceback.

## Railway Deployment

Railway will deploy this successfully, but the `/api/users` endpoint will crash at runtime.
