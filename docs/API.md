# API Documentation

Base URL: `/api/v1`

## Authentication
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`

## Projects
- `POST /projects/` - Create project (triggers generation)
- `GET /projects/{id}` - Get project details
- `GET /projects/` - List projects (paginated)

## Tasks
- `GET /tasks/project/{project_id}` - Get all tasks for a project

## Artifacts
- `GET /artifacts/project/{project_id}` - List generated files
- `PUT /artifacts/{id}` - Update artifact content

## WebSocket
- `ws://host/api/v1/ws/{project_id}?token=JWT` - Live generation updates