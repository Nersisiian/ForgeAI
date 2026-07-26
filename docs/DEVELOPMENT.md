# Development Guide

## Setup
1. Create virtualenv, install `requirements.txt`
2. Start PostgreSQL and Redis (e.g., via docker-compose up db redis)
3. Copy `.env.example` to `.env`
4. Run `alembic upgrade head`
5. `uvicorn app.main:app --reload`
6. For frontend: `cd frontend && npm install && npm run dev`

## Testing
- Backend: `pytest --cov=app --cov-report=html`
- Frontend: `npm run lint`

## Code Quality
- Format: `black backend/` and `prettier frontend/`
- Lint: `ruff check backend/`
- Type check: `mypy backend/`

## Pre-commit
Install pre-commit hooks: `pre-commit install`