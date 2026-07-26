# Architecture

## Overview
Clean Architecture, DDD, SOLID. Backend in FastAPI + SQLAlchemy async, frontend React + MUI. AI agents orchestrated via Celery.

## Components
- **API Layer**: FastAPI with JWT auth, WebSockets, rate limiting.
- **Domain**: Services, agents, entities.
- **Infrastructure**: PostgreSQL, Redis, OpenAI API.
- **Frontend**: React SPA with dark mode, dashboard, project builder.

## Agent Pipeline
1. Planner - high-level plan
2. Architect - detailed tech spec
3. Database - SQLAlchemy models + migration
4. Backend - Full FastAPI app
5. Frontend - React app
6. Docker - Dockerfiles, compose
7. Testing - pytest suite
8. Documentation - README, guides
9. Review - lint, type check
10. Fix - auto-fix issues

The output is a complete, runnable project.