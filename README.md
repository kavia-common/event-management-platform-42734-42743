# event-management-platform-42734-42743

Backend (Flask) runs on port 3001 and exposes Swagger UI at /docs.
Frontend (Next.js) runs on port 3000 and calls the backend via NEXT_PUBLIC_API_BASE.

Quick start:
- Copy event_management_backend/.env.example to .env and set values.
- docker-compose up -d (to start Postgres and backend) or run backend locally with python run.py.
- Regenerate OpenAPI (optional): from backend folder run `python generate_openapi.py`.