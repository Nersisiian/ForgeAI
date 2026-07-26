.PHONY: up down build test lint

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

test:
	cd backend && pytest

lint:
	ruff check backend/
	black --check backend/
	mypy backend/
	cd frontend && npm run lint