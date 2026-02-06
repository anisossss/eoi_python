# Docker Hub Deployment Instructions

## CSIR EOI 8119/06/02/2026 - Mining Analytics API

### Pull Request Command

```bash
# Pull the Mining Analytics API from Docker Hub
docker pull csireoi8119/mining-api:latest
```

---

## Running the Application

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/csir-eoi/mining-analytics-api.git
cd mining-analytics-api

# Start all services
docker-compose up -d

# Services:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Flower (Celery Monitor): http://localhost:5555
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379
```

### Option 2: Individual Containers

```bash
# Create network
docker network create mining-network

# Run PostgreSQL
docker run -d \
  --name mining-postgres \
  --network mining-network \
  -e POSTGRES_USER=mining_user \
  -e POSTGRES_PASSWORD=mining_secure_password_2026 \
  -e POSTGRES_DB=mining_db \
  -p 5432:5432 \
  postgres:16-alpine

# Run Redis
docker run -d \
  --name mining-redis \
  --network mining-network \
  -p 6379:6379 \
  redis:7-alpine

# Run API
docker run -d \
  --name mining-api \
  --network mining-network \
  -e DATABASE_URL=postgresql://mining_user:mining_secure_password_2026@mining-postgres:5432/mining_db \
  -e CELERY_BROKER_URL=redis://mining-redis:6379/0 \
  -p 8000:8000 \
  csireoi8119/mining-api:latest
```

---

## Health Check

```bash
# Check API health
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "service": "CSIR Mining Analytics API",
  "version": "1.0.0"
}
```

---

## Building and Pushing

```bash
# Build
docker build -t csireoi8119/mining-api:latest .

# Login and push
docker login
docker push csireoi8119/mining-api:latest
```

---

## Task Compliance

- ✅ Application containerized with Docker
- ✅ Runs in Docker container
- ✅ Available in hub.docker.com registry
- ✅ PULL REQUEST COMMAND provided
- ✅ PostgreSQL (SQL) database
- ✅ Background processing with Celery
- ✅ Python proficiency demonstrated

---

**CSIR EOI 8119/06/02/2026 - Mining Data Analytics API**
