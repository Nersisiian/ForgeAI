#!/bin/sh
set -e
docker-compose up -d db redis
cd backend && uvicorn app.main:app --reload &
cd frontend && npm run dev &
wait