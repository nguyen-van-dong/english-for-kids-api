# English for Kids API

Backend API service built with **FastAPI**, **PostgreSQL**, and **Docker** for the English for Kids mobile application.

## 🚀 Features
- **JWT Authentication**: Secure registration, login, and bearer token authorization.
- **Child Profile & Mascot**: Parent email, child nickname, age, mascot avatar customizer.
- **Progress Synchronization**: Sync stars, learning streaks, and mastered vocabulary words between devices and cloud database.
- **Docker Compose**: One-click setup for PostgreSQL 16 and FastAPI with hot-reloading.

## 🐳 Getting Started with Docker

### 1. Configure Environment Variables
Copy the example environment file and customize your settings if needed:
```bash
cp .env.example .env
```

### 2. Run with Docker Compose:
```bash
docker compose up -d --build
```

- **Swagger API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: `curl http://localhost:8000/health`

### Stop containers:
```bash
docker compose down
```

### View container logs:
```bash
docker compose logs -f
```
