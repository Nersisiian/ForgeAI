# Deployment

## Docker Compose
Recommended for production-like deployment. Includes PostgreSQL, Redis, backend, Celery worker, frontend with Nginx.

1. Set environment variables in `.env`
2. `docker-compose up -d`
3. Access at port 80.

## Scaling
- Scale Celery workers: `docker-compose up --scale celery=3`
- Use managed PostgreSQL/Redis in production.
- Set `SECRET_KEY` to a strong random string.

## Monitoring
Backend exposes `/health` endpoint and structured logging. Integrate with Prometheus/Grafana if needed.